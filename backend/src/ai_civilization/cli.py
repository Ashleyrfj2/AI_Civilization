"""Command-line interface for the Phase 0 skeleton simulation."""

from __future__ import annotations

import argparse
import json
import sys

from ai_civilization import __version__
from ai_civilization.config import SimulationConfig, load_config
from ai_civilization.persistence.store import init_db
from ai_civilization.simulation.engine import SimulationEngine


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="ai-civ", description="AI_Civilization Phase 0 skeleton")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("run", help="run the skeleton simulation")
    run.add_argument("--config", default=None, help="path to TOML config file")
    run.add_argument("--ticks", type=int, default=None, help="override tick count")
    run.add_argument("--seed", type=int, default=None, help="override RNG seed")
    run.add_argument("--db", default=None, help="override SQLite path (use :memory: for no file)")
    sub.add_parser("info", help="print version and module responsibilities")
    return parser


def cmd_run(args: argparse.Namespace) -> int:
    """Run the skeleton simulation and print the JSON summary."""
    cfg = load_config(args.config)
    overrides = {}
    if args.ticks is not None:
        overrides["ticks"] = args.ticks
    if args.seed is not None:
        overrides["seed"] = args.seed
    if args.db is not None:
        overrides["db_path"] = args.db
    if overrides:
        cfg = SimulationConfig(**{**cfg.model_dump(), **overrides})

    store = init_db(cfg.db_path)
    engine = SimulationEngine(cfg, store)
    summary = engine.run(cfg.ticks)
    print(json.dumps(summary, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if args.command == "run" or args.command is None:
        # Default to a short run so bare `python -m ai_civilization.cli` works.
        if args.command is None:
            args.config, args.ticks, args.seed, args.db = None, 5, None, None
        return cmd_run(args)
    if args.command == "info":
        print(f"ai-civilization {__version__}: agents propose, simulation validates/executes.")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
