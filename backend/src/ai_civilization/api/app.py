"""Future HTTP entrypoint. Phase 0: importable placeholder, no server started."""

from __future__ import annotations


def create_app() -> dict:
    """Return a stub app descriptor."""
    return {"name": "ai-civilization", "phase": 0, "http": "not-implemented"}
