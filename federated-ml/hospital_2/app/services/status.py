from __future__ import annotations

from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from hospital_2.app.services.evaluation import evaluate_active_model
from hospital_2.app.services.model_registry import get_active, get_versions
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_dataset_path, normalize_dataset_key


def _safe_eval(dataset: str) -> dict[str, object] | None:
    try:
        return evaluate_active_model(dataset)
    except Exception:  # noqa: BLE001
        return None


def _eval_model_path(model_path: str, test_dataset: str) -> dict[str, float]:
    model = joblib.load(model_path)
    df = pd.read_csv(get_dataset_path(test_dataset))
    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    preds = model.predict(x)
    return {
        "accuracy": float(accuracy_score(y, preds)),
        "precision": float(precision_score(y, preds, zero_division=0)),
        "recall": float(recall_score(y, preds, zero_division=0)),
        "f1": float(f1_score(y, preds, zero_division=0)),
    }


def get_training_set_comparison(test_dataset: str) -> dict[str, object]:
    selected_test = normalize_dataset_key(test_dataset)
    versions = get_versions()

    by_dataset: dict[str, dict[str, object] | None] = {
        "set1": None,
        "set2": None,
        "set3": None,
    }

    for dataset_key in ["set1", "set2", "set3"]:
        candidates = [
            item
            for item in versions
            if item.get("metadata", {}).get("dataset") == dataset_key
        ]
        if not candidates:
            continue

        latest = max(candidates, key=lambda item: int(item.get("version", 0)))
        metrics = _eval_model_path(latest["path"], selected_test)
        by_dataset[dataset_key] = {
            "version_name": latest["version_name"],
            "test_dataset": selected_test,
            "metrics": metrics,
        }

    return {
        "service": "hospital_2",
        "test_dataset": selected_test,
        "comparison": by_dataset,
    }


def get_system_status() -> dict[str, object]:
    active = get_active()
    versions = get_versions()

    return {
        "timestamp_utc": datetime.now(tz=timezone.utc).isoformat(),
        "service": "hospital_2",
        "active_model": active,
        "version_count": len(versions),
        "versions": versions,
        "evaluation_by_set": {
            "set1": _safe_eval("set1"),
            "set2": _safe_eval("set2"),
            "set3": _safe_eval("set3"),
        },
    }
