"""galene-ai — Python SDK for the Galene.AI platform.

Quick start::

    from galene_ai import Galene

    client = Galene(api_key="sk-...")               # or GALENE_AI_API_KEY env var
    reply = client.chat.create(model="Galene/LLM", messages=[{"role": "user", "content": "Hi"}])
"""

from galene_ai import resources as resources  # noqa: F401  side effect: registers namespaces
from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.auth import ApiKeyAuth, SessionAuth
from galene_ai._core.pagination import (
    AsyncCursorPage,
    AsyncOffsetPage,
    CursorPage,
    OffsetPage,
)
from galene_ai._core.streaming import AsyncStream, Stream
from galene_ai.errors import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    GaleneError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)

__version__ = "1.1.0"
__api_version__ = "1.0.0"  # kept in sync with spec/VERSION

__all__ = [
    # clients
    "Galene",
    "AsyncGalene",
    # auth
    "ApiKeyAuth",
    "SessionAuth",
    # pagination
    "CursorPage",
    "OffsetPage",
    "AsyncCursorPage",
    "AsyncOffsetPage",
    # streaming
    "Stream",
    "AsyncStream",
    # errors
    "GaleneError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    # metadata
    "__version__",
    "__api_version__",
]
