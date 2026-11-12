"""Configuration loading and precedence regression tests."""

import pytest

from ai_civilization.config import SimulationConfig, load_config


@pytest.fixture(autouse=True)
def isolated_config(monkeypatch, tmp_path):
    """Avoid machine-specific environment variables and local .env files."""
    monkeypatch.chdir(tmp_path)
    for key in ("AICIV_EXPERIMENT", "AICIV_SEED", "AICIV_DB_PATH"):
        monkeypatch.delenv(key, raising=False)


def test_defaults():
    """Defaults are sane and valid."""
    cfg = SimulationConfig()
    assert cfg.seed == 42
    assert cfg.ticks == 5


def test_load_toml(tmp_path):
    """TOML configuration is used when neither .env nor exports override it."""
    path = tmp_path / "sim.toml"
    path.write_text('[simulation]\nexperiment_name = "t"\nseed = 7\nticks = 3\n')
    cfg = load_config(path)
    assert (cfg.seed, cfg.ticks) == (7, 3)


def test_dotenv_overrides_toml(tmp_path):
    """.env settings must be loaded as the development documentation promises."""
    path = tmp_path / "sim.toml"
    path.write_text(
        '[simulation]\nexperiment_name = "from-toml"\nseed = 7\n'
        'ticks = 3\ndb_path = "./toml.db"\n'
    )
    (tmp_path / ".env").write_text(
        'AICIV_EXPERIMENT=from-dotenv\nAICIV_SEED=11\nAICIV_DB_PATH=./dotenv.db\n'
    )

    cfg = load_config(path)
    assert cfg.experiment_name == "from-dotenv"
    assert cfg.seed == 11
    assert cfg.db_path == "./dotenv.db"
    assert cfg.ticks == 3


def test_exported_env_takes_precedence_over_dotenv_and_toml(tmp_path, monkeypatch):
    """Explicit environment variables override .env and TOML values."""
    path = tmp_path / "sim.toml"
    path.write_text('[simulation]\nseed = 7\ndb_path = "./toml.db"\n')
    (tmp_path / ".env").write_text('AICIV_SEED=11\nAICIV_DB_PATH=./dotenv.db\n')
    monkeypatch.setenv("AICIV_SEED", "23")
    monkeypatch.setenv("AICIV_DB_PATH", "./exported.db")

    cfg = load_config(path)
    assert cfg.seed == 23
    assert cfg.db_path == "./exported.db"
