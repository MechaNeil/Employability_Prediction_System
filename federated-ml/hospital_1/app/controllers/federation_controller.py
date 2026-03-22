from hospital_1.app.services.deployment import deploy_model_to_main_server
from hospital_1.app.services.evaluation import evaluate_active_model
from hospital_1.app.services.status import get_system_status
from hospital_1.app.services.training import activate_model_version, train_or_retrain_model
from hospital_1.app.views.dashboard_view import get_dashboard_html


def render_dashboard() -> str:
    return get_dashboard_html()


def get_health_status() -> dict[str, str]:
    return {"status": "ok", "service": "hospital_1"}


def get_status() -> dict[str, object]:
    return get_system_status()


def train_model(dataset: str, retrain_from_main: bool) -> dict[str, object]:
    return train_or_retrain_model(dataset_key=dataset, retrain_from_main=retrain_from_main)


def evaluate_model(test_dataset: str) -> dict[str, object]:
    return evaluate_active_model(test_dataset)


def set_active_version(version_name: str) -> dict[str, object]:
    return activate_model_version(version_name)


def deploy_to_main(version_name: str | None = None) -> dict[str, object]:
    return deploy_model_to_main_server(version_name)
