import os

from galene_ai._config import (
    DEFAULT_BASE_URL,
    ENV_API_KEY,
    ENV_BASE_URL,
    ClientConfig,
    load_env_file,
)


def test_default_base_url_is_playground():
    assert DEFAULT_BASE_URL == "https://api.playground.galene.ai"


def test_resolve_uses_explicit_over_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # isolate from any developer .env
    monkeypatch.setenv(ENV_API_KEY, "env-key")
    monkeypatch.setenv(ENV_BASE_URL, "https://env.example")
    cfg = ClientConfig.resolve(api_key="explicit", base_url="https://explicit.example")
    assert cfg.api_key == "explicit"
    assert cfg.base_url == "https://explicit.example"


def test_resolve_falls_back_to_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(ENV_API_KEY, "env-key")
    monkeypatch.setenv(ENV_BASE_URL, "https://x.example/")
    cfg = ClientConfig.resolve()
    assert cfg.api_key == "env-key"
    assert cfg.base_url == "https://x.example"  # trailing slash stripped


def test_resolve_defaults_to_playground(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    monkeypatch.delenv(ENV_BASE_URL, raising=False)
    cfg = ClientConfig.resolve()
    assert cfg.api_key is None
    assert cfg.base_url == DEFAULT_BASE_URL


def test_load_env_file_populates_missing_vars(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    monkeypatch.delenv(ENV_BASE_URL, raising=False)
    (tmp_path / ".env").write_text(
        '# credentials\nGALENE_AI_API_KEY="from-dotenv"\nexport GALENE_AI_BASE_URL=https://env.example\n'
    )
    cfg = ClientConfig.resolve()
    assert cfg.api_key == "from-dotenv"
    assert cfg.base_url == "https://env.example"


def test_load_env_file_does_not_override_real_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(ENV_API_KEY, "real-env-wins")
    (tmp_path / ".env").write_text("GALENE_AI_API_KEY=from-dotenv\n")
    load_env_file()
    assert os.environ[ENV_API_KEY] == "real-env-wins"


def test_load_env_file_missing_is_noop(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    load_env_file()  # no .env here — must not raise
