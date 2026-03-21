from __future__ import annotations

import joblib
import pandas as pd

from main_server.app.core.config import BASE_MODEL_PATH, GLOBAL_MODEL_PATH
from shared.constants import FEATURE_COLUMNS, INV_LABEL_MAP


def _load_active_model():
    model_path = GLOBAL_MODEL_PATH if GLOBAL_MODEL_PATH.exists() else BASE_MODEL_PATH
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
