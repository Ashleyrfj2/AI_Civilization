"""Seeded deterministic simulation engine (Phase 0 skeleton)."""

from __future__ import annotations

import random

from ai_civilization.config import SimulationConfig
from ai_civilization.persistence.store import EventStore
from ai_civilization.world.models import WorldEvent, WorldState


class SimulationEngine:
    """Advances a deterministic empty world a fixed number of ticks.

    Determinism: all randomness comes from random.Random(seed). No wall-clock
    or unseeded randomness may influence state transitions.
    """

    def __init__(self, config: SimulationConfig, store: EventStore) -> None:
        self.config = config
        self.store = store
        self.rng = random.Random(config.seed)
        self.world = WorldState(name=config.world_name, seed=config.seed)
        self.world_id = store.create_world(config.world_name, config.seed)

    def step(self) -> WorldEvent:
        """Advance one tick and record a heartbeat event."""
        checkpoint = self.rng.random()
        self.world.tick += 1
        event = WorldEvent(
            tick=self.world.tick,
            kind="heartbeat",
            payload={"checkpoint": checkpoint, "world": self.world.name},
        )
        self.store.append_event(self.world_id, event)
        return event

    def run(self, ticks: int | None = None) -> dict:
        """Run n ticks, write a snapshot row, and return a JSON-serializable summary."""
        total = ticks if ticks is not None else self.config.ticks
        events: list[WorldEvent] = [self.step() for _ in range(total)]
        self.store.snapshot(self.world_id, self.world.tick, self.world.model_dump_json())
        last = events[-1].payload["checkpoint"] if events else None
        return {
            "experiment": self.config.experiment_name,
            "world": self.world.name,
            "seed": self.config.seed,
            "ticks": self.world.tick,
            "events": len(events),
            "last_checkpoint": last,
            "db_path": self.config.db_path,
            "status": "ok",
        }
