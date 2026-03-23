from main_server.app.views.dashboard_view import get_dashboard_html


def render_dashboard() -> str:
    return get_dashboard_html()
