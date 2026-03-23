from __future__ import annotations

from main_server.app.services.evaluation import evaluate_main_model
from main_server.app.services.inference import predict_records
from main_server.app.services.orchestration import (
    aggregate_pipeline,
    deploy_to_hospitals,
    forward_uploaded_model,
    retrain_hospitals,
)
from main_server.app.services.status import (
    cache_latest_evaluation,
    compare_named_versions,
    get_model_versions,
    get_system_status,
    trigger_status_refresh,
)
from main_server.app.services.training import train_main_model
from main_server.app.services.model_registry import clear_model_artifacts
from main_server.app.services.model_registry import delete_all_model_files
from main_server.app.services.model_registry import delete_model_family
from main_server.app.services.model_registry import delete_model_version
from main_server.app.views.dashboard_view import get_dashboard_html


def render_dashboard() -> str:
    return get_dashboard_html()


def get_health_status() -> dict[str, str]:
    return {"status": "ok", "service": "main_server"}


def get_status() -> dict[str, object]:
    return get_system_status()


def get_versions() -> dict[str, object]:
    return get_model_versions()


def train_model(dataset: str = "set1") -> dict[str, object]:
    return train_main_model(dataset)


def aggregate_model() -> dict[str, object]:
    return aggregate_pipeline()


def deploy_model() -> dict[str, object]:
    return deploy_to_hospitals()


def retrain_remote_models(targets: list[str], dataset: str = "set2") -> dict[str, object]:
    return retrain_hospitals(targets=targets, dataset=dataset)


def evaluate_model(dataset: str = "all") -> dict[str, object]:
    result = evaluate_main_model(dataset=dataset)
    cache_latest_evaluation(result)
    trigger_status_refresh(force=True)
    return result


def predict_model(records: list[dict[str, float]]) -> dict[str, object]:
    return predict_records(records)


def compare_versions(test_dataset: str, items: list[dict[str, str]]) -> dict[str, object]:
    return compare_named_versions(test_dataset=test_dataset, items=items)


def clean_start_models() -> dict[str, object]:
    result = clear_model_artifacts()
    trigger_status_refresh(force=True)
    return result


def delete_models_version(model_family: str, version_name: str) -> dict[str, object]:
    result = delete_model_version(model_family=model_family, version_name=version_name)
    trigger_status_refresh(force=True)
    return result


def delete_models_family(model_family: str) -> dict[str, object]:
    result = delete_model_family(model_family=model_family)
    trigger_status_refresh(force=True)
    return result


def delete_models_all() -> dict[str, object]:
    result = delete_all_model_files()
    trigger_status_refresh(force=True)
    return result


def forward_uploaded_model_to_target(
    file_path,
    *,
    source_server: str,
    target_server: str,
    model_family: str,
) -> dict[str, object]:
    return forward_uploaded_model(
        file_path,
        source_server=source_server,
        target_server=target_server,
        model_family=model_family,
    )
