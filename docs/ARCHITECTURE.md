# Architecture (Phase 0)

## Central rule
AI agents propose actions; independent simulation systems validate and execute them.

## Authority split
- **Python backend owns:** persistent records (SQLite), transactions, tick
  scheduling, state transitions, experiment coordination, snapshot writes.
- **Godot/Jolt owns:** physical calculations (stability, loads, mechanisms).
  Godot returns a `PhysicsOutcome`; the backend validates and commits it.
  There is exactly one physics authority (Jolt). No Rapier.
- Snapshot restore / recovery is NOT implemented in Phase 0 (snapshots are
  written for future use; no restore path exists yet).

## Module responsibilities
- `agents/` — IDs, observations, proposed actions, provider interface.
- `cognition/` / `memory/` — reasoning/planning and memory access (placeholders).
- `world/` — world state, time, entities, events (skeleton models).
- `resources/` — materials, quantities, ownership, conservation (contracts only).
- `economy/` — inventories, offers, transactions (contracts only).
- `construction/` — design proposals + validation results (contracts only).
- `physics/` — `PhysicsGateway` abstraction (contract only, raises until wired).
- `simulation/` — seeded deterministic engine (real skeleton).
- `persistence/` — SQLite init, event log, snapshot writes (restore not implemented).
- `experiments/` — experiment configs + reproducibility metadata.
- `models/` — provider adapters (`NullProvider` default; Ollama-ready stub).
- `telemetry/` — logging helpers.

## Determinism
Seeded `random.Random(seed)` only. No wall-clock in transitions.
Configs + seeds are logged with every run for reproducibility.
