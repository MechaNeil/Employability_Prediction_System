from __future__ import annotations

from functools import lru_cache
from pathlib import Path


TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "dashboard.html"


@lru_cache(maxsize=1)
def get_dashboard_html() -> str:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Dashboard template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")
