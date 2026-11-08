# Physics and resources (Phase 0 stub)

- One physics authority: Godot/Jolt. See `godot/BRIDGE.md`.
- Python submits `PhysicsTestCase`; Godot returns `PhysicsOutcome`;
  the backend commits validated results. Bridge not wired in Phase 0.
- Resource conservation (no creation/destruction except via validated rules)
  is a contract in `resources/models.py`; enforcement comes in a later phase.
