"""BGE embedding node."""

from typing import Any

from app.import_process.state import State


def embed_with_bge(state: State) -> dict[str, Any]:
    """Vectorize chunks with an injected BGE-compatible embedder."""

    try:
        if state.bge_embedder is None:
            embeddings: list[list[float]] = []
        elif hasattr(state.bge_embedder, "embed_documents"):
            embeddings = state.bge_embedder.embed_documents(state.chunks)
        elif hasattr(state.bge_embedder, "encode"):
            encoded = state.bge_embedder.encode(state.chunks)
            embeddings = encoded.tolist() if hasattr(encoded, "tolist") else list(encoded)
        else:
            raise TypeError("bge_embedder must provide embed_documents() or encode()")

        return {"embeddings": embeddings, "status": "vectorized", "error": None}
    except Exception as exc:
        return {"status": "failed", "error": f"BGE vectorization failed: {exc}"}
