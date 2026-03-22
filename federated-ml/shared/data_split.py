from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd
from sklearn.model_selection import train_test_split

from shared.constants import (
    FEATURE_COLUMNS,
    LABEL_MAP,
    NAME_COLUMN,
    RANDOM_STATE,
    SET1_TEST_FILE,
    SET1_TRAIN_FILE,
    SET2_TEST_FILE,
    SET2_TRAIN_FILE,
    SET3_TEST_FILE,
    SET3_TRAIN_FILE,
    SOURCE_DATASET,
    TARGET_COLUMN,
)


def _validate_source_columns(df: pd.DataFrame) -> None:
    expected = set(FEATURE_COLUMNS + [TARGET_COLUMN, NAME_COLUMN])
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")


def _save_split(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _build_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return x, y


def _merge_xy(x: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    return pd.concat([x, y.rename(TARGET_COLUMN)], axis=1)


def _stratified_fixed_split(
    x: pd.DataFrame,
    y: pd.Series,
    *,
    train_size: int,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    return tuple(train_test_split(
        x,
        y,
        train_size=train_size,
        stratify=y,
        random_state=random_state,
    ))


def _split_train_test(
    set_df: pd.DataFrame,
    *,
    train_size: int,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    x, y = _build_xy(set_df)
    x_train, x_test, y_train, y_test = _stratified_fixed_split(
        x,
        y,
        train_size=train_size,
        random_state=random_state,
    )
    return _merge_xy(x_train, y_train), _merge_xy(x_test, y_test)


def _split_into_set_blocks(
    x: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Target total rows by set: Set-1=1250, Set-2=1000, Set-3=733.
    x_set1, x_remaining, y_set1, y_remaining = _stratified_fixed_split(
        x,
        y,
        train_size=1250,
        random_state=RANDOM_STATE,
    )

    x_set2, x_set3, y_set2, y_set3 = _stratified_fixed_split(
        x_remaining,
        y_remaining,
        train_size=1000,
        random_state=RANDOM_STATE,
    )

    return _merge_xy(x_set1, y_set1), _merge_xy(x_set2, y_set2), _merge_xy(x_set3, y_set3)


def _split_stats(df: pd.DataFrame) -> dict[str, int]:
    return {
        "rows": int(len(df)),
        "class_0": int((df[TARGET_COLUMN] == 0).sum()),
        "class_1": int((df[TARGET_COLUMN] == 1).sum()),
    }


def create_split_files() -> Mapping[str, object]:
    df = pd.read_csv(SOURCE_DATASET)
    _validate_source_columns(df)

    working_df = df.drop(columns=[NAME_COLUMN]).copy()
    working_df[TARGET_COLUMN] = working_df[TARGET_COLUMN].map(LABEL_MAP)

    if working_df[TARGET_COLUMN].isna().any():
        raise ValueError("Found unmapped labels in CLASS column.")

    x_all = working_df[FEATURE_COLUMNS]
    y_all = working_df[TARGET_COLUMN]

    set1_total_df, set2_total_df, set3_total_df = _split_into_set_blocks(x_all, y_all)

    set1_train_df, set1_test_df = _split_train_test(
        set1_total_df,
        train_size=1000,
        random_state=RANDOM_STATE,
    )
    set2_train_df, set2_test_df = _split_train_test(
        set2_total_df,
        train_size=800,
        random_state=RANDOM_STATE,
    )
    set3_train_df, set3_test_df = _split_train_test(
        set3_total_df,
        train_size=586,
        random_state=RANDOM_STATE,
    )

    for split_name, split_df in {
        "set1_train": set1_train_df,
        "set1_test": set1_test_df,
        "set2_train": set2_train_df,
        "set2_test": set2_test_df,
        "set3_train": set3_train_df,
        "set3_test": set3_test_df,
    }.items():
        if list(split_df.columns[:-1]) != FEATURE_COLUMNS:
            raise ValueError(f"Feature mismatch in {split_name}")

    _save_split(set1_train_df, SET1_TRAIN_FILE)
    _save_split(set1_test_df, SET1_TEST_FILE)
    _save_split(set2_train_df, SET2_TRAIN_FILE)
    _save_split(set2_test_df, SET2_TEST_FILE)
    _save_split(set3_train_df, SET3_TRAIN_FILE)
    _save_split(set3_test_df, SET3_TEST_FILE)

    stats: dict[str, object] = {
        "total_rows": int(len(working_df)),
        "set1": {
            "total": int(len(set1_total_df)),
            "train": _split_stats(set1_train_df),
            "test": _split_stats(set1_test_df),
        },
        "set2": {
            "total": int(len(set2_total_df)),
            "train": _split_stats(set2_train_df),
            "test": _split_stats(set2_test_df),
        },
        "set3": {
            "total": int(len(set3_total_df)),
            "train": _split_stats(set3_train_df),
            "test": _split_stats(set3_test_df),
        },
        "totals": {
            "train_rows": int(len(set1_train_df) + len(set2_train_df) + len(set3_train_df)),
            "test_rows": int(len(set1_test_df) + len(set2_test_df) + len(set3_test_df)),
            "rows": int(
                len(set1_train_df)
                + len(set1_test_df)
                + len(set2_train_df)
                + len(set2_test_df)
                + len(set3_train_df)
                + len(set3_test_df)
            ),
        },
    }

    return stats


if __name__ == "__main__":
    split_stats = create_split_files()
    for split_name, split_info in split_stats.items():
        print(f"{split_name}: {split_info}")
