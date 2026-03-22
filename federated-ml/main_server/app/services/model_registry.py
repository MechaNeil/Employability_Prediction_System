from __future__ import annotations

from pathlib import Path
from typing import Any

from main_server.app.core.config import BASE_MODEL_PATH, GLOBAL_MODEL_PATH, MODELS_DIR
from shared.model_registry import VersionEntry, get_active_version, list_versions, register_model_artifact


def bootstrap_registry() -> None:
    main_active = get_active_version(MODELS_DIR, "main_model")
    if main_active is None and BASE_MODEL_PATH.exists():
        register_model_artifact(
            MODELS_DIR,
            "main_model",
            BASE_MODEL_PATH,
            metadata={"source": "legacy_bootstrap", "dataset": "set1"},
        )

    global_active = get_active_version(MODELS_DIR, "global_model")
    if global_active is None and GLOBAL_MODEL_PATH.exists():
        register_model_artifact(
            MODELS_DIR,
            "global_model",
            GLOBAL_MODEL_PATH,
            metadata={"source": "legacy_bootstrap"},
        )


def register_main_model(path: Path, metadata: dict[str, Any]) -> VersionEntry:
    return register_model_artifact(MODELS_DIR, "main_model", path, metadata=metadata)


def register_global_model(path: Path, metadata: dict[str, Any]) -> VersionEntry:
    return register_model_artifact(MODELS_DIR, "global_model", path, metadata=metadata)


def register_remote_model(model_family: str, path: Path, metadata: dict[str, Any]) -> VersionEntry:
    return register_model_artifact(MODELS_DIR, model_family, path, metadata=metadata)


def get_registry_overview() -> dict[str, object]:
    registry_file = MODELS_DIR / "registry.json"
    if not registry_file.exists():
        return {
            "main_model": {"active": None, "versions": []},
            "global_model": {"active": None, "versions": []},
            "hospital_1_model": {"active": None, "versions": []},
            "hospital_2_model": {"active": None, "versions": []},
        }

    return {
        "main_model": {
            "active": get_active_version(MODELS_DIR, "main_model"),
            "versions": list_versions(MODELS_DIR, "main_model"),
        },
        "global_model": {
            "active": get_active_version(MODELS_DIR, "global_model"),
            "versions": list_versions(MODELS_DIR, "global_model"),
        },
        "hospital_1_model": {
            "active": get_active_version(MODELS_DIR, "hospital_1_model"),
            "versions": list_versions(MODELS_DIR, "hospital_1_model"),
        },
        "hospital_2_model": {
            "active": get_active_version(MODELS_DIR, "hospital_2_model"),
            "versions": list_versions(MODELS_DIR, "hospital_2_model"),
        },
    }
