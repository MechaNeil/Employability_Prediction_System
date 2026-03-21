from __future__ import annotations

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from main_server.app.core.config import BASE_MODEL_PATH
from shared.constants import FEATURE_COLUMNS, RANDOM_STATE, SET1_FILE, TARGET_COLUMN


def train_main_model() -> dict[str, object]:
    df = pd.read_csv(SET1_FILE)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(x, y)

    joblib.dump(model, BASE_MODEL_PATH)

    return {
        "message": "Main model trained.",
        "model_path": str(BASE_MODEL_PATH),
        "rows": int(len(df)),
    }


if __name__ == "__main__":
    print(train_main_model())
