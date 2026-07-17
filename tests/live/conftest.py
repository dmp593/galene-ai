"""Load a local `.env` before live tests run.

The SDK auto-loads `.env` when a client is constructed, but the live fixtures
check `os.environ` for `GALENE_AI_API_KEY` *before* building a client to decide
whether to skip. Loading it here (at collection time, non-overriding) makes the
`.env`-configured key/base-url visible to those skip checks.
"""

from galene_ai._config import load_env_file

load_env_file()
