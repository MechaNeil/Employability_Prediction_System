from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from fastapi.responses import HTMLResponse

from main_server.app.controllers import federation_controller
from main_server.app.core.config import MODELS_DIR
from main_server.app.models.schemas import (
    DeleteModelFamilyRequest,
    DeleteModelVersionRequest,
    PredictRequest,
    RetrainTargetsRequest,
    TrainMainRequest,
    VersionCompareRequest,
)
from main_server.app.services.model_registry import register_remote_model

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
def train(payload: TrainMainRequest) -> dict[str, object]:
    try:
        return federation_controller.train_model(payload.dataset)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/aggregate")
def aggregate() -> dict[str, object]:
    try:
        return federation_controller.aggregate_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/deploy")
def deploy() -> dict[str, object]:
    try:
        return federation_controller.deploy_model()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/models/clean-start")
def clean_start_models() -> dict[str, object]:
    try:
        return federation_controller.clean_start_models()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/models/delete-version")
def delete_model_version(payload: DeleteModelVersionRequest) -> dict[str, object]:
    try:
        return federation_controller.delete_models_version(
            model_family=payload.model_family,
            version_name=payload.version_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/models/delete-family")
def delete_model_family(payload: DeleteModelFamilyRequest) -> dict[str, object]:
    try:
        return federation_controller.delete_models_family(model_family=payload.model_family)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/models/delete-all")
def delete_all_models() -> dict[str, object]:
    try:
        return federation_controller.delete_models_all()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/retrain-employabilitys")
def retrain_remote(payload: RetrainTargetsRequest) -> dict[str, object]:
    try:
        response = federation_controller.retrain_remote_models(payload.targets, payload.dataset)
        if "main" in [target.lower() for target in payload.targets]:
            response["main_train"] = federation_controller.train_model(payload.dataset)
        return response
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/evaluate")
def evaluate(dataset: str = "all", scope: str = "main") -> dict[str, object]:
    try:
        return federation_controller.evaluate_model(dataset=dataset, scope=scope)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/predict")
def predict(payload: PredictRequest) -> dict[str, object]:
    try:
        return federation_controller.predict_model(payload.records)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/remote-models/upload")
async def upload_remote_model(
    source_server: str = Form(...),
    target_server: str = Form(...),
    model_family: str = Form(...),
    model_file: UploadFile = File(...),
) -> dict[str, object]:
    try:
        temp_path = MODELS_DIR / f"_upload_{model_file.filename}"
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_bytes(await model_file.read())

        entry = register_remote_model(
            model_family=model_family,
            path=temp_path,
            metadata={
                "source_server": source_server,
                "target_server": target_server,
                "upload_filename": model_file.filename,
            },
        )
        forward_result = federation_controller.forward_uploaded_model_to_target(
            temp_path,
            source_server=source_server,
            target_server=target_server,
            model_family=model_family,
        )
        if temp_path.exists():
            temp_path.unlink()

        return {
            "message": "Remote model uploaded successfully.",
            "model_family": model_family,
            "active_version": entry["version_name"],
            "model_path": entry["path"],
            "forward_result": forward_result,
        }
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/compare-versions")
def compare_versions(payload: VersionCompareRequest) -> dict[str, object]:
    try:
        return federation_controller.compare_versions(
            test_dataset=payload.test_dataset,
            items=[item.model_dump() for item in payload.items],
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

