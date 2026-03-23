from employability_2.app.services.deployment import deploy_model_to_main_server
from employability_2.app.services.evaluation import evaluate_active_model
from employability_2.app.services.model_registry import delete_local_family, delete_local_version
from employability_2.app.services.status import get_system_status
from employability_2.app.services.training import activate_model_version, train_or_retrain_model
from employability_2.app.views.dashboard_view import get_dashboard_html


def render_dashboard() -> str:
    return get_dashboard_html()


def get_health_status() -> dict[str, str]:
    return {"status": "ok", "service": "employability_2"}


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


def delete_local_model_version(version_name: str) -> dict[str, object]:
    return delete_local_version(version_name)


def delete_local_model_family() -> dict[str, object]:
    return delete_local_family()

