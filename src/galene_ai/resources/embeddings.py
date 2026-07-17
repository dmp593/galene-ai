"""`embeddings` resource: OpenAI-compatible embedding creation.

`/v1/embeddings` (and the mode-prefixed `/{mode}/v1/embeddings`) mirror OpenAI's
Embeddings API. Both operations share a single ergonomic `create` method that expands
the request fields as keyword arguments (per the inference-namespace convention) and
selects the mode-prefixed path when `mode` is supplied.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models import EmbeddingResponse


def _embeddings_path(mode: str | None) -> str:
    return f"/{mode}/v1/embeddings" if mode else "/v1/embeddings"


class Embeddings(SyncResource):
    """Create OpenAI-compatible embeddings."""

    namespace: ClassVar[str] = "embeddings"

    @operation("_embeddings_v1_embeddings_post")
    def create(
        self,
        *,
        model: str,
        input: str | list[str],
        mode: str | None = None,
        **extra: Any,
    ) -> EmbeddingResponse:
        """Create embeddings."""
        payload: dict[str, Any] = {"model": model, "input": input, **extra}
        return cast(
            EmbeddingResponse,
            self._client.post(
                _embeddings_path(mode),
                json_body=payload,
                cast_to=EmbeddingResponse,
            ),
        )

    @operation("_mode_embeddings__mode__v1_embeddings_post")
    def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        input: str | list[str],
        **extra: Any,
    ) -> EmbeddingResponse:
        """Create embeddings (with mode prefix)."""
        return self.create(model=model, input=input, mode=mode, **extra)


class AsyncEmbeddings(AsyncResource):
    """Async counterpart of `Embeddings`."""

    namespace: ClassVar[str] = "embeddings"

    @operation("_embeddings_v1_embeddings_post")
    async def create(
        self,
        *,
        model: str,
        input: str | list[str],
        mode: str | None = None,
        **extra: Any,
    ) -> EmbeddingResponse:
        """Create embeddings."""
        payload: dict[str, Any] = {"model": model, "input": input, **extra}
        return cast(
            EmbeddingResponse,
            await self._client.post(
                _embeddings_path(mode),
                json_body=payload,
                cast_to=EmbeddingResponse,
            ),
        )

    @operation("_mode_embeddings__mode__v1_embeddings_post")
    async def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        input: str | list[str],
        **extra: Any,
    ) -> EmbeddingResponse:
        """Create embeddings (with mode prefix)."""
        return await self.create(model=model, input=input, mode=mode, **extra)


Galene._NAMESPACES.append(Embeddings)
AsyncGalene._NAMESPACES.append(AsyncEmbeddings)
