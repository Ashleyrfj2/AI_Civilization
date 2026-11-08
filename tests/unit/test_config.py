"""Config load/validate tests."""

from ai_civilization.config import SimulationConfig, load_config


def test_defaults():
    """Defaults are sane and valid."""
    cfg = SimulationConfig()
    assert cfg.seed == 42
    assert cfg.ticks == 5


def test_load_toml(tmp_path):
    """TOML [simulation] section loads correctly."""
    path = tmp_path / "sim.toml"
    path.write_text('[simulation]\nexperiment_name = "t"\nseed = 7\nticks = 3\n')
    cfg = load_config(path)
    assert (cfg.seed, cfg.ticks) == (7, 3)
