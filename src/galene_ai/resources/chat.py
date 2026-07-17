"""`chat` resource: OpenAI-compatible chat completions.

Two spec operations back this namespace:

- `_completions_v1_chat_completions_post` — direct `POST /v1/chat/completions`.
- `_mode_completions__mode__v1_chat_completions_post` — mode-prefixed
  `POST /{mode}/v1/chat/completions`, selecting an inference mode.

Per the SDK's ergonomic-kwargs convention for the inference namespaces
(`chat`/`responses`/`embeddings`/`moderations`), callers pass `model` and
`messages` (plus any extra OpenAI parameters via `**extra`) rather than
constructing a request model themselves. The request body is assembled here as
a plain JSON payload matching `OpenaiChatCompletionRequest`. Non-streaming
responses decode to `OpenaiChatCompletionResponse`; streaming responses
(`stream=True`) yield raw SSE `dict` chunks (the spec defines no chunk model).
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai._core.streaming import AsyncStream, Stream
from galene_ai.models._generated import OpenaiChatCompletionResponse


def _payload(
    model: str, messages: list[dict[str, Any]], stream: bool, extra: dict[str, Any]
) -> dict[str, Any]:
    return {"model": model, "messages": messages, "stream": stream, **extra}


class Chat(SyncResource):
    """Generate OpenAI-compatible chat completions."""

    namespace: ClassVar[str] = "chat"

    @operation("_completions_v1_chat_completions_post")
    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiChatCompletionResponse | Stream[dict[str, Any]]:
        """Generate direct chat completions."""
        payload = _payload(model, messages, stream, extra)
        if stream:
            return cast(
                Stream[dict[str, Any]],
                self._client.post("/v1/chat/completions", json_body=payload, stream_type=dict),
            )
        return cast(
            OpenaiChatCompletionResponse,
            self._client.post(
                "/v1/chat/completions",
                json_body=payload,
                cast_to=OpenaiChatCompletionResponse,
            ),
        )

    @operation("_mode_completions__mode__v1_chat_completions_post")
    def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiChatCompletionResponse | Stream[dict[str, Any]]:
        """Generate chat completions with different modes."""
        payload = _payload(model, messages, stream, extra)
        path = f"/{mode}/v1/chat/completions"
        if stream:
            return cast(
                Stream[dict[str, Any]],
                self._client.post(path, json_body=payload, stream_type=dict),
            )
        return cast(
            OpenaiChatCompletionResponse,
            self._client.post(path, json_body=payload, cast_to=OpenaiChatCompletionResponse),
        )


class AsyncChat(AsyncResource):
    """Async counterpart of `Chat`."""

    namespace: ClassVar[str] = "chat"

    @operation("_completions_v1_chat_completions_post")
    async def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiChatCompletionResponse | AsyncStream[dict[str, Any]]:
        """Generate direct chat completions."""
        payload = _payload(model, messages, stream, extra)
        if stream:
            return cast(
                AsyncStream[dict[str, Any]],
                await self._client.post(
                    "/v1/chat/completions", json_body=payload, stream_type=dict
                ),
            )
        return cast(
            OpenaiChatCompletionResponse,
            await self._client.post(
                "/v1/chat/completions",
                json_body=payload,
                cast_to=OpenaiChatCompletionResponse,
            ),
        )

    @operation("_mode_completions__mode__v1_chat_completions_post")
    async def create_with_mode(
        self,
        mode: str,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **extra: Any,
    ) -> OpenaiChatCompletionResponse | AsyncStream[dict[str, Any]]:
        """Generate chat completions with different modes."""
        payload = _payload(model, messages, stream, extra)
        path = f"/{mode}/v1/chat/completions"
        if stream:
            return cast(
                AsyncStream[dict[str, Any]],
                await self._client.post(path, json_body=payload, stream_type=dict),
            )
        return cast(
            OpenaiChatCompletionResponse,
            await self._client.post(path, json_body=payload, cast_to=OpenaiChatCompletionResponse),
        )


Galene._NAMESPACES.append(Chat)
AsyncGalene._NAMESPACES.append(AsyncChat)
