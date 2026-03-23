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
from main_server.app.services.evaluation import evaluate_global_model
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
    if not BASE_MODEL_PATH.exists():
        raise FileNotFoundError("Main model missing. Train main model first.")

    logger.info("event=aggregate_pipeline status=start")

    main_model = joblib.load(BASE_MODEL_PATH)
    models = [main_model]
    contributors = [
        {
            "model_family": "main_model",
            "path": str(BASE_MODEL_PATH),
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

    output_path = aggregate_models(models)
    metrics = evaluate_global_model()
    logger.info(
        "event=aggregate_pipeline status=complete output=%s members=%s metrics=%s",
        output_path,
        len(models),
        metrics,
    )

    return {
        "message": "Aggregation complete.",
        "global_model_path": output_path,
        "contributors": contributors,
        "member_count": len(models),
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


def deploy_to_hospitals() -> dict[str, str]:
    return {
        "message": (
            "Push-to-hospital deployment is disabled. "
            "Hospitals control training and deploy models to main_server explicitly."
        ),
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
