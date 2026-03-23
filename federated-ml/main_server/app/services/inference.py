from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from main_server.app.core.config import BASE_MODEL_PATH, MODELS_DIR
from shared.constants import FEATURE_COLUMNS, INV_LABEL_MAP
from shared.model_registry import get_active_version


def _load_active_model():
    active = get_active_version(MODELS_DIR, "main_model")
    model_path = BASE_MODEL_PATH if active is None else Path(str(active["path"]))
    if not model_path.exists():
        raise FileNotFoundError("No model available. Run /train first.")
    return joblib.load(model_path), str(model_path)


def predict_records(records: list[dict[str, float]]) -> dict[str, object]:
    if not records:
        raise ValueError("records cannot be empty")

    frame = pd.DataFrame(records)

    missing = [column for column in FEATURE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    x = frame[FEATURE_COLUMNS]
    model, model_path = _load_active_model()

    raw_predictions = model.predict(x)
    labels = [INV_LABEL_MAP.get(int(pred), str(pred)) for pred in raw_predictions]

    response: dict[str, object] = {
        "model_path": model_path,
        "predictions": labels,
    }

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(x)
        response["confidence"] = [float(max(row)) for row in probabilities]

    return response
