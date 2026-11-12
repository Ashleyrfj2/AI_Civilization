"""Physics authority boundary.

Godot/Jolt owns ALL physical calculations. Python submits PhysicsTestCase
payloads and receives PhysicsOutcome records, which the backend commits to
world state. Nothing here simulates physics; Phase 0 raises NotImplementedError
until the bridge is wired (see godot/BRIDGE.md and contracts/schemas/).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PhysicsTestCase(BaseModel):
    """A physics question for Godot/Jolt, e.g. stability, load, mechanism."""

    case_id: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class PhysicsOutcome(BaseModel):
    """Authoritative answer from Godot/Jolt."""

    case_id: str
    passed: bool
    measurements: dict[str, Any] = Field(default_factory=dict)
    notes: str = ""


class PhysicsGateway:
    """Abstract bridge to Godot/Jolt. Phase 0: contract only."""

    def submit(self, case: PhysicsTestCase) -> PhysicsOutcome:
        """Submit a case. Always raises until the bridge is wired."""
        raise NotImplementedError("Physics bridge not wired in Phase 0 (see godot/BRIDGE.md).")
