from __future__ import annotations

import io
import logging
import time

import joblib
import requests

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    HOSPITAL_1_MODEL_URL,
    HOSPITAL_1_RETRAIN_URL,
    HOSPITAL_2_MODEL_URL,
    HOSPITAL_2_RETRAIN_URL,
    REQUEST_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
)
from main_server.app.services.aggregation import aggregate_models
from main_server.app.services.evaluation import evaluate_global_model


logger = logging.getLogger("main_server.orchestration")


def _post_with_retry(url: str, retries: int = REQUEST_RETRIES, timeout: int = REQUEST_TIMEOUT_SECONDS) -> None:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            logger.info("event=post_request status=start url=%s attempt=%s", url, attempt + 1)
            response = requests.post(url, timeout=timeout)
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
