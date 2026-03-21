from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from main_server.app.services.evaluation import evaluate_global_model
from main_server.app.services.inference import predict_records
from main_server.app.services.status import get_model_versions, get_system_status
from main_server.app.services.training import train_main_model
from main_server.app.views.model_view import aggregate_pipeline, deploy_to_hospitals, retrain_hospitals

router = APIRouter()


class PredictRequest(BaseModel):
    records: list[dict[str, float]]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "main_server"}


@router.get("/status")
def status() -> dict[str, object]:
    return get_system_status()


@router.get("/model-version")
def model_version() -> dict[str, object]:
    return get_model_versions()


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


@router.post("/deploy")
def deploy() -> dict[str, str]:
    try:
        return deploy_to_hospitals()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/retrain-hospitals")
def retrain_remote() -> dict[str, str]:
    try:
        return retrain_hospitals()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/evaluate")
def evaluate() -> dict[str, float]:
    try:
        return evaluate_global_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/predict")
def predict(payload: PredictRequest) -> dict[str, object]:
    try:
        return predict_records(payload.records)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
