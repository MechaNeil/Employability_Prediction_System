from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse

from hospital_1.app.services.model_registry import get_active, register_version
from hospital_1.app.services.training import LOCAL_MODEL_PATH, retrain_model


def trigger_retrain() -> dict[str, object]:
    return retrain_model()


def get_model_file() -> FileResponse:
    active = get_active()
    if active is None and not Path(LOCAL_MODEL_PATH).exists():
        retrain_model()
        active = get_active()

    model_path = Path(active["path"]) if active is not None else Path(LOCAL_MODEL_PATH)
    filename = active["version_name"] + ".pkl" if active is not None else "hospital1_model.pkl"
    return FileResponse(path=model_path, media_type="application/octet-stream", filename=filename)


async def upload_model_file(model_file: UploadFile) -> dict[str, object]:
    temp_path = Path(LOCAL_MODEL_PATH).parent / f"_upload_{model_file.filename}"
    contents = await model_file.read()
    temp_path.write_bytes(contents)
    entry = register_version(temp_path, metadata={"source": "manual_upload"})
    if temp_path.exists():
        temp_path.unlink()

    return {
        "message": "Manual model upload complete.",
        "active_version": entry["version_name"],
        "model_path": entry["path"],
    }
