from __future__ import annotations

from pathlib import Path

from shared.constants import (
    SET1_TEST_FILE,
    SET1_TRAIN_FILE,
    SET2_TEST_FILE,
    SET2_TRAIN_FILE,
    SET3_TEST_FILE,
    SET3_TRAIN_FILE,
)

TRAIN_DATASET_MAP: dict[str, Path] = {
    "set1": SET1_TRAIN_FILE,
    "set2": SET2_TRAIN_FILE,
    "set3": SET3_TRAIN_FILE,
}

TEST_DATASET_MAP: dict[str, Path] = {
    "set1": SET1_TEST_FILE,
    "set2": SET2_TEST_FILE,
    "set3": SET3_TEST_FILE,
}


def normalize_dataset_key(dataset_key: str) -> str:
    normalized = dataset_key.strip().lower().replace("-", "")
    if normalized not in TRAIN_DATASET_MAP:
        raise ValueError(f"Unknown dataset key: {dataset_key}")
    return normalized


def get_dataset_path(dataset_key: str, purpose: str = "train") -> Path:
    normalized = normalize_dataset_key(dataset_key)
    selected_purpose = purpose.strip().lower()

    if selected_purpose == "train":
        return TRAIN_DATASET_MAP[normalized]
    if selected_purpose == "test":
        return TEST_DATASET_MAP[normalized]

    raise ValueError("purpose must be 'train' or 'test'.")


def get_all_test_dataset_paths() -> list[Path]:
    return [TEST_DATASET_MAP["set1"], TEST_DATASET_MAP["set2"], TEST_DATASET_MAP["set3"]]
