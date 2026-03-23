from __future__ import annotations

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from employability_1.app.services.model_registry import get_active
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_dataset_path, normalize_dataset_key


def evaluate_active_model(test_dataset: str) -> dict[str, object]:
    active = get_active()
    if active is None:
        raise FileNotFoundError("No active model available for employability_1.")

    model = joblib.load(active["path"])
    dataset_key = normalize_dataset_key(test_dataset)
    dataset_path = get_dataset_path(dataset_key, purpose="test")
    df = pd.read_csv(dataset_path)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    preds = model.predict(x)

    return {
        "version_name": active["version_name"],
        "dataset": dataset_key,
        "rows": int(len(df)),
        "accuracy": float(accuracy_score(y, preds)),
        "precision": float(precision_score(y, preds, zero_division=0)),
        "recall": float(recall_score(y, preds, zero_division=0)),
        "f1": float(f1_score(y, preds, zero_division=0)),
    }

