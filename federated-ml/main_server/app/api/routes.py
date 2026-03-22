from fastapi import APIRouter, HTTPException

from fastapi.responses import HTMLResponse

from main_server.app.controllers import federation_controller
from main_server.app.models.schemas import PredictRequest

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return federation_controller.get_health_status()


@router.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return federation_controller.render_dashboard()


@router.get("/status")
def status() -> dict[str, object]:
    return federation_controller.get_status()


@router.get("/model-version")
def model_version() -> dict[str, object]:
    return federation_controller.get_versions()


@router.post("/train")
def train() -> dict[str, object]:
    try:
        return federation_controller.train_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/aggregate")
def aggregate() -> dict[str, object]:
    try:
        return federation_controller.aggregate_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/deploy")
def deploy() -> dict[str, str]:
    try:
        return federation_controller.deploy_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/retrain-hospitals")
def retrain_remote() -> dict[str, str]:
    try:
        return federation_controller.retrain_remote_models()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/evaluate")
def evaluate() -> dict[str, float]:
    try:
        return federation_controller.evaluate_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/predict")
def predict(payload: PredictRequest) -> dict[str, object]:
    try:
        return federation_controller.predict_model(payload.records)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
