from __future__ import annotations

import io
import time

import joblib
import requests

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    HOSPITAL_1_MODEL_URL,
    HOSPITAL_1_RETRAIN_URL,
    HOSPITAL_2_MODEL_URL,
    HOSPITAL_2_RETRAIN_URL,
)
from main_server.app.services.aggregation import aggregate_models
from main_server.app.services.evaluation import evaluate_global_model


def _post_with_retry(url: str, retries: int = 3, timeout: int = 30) -> None:
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            response = requests.post(url, timeout=timeout)
            response.raise_for_status()
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Failed calling {url}: {last_error}")


def _get_model_with_retry(url: str, retries: int = 3, timeout: int = 30):
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return joblib.load(io.BytesIO(response.content))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Failed downloading model from {url}: {last_error}")


def aggregate_pipeline() -> dict[str, object]:
    if not BASE_MODEL_PATH.exists():
        raise FileNotFoundError("Main model missing. Train main model first.")

    _post_with_retry(HOSPITAL_1_RETRAIN_URL)
    _post_with_retry(HOSPITAL_2_RETRAIN_URL)

    main_model = joblib.load(BASE_MODEL_PATH)
    hospital_1_model = _get_model_with_retry(HOSPITAL_1_MODEL_URL)
    hospital_2_model = _get_model_with_retry(HOSPITAL_2_MODEL_URL)

    output_path = aggregate_models([main_model, hospital_1_model, hospital_2_model])
    metrics = evaluate_global_model()

    return {
        "message": "Aggregation complete.",
        "global_model_path": output_path,
        "metrics": metrics,
    }
