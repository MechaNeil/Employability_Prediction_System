from __future__ import annotations

from pathlib import Path

import requests

from hospital_1.app.core.config import MAIN_SERVER_UPLOAD_URL, REQUEST_TIMEOUT_SECONDS
from hospital_1.app.services.model_registry import get_active


def deploy_model_to_main_server(version_name: str | None = None) -> dict[str, object]:
    active = get_active()
    if active is None:
        raise FileNotFoundError("No active hospital_1 model to deploy.")

    if version_name and active["version_name"] != version_name:
        raise ValueError("Only active model deployment is currently supported.")

    artifact_path = Path(active["path"])
    files = {"model_file": (artifact_path.name, artifact_path.read_bytes(), "application/octet-stream")}
    data = {
        "source_server": "hospital_1",
        "target_server": "main_server",
        "model_family": "hospital_1_model",
    }

    response = requests.post(MAIN_SERVER_UPLOAD_URL, data=data, files=files, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    return {
        "message": "Model deployed to main_server.",
        "uploaded_version": active["version_name"],
        "main_server_response": response.json(),
    }
