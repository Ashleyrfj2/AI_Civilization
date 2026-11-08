"""CLI run integration test (temporary file DB)."""

import json
import subprocess
import sys


def test_cli_run_ok(tmp_path):
    """CLI exits 0 and reports 3 ticks."""
    db = tmp_path / "t.db"
    proc = subprocess.run(
        [sys.executable, "-m", "ai_civilization.cli", "run", "--ticks", "3", "--db", str(db)],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["status"] == "ok" and summary["ticks"] == 3
