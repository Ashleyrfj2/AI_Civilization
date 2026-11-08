"""Engine determinism and persistence tests."""

from ai_civilization.config import SimulationConfig
from ai_civilization.persistence.store import init_db
from ai_civilization.simulation.engine import SimulationEngine


def run_summary(seed=42, ticks=5):
    """Run a short in-memory simulation and return its summary."""
    cfg = SimulationConfig(seed=seed, ticks=ticks, db_path=":memory:")
    engine = SimulationEngine(cfg, init_db(":memory:"))
    return engine.run()


def test_deterministic_same_seed():
    """Same seed yields the same checkpoint."""
    assert run_summary()["last_checkpoint"] == run_summary()["last_checkpoint"]


def test_different_seed_differs():
    """Different seeds diverge."""
    assert run_summary(seed=1)["last_checkpoint"] != run_summary(seed=2)["last_checkpoint"]


def test_events_recorded():
    """Each tick appends exactly one event row."""
    cfg = SimulationConfig(seed=42, ticks=4, db_path=":memory:")
    store = init_db(":memory:")
    engine = SimulationEngine(cfg, store)
    summary = engine.run()
    assert summary["events"] == 4
    assert store.count_events(engine.world_id) == 4
