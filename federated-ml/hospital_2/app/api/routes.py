from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from hospital_2.app.views.model_view import get_model_file, trigger_retrain

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "hospital_2"}


@router.post("/retrain")
def retrain() -> dict[str, object]:
    try:
        return trigger_retrain()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/model", response_class=FileResponse)
def model() -> FileResponse:
    try:
        return get_model_file()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
