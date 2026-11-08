# AI_Civilization

Experimental platform for studying autonomous AI agents living in a persistent,
physically grounded 3D environment.

> **Phase 0: Project Foundation.** This repo currently contains the working skeleton:
> a deterministic seeded Python simulation with SQLite persistence, typed
> architectural boundaries, and a minimal Godot 4.6 project skeleton.
> Autonomous agents, resources/trading, and physics validation are placeholders.

## Central rule

**AI agents propose actions; independent simulation systems validate and execute them.**
Agents cannot directly rewrite world state, invent resources, or declare that
their constructions work. The Python backend owns persistent records, transactions,
and experiment coordination, while Godot/Jolt owns physical calculations
(see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).

## Quickstart (macOS / Windows)

```bash
python3 --version   # 3.11+
make install        # pip install -e ".[dev]"
make test           # pytest
make run            # run skeleton sim (5 ticks)
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for full setup, including
Windows-server + Mac-mini control notes.

## Layout

- `backend/src/ai_civilization/` — Python backend (simulation, world, persistence, placeholder domains)
- `godot/` — Godot 4.6 + Jolt project skeleton and bridge contract
- `contracts/schemas/` — JSON schemas shared across the Python/Godot boundary
- `configs/` — simulation and experiment configs
- `tests/` — unit, integration, smoke
- `docs/` — architecture, development, experiment design, physics/resources, roadmap

## Status: real vs placeholder

| System | Status |
|---|---|
| CLI, config load/validate, seeded engine, SQLite persistence | Real (skeleton) |
| Deterministic ticks + event log | Real (skeleton) |
| Snapshot restore / recovery | Not implemented (writes snapshots only) |
| Python/Godot bridge | Contract only, not wired |
| Agents, memory, cognition, economy, construction, physics validation | Typed placeholders |
