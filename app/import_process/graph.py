from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.import_process.nodes import (
    convert_pdf_to_markdown,
    embed_with_bge,
    prepare_import,
    process_images,
    recognize_entry_names,
    split_document,
    write_to_milvus,
)
from app.import_process.state import State


def route_after_entry(state: State) -> Literal["convert_pdf", "process_images"]:
    """Route PDF inputs through conversion and all other inputs directly onward."""

    return "convert_pdf" if state.needs_pdf_conversion else "process_images"


def build_import_graph():
    builder = StateGraph(State)

    builder.add_node("prepare_import", prepare_import)
    builder.add_node("convert_pdf_to_markdown", convert_pdf_to_markdown)
    builder.add_node("process_images", process_images)
    builder.add_node("split_document", split_document)
    builder.add_node("recognize_entry_names", recognize_entry_names)
    builder.add_node("embed_with_bge", embed_with_bge)
    builder.add_node("write_to_milvus", write_to_milvus)

    builder.add_edge(START, "prepare_import")
    builder.add_conditional_edges(
        "prepare_import",
        route_after_entry,
        {
            "convert_pdf": "convert_pdf_to_markdown",
            "process_images": "process_images",
        },
    )
    builder.add_edge("convert_pdf_to_markdown", "process_images")
    builder.add_edge("process_images", "split_document")
    builder.add_edge("split_document", "recognize_entry_names")
    builder.add_edge("recognize_entry_names", "embed_with_bge")
    builder.add_edge("embed_with_bge", "write_to_milvus")
    builder.add_edge("write_to_milvus", END)

    return builder.compile()


import_graph = build_import_graph()
