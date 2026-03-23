from pathlib import Path
import os

MAIN_SERVER_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = MAIN_SERVER_ROOT.parents[1]

MODELS_DIR = MAIN_SERVER_ROOT / "app" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODEL_PATH = MODELS_DIR / "model.pkl"
AGGREGATION_DATASETS = ("set1", "set2", "set3")

EMPLOYABILITY_1_RETRAIN_URL = "http://localhost:8001/retrain"
EMPLOYABILITY_1_MODEL_URL = "http://localhost:8001/model"
EMPLOYABILITY_1_UPLOAD_URL = "http://localhost:8001/model/upload"
EMPLOYABILITY_1_ACTIVATE_URL = "http://localhost:8001/model/activate"
EMPLOYABILITY_2_RETRAIN_URL = "http://localhost:8002/retrain"
EMPLOYABILITY_2_MODEL_URL = "http://localhost:8002/model"
EMPLOYABILITY_2_UPLOAD_URL = "http://localhost:8002/model/upload"
EMPLOYABILITY_2_ACTIVATE_URL = "http://localhost:8002/model/activate"
EMPLOYABILITY_1_HEALTH_URL = "http://localhost:8001/health"
EMPLOYABILITY_2_HEALTH_URL = "http://localhost:8002/health"

REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "3"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

