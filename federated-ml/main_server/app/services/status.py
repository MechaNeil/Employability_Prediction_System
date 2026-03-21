from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import requests

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    GLOBAL_MODEL_PATH,
    HOSPITAL_1_HEALTH_URL,
    HOSPITAL_2_HEALTH_URL,
)
from main_server.app.services.evaluation import evaluate_global_model


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


def get_system_status() -> dict[str, object]:
    metrics: dict[str, object]
    try:
        metrics = evaluate_global_model()
    except Exception as exc:  # noqa: BLE001
        metrics = {"available": False, "reason": str(exc)}

    versions = get_model_versions()

    return {
        "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
        "hospitals": {
            "hospital_1": _service_health(HOSPITAL_1_HEALTH_URL),
            "hospital_2": _service_health(HOSPITAL_2_HEALTH_URL),
        },
        "models": versions,
        "metrics": metrics,
    }
