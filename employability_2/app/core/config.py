from pathlib import Path
import os

EMPLOYABILITY_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = EMPLOYABILITY_ROOT.parents[1]

MODELS_DIR = EMPLOYABILITY_ROOT / "app" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

LEGACY_MODEL_PATH = MODELS_DIR / "employability_model.pkl"
MODEL_FAMILY = "employability_2_model"

MAIN_SERVER_BASE_URL = os.getenv("MAIN_SERVER_BASE_URL", "http://localhost:8000")
MAIN_SERVER_UPLOAD_URL = f"{MAIN_SERVER_BASE_URL}/remote-models/upload"
_fallback_bases = [
	item.strip()
	for item in os.getenv(
		"MAIN_SERVER_BASE_URL_FALLBACKS",
		"http://host.docker.internal:8000,http://main_server:8000,http://localhost:8000",
	).split(",")
	if item.strip()
]
_all_bases = [MAIN_SERVER_BASE_URL, *_fallback_bases]
MAIN_SERVER_UPLOAD_URLS = list(dict.fromkeys(f"{base.rstrip('/')}/remote-models/upload" for base in _all_bases))

REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "3"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))

