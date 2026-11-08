"""Engine determinism and persistence regression tests."""

from ai_civilization.config import SimulationConfig
from ai_civilization.persistence.store import init_db
from ai_civilization.simulation.engine import SimulationEngine


def run_summary(seed=42, ticks=5):
    """Run a short in-memory simulation and return its summary."""
    cfg = SimulationConfig(seed=seed, ticks=ticks, db_path=":memory:")
    engine = SimulationEngine(cfg, init_db(":memory:"))
    return engine.run()


def run_history(seed=42, ticks=5):
    """Capture returned events and persisted logical records for an independent run."""
    cfg = SimulationConfig(seed=seed, ticks=ticks, db_path=":memory:")
    store = init_db(":memory:")
    engine = SimulationEngine(cfg, store)
    events = [engine.step().model_dump(mode="json") for _ in range(ticks)]
    store.snapshot(engine.world_id, engine.world.tick, engine.world.model_dump_json())
    persisted_events = store.conn.execute(
        "SELECT tick, kind, payload_json FROM events ORDER BY id"
    ).fetchall()
    persisted_snapshots = store.conn.execute(
        "SELECT tick, state_json FROM snapshots ORDER BY id"
    ).fetchall()
    store.conn.close()
    return events, persisted_events, persisted_snapshots


def test_deterministic_same_seed():
    """Same seed yields the same checkpoint."""
    assert run_summary()["last_checkpoint"] == run_summary()["last_checkpoint"]


def test_complete_history_is_deterministic():
    """Identical seeds reproduce entire event histories and persisted state."""
    first = run_history()
    second = run_history()
    assert first == second
    assert len(first[0]) == 5
    assert all("created_at" not in event for event in first[0])


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
