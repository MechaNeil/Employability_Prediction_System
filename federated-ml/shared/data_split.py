from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from shared.constants import (
    FEATURE_COLUMNS,
    LABEL_MAP,
    NAME_COLUMN,
    RANDOM_STATE,
    SET1_FILE,
    SET2_FILE,
    SET3_FILE,
    SOURCE_DATASET,
    TARGET_COLUMN,
    TEST_FILE,
)


def _validate_source_columns(df: pd.DataFrame) -> None:
    expected = set(FEATURE_COLUMNS + [TARGET_COLUMN, NAME_COLUMN])
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")


def _save_split(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def create_split_files() -> dict[str, dict[str, int]]:
    df = pd.read_csv(SOURCE_DATASET)
    _validate_source_columns(df)

    working_df = df.drop(columns=[NAME_COLUMN]).copy()
    working_df[TARGET_COLUMN] = working_df[TARGET_COLUMN].map(LABEL_MAP)

    if working_df[TARGET_COLUMN].isna().any():
        raise ValueError("Found unmapped labels in CLASS column.")

    x = working_df[FEATURE_COLUMNS]
    y = working_df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    # Set-1/2/3 are 52/24/24 of the training block.
    # Equivalent to 0.35 test split followed by 0.48 split of the remainder:
    # 65% -> set1, 35% -> temp ; temp -> 48.57% set2, 51.43% set3.
    x_set1, x_temp, y_set1, y_temp = train_test_split(
        x_train,
        y_train,
        test_size=0.35,
        stratify=y_train,
        random_state=RANDOM_STATE,
    )

    x_set2, x_set3, y_set2, y_set3 = train_test_split(
        x_temp,
        y_temp,
        test_size=0.5142857143,
        stratify=y_temp,
        random_state=RANDOM_STATE,
    )

    set1_df = pd.concat([x_set1, y_set1.rename(TARGET_COLUMN)], axis=1)
    set2_df = pd.concat([x_set2, y_set2.rename(TARGET_COLUMN)], axis=1)
    set3_df = pd.concat([x_set3, y_set3.rename(TARGET_COLUMN)], axis=1)
    test_df = pd.concat([x_test, y_test.rename(TARGET_COLUMN)], axis=1)

    for split_name, split_df in {
        "set1": set1_df,
        "set2": set2_df,
        "set3": set3_df,
        "test": test_df,
    }.items():
        if list(split_df.columns[:-1]) != FEATURE_COLUMNS:
            raise ValueError(f"Feature mismatch in {split_name}")

    _save_split(set1_df, SET1_FILE)
    _save_split(set2_df, SET2_FILE)
    _save_split(set3_df, SET3_FILE)
    _save_split(test_df, TEST_FILE)

    stats: dict[str, dict[str, int]] = {}
    for name, split_df in {
        "set1": set1_df,
        "set2": set2_df,
        "set3": set3_df,
        "test": test_df,
    }.items():
        stats[name] = {
            "rows": int(len(split_df)),
            "class_0": int((split_df[TARGET_COLUMN] == 0).sum()),
            "class_1": int((split_df[TARGET_COLUMN] == 1).sum()),
        }

    return stats


if __name__ == "__main__":
    split_stats = create_split_files()
    for split_name, split_info in split_stats.items():
        print(f"{split_name}: {split_info}")
