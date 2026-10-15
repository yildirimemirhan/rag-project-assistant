"""Health payload for the warm-up / keep-alive probe. Pure Python, no heavy imports."""


def health_status(state: dict, model_name: str) -> tuple[int, dict]:
    """Return (http_status, body). 503 until init_rag() has populated state."""
    collection = state.get("collection")
    if collection is None:
        return 503, {"status": "warming"}
    return 200, {"status": "ok", "chunks": collection.count(), "model": model_name}
