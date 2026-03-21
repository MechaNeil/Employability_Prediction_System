from pathlib import Path
import os

MAIN_SERVER_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = MAIN_SERVER_ROOT.parents[1]

MODELS_DIR = MAIN_SERVER_ROOT / "app" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODEL_PATH = MODELS_DIR / "model.pkl"
GLOBAL_MODEL_PATH = MODELS_DIR / "main_model_v2.pkl"

HOSPITAL_1_RETRAIN_URL = "http://localhost:8001/retrain"
HOSPITAL_1_MODEL_URL = "http://localhost:8001/model"
HOSPITAL_2_RETRAIN_URL = "http://localhost:8002/retrain"
HOSPITAL_2_MODEL_URL = "http://localhost:8002/model"
HOSPITAL_1_HEALTH_URL = "http://localhost:8001/health"
HOSPITAL_2_HEALTH_URL = "http://localhost:8002/health"

REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "3"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
