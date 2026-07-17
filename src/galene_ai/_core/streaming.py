from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from types import TracebackType

import httpx
import msgspec

from galene_ai._core.sse import aiter_sse_lines, iter_sse_lines


class Stream[T]:
    def __init__(self, response: httpx.Response, chunk_type: type[T]) -> None:
        self._response = response
        self._chunk_type = chunk_type

    def __iter__(self) -> Iterator[T]:
        for payload in iter_sse_lines(self._response.iter_lines()):
            yield msgspec.json.decode(payload.encode(), type=self._chunk_type)

    def __enter__(self) -> Stream[T]:
        return self

    def __exit__(self, *exc: object) -> None:
        self._response.close()


class AsyncStream[T]:
    def __init__(self, response: httpx.Response, chunk_type: type[T]) -> None:
        self._response = response
        self._chunk_type = chunk_type

    async def __aiter__(self) -> AsyncIterator[T]:
        async for payload in aiter_sse_lines(self._response.aiter_lines()):
            yield msgspec.json.decode(payload.encode(), type=self._chunk_type)

    async def __aenter__(self) -> AsyncStream[T]:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self._response.aclose()
