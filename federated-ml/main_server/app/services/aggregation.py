from __future__ import annotations

import numpy as np
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from main_server.app.core.config import AGGREGATION_DATASETS, BASE_MODEL_PATH
from main_server.app.services.model_registry import bootstrap_registry, register_main_model
from shared.constants import FEATURE_COLUMNS, RANDOM_STATE
from shared.datasets import get_dataset_path


def _majority_vote_labels(models: list[object], x: pd.DataFrame) -> np.ndarray:
    predictions = np.array([model.predict(x) for model in models])
    votes_for_one = predictions.sum(axis=0)
    return (votes_for_one >= (len(models) / 2)).astype(int)


def aggregate_models(models: list[object], contributors: list[dict[str, object]]) -> dict[str, object]:
    bootstrap_registry()
    train_frames = [pd.read_csv(get_dataset_path(dataset_key, purpose="train")) for dataset_key in AGGREGATION_DATASETS]
    train_df = pd.concat(train_frames, ignore_index=True)
    x = train_df[FEATURE_COLUMNS]

    pseudo_targets = _majority_vote_labels(models, x)
    aggregated_model = RandomForestClassifier(n_estimators=120, random_state=RANDOM_STATE)
    aggregated_model.fit(x, pseudo_targets)

    joblib.dump(aggregated_model, BASE_MODEL_PATH)
    version_entry = register_main_model(
        BASE_MODEL_PATH,
        metadata={
            "mode": "aggregate_distill",
            "members": len(models),
            "contributors": contributors,
            "datasets": list(AGGREGATION_DATASETS),
            "rows": int(len(train_df)),
        },
    )
    return {
        "model_path": str(BASE_MODEL_PATH),
        "active_version": version_entry["version_name"],
        "rows": int(len(train_df)),
        "datasets": list(AGGREGATION_DATASETS),
    }
