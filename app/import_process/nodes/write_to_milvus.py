"""Milvus persistence node."""

from typing import Any

from app.import_process.state import State


def write_to_milvus(state: State) -> dict[str, Any]:
    """Write vectors through an injected Milvus adapter."""

    try:
        ids = state.milvus_ids
        if state.milvus_writer is not None:
            ids = state.milvus_writer(
                state.chunks,
                state.embeddings,
                state.entry_names,
                state.metadata,
            )
        return {"milvus_ids": ids, "status": "completed", "error": None}
    except Exception as exc:
        return {"status": "failed", "error": f"Milvus write failed: {exc}"}
