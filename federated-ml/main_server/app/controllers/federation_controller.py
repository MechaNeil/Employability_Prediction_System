from __future__ import annotations

from main_server.app.services.evaluation import evaluate_global_model
from main_server.app.services.inference import predict_records
from main_server.app.services.orchestration import (
    aggregate_pipeline,
    deploy_to_hospitals,
    retrain_hospitals,
)
from main_server.app.services.status import get_model_versions, get_system_status
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


def train_model() -> dict[str, object]:
    return train_main_model()


def aggregate_model() -> dict[str, object]:
    return aggregate_pipeline()


def deploy_model() -> dict[str, str]:
    return deploy_to_hospitals()


def retrain_remote_models() -> dict[str, str]:
    return retrain_hospitals()


def evaluate_model() -> dict[str, float]:
    return evaluate_global_model()


def predict_model(records: list[dict[str, float]]) -> dict[str, object]:
    return predict_records(records)
