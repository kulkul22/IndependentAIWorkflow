"""Shared workflow status normalization."""

STATUS_ALIASES = {
    "processing": "in_progress", "working": "in_progress",
    "coding": "in_progress", "inprogress": "in_progress",
    "qa": "in_test", "test": "in_test", "testing": "in_test",
    "completed": "done", "complete": "done", "finished": "done",
}


def normalize_status(value):
    """Return a dashboard status while preserving unknown values safely."""
    if not isinstance(value, str):
        return "todo"
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    return STATUS_ALIASES.get(normalized, normalized or "todo")
