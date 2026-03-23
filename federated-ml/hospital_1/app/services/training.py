from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from hospital_1.app.core.config import LEGACY_MODEL_PATH, MODELS_DIR
from hospital_1.app.services.model_registry import activate, get_active, initialize_registry, register_version
from shared.constants import FEATURE_COLUMNS, RANDOM_STATE, TARGET_COLUMN
from shared.datasets import get_dataset_path, normalize_dataset_key
from shared.model_registry import get_active_version

ROOT = Path(__file__).resolve().parents[3]
LOCAL_MODEL_PATH = LEGACY_MODEL_PATH
MAIN_MODELS_DIR = ROOT / "main_server" / "app" / "models"
MAIN_MODEL_V1 = ROOT / "main_server" / "app" / "models" / "model.pkl"


def _fit_fresh_model(dataset_key: str):
    dataset_path = get_dataset_path(dataset_key, purpose="train")
    df = pd.read_csv(dataset_path)
    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(x, y)
    return model, int(len(df)), dataset_path


def _load_source_model_or_none():
    active_main = get_active_version(MAIN_MODELS_DIR, "main_model")
    if active_main is not None:
        source_model_path = Path(str(active_main["path"]))
    else:
        source_model_path = MAIN_MODEL_V1

    if not source_model_path.exists():
        return None
    return joblib.load(source_model_path)


def _persist_version(model, *, dataset_key: str, mode: str) -> dict[str, object]:
    tmp_path = MODELS_DIR / "_tmp_hospital_1.pkl"
    joblib.dump(model, tmp_path)
    entry = register_version(tmp_path, metadata={"dataset": dataset_key, "mode": mode})
    if tmp_path.exists():
        tmp_path.unlink()
    return entry


def train_or_retrain_model(dataset_key: str = "set2", retrain_from_main: bool = False) -> dict[str, object]:
    initialize_registry()
    selected_dataset = normalize_dataset_key(dataset_key)
    df = pd.read_csv(get_dataset_path(selected_dataset, purpose="train"))
    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    mode = "local_train"
    model = None
    if retrain_from_main:
        model = _load_source_model_or_none()
        mode = "retrain_from_main" if model is not None else "main_unavailable_fallback"

    if model is not None and hasattr(model, "fit"):
        model.fit(x, y)
    elif model is None:
        model, _, _ = _fit_fresh_model(selected_dataset)

    entry = _persist_version(model, dataset_key=selected_dataset, mode=mode)
    return {
        "message": "Hospital-1 model training completed.",
        "dataset": selected_dataset,
        "mode": mode,
        "rows": int(len(df)),
        "active_version": entry["version_name"],
        "model_path": entry["path"],
    }


def activate_model_version(version_name: str) -> dict[str, object]:
    entry = activate(version_name)
    return {
        "message": "Hospital-1 model version activated.",
        "active_version": entry["version_name"],
        "model_path": entry["path"],
    }


def retrain_model() -> dict[str, object]:
    initialize_registry()
    return train_or_retrain_model(dataset_key="set2", retrain_from_main=True)


if __name__ == "__main__":
    initialize_registry()
    if not LOCAL_MODEL_PATH.exists():
        print(train_or_retrain_model(dataset_key="set2", retrain_from_main=False))
    else:
        active = get_active()
        print({"active_model": active["version_name"] if active else None, "model_path": str(LOCAL_MODEL_PATH)})
