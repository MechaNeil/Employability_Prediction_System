from pathlib import Path

from fastapi.responses import FileResponse

from hospital_2.app.services.training import LOCAL_MODEL_PATH, retrain_model


def trigger_retrain() -> dict[str, object]:
    return retrain_model()


def get_model_file() -> FileResponse:
    if not Path(LOCAL_MODEL_PATH).exists():
        retrain_model()
    return FileResponse(path=LOCAL_MODEL_PATH, media_type="application/octet-stream", filename="hospital2_model.pkl")
