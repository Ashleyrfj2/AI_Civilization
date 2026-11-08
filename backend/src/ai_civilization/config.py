"""Simulation configuration loading and validation (Pydantic)."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class SimulationConfig(BaseModel):
    """Validated top-level simulation configuration."""

    experiment_name: str = Field(default="phase0-smoke", min_length=1)
    seed: int = Field(default=42, ge=0)
    ticks: int = Field(default=5, ge=1, le=100_000)
    db_path: str = Field(default="./data/dev.db")
    world_name: str = Field(default="empty-world")


def load_config(path: str | os.PathLike[str] | None = None) -> SimulationConfig:
    """Load config from a TOML file with env overrides, else defaults."""
    data: dict = {}
    if path is not None:
        with open(Path(path), "rb") as f:
            raw = tomllib.load(f)
        data = raw.get("simulation", raw)
    return SimulationConfig(
        experiment_name=os.getenv("AICIV_EXPERIMENT", data.get("experiment_name", "phase0-smoke")),
        seed=int(os.getenv("AICIV_SEED", data.get("seed", 42))),
        ticks=int(data.get("ticks", 5)),
        db_path=os.getenv("AICIV_DB_PATH", data.get("db_path", "./data/dev.db")),
        world_name=data.get("world_name", "empty-world"),
    )
