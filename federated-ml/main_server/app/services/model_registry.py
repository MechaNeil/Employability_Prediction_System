from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Any

from main_server.app.core.config import BASE_MODEL_PATH, GLOBAL_MODEL_PATH, MODELS_DIR
from shared.model_registry import (
    VersionEntry,
    get_active_version,
    list_versions,
    load_registry,
    register_model_artifact,
    save_registry,
)


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


def _family_alias_files(model_family: str) -> list[Path]:
    aliases: dict[str, list[Path]] = {
        "main_model": [BASE_MODEL_PATH],
        "global_model": [GLOBAL_MODEL_PATH],
    }
    return aliases.get(model_family, [])


def _safe_unlink(path: Path, skipped: list[dict[str, str]]) -> bool:
    try:
        if path.exists() and path.is_file():
            path.unlink()
            return True
    except Exception as exc:  # noqa: BLE001
        skipped.append({"path": str(path), "reason": str(exc)})
    return False


def delete_model_version(model_family: str, version_name: str) -> dict[str, object]:
    registry = load_registry(MODELS_DIR)
    families = registry["families"]
    family = families.get(model_family)
    if family is None:
        raise ValueError(f"Model family not found: {model_family}")

    versions = family["versions"]
    selected: VersionEntry | None = None
    for entry in versions:
        if entry["version_name"] == version_name:
            selected = entry
            break

    if selected is None:
        raise ValueError(f"Version not found for {model_family}: {version_name}")

    skipped: list[dict[str, str]] = []
    deleted_files: list[str] = []

    artifact_path = Path(str(selected["path"]))
    if _safe_unlink(artifact_path, skipped):
        deleted_files.append(str(artifact_path))

    family["versions"] = [entry for entry in versions if entry["version_name"] != version_name]

    if family["active"] == version_name:
        if family["versions"]:
            latest = max(family["versions"], key=lambda item: int(item["version"]))
            family["active"] = latest["version_name"]
        else:
            family["active"] = None

    save_registry(MODELS_DIR, registry)

    if not family["versions"]:
        family_dir = MODELS_DIR / model_family
        if family_dir.exists() and family_dir.is_dir():
            try:
                shutil.rmtree(family_dir)
            except Exception as exc:  # noqa: BLE001
                skipped.append({"path": str(family_dir), "reason": str(exc)})

        for alias_path in _family_alias_files(model_family):
            if _safe_unlink(alias_path, skipped):
                deleted_files.append(str(alias_path))

    return {
        "message": "Model version deleted.",
        "model_family": model_family,
        "version_name": version_name,
        "deleted_files": deleted_files,
        "active_version": family["active"],
        "remaining_versions": [entry["version_name"] for entry in family["versions"]],
        "skipped": skipped,
    }


def delete_model_family(model_family: str) -> dict[str, object]:
    registry = load_registry(MODELS_DIR)
    families = registry["families"]
    family = families.get(model_family)
    if family is None:
        raise ValueError(f"Model family not found: {model_family}")

    skipped: list[dict[str, str]] = []
    deleted_files: list[str] = []
    deleted_dirs: list[str] = []

    for entry in family["versions"]:
        artifact_path = Path(str(entry["path"]))
        if _safe_unlink(artifact_path, skipped):
            deleted_files.append(str(artifact_path))

    family_dir = MODELS_DIR / model_family
    if family_dir.exists() and family_dir.is_dir():
        try:
            shutil.rmtree(family_dir)
            deleted_dirs.append(str(family_dir))
        except Exception as exc:  # noqa: BLE001
            skipped.append({"path": str(family_dir), "reason": str(exc)})

    for alias_path in _family_alias_files(model_family):
        if _safe_unlink(alias_path, skipped):
            deleted_files.append(str(alias_path))

    families.pop(model_family, None)
    save_registry(MODELS_DIR, registry)

    return {
        "message": "Model family deleted.",
        "model_family": model_family,
        "deleted_files": deleted_files,
        "deleted_directories": deleted_dirs,
        "skipped": skipped,
    }


def delete_all_model_files() -> dict[str, object]:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    preserved_names = {"__pycache__", "schemas.py", "__init__.py", ".gitkeep"}
    deleted_files: list[str] = []
    deleted_dirs: list[str] = []
    skipped: list[dict[str, str]] = []

    for item in MODELS_DIR.iterdir():
        if item.name in preserved_names:
            continue

        try:
            if item.is_dir():
                shutil.rmtree(item)
                deleted_dirs.append(str(item))
            elif item.is_file():
                item.unlink()
                deleted_files.append(str(item))
        except Exception as exc:  # noqa: BLE001
            skipped.append({"path": str(item), "reason": str(exc)})

    registry_path = MODELS_DIR / "registry.json"
    if not registry_path.exists():
        registry_path.write_text(json.dumps({"families": {}}, indent=2), encoding="utf-8")

    return {
        "message": "All model files deleted from main server.",
        "models_dir": str(MODELS_DIR),
        "deleted_files": deleted_files,
        "deleted_directories": deleted_dirs,
        "skipped": skipped,
    }


def clear_model_artifacts() -> dict[str, object]:
    return delete_all_model_files()


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
