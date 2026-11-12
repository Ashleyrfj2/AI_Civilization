"""SQLite persistence: init, event log, snapshots (skeleton).

Snapshot restore / recovery is NOT implemented in Phase 0: snapshots are
written for future use, but no restore path exists yet.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from ai_civilization.world.models import WorldEvent

SCHEMA = """
CREATE TABLE IF NOT EXISTS worlds (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  seed INTEGER NOT NULL,
  created_tick INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  world_id INTEGER NOT NULL REFERENCES worlds(id),
  tick INTEGER NOT NULL,
  kind TEXT NOT NULL,
  payload_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS snapshots (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  world_id INTEGER NOT NULL REFERENCES worlds(id),
  tick INTEGER NOT NULL,
  state_json TEXT NOT NULL
);
"""


class EventStore:
    """Thin SQLite wrapper for worlds, events, and snapshot rows."""

    def __init__(self, conn: sqlite3.Connection, db_path: str) -> None:
        self.conn = conn
        self.db_path = db_path

    def create_world(self, name: str, seed: int) -> int:
        """Insert a world row and return its id."""
        cur = self.conn.execute(
            "INSERT INTO worlds (name, seed, created_tick) VALUES (?, ?, 0)", (name, seed)
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def append_event(self, world_id: int, event: WorldEvent) -> None:
        """Append one event row."""
        payload = event.model_dump_json(include={"payload"})
        self.conn.execute(
            "INSERT INTO events (world_id, tick, kind, payload_json) VALUES (?, ?, ?, ?)",
            (world_id, event.tick, event.kind, payload),
        )
        self.conn.commit()

    def snapshot(self, world_id: int, tick: int, state_json: str) -> None:
        """Write a snapshot row (restore not implemented in Phase 0)."""
        self.conn.execute(
            "INSERT INTO snapshots (world_id, tick, state_json) VALUES (?, ?, ?)",
            (world_id, tick, state_json),
        )
        self.conn.commit()

    def count_events(self, world_id: int) -> int:
        """Count event rows for a world."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM events WHERE world_id = ?", (world_id,)
        ).fetchone()
        return int(row[0])


def init_db(db_path: str) -> EventStore:
    """Create parent dirs, apply schema, and return an EventStore."""
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return EventStore(conn, db_path)
