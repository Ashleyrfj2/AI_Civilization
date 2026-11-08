"""CLI integration tests."""

import json
import subprocess
import sys

from ai_civilization.cli import main


def test_cli_run_ok(tmp_path):
    """CLI exits 0 and reports 3 ticks."""
    db = tmp_path / "t.db"
    proc = subprocess.run(
        [sys.executable, "-m", "ai_civilization.cli", "run", "--ticks", "3", "--db", str(db)],
        capture_output=True,
        text=True,
        cwd=".",
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["status"] == "ok" and summary["ticks"] == 3


def test_cli_overrides_exported_env_dotenv_and_toml(tmp_path, monkeypatch, capsys):
    """CLI seed and database flags have higher priority than all config sources."""
    monkeypatch.chdir(tmp_path)
    toml = tmp_path / "sim.toml"
    toml.write_text('[simulation]\nseed = 7\nticks = 2\ndb_path = "./toml.db"\n')
    (tmp_path / ".env").write_text('AICIV_SEED=11\nAICIV_DB_PATH=./dotenv.db\n')
    monkeypatch.setenv("AICIV_SEED", "23")
    monkeypatch.setenv("AICIV_DB_PATH", "./exported.db")

    assert main(["run", "--config", str(toml), "--ticks", "4", "--seed", "41", "--db", ":memory:"]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["seed"] == 41
    assert summary["ticks"] == 4
    assert summary["db_path"] == ":memory:"
