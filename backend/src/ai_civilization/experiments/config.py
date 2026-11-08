"""Experiment configuration and reproducibility metadata (placeholder)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ExperimentConfig(BaseModel):
    """Identifies an experiment run for future reproducibility."""

    name: str = Field(min_length=1)
    seed: int = Field(default=42, ge=0)
    notes: str = ""
    parameters: dict[str, str] = Field(default_factory=dict)
