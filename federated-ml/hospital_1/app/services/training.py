from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from shared.constants import FEATURE_COLUMNS, SET2_FILE, TARGET_COLUMN

ROOT = Path(__file__).resolve().parents[3]
LOCAL_MODEL_PATH = ROOT / "hospital_1" / "app" / "models" / "hospital_model.pkl"
MAIN_MODEL_V2 = ROOT / "main_server" / "app" / "models" / "main_model_v2.pkl"
MAIN_MODEL_V1 = ROOT / "main_server" / "app" / "models" / "model.pkl"


def retrain_model() -> dict[str, object]:
    source_model_path = MAIN_MODEL_V2 if MAIN_MODEL_V2.exists() else MAIN_MODEL_V1
    if not source_model_path.exists():
        raise FileNotFoundError("No source global model found in main server.")

    model = joblib.load(source_model_path)
    df = pd.read_csv(SET2_FILE)
    # Validate schema so local data issues are caught early at startup/retrain time.
    _ = df[FEATURE_COLUMNS]
    _ = df[TARGET_COLUMN]

    LOCAL_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, LOCAL_MODEL_PATH)

    return {
        "message": "Hospital-1 local model refresh complete.",
        "model_path": str(LOCAL_MODEL_PATH),
        "rows": int(len(df)),
    }


if __name__ == "__main__":
    print(retrain_model())
