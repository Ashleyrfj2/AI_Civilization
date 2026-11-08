# Development

## Requirements
- Python 3.11+ (3.11, 3.12, 3.13 supported)
- Godot 4.6 (for the `godot/` scene; optional for Python-only work)
- macOS or Windows; Linux CI via GitHub Actions

## Setup
```bash
python3 --version   # >=3.11
make install        # pip install -e ".[dev]"
make lint
make test
make run            # skeleton sim, 5 ticks
```

## Determinism check
```bash
bash scripts/check_determinism.sh
```

## Godot
Open `godot/project.godot` in Godot 4.6 and run the Main scene, or headless:

```bash
bash scripts/check_godot.sh   # SKIP if no Godot binary; real run otherwise
```

Headless CI validation is a file-presence check only (no Godot binary in CI).

## Windows server + Mac mini control
- The simulation is headless-capable: run `python -m ai_civilization.cli run`
  on the Windows server (Python 3.11+, no display needed).
- Control/monitor from the Mac over SSH; copy the SQLite DB in `data/` or
  point `AICIV_DB_PATH` at a shared path. No Docker/K8s required in Phase 0.

## Env
Copy `.env.example` to `.env`. Never commit real keys (external providers
are disabled by default; no keys needed for tests).
