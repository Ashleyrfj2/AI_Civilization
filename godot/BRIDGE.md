# Python/Godot Bridge (Phase 0: contract only, NOT wired)

## Authority split
- Python backend: persistent records, transactions, ticks, experiment coordination.
- Godot/Jolt: physical calculations. Godot never writes world state directly.

## Planned flow
1. Python builds a `PhysicsTestCase` (see `contracts/schemas/physics_case.schema.json`).
2. Godot loads the case, runs Jolt simulation headless, returns `PhysicsOutcome`.
3. Python validates + commits the outcome to SQLite via the simulation engine.

## Status
Not implemented or tested in Phase 0. `PhysicsGateway.submit()` raises
`NotImplementedError` by design. Do not claim integration until wired + tested.
