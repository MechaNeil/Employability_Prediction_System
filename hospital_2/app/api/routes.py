from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from hospital_2.app.controllers import federation_controller
from hospital_2.app.models.schemas import (
    ActivateVersionRequest,
    DeleteVersionRequest,
    DeployRequest,
    EvaluateRequest,
    TrainRequest,
)
from hospital_2.app.services.model_registry import get_active, get_versions
from hospital_2.app.services.status import get_training_set_comparison
from hospital_2.app.views.model_view import get_model_file, upload_model_file

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
    return {
        "service": "hospital_2",
        "active_model": get_active(),
        "versions": get_versions(),
    }


@router.post("/retrain")
def retrain(payload: TrainRequest | None = None) -> dict[str, object]:
    data = payload or TrainRequest(dataset="set3", retrain_from_main=True)
    try:
        return federation_controller.train_model(data.dataset, retrain_from_main=data.retrain_from_main)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/train")
def train(payload: TrainRequest) -> dict[str, object]:
    try:
        return federation_controller.train_model(payload.dataset, retrain_from_main=payload.retrain_from_main)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/evaluate")
def evaluate(payload: EvaluateRequest) -> dict[str, object]:
    try:
        return federation_controller.evaluate_model(payload.test_dataset)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/compare-by-training-set")
def compare_by_training_set(test_dataset: str = "set1") -> dict[str, object]:
    try:
        return get_training_set_comparison(test_dataset)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/model", response_class=FileResponse)
def model() -> FileResponse:
    try:
        return get_model_file()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/model/upload")
async def upload_model(model_file: UploadFile = File(...)) -> dict[str, object]:
    try:
        return await upload_model_file(model_file)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/model/activate")
def activate_model(payload: ActivateVersionRequest) -> dict[str, object]:
    try:
        return federation_controller.set_active_version(payload.version_name)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/deploy-to-main")
def deploy_to_main(payload: DeployRequest) -> dict[str, object]:
    try:
        return federation_controller.deploy_to_main(payload.version_name)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/model/delete-version")
def delete_model_version(payload: DeleteVersionRequest) -> dict[str, object]:
    try:
        return federation_controller.delete_local_model_version(payload.version_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/model/delete-family")
def delete_model_family() -> dict[str, object]:
    try:
        return federation_controller.delete_local_model_family()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
