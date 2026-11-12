# AGENTS.md — instructions for coding agents

## Project rule
**Agents propose actions; simulation systems validate and execute them.**
Never add code paths that let model output directly mutate world state,
invent resources, or bypass validation. All state transitions go through
the simulation engine + persistence layer.

## Boundaries
- Python backend (`backend/src/ai_civilization/`) owns: persistent records,
  transactions, scheduling/ticks, experiment coordination.
- Godot/Jolt (`godot/`) owns: physical calculations. Results return as
  `PhysicsOutcome` and are committed by the backend — never applied inside Godot.
- One physics authority (Jolt). Do not add Rapier or a second engine.
- No mandatory API keys for tests or basic simulation startup.
- No fake social/emergent behavior to look functional. Placeholders must say so.

## Workflow
- Python 3.11+, `backend/src` layout, `pydantic>=2` for contracts.
- Lint/format: `ruff check` + `ruff format`. Tests: `pytest`.
- Keep modules small with a documented responsibility (see each `__init__.py`).
- Add/extend JSON schemas in `contracts/schemas/` when crossing Python/Godot.
- Determinism: seeded RNG only (`random.Random(seed)`), no wall-clock in state transitions.
- Never commit secrets, `.db` files, model weights, or generated assets.

## Commands
```bash
make install   # pip install -e ".[dev]"
make lint
make test
make run       # skeleton sim
```

## Docs to read before changes
- `docs/ARCHITECTURE.md` (authority split)
- `docs/DEVELOPMENT.md` (setup)
- `docs/ROADMAP.md` (what comes next; stay in scope)
