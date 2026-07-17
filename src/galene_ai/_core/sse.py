from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator

_DATA = "data:"
_DONE = "[DONE]"


def iter_sse_lines(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        if not line.startswith(_DATA):
            continue
        payload = line[len(_DATA) :].strip()
        if payload == _DONE:
            return
        if payload:
            yield payload


async def aiter_sse_lines(lines: AsyncIterable[str]) -> AsyncIterator[str]:
    async for line in lines:
        if not line.startswith(_DATA):
            continue
        payload = line[len(_DATA) :].strip()
        if payload == _DONE:
            return
        if payload:
            yield payload
