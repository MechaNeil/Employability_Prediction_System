from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATASET = PROJECT_ROOT / "Student-Employability-Datasets.csv"
SPLIT_DIR = PROJECT_ROOT / "dataset"

SET1_DIR = SPLIT_DIR / "Set-1"
SET2_DIR = SPLIT_DIR / "Set-2"
SET3_DIR = SPLIT_DIR / "Set-3"

NAME_COLUMN = "Name of Student"
TARGET_COLUMN = "CLASS"

FEATURE_COLUMNS = [
    "GENERAL APPEARANCE",
    "MANNER OF SPEAKING",
    "PHYSICAL CONDITION",
    "MENTAL ALERTNESS",
    "SELF-CONFIDENCE",
    "ABILITY TO PRESENT IDEAS",
    "COMMUNICATION SKILLS",
    "Student Performance Rating",
]

LABEL_MAP = {
    "LessEmployable": 0,
    "Employable": 1,
}

INV_LABEL_MAP = {value: key for key, value in LABEL_MAP.items()}

SET1_TRAIN_FILE = SET1_DIR / "set-1_train_data.csv"
SET1_TEST_FILE = SET1_DIR / "set-1_test_data.csv"
SET2_TRAIN_FILE = SET2_DIR / "set-2_train_data.csv"
SET2_TEST_FILE = SET2_DIR / "set-2_test_data.csv"
SET3_TRAIN_FILE = SET3_DIR / "set-3_train_data.csv"
SET3_TEST_FILE = SET3_DIR / "set-3_test_data.csv"

# Backward-compatible aliases used by existing training logic.
SET1_FILE = SET1_TRAIN_FILE
SET2_FILE = SET2_TRAIN_FILE
SET3_FILE = SET3_TRAIN_FILE

RANDOM_STATE = 42
