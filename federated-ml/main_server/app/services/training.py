from __future__ import annotations

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from main_server.app.core.config import BASE_MODEL_PATH
from main_server.app.services.model_registry import bootstrap_registry, register_main_model
from shared.constants import FEATURE_COLUMNS, RANDOM_STATE, TARGET_COLUMN
from shared.datasets import get_dataset_path, normalize_dataset_key


def train_main_model(dataset: str = "set1") -> dict[str, object]:
    bootstrap_registry()
    dataset_key = normalize_dataset_key(dataset)
    dataset_path = get_dataset_path(dataset_key, purpose="train")
    df = pd.read_csv(dataset_path)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(x, y)

    joblib.dump(model, BASE_MODEL_PATH)
    version_entry = register_main_model(
        BASE_MODEL_PATH,
        metadata={"dataset": dataset_key, "mode": "main_train"},
    )

    return {
        "message": "Main model trained.",
        "model_path": str(BASE_MODEL_PATH),
        "active_version": version_entry["version_name"],
        "dataset": dataset_key,
        "rows": int(len(df)),
    }


if __name__ == "__main__":
    print(train_main_model())
