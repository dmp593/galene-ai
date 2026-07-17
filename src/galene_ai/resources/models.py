"""`models` resource: list OpenAI-compatible available models.

Both operations return the OpenAI model-list envelope `{"object": "list", "data": [...]}`
as a plain `dict` (the spec's 200 schema is empty, so no dedicated model was generated).
`list` targets `/v1/models`; `list_with_mode` targets the mode-prefixed
`/{mode}/v1/models` variant.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation


class Models(SyncResource):
    """List available OpenAI-compatible models."""

    namespace: ClassVar[str] = "models"

    @operation("_models_v1_models_get")
    def list(self) -> dict[str, Any]:
        """List available models."""
        return cast(dict[str, Any], self._client.get("/v1/models", cast_to=dict))

    @operation("_mode_models__mode__v1_models_get")
    def list_with_mode(self, mode: str) -> dict[str, Any]:
        """List available models with mode."""
        return cast(dict[str, Any], self._client.get(f"/{mode}/v1/models", cast_to=dict))


class AsyncModels(AsyncResource):
    """Async counterpart of `Models`."""

    namespace: ClassVar[str] = "models"

    @operation("_models_v1_models_get")
    async def list(self) -> dict[str, Any]:
        """List available models."""
        return cast(dict[str, Any], await self._client.get("/v1/models", cast_to=dict))

    @operation("_mode_models__mode__v1_models_get")
    async def list_with_mode(self, mode: str) -> dict[str, Any]:
        """List available models with mode."""
        return cast(dict[str, Any], await self._client.get(f"/{mode}/v1/models", cast_to=dict))


Galene._NAMESPACES.append(Models)
AsyncGalene._NAMESPACES.append(AsyncModels)
