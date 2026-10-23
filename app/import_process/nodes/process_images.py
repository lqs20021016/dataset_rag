"""Image processing node."""

from typing import Any

from app.import_process.state import State


def process_images(state: State) -> dict[str, Any]:
    """Process document images through an optional injected adapter."""

    try:
        content = state.document_content
        if state.image_processor is not None:
            content = state.image_processor(content, state.image_paths)
        return {
            "document_content": content,
            "status": "images_processed",
            "error": None,
        }
    except Exception as exc:
        return {"status": "failed", "error": f"Image processing failed: {exc}"}
