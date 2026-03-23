from __future__ import annotations

from pathlib import Path

import requests

from employability_2.app.core.config import MAIN_SERVER_UPLOAD_URLS, REQUEST_TIMEOUT_SECONDS
from employability_2.app.services.model_registry import get_active


def deploy_model_to_main_server(version_name: str | None = None) -> dict[str, object]:
    active = get_active()
    if active is None:
        raise FileNotFoundError("No active employability_2 model to deploy.")

    if version_name and active["version_name"] != version_name:
        raise ValueError("Only active model deployment is currently supported.")

    artifact_path = Path(active["path"])
    files = {"model_file": (artifact_path.name, artifact_path.read_bytes(), "application/octet-stream")}
    data = {
        "source_server": "employability_2",
        "target_server": "main",
        "model_family": "employability_2_model",
    }

    last_error = None
    response = None
    used_url = None
    for upload_url in MAIN_SERVER_UPLOAD_URLS:
        try:
            response = requests.post(upload_url, data=data, files=files, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            used_url = upload_url
            last_error = None
            break
        except Exception as exc:  # noqa: BLE001
            last_error = f"{upload_url}: {exc}"

    if response is None or last_error is not None:
        raise RuntimeError(
            "Unable to connect to main_server upload endpoint. "
            f"Attempted URLs: {MAIN_SERVER_UPLOAD_URLS}. Last error: {last_error}"
        )

    return {
        "message": "Model deployed to main_server.",
        "uploaded_version": active["version_name"],
        "upload_url": used_url,
        "main_server_response": response.json(),
    }

