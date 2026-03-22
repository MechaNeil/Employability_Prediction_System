from __future__ import annotations

import io
import logging
from pathlib import Path
import time

import joblib
import requests

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    HOSPITAL_1_MODEL_URL,
    HOSPITAL_1_RETRAIN_URL,
    HOSPITAL_1_UPLOAD_URL,
    HOSPITAL_2_MODEL_URL,
    HOSPITAL_2_RETRAIN_URL,
    HOSPITAL_2_UPLOAD_URL,
    REQUEST_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
)
from main_server.app.services.aggregation import aggregate_models
from main_server.app.services.evaluation import evaluate_global_model


logger = logging.getLogger("main_server.orchestration")

TARGET_ENDPOINTS = {
    "hospital_1": {
        "retrain": HOSPITAL_1_RETRAIN_URL,
        "upload": HOSPITAL_1_UPLOAD_URL,
        "model_family": "hospital_1_model",
    },
    "hospital_2": {
        "retrain": HOSPITAL_2_RETRAIN_URL,
        "upload": HOSPITAL_2_UPLOAD_URL,
        "model_family": "hospital_2_model",
    },
}


def _post_with_retry(
    url: str,
    *,
    json_payload: dict[str, object] | None = None,
    retries: int = REQUEST_RETRIES,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> None:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            logger.info("event=post_request status=start url=%s attempt=%s", url, attempt + 1)
            response = requests.post(url, json=json_payload, timeout=timeout)
            response.raise_for_status()
            logger.info("event=post_request status=ok url=%s attempt=%s", url, attempt + 1)
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            delay = 2**attempt
            logger.warning(
                "event=post_request status=retry url=%s attempt=%s delay_seconds=%s error=%s",
                url,
                attempt + 1,
                delay,
                exc,
            )
            time.sleep(delay)
    raise RuntimeError(f"Failed calling {url}: {last_error}")


def _get_model_with_retry(url: str, retries: int = REQUEST_RETRIES, timeout: int = REQUEST_TIMEOUT_SECONDS):
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            logger.info("event=model_download status=start url=%s attempt=%s", url, attempt + 1)
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logger.info("event=model_download status=ok url=%s attempt=%s", url, attempt + 1)
            return joblib.load(io.BytesIO(response.content))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            delay = 2**attempt
            logger.warning(
                "event=model_download status=retry url=%s attempt=%s delay_seconds=%s error=%s",
                url,
                attempt + 1,
                delay,
                exc,
            )
            time.sleep(delay)
    raise RuntimeError(f"Failed downloading model from {url}: {last_error}")


def aggregate_pipeline() -> dict[str, object]:
    if not BASE_MODEL_PATH.exists():
        raise FileNotFoundError("Main model missing. Train main model first.")

    logger.info("event=aggregate_pipeline status=start")

    _post_with_retry(HOSPITAL_1_RETRAIN_URL)
    _post_with_retry(HOSPITAL_2_RETRAIN_URL)

    main_model = joblib.load(BASE_MODEL_PATH)
    hospital_1_model = _get_model_with_retry(HOSPITAL_1_MODEL_URL)
    hospital_2_model = _get_model_with_retry(HOSPITAL_2_MODEL_URL)

    output_path = aggregate_models([main_model, hospital_1_model, hospital_2_model])
    metrics = evaluate_global_model()
    logger.info("event=aggregate_pipeline status=complete output=%s metrics=%s", output_path, metrics)

    return {
        "message": "Aggregation complete.",
        "global_model_path": output_path,
        "metrics": metrics,
    }


def retrain_hospitals(targets: list[str], dataset: str = "set2") -> dict[str, object]:
    normalized_targets = [target.strip().lower() for target in targets if target.strip()]
    if not normalized_targets:
        raise ValueError("At least one retrain target is required.")

    successful: list[str] = []
    failed: list[dict[str, str]] = []

    for target in normalized_targets:
        if target == "main":
            continue
        endpoint = TARGET_ENDPOINTS.get(target)
        if endpoint is None:
            failed.append({"target": target, "error": "Unknown retrain target"})
            continue
        try:
            _post_with_retry(endpoint["retrain"], json_payload={"dataset": dataset})
            successful.append(target)
        except Exception as exc:  # noqa: BLE001
            failed.append({"target": target, "error": str(exc)})

    return {
        "message": "Retrain request processed.",
        "dataset": dataset,
        "successful": successful,
        "failed": failed,
    }


def deploy_to_hospitals() -> dict[str, str]:
    if not BASE_MODEL_PATH.exists():
        raise FileNotFoundError("Main model missing. Train main model first.")
    return {
        "message": "Deployment simulation complete. Hospitals pull the latest central model on retraining.",
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
