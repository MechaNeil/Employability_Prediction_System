from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

from employability_1.app.core.config import LEGACY_MODEL_PATH, MODEL_FAMILY, MODELS_DIR
from shared.model_registry import (
    VersionEntry,
    get_active_version,
    list_versions,
    load_registry,
    register_model_artifact,
    save_registry,
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


def delete_local_version(version_name: str) -> dict[str, object]:
    registry = load_registry(MODELS_DIR)
    family = registry["families"].get(MODEL_FAMILY)
    if family is None:
        raise ValueError("No employability model family exists.")

    versions = family["versions"]
    selected: VersionEntry | None = None
    for entry in versions:
        if entry["version_name"] == version_name:
            selected = entry
            break

    if selected is None:
        raise ValueError(f"Version not found: {version_name}")

    artifact_path = Path(str(selected["path"]))
    deleted_files: list[str] = []
    if artifact_path.exists():
        artifact_path.unlink()
        deleted_files.append(str(artifact_path))

    family["versions"] = [entry for entry in versions if entry["version_name"] != version_name]
    if family["active"] == version_name:
        if family["versions"]:
            latest = max(family["versions"], key=lambda item: int(item["version"]))
            family["active"] = latest["version_name"]
            _sync_legacy_model(Path(str(latest["path"])))
        else:
            family["active"] = None
            if LEGACY_MODEL_PATH.exists():
                LEGACY_MODEL_PATH.unlink()
                deleted_files.append(str(LEGACY_MODEL_PATH))

    save_registry(MODELS_DIR, registry)

    return {
        "message": "Employability-1 model version deleted.",
        "model_family": MODEL_FAMILY,
        "version_name": version_name,
        "deleted_files": deleted_files,
        "active_version": family["active"],
        "remaining_versions": [entry["version_name"] for entry in family["versions"]],
    }


def delete_local_family() -> dict[str, object]:
    registry = load_registry(MODELS_DIR)
    family = registry["families"].get(MODEL_FAMILY)
    if family is None:
        raise ValueError("No employability model family exists.")

    deleted_files: list[str] = []
    for entry in family["versions"]:
        artifact_path = Path(str(entry["path"]))
        if artifact_path.exists():
            artifact_path.unlink()
            deleted_files.append(str(artifact_path))

    model_dir = MODELS_DIR / MODEL_FAMILY
    if model_dir.exists() and model_dir.is_dir():
        shutil.rmtree(model_dir)

    if LEGACY_MODEL_PATH.exists():
        LEGACY_MODEL_PATH.unlink()
        deleted_files.append(str(LEGACY_MODEL_PATH))

    registry["families"].pop(MODEL_FAMILY, None)
    save_registry(MODELS_DIR, registry)

    return {
        "message": "Employability-1 model family deleted.",
        "model_family": MODEL_FAMILY,
        "deleted_files": deleted_files,
    }

