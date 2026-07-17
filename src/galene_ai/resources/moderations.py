"""`moderations` resource: OpenAI-compatible content moderation via Generative Shield.

`POST /v1/moderations` mirrors OpenAI's Moderations API. Following the ergonomic-kwargs
convention for the inference namespaces, `create` expands `input`/`model` (plus any
provider-specific `**extra`) into the JSON payload rather than taking a single `body:`
model, and decodes the un-enveloped `ModerationResponse`.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models import ModerationResponse


def _moderation_payload(
    input: str | list[str], model: str | None, extra: dict[str, Any]
) -> dict[str, Any]:
    payload: dict[str, Any] = {"input": input}
    if model is not None:
        payload["model"] = model
    payload.update(extra)
    return payload


class Moderations(SyncResource):
    """Moderate content with Generative Shield."""

    namespace: ClassVar[str] = "moderations"

    @operation("_moderations_v1_moderations_post")
    def create(
        self, *, input: str | list[str], model: str | None = None, **extra: Any
    ) -> ModerationResponse:
        """Use Generative Shield standalone."""
        return cast(
            ModerationResponse,
            self._client.post(
                "/v1/moderations",
                json_body=_moderation_payload(input, model, extra),
                cast_to=ModerationResponse,
            ),
        )


class AsyncModerations(AsyncResource):
    """Async counterpart of `Moderations`."""

    namespace: ClassVar[str] = "moderations"

    @operation("_moderations_v1_moderations_post")
    async def create(
        self, *, input: str | list[str], model: str | None = None, **extra: Any
    ) -> ModerationResponse:
        """Use Generative Shield standalone."""
        return cast(
            ModerationResponse,
            await self._client.post(
                "/v1/moderations",
                json_body=_moderation_payload(input, model, extra),
                cast_to=ModerationResponse,
            ),
        )


Galene._NAMESPACES.append(Moderations)
AsyncGalene._NAMESPACES.append(AsyncModerations)
