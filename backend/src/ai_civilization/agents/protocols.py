"""Agent boundary contracts (Phase 0: typed placeholders)."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Observation(BaseModel):
    """What an agent sees at a tick."""

    agent_id: UUID
    tick: int = Field(ge=0)
    payload: dict[str, Any] = Field(default_factory=dict)


class ProposedAction(BaseModel):
    """Something an agent proposes. Never applied directly — it must be
    validated by the simulation engine and committed via persistence."""

    agent_id: UUID
    kind: str = Field(min_length=1)
    params: dict[str, Any] = Field(default_factory=dict)


class AgentRecord(BaseModel):
    """Registered agent identity."""

    agent_id: UUID
    name: str = Field(min_length=1)
