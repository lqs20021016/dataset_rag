"""Entry node for preparing an import request."""

from pathlib import Path
from typing import Any

from app.import_process.state import State


def prepare_import(state: State) -> dict[str, Any]:
    source_path = state.source_path.strip()
    source_type = (state.source_type or Path(source_path).suffix.lstrip(".")).lower()

    if not source_path:
        return {"status": "failed", "error": "source_path is required"}

    return {
        "source_path": source_path,
        "source_type": source_type,
        "needs_pdf_conversion": source_type == "pdf",
        "status": "prepared",
        "error": None,
    }
