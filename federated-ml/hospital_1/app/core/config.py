from pathlib import Path
import os

HOSPITAL_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = HOSPITAL_ROOT.parents[1]

MODELS_DIR = HOSPITAL_ROOT / "app" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

LEGACY_MODEL_PATH = MODELS_DIR / "hospital_model.pkl"
MODEL_FAMILY = "hospital_1_model"

MAIN_SERVER_BASE_URL = os.getenv("MAIN_SERVER_BASE_URL", "http://localhost:8000")
MAIN_SERVER_UPLOAD_URL = f"{MAIN_SERVER_BASE_URL}/remote-models/upload"

REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "3"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
