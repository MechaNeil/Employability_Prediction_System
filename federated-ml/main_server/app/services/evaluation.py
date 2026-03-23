from __future__ import annotations

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from main_server.app.core.config import GLOBAL_MODEL_PATH
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_all_test_dataset_paths


def evaluate_global_model() -> dict[str, float]:
    if not GLOBAL_MODEL_PATH.exists():
        raise FileNotFoundError("Global model does not exist. Run /aggregate first.")

    model = joblib.load(GLOBAL_MODEL_PATH)
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
