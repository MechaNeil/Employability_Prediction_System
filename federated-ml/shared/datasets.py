from __future__ import annotations

from pathlib import Path

from shared.constants import SET1_FILE, SET2_FILE, SET3_FILE

DATASET_MAP: dict[str, Path] = {
    "set1": SET1_FILE,
    "set2": SET2_FILE,
    "set3": SET3_FILE,
}


def normalize_dataset_key(dataset_key: str) -> str:
    normalized = dataset_key.strip().lower()
    if normalized not in DATASET_MAP:
        raise ValueError(f"Unknown dataset key: {dataset_key}")
    return normalized


def get_dataset_path(dataset_key: str) -> Path:
    return DATASET_MAP[normalize_dataset_key(dataset_key)]
