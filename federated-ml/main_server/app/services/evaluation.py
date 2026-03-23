from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from main_server.app.core.config import BASE_MODEL_PATH, MODELS_DIR
from shared.constants import FEATURE_COLUMNS, TARGET_COLUMN
from shared.datasets import get_all_test_dataset_paths, get_dataset_path, normalize_dataset_key
from shared.model_registry import get_active_version


def _active_main_model_path() -> str:
    active = get_active_version(MODELS_DIR, "main_model")
    if active is not None:
        return str(active["path"])
    return str(BASE_MODEL_PATH)


def evaluate_main_model(dataset: str = "all") -> dict[str, object]:
    model_path = _active_main_model_path()
    if not Path(model_path).exists():
        raise FileNotFoundError("Main model does not exist. Run /train first.")

    model = joblib.load(model_path)
    dataset_key = dataset.strip().lower().replace("-", "")
    if dataset_key == "all":
        test_paths = get_all_test_dataset_paths()
        selected_dataset = "all"
    else:
        selected_dataset = normalize_dataset_key(dataset)
        test_paths = [get_dataset_path(selected_dataset, purpose="test")]

    test_frames = [pd.read_csv(path) for path in test_paths]
    df = pd.concat(test_frames, ignore_index=True)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    preds = model.predict(x)

    metrics = {
        "accuracy": float(accuracy_score(y, preds)),
        "precision": float(precision_score(y, preds, zero_division=0)),
        "recall": float(recall_score(y, preds, zero_division=0)),
        "f1": float(f1_score(y, preds, zero_division=0)),
    }

    return {
        "dataset": selected_dataset,
        "rows_evaluated": int(len(df)),
        "metrics": metrics,
    }


def evaluate_global_model(dataset: str = "all") -> dict[str, object]:
    return evaluate_main_model(dataset=dataset)
