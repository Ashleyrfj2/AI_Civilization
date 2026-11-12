"""Simulation configuration loading and validation (Pydantic)."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel, Field


class SimulationConfig(BaseModel):
    """Validated top-level simulation configuration."""

    experiment_name: str = Field(default="phase0-smoke", min_length=1)
    seed: int = Field(default=42, ge=0)
    ticks: int = Field(default=5, ge=1, le=100_000)
    db_path: str = Field(default="./data/dev.db")
    world_name: str = Field(default="empty-world")


def load_config(path: str | os.PathLike[str] | None = None) -> SimulationConfig:
    """Load TOML, then overlay .env and exported environment settings.

    Precedence (highest first): CLI overrides applied by the caller,
    exported environment, .env in the working directory, TOML, defaults.
    Reading .env does not modify os.environ.
    """
    data: dict = {}
    if path is not None:
        with open(Path(path), "rb") as f:
            raw = tomllib.load(f)
        data = raw.get("simulation", raw)

    local_values = dotenv_values(Path.cwd() / ".env")

    def setting(key: str, fallback: str | int) -> str | int:
        if key in os.environ:
            return os.environ[key]
        local_value = local_values.get(key)
        return local_value if local_value is not None else fallback

    return SimulationConfig(
        experiment_name=setting("AICIV_EXPERIMENT", data.get("experiment_name", "phase0-smoke")),
        seed=setting("AICIV_SEED", data.get("seed", 42)),
        ticks=data.get("ticks", 5),
        db_path=setting("AICIV_DB_PATH", data.get("db_path", "./data/dev.db")),
        world_name=data.get("world_name", "empty-world"),
    )
