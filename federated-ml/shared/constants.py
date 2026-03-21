from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATASET = PROJECT_ROOT.parent / "Student-Employability-Datasets.csv"
SPLIT_DIR = PROJECT_ROOT / "dataset"

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

SET1_FILE = SPLIT_DIR / "set1.csv"
SET2_FILE = SPLIT_DIR / "set2.csv"
SET3_FILE = SPLIT_DIR / "set3.csv"
TEST_FILE = SPLIT_DIR / "test.csv"

RANDOM_STATE = 42
