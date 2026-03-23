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


def _resolve_test_frame(dataset: str) -> tuple[str, pd.DataFrame]:
    dataset_key = dataset.strip().lower().replace("-", "")
    if dataset_key == "all":
        test_paths = get_all_test_dataset_paths()
        selected_dataset = "all"
    else:
        selected_dataset = normalize_dataset_key(dataset)
        test_paths = [get_dataset_path(selected_dataset, purpose="test")]

    test_frames = [pd.read_csv(path) for path in test_paths]
    return selected_dataset, pd.concat(test_frames, ignore_index=True)


def _evaluate_loaded_model(model, df: pd.DataFrame) -> dict[str, float]:
    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    preds = model.predict(x)

    return {
        "accuracy": float(accuracy_score(y, preds)),
        "precision": float(precision_score(y, preds, zero_division=0)),
        "recall": float(recall_score(y, preds, zero_division=0)),
        "f1": float(f1_score(y, preds, zero_division=0)),
    }


def _load_active_model(model_family: str):
    if model_family == "main_model":
        main_path = Path(_active_main_model_path())
        if not main_path.exists():
            raise FileNotFoundError("Main model does not exist. Run /train first.")
        return joblib.load(main_path)

    active = get_active_version(MODELS_DIR, model_family)
    if active is None:
        return None

    artifact_path = Path(str(active["path"]))
    if not artifact_path.exists():
        return None

    return joblib.load(artifact_path)


def evaluate_models(dataset: str = "all", scope: str = "main") -> dict[str, object]:
    selected_scope = scope.strip().lower().replace("-", "_")
    if selected_scope not in {"main", "all"}:
        raise ValueError("scope must be 'main' or 'all'.")

    selected_dataset, df = _resolve_test_frame(dataset)
    main_model = _load_active_model("main_model")

    model_metrics: dict[str, dict[str, float] | None] = {
        "main": _evaluate_loaded_model(main_model, df),
        "employability_1": None,
        "employability_2": None,
    }

    if selected_scope == "all":
        employability_1_model = _load_active_model("employability_1_model")
        if employability_1_model is not None:
            model_metrics["employability_1"] = _evaluate_loaded_model(employability_1_model, df)

        employability_2_model = _load_active_model("employability_2_model")
        if employability_2_model is not None:
            model_metrics["employability_2"] = _evaluate_loaded_model(employability_2_model, df)

    evaluated_models = [name for name, metrics in model_metrics.items() if metrics is not None]
    missing_models = [name for name, metrics in model_metrics.items() if metrics is None]

    return {
        "dataset": selected_dataset,
        "scope": selected_scope,
        "rows_evaluated": int(len(df)),
        "metrics": model_metrics["main"],
        "model_metrics": model_metrics,
        "evaluated_models": evaluated_models,
        "missing_models": missing_models,
    }


def evaluate_main_model(dataset: str = "all") -> dict[str, object]:
    return evaluate_models(dataset=dataset, scope="main")


def evaluate_global_model(dataset: str = "all") -> dict[str, object]:
    return evaluate_main_model(dataset=dataset)
