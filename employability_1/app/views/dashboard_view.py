from pathlib import Path

_TEMPLATE_CACHE: str | None = None


def get_dashboard_html() -> str:
    global _TEMPLATE_CACHE  # noqa: PLW0603
    if _TEMPLATE_CACHE is not None:
        return _TEMPLATE_CACHE

    template_path = Path(__file__).resolve().parent / "templates" / "dashboard.html"
    _TEMPLATE_CACHE = template_path.read_text(encoding="utf-8")
    return _TEMPLATE_CACHE
