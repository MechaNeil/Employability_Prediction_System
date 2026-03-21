from __future__ import annotations

import io
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import requests
from sklearn.metrics import accuracy_score

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    GLOBAL_MODEL_PATH,
    HOSPITAL_1_HEALTH_URL,
    HOSPITAL_1_MODEL_URL,
    HOSPITAL_2_HEALTH_URL,
    HOSPITAL_2_MODEL_URL,
)
from main_server.app.services.evaluation import evaluate_global_model
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN, TEST_FILE


def _model_info(path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "exists": False,
            "path": str(path),
            "size_bytes": 0,
            "updated_utc": None,
        }

    stat = path.stat()
    return {
        "exists": True,
        "path": str(path),
        "size_bytes": int(stat.st_size),
        "updated_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }


def _service_health(url: str) -> dict[str, object]:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        payload = response.json()
        return {
            "online": True,
            "details": payload,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "online": False,
            "details": str(exc),
        }


def get_model_versions() -> dict[str, object]:
    return {
        "base_model": _model_info(BASE_MODEL_PATH),
        "global_model": _model_info(GLOBAL_MODEL_PATH),
    }


def _safe_accuracy(model) -> float | None:
    try:
        df = pd.read_csv(TEST_FILE)
        x = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]
        preds = model.predict(x)
        return float(accuracy_score(y, preds))
    except Exception:  # noqa: BLE001
        return None


def _load_hospital_model(model_url: str):
    try:
        response = requests.get(model_url, timeout=10)
        response.raise_for_status()
        return joblib.load(io.BytesIO(response.content))
    except Exception:  # noqa: BLE001
        return None


def get_performance_comparison() -> dict[str, float | None]:
    base_accuracy: float | None = None
    if BASE_MODEL_PATH.exists():
        base_model = joblib.load(BASE_MODEL_PATH)
        base_accuracy = _safe_accuracy(base_model)

    global_accuracy: float | None = None
    if GLOBAL_MODEL_PATH.exists():
        global_model = joblib.load(GLOBAL_MODEL_PATH)
        global_accuracy = _safe_accuracy(global_model)

    h1_model = _load_hospital_model(HOSPITAL_1_MODEL_URL)
    h2_model = _load_hospital_model(HOSPITAL_2_MODEL_URL)
    h1_accuracy = _safe_accuracy(h1_model) if h1_model is not None else None
    h2_accuracy = _safe_accuracy(h2_model) if h2_model is not None else None

    return {
        "main": base_accuracy,
        "hospital_1": h1_accuracy,
        "hospital_2": h2_accuracy,
        "global": global_accuracy,
    }


def get_system_status() -> dict[str, object]:
    metrics: dict[str, object]
    try:
        metrics = evaluate_global_model()
    except Exception as exc:  # noqa: BLE001
        metrics = {"available": False, "reason": str(exc)}

    versions = get_model_versions()
    comparison = get_performance_comparison()

    return {
        "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
        "hospitals": {
            "hospital_1": _service_health(HOSPITAL_1_HEALTH_URL),
            "hospital_2": _service_health(HOSPITAL_2_HEALTH_URL),
        },
        "models": versions,
        "metrics": metrics,
        "comparison": comparison,
    }
