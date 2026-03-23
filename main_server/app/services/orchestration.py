from __future__ import annotations

import logging
from pathlib import Path

import joblib
import requests

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    HOSPITAL_1_UPLOAD_URL,
    HOSPITAL_2_UPLOAD_URL,
    MODELS_DIR,
    REQUEST_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
)
from main_server.app.services.aggregation import aggregate_models
from main_server.app.services.evaluation import evaluate_main_model
from shared.model_registry import get_active_version


logger = logging.getLogger("main_server.orchestration")

TARGET_ENDPOINTS = {
    "hospital_1": {
        "upload": HOSPITAL_1_UPLOAD_URL,
        "model_family": "hospital_1_model",
    },
    "hospital_2": {
        "upload": HOSPITAL_2_UPLOAD_URL,
        "model_family": "hospital_2_model",
    },
}


def _load_uploaded_model(model_family: str):
    entry = get_active_version(MODELS_DIR, model_family)
    if entry is None:
        return None, None

    artifact_path = Path(str(entry["path"]))
    if not artifact_path.exists():
        raise FileNotFoundError(
            f"Active {model_family} artifact is missing on main server: {artifact_path}"
        )

    model = joblib.load(artifact_path)
    contributor = {
        "model_family": model_family,
        "version_name": entry["version_name"],
        "path": str(artifact_path),
    }
    return model, contributor


def aggregate_pipeline() -> dict[str, object]:
    main_entry = get_active_version(MODELS_DIR, "main_model")
    main_path = Path(str(main_entry["path"])) if main_entry is not None else BASE_MODEL_PATH
    if not main_path.exists():
        raise FileNotFoundError("Main model missing. Train main model first.")

    logger.info("event=aggregate_pipeline status=start")

    main_model = joblib.load(main_path)
    models = [main_model]
    contributors = [
        {
            "model_family": "main_model",
            "version_name": main_entry["version_name"] if main_entry is not None else None,
            "path": str(main_path),
        }
    ]

    for family in ("hospital_1_model", "hospital_2_model"):
        uploaded_model, contributor = _load_uploaded_model(family)
        if uploaded_model is None or contributor is None:
            continue
        models.append(uploaded_model)
        contributors.append(contributor)

    if len(models) == 1:
        raise FileNotFoundError(
            "No deployed hospital model found on main server. "
            "Hospitals must deploy/upload first."
        )

    aggregate_result = aggregate_models(models, contributors)
    metrics = evaluate_main_model()
    logger.info(
        "event=aggregate_pipeline status=complete output=%s members=%s metrics=%s",
        aggregate_result["model_path"],
        len(models),
        metrics,
    )

    return {
        "message": "Aggregation complete. Main model updated.",
        "main_model_path": aggregate_result["model_path"],
        "active_version": aggregate_result["active_version"],
        "contributors": contributors,
        "member_count": len(models),
        "rows": aggregate_result["rows"],
        "datasets": aggregate_result["datasets"],
        "metrics": metrics,
    }


def retrain_hospitals(targets: list[str], dataset: str = "set2") -> dict[str, object]:
    normalized_targets = [target.strip().lower() for target in targets if target.strip()]
    if not normalized_targets:
        raise ValueError("At least one retrain target is required.")

    disabled: list[str] = []
    unknown: list[str] = []

    for target in normalized_targets:
        if target == "main":
            continue
        if TARGET_ENDPOINTS.get(target) is None:
            unknown.append(target)
            continue
        disabled.append(target)

    return {
        "message": (
            "Main-driven hospital retraining is disabled. "
            "Hospitals must retrain locally and deploy/upload explicitly."
        ),
        "dataset": dataset,
        "disabled_targets": disabled,
        "unknown_targets": unknown,
    }


def deploy_to_hospitals() -> dict[str, object]:
    main_entry = get_active_version(MODELS_DIR, "main_model")
    model_path = Path(str(main_entry["path"])) if main_entry is not None else BASE_MODEL_PATH
    if not model_path.exists():
        raise FileNotFoundError("No main model available to deploy. Train or aggregate first.")

    results: dict[str, object] = {}
    success_count = 0

    for hospital_name, endpoint in TARGET_ENDPOINTS.items():
        last_error: str | None = None
        for _ in range(max(1, REQUEST_RETRIES)):
            try:
                with model_path.open("rb") as handle:
                    files = {"model_file": (model_path.name, handle, "application/octet-stream")}
                    response = requests.post(endpoint["upload"], files=files, timeout=REQUEST_TIMEOUT_SECONDS)
                response.raise_for_status()
                payload = response.json()
                results[hospital_name] = {
                    "ok": True,
                    "endpoint": endpoint["upload"],
                    "response": payload,
                }
                success_count += 1
                last_error = None
                break
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)

        if last_error is not None:
            results[hospital_name] = {
                "ok": False,
                "endpoint": endpoint["upload"],
                "error": last_error,
            }

    if success_count == 0:
        raise RuntimeError("Deployment to hospitals failed for all targets.")

    return {
        "message": "Main model pushed to hospitals.",
        "source_version": main_entry["version_name"] if main_entry is not None else None,
        "model_path": str(model_path),
        "success_count": success_count,
        "results": results,
    }


def forward_uploaded_model(
    file_path: Path,
    *,
    source_server: str,
    target_server: str,
    model_family: str,
) -> dict[str, object]:
    target_key = target_server.strip().lower()
    if target_key == "main":
        return {
            "target": "main",
            "mode": "local_registry",
            "message": "Model retained on main server registry.",
        }

    endpoint = TARGET_ENDPOINTS.get(target_key)
    if endpoint is None:
        raise ValueError(f"Unknown target server: {target_server}")

    with file_path.open("rb") as handle:
        files = {"model_file": (file_path.name, handle, "application/octet-stream")}
        data = {
            "source_server": source_server,
            "target_server": target_key,
            "model_family": endpoint["model_family"],
        }
        response = requests.post(endpoint["upload"], data=data, files=files, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()

    return {
        "target": target_key,
        "mode": "forwarded_upload",
        "target_response": payload,
        "model_family": model_family,
    }
