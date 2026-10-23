"""Document splitting node."""

from typing import Any

from app.import_process.state import State


def split_document(state: State) -> dict[str, Any]:
    """Split content with an adapter or a paragraph-based fallback."""

    try:
        if state.document_splitter is not None:
            chunks = state.document_splitter(state.document_content)
        else:
            chunks = [
                block.strip()
                for block in state.document_content.split("\n\n")
                if block.strip()
            ]
        return {"chunks": chunks, "status": "document_split", "error": None}
    except Exception as exc:
        return {"status": "failed", "error": f"Document splitting failed: {exc}"}
