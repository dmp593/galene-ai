from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Default host when neither `base_url=` nor GALENE_AI_BASE_URL is set: the public
# playground. Point at your own deployment via the env var or the constructor.
DEFAULT_BASE_URL = "https://api.playground.galene.ai"

ENV_API_KEY = "GALENE_AI_API_KEY"
ENV_BASE_URL = "GALENE_AI_BASE_URL"


def load_env_file(path: str | os.PathLike[str] = ".env") -> None:
    """Load ``KEY=VALUE`` pairs from a ``.env`` file into ``os.environ``.

    No-op if the file is absent. Variables already present in the real
    environment are NOT overridden (the real environment wins). Minimal parser
    with no third-party dependency: supports ``#`` comments, blank lines, a
    leading ``export``, and single/double-quoted values.
    """
    p = Path(path)
    if not p.is_file():
        return
    for raw in p.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass
class ClientConfig:
    api_key: str | None = None
    base_url: str = DEFAULT_BASE_URL
    timeout: float = 60.0
    max_retries: int = 2
    default_headers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def resolve(
        cls,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        default_headers: dict[str, str] | None = None,
    ) -> ClientConfig:
        # Fill missing values from a local .env (never overriding the real env),
        # then resolve: explicit argument > environment variable > default.
        load_env_file()
        resolved_url = (base_url or os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL).rstrip("/")
        return cls(
            api_key=api_key or os.environ.get(ENV_API_KEY),
            base_url=resolved_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=dict(default_headers or {}),
        )
