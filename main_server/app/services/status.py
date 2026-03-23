from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import requests
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from main_server.app.core.config import (
    BASE_MODEL_PATH,
    EMPLOYABILITY_1_HEALTH_URL,
    EMPLOYABILITY_2_HEALTH_URL,
    MODELS_DIR,
)
from main_server.app.services.model_registry import get_registry_overview
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_all_test_dataset_paths, get_dataset_path, normalize_dataset_key
from shared.model_registry import get_active_version


def _default_comparison() -> dict[str, float | None]:
    return {
        "main": None,
        "employability_1": None,
        "employability_2": None,
        "aggregated_main": None,
    }


def _default_model_metrics() -> dict[str, dict[str, float] | None]:
    return {
        "main": None,
        "employability_1": None,
        "employability_2": None,
        "aggregated_main": None,
    }


_STATUS_REFRESH_MIN_SECONDS = 12
_CACHE_LOCK = threading.Lock()
_STATUS_CACHE: dict[str, Any] = {
    "metrics": {"available": False, "reason": "No evaluation available yet."},
    "comparison": _default_comparison(),
    "model_metrics": _default_model_metrics(),
    "last_refresh_utc": None,
    "refreshing": False,
}


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
        "registry": get_registry_overview(),
    }


def _safe_accuracy(model) -> float | None:
    try:
        test_frames = [pd.read_csv(path) for path in get_all_test_dataset_paths()]
        df = pd.concat(test_frames, ignore_index=True)
        x = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]
        preds = model.predict(x)
        return float(accuracy_score(y, preds))
    except Exception:  # noqa: BLE001
        return None


def _safe_metric_bundle(model) -> dict[str, float] | None:
    if model is None:
        return None

    try:
        test_frames = [pd.read_csv(path) for path in get_all_test_dataset_paths()]
        df = pd.concat(test_frames, ignore_index=True)
        x = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]
        preds = model.predict(x)
        return {
            "accuracy": float(accuracy_score(y, preds)),
            "precision": float(precision_score(y, preds, zero_division=0)),
            "recall": float(recall_score(y, preds, zero_division=0)),
            "f1": float(f1_score(y, preds, zero_division=0)),
        }
    except Exception:  # noqa: BLE001
        return None


def _metric_bundle_for_dataset(model, dataset_key: str) -> dict[str, float] | None:
    try:
        dataset_path = get_dataset_path(dataset_key, purpose="test")
        df = pd.read_csv(dataset_path)
        x = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]
        preds = model.predict(x)
        return {
            "accuracy": float(accuracy_score(y, preds)),
            "precision": float(precision_score(y, preds, zero_division=0)),
            "recall": float(recall_score(y, preds, zero_division=0)),
            "f1": float(f1_score(y, preds, zero_division=0)),
        }
    except Exception:  # noqa: BLE001
        return None


def _load_employability_model(model_family: str):
    try:
        active_version = get_active_version(MODELS_DIR, model_family)
        if active_version is None:
            return None
        artifact_path = Path(str(active_version["path"]))
        if not artifact_path.exists():
            return None
        return joblib.load(artifact_path)
    except Exception:  # noqa: BLE001
        return None


def get_performance_comparison() -> dict[str, float | None]:
    active_main = get_active_version(MODELS_DIR, "main_model")
    main_model = None
    if active_main is not None:
        active_path = Path(str(active_main["path"]))
        if active_path.exists():
            main_model = joblib.load(active_path)
    elif BASE_MODEL_PATH.exists():
        main_model = joblib.load(BASE_MODEL_PATH)

    base_accuracy = _safe_accuracy(main_model) if main_model is not None else None

    h1_model = _load_employability_model("employability_1_model")
    h2_model = _load_employability_model("employability_2_model")
    h1_accuracy = _safe_accuracy(h1_model) if h1_model is not None else None
    h2_accuracy = _safe_accuracy(h2_model) if h2_model is not None else None

    return {
        "main": base_accuracy,
        "employability_1": h1_accuracy,
        "employability_2": h2_accuracy,
        "aggregated_main": base_accuracy,
    }


def get_model_metric_comparison() -> dict[str, dict[str, float] | None]:
    active_main = get_active_version(MODELS_DIR, "main_model")
    base_model = None
    if active_main is not None:
        active_path = Path(str(active_main["path"]))
        if active_path.exists():
            base_model = joblib.load(active_path)
    elif BASE_MODEL_PATH.exists():
        base_model = joblib.load(BASE_MODEL_PATH)

    h1_model = _load_employability_model("employability_1_model")
    h2_model = _load_employability_model("employability_2_model")

    main_bundle = _safe_metric_bundle(base_model)

    return {
        "main": main_bundle,
        "employability_1": _safe_metric_bundle(h1_model),
        "employability_2": _safe_metric_bundle(h2_model),
        "aggregated_main": main_bundle,
    }


def _compute_expensive_snapshot() -> dict[str, Any]:
    comparison = get_performance_comparison()
    model_metrics = get_model_metric_comparison()
    return {
        "comparison": comparison,
        "model_metrics": model_metrics,
        "last_refresh_utc": datetime.now(tz=timezone.utc).isoformat(),
    }


def _refresh_cache_worker() -> None:
    snapshot: dict[str, Any] | None = None
    try:
        snapshot = _compute_expensive_snapshot()
    finally:
        with _CACHE_LOCK:
            if snapshot is not None:
                _STATUS_CACHE.update(snapshot)
            _STATUS_CACHE["refreshing"] = False


def trigger_status_refresh(force: bool = False) -> None:
    with _CACHE_LOCK:
        last_refresh = _STATUS_CACHE.get("last_refresh_utc")
        stale = True
        if isinstance(last_refresh, str):
            try:
                parsed = datetime.fromisoformat(last_refresh)
                stale = (datetime.now(tz=timezone.utc) - parsed).total_seconds() >= _STATUS_REFRESH_MIN_SECONDS
            except ValueError:
                stale = True

        if not force and not stale:
            return
        if _STATUS_CACHE["refreshing"]:
            return
        _STATUS_CACHE["refreshing"] = True

    thread = threading.Thread(target=_refresh_cache_worker, daemon=True)
    thread.start()


def cache_latest_evaluation(metrics: dict[str, object]) -> None:
    with _CACHE_LOCK:
        _STATUS_CACHE["metrics"] = metrics
        _STATUS_CACHE["last_refresh_utc"] = datetime.now(tz=timezone.utc).isoformat()


def get_system_status() -> dict[str, object]:
    versions = get_model_versions()
    trigger_status_refresh(force=False)

    with ThreadPoolExecutor(max_workers=2) as executor:
        employability_1_future = executor.submit(_service_health, EMPLOYABILITY_1_HEALTH_URL)
        employability_2_future = executor.submit(_service_health, EMPLOYABILITY_2_HEALTH_URL)
        employability_1 = employability_1_future.result()
        employability_2 = employability_2_future.result()

    with _CACHE_LOCK:
        metrics = dict(_STATUS_CACHE.get("metrics") or {})
        comparison = dict(_STATUS_CACHE.get("comparison") or _default_comparison())
        model_metrics = dict(_STATUS_CACHE.get("model_metrics") or _default_model_metrics())
        cache_refreshing = bool(_STATUS_CACHE.get("refreshing"))
        cache_last_refresh = _STATUS_CACHE.get("last_refresh_utc")

    return {
        "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
        "employabilitys": {
            "employability_1": employability_1,
            "employability_2": employability_2,
        },
        "models": versions,
        "metrics": metrics,
        "comparison": comparison,
        "model_metrics": model_metrics,
        "status_cache": {
            "refreshing": cache_refreshing,
            "last_refresh_utc": cache_last_refresh,
        },
    }


def compare_named_versions(test_dataset: str, items: list[dict[str, str]]) -> dict[str, object]:
    dataset_key = normalize_dataset_key(test_dataset)
    registry = get_registry_overview()
    results: list[dict[str, Any]] = []

    for item in items:
        label = item.get("label", "")
        model_family = item.get("model_family", "")
        version_name = item.get("version_name", "")

        family = registry.get(model_family)
        versions = family.get("versions", []) if isinstance(family, dict) else []

        selected = None
        for version in versions:
            if version.get("version_name") == version_name:
                selected = version
                break

        if selected is None:
            results.append(
                {
                    "label": label or version_name,
                    "model_family": model_family,
                    "version_name": version_name,
                    "metrics": None,
                    "error": "Version not found in registry.",
                }
            )
            continue

        model_path = Path(str(selected.get("path", "")))
        if not model_path.exists():
            results.append(
                {
                    "label": label or version_name,
                    "model_family": model_family,
                    "version_name": version_name,
                    "metrics": None,
                    "error": f"Model artifact missing: {model_path}",
                }
            )
            continue

        model = joblib.load(model_path)
        metrics = _metric_bundle_for_dataset(model, dataset_key)
        results.append(
            {
                "label": label or version_name,
                "model_family": model_family,
                "version_name": version_name,
                "metrics": metrics,
                "error": None if metrics is not None else "Evaluation failed.",
            }
        )

    return {
        "test_dataset": dataset_key,
        "results": results,
    }

