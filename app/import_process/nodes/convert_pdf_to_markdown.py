"""PDF-to-Markdown conversion node."""

from typing import Any

from app.import_process.state import State


def convert_pdf_to_markdown(state: State) -> dict[str, Any]:
    """Convert a PDF through the injected adapter when one is configured."""

    try:
        content = state.document_content
        if state.pdf_to_markdown is not None:
            content = state.pdf_to_markdown(state.source_path)
        return {
            "document_content": content,
            "status": "pdf_converted",
            "error": None,
        }
    except Exception as exc:
        return {"status": "failed", "error": f"PDF conversion failed: {exc}"}
