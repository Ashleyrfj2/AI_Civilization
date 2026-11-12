"""Smoke: skeleton simulation starts, ticks, persists, exits cleanly."""

from ai_civilization.config import SimulationConfig
from ai_civilization.persistence.store import init_db
from ai_civilization.simulation.engine import SimulationEngine


def test_smoke_run(tmp_path):
    """Three ticks produce three events and status ok."""
    db = str(tmp_path / "smoke.db")
    cfg = SimulationConfig(seed=42, ticks=3, db_path=db)
    summary = SimulationEngine(cfg, init_db(db)).run()
    assert summary["status"] == "ok"
    assert summary["ticks"] == 3 and summary["events"] == 3
