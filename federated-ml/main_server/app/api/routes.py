from fastapi import APIRouter, HTTPException

from main_server.app.services.evaluation import evaluate_global_model
from main_server.app.services.training import train_main_model
from main_server.app.views.model_view import aggregate_pipeline

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "main_server"}


@router.post("/train")
def train() -> dict[str, object]:
    try:
        return train_main_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/aggregate")
def aggregate() -> dict[str, object]:
    try:
        return aggregate_pipeline()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/evaluate")
def evaluate() -> dict[str, float]:
    try:
        return evaluate_global_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
