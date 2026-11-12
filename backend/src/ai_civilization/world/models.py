"""World state models (Phase 0 skeleton)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class WorldState(BaseModel):
    """Minimal world record."""

    name: str = "empty-world"
    tick: int = Field(default=0, ge=0)
    seed: int = Field(default=42, ge=0)
    entities: list[dict[str, Any]] = Field(default_factory=list)


class WorldEvent(BaseModel):
    """A deterministic state-transition event.

    Real-world timestamps belong in telemetry, not simulation state.
    """

    tick: int = Field(ge=0)
    kind: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
