from __future__ import annotations

from main_server.app.services.evaluation import evaluate_global_model
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


def deploy_model() -> dict[str, str]:
    return deploy_to_hospitals()


def retrain_remote_models(targets: list[str], dataset: str = "set2") -> dict[str, object]:
    return retrain_hospitals(targets=targets, dataset=dataset)


def evaluate_model(dataset: str = "all") -> dict[str, object]:
    result = evaluate_global_model(dataset=dataset)
    cache_latest_evaluation(result)
    trigger_status_refresh(force=True)
    return result


def predict_model(records: list[dict[str, float]]) -> dict[str, object]:
    return predict_records(records)


def compare_versions(test_dataset: str, items: list[dict[str, str]]) -> dict[str, object]:
    return compare_named_versions(test_dataset=test_dataset, items=items)


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
