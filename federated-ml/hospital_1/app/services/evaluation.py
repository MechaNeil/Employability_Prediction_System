from __future__ import annotations

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from hospital_1.app.services.model_registry import get_active
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_dataset_path


def evaluate_active_model(test_dataset: str) -> dict[str, object]:
    active = get_active()
    if active is None:
        raise FileNotFoundError("No active model available for hospital_1.")

    model = joblib.load(active["path"])
    dataset_path = get_dataset_path(test_dataset)
    df = pd.read_csv(dataset_path)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    preds = model.predict(x)

    return {
        "version_name": active["version_name"],
        "dataset": test_dataset,
        "rows": int(len(df)),
        "accuracy": float(accuracy_score(y, preds)),
        "precision": float(precision_score(y, preds, zero_division=0)),
        "recall": float(recall_score(y, preds, zero_division=0)),
        "f1": float(f1_score(y, preds, zero_division=0)),
    }
