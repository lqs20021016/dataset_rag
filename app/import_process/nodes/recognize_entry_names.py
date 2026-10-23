"""Entry-name recognition node."""

from typing import Any

from app.import_process.state import State


def recognize_entry_names(state: State) -> dict[str, Any]:
    """Recognize one entry name for every chunk."""

    try:
        if state.entry_name_recognizer is not None:
            names = [state.entry_name_recognizer(chunk) for chunk in state.chunks]
        else:
            names = [
                (chunk.splitlines()[0].strip()[:120] if chunk.strip() else "")
                for chunk in state.chunks
            ]
        return {"entry_names": names, "status": "entry_names_recognized", "error": None}
    except Exception as exc:
        return {"status": "failed", "error": f"Entry-name recognition failed: {exc}"}
