from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class State:
    """State shared by all nodes in the document import graph."""

    source_path: str = ""
    source_type: str = ""
    needs_pdf_conversion: bool = False

    document_content: str = ""
    image_paths: list[str] = field(default_factory=list)
    chunks: list[str] = field(default_factory=list)
    entry_names: list[str] = field(default_factory=list)
    embeddings: list[list[float]] = field(default_factory=list)
    milvus_ids: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    error: str | None = None

    # Optional adapters. Production code can inject concrete implementations;
    # nodes remain importable and testable without external services.
    pdf_to_markdown: Callable[[str], str] | None = None
    image_processor: Callable[[str, list[str]], str] | None = None
    document_splitter: Callable[[str], list[str]] | None = None
    entry_name_recognizer: Callable[[str], str] | None = None
    bge_embedder: Any = None
    milvus_writer: Callable[
        [list[str], list[list[float]], list[str], dict[str, Any]], list[str]
    ] | None = None

