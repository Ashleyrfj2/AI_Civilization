"""Construction proposal contracts (Phase 0 placeholders)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DesignProposal(BaseModel):
    """An agent-proposed design. Requires physics validation."""

    proposal_id: str = Field(min_length=1)
    author_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    materials: dict[str, float] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    """Outcome of validating a proposal."""

    proposal_id: str
    ok: bool
    reasons: list[str] = Field(default_factory=list)
