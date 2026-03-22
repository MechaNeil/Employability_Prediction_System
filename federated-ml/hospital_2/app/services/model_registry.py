from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

from hospital_2.app.core.config import LEGACY_MODEL_PATH, MODEL_FAMILY, MODELS_DIR
from shared.model_registry import (
    VersionEntry,
    get_active_version,
    list_versions,
    register_model_artifact,
    set_active_version,
)


def initialize_registry() -> None:
    active = get_active_version(MODELS_DIR, MODEL_FAMILY)
    if active is not None:
        _sync_legacy_model(Path(active["path"]))
        return

    if LEGACY_MODEL_PATH.exists():
        entry = register_model_artifact(
            MODELS_DIR,
            MODEL_FAMILY,
            LEGACY_MODEL_PATH,
            metadata={"source": "legacy_bootstrap"},
        )
        _sync_legacy_model(Path(entry["path"]))


def register_version(artifact_path: Path, metadata: dict[str, Any] | None = None) -> VersionEntry:
    entry = register_model_artifact(MODELS_DIR, MODEL_FAMILY, artifact_path, metadata=metadata)
    _sync_legacy_model(Path(entry["path"]))
    return entry


def get_versions() -> list[VersionEntry]:
    return list_versions(MODELS_DIR, MODEL_FAMILY)


def get_active() -> VersionEntry | None:
    return get_active_version(MODELS_DIR, MODEL_FAMILY)


def activate(version_name: str) -> VersionEntry:
    entry = set_active_version(MODELS_DIR, MODEL_FAMILY, version_name)
    _sync_legacy_model(Path(entry["path"]))
    return entry


def _sync_legacy_model(path: Path) -> None:
    LEGACY_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, LEGACY_MODEL_PATH)
