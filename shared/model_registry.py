from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any, TypedDict, cast


class VersionEntry(TypedDict):
    version: int
    version_name: str
    path: str
    created_utc: str
    size_bytes: int
    metadata: dict[str, Any]


class FamilyEntry(TypedDict):
    active: str | None
    versions: list[VersionEntry]


class RegistryPayload(TypedDict):
    families: dict[str, FamilyEntry]


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _registry_path(models_dir: Path) -> Path:
    return models_dir / "registry.json"


def ensure_registry(models_dir: Path) -> Path:
    models_dir.mkdir(parents=True, exist_ok=True)
    registry_path = _registry_path(models_dir)
    if not registry_path.exists():
        payload: RegistryPayload = {"families": {}}
        registry_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return registry_path


def load_registry(models_dir: Path) -> RegistryPayload:
    registry_path = ensure_registry(models_dir)
    loaded = json.loads(registry_path.read_text(encoding="utf-8"))
    return cast(RegistryPayload, loaded)


def save_registry(models_dir: Path, payload: RegistryPayload) -> None:
    registry_path = ensure_registry(models_dir)
    registry_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _next_version(versions: list[VersionEntry]) -> int:
    if not versions:
        return 1
    return max(item["version"] for item in versions) + 1


def register_model_artifact(
    models_dir: Path,
    family: str,
    source_path: Path,
    *,
    metadata: dict[str, object] | None = None,
) -> VersionEntry:
    if not source_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {source_path}")

    registry = load_registry(models_dir)
    families = registry["families"]
    family_data = families.setdefault(family, {"active": None, "versions": []})
    versions = family_data["versions"]

    version_no = _next_version(versions)
    version_name = f"{family}_v{version_no}"

    artifact_dir = models_dir / family
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / f"{version_name}.pkl"
    shutil.copy2(source_path, artifact_path)

    entry: VersionEntry = {
        "version": version_no,
        "version_name": version_name,
        "path": str(artifact_path),
        "created_utc": _now_utc(),
        "size_bytes": int(artifact_path.stat().st_size),
        "metadata": cast(dict[str, Any], metadata or {}),
    }
    versions.append(entry)
    family_data["active"] = version_name
    save_registry(models_dir, registry)
    return entry


def list_versions(models_dir: Path, family: str) -> list[VersionEntry]:
    registry = load_registry(models_dir)
    families = registry["families"]
    family_data = families.get(family)
    if family_data is None:
        return []
    return list(family_data["versions"])


def get_active_version(models_dir: Path, family: str) -> VersionEntry | None:
    registry = load_registry(models_dir)
    families = registry["families"]
    family_data = families.get(family)
    if family_data is None:
        return None

    active_name = family_data["active"]
    if not active_name:
        return None
    for item in family_data["versions"]:
        if item["version_name"] == active_name:
            return item
    return None


def set_active_version(models_dir: Path, family: str, version_name: str) -> VersionEntry:
    registry = load_registry(models_dir)
    families = registry["families"]
    family_data = families.setdefault(family, {"active": None, "versions": []})
    versions = family_data["versions"]

    candidate: VersionEntry | None = None
    for item in versions:
        if item["version_name"] == version_name:
            candidate = item
            break

    if candidate is None:
        raise ValueError(f"Version not found for {family}: {version_name}")

    family_data["active"] = version_name
    save_registry(models_dir, registry)
    return candidate
