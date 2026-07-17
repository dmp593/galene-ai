"""`responses` resource: OpenAI-compatible Responses API (`/v1/responses`).

Two spec operations back this namespace: the direct endpoint (`/v1/responses`,
`_responses_v1_responses_post`) and the mode-prefixed variant
(`/{mode}/v1/responses`, `_mode_responses__mode__v1_responses_post`) which routes
generation through the shield/direct pipeline selected by the `mode` path segment.

Following the ergonomic-kwargs convention for the inference namespaces (see
`TYPING_RULES.md`), both methods expand the request into keyword arguments
(`model`, `input`, plus arbitrary `**extra` passthrough) and build the JSON body
internally rather than accepting a `body:` model. When `stream=True` the response
is a Server-Sent-Events `Stream` of raw `dict` chunks (there is no chunk model).
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai._core.streaming import AsyncStream, Stream
from galene_ai.models._generated import OpenaiResponsesResponse


def _payload(model: str, input: Any, stream: bool, extra: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {"model": model, "input": input, **extra}
    if stream:
        body["stream"] = True
    return body


class Responses(SyncResource):
    """Generate model responses (OpenAI Responses API)."""

    namespace: ClassVar[str] = "responses"

    @operation("_responses_v1_responses_post")
    def create(
        self,
        *,
        model: str,
        input: Any,
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiResponsesResponse | Stream[dict[str, Any]]:
        """Generate direct responses."""
        body = _payload(model, input, stream, extra)
        if stream:
            return cast(
                Stream[dict[str, Any]],
                self._client.post("/v1/responses", json_body=body, stream_type=dict),
            )
        return cast(
            OpenaiResponsesResponse,
            self._client.post("/v1/responses", json_body=body, cast_to=OpenaiResponsesResponse),
        )

    @operation("_mode_responses__mode__v1_responses_post")
    def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        input: Any,
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiResponsesResponse | Stream[dict[str, Any]]:
        """Generate responses with mode (shield/direct)."""
        body = _payload(model, input, stream, extra)
        path = f"/{mode}/v1/responses"
        if stream:
            return cast(
                Stream[dict[str, Any]],
                self._client.post(path, json_body=body, stream_type=dict),
            )
        return cast(
            OpenaiResponsesResponse,
            self._client.post(path, json_body=body, cast_to=OpenaiResponsesResponse),
        )


class AsyncResponses(AsyncResource):
    """Async counterpart of `Responses`."""

    namespace: ClassVar[str] = "responses"

    @operation("_responses_v1_responses_post")
    async def create(
        self,
        *,
        model: str,
        input: Any,
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiResponsesResponse | AsyncStream[dict[str, Any]]:
        """Generate direct responses."""
        body = _payload(model, input, stream, extra)
        if stream:
            return cast(
                AsyncStream[dict[str, Any]],
                await self._client.post("/v1/responses", json_body=body, stream_type=dict),
            )
        return cast(
            OpenaiResponsesResponse,
            await self._client.post(
                "/v1/responses", json_body=body, cast_to=OpenaiResponsesResponse
            ),
        )

    @operation("_mode_responses__mode__v1_responses_post")
    async def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        input: Any,
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiResponsesResponse | AsyncStream[dict[str, Any]]:
        """Generate responses with mode (shield/direct)."""
        body = _payload(model, input, stream, extra)
        path = f"/{mode}/v1/responses"
        if stream:
            return cast(
                AsyncStream[dict[str, Any]],
                await self._client.post(path, json_body=body, stream_type=dict),
            )
        return cast(
            OpenaiResponsesResponse,
            await self._client.post(path, json_body=body, cast_to=OpenaiResponsesResponse),
        )


Galene._NAMESPACES.append(Responses)
AsyncGalene._NAMESPACES.append(AsyncResponses)
