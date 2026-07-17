import httpx
import msgspec
import pytest

from galene_ai._core.sse import aiter_sse_lines, iter_sse_lines
from galene_ai._core.streaming import AsyncStream, Stream


class Chunk(msgspec.Struct):
    n: int


def test_iter_sse_lines_extracts_data_and_stops_on_done():
    raw = [
        'data: {"n":1}',
        "",
        'data: {"n":2}',
        "",
        "data: [DONE]",
        "",
    ]
    assert list(iter_sse_lines(raw)) == ['{"n":1}', '{"n":2}']


def _sse_response() -> httpx.Response:
    body = b'data: {"n": 1}\n\ndata: {"n": 2}\n\ndata: [DONE]\n\n'
    return httpx.Response(200, content=body, request=httpx.Request("GET", "https://x/y"))


def test_stream_iterates_typed_chunks_and_stops_on_done():
    response = _sse_response()
    chunks = list(Stream(response, Chunk))
    assert len(chunks) == 2
    assert chunks[0].n == 1
    assert chunks[1].n == 2


def test_stream_context_manager_closes_response():
    response = _sse_response()
    with Stream(response, Chunk) as stream:
        list(stream)
    assert response.is_closed is True


@pytest.mark.asyncio
async def test_async_stream_iterates_typed_chunks():
    response = _sse_response()
    chunks = []
    async for chunk in AsyncStream(response, Chunk):
        chunks.append(chunk)
    assert len(chunks) == 2
    assert chunks[0].n == 1
    assert chunks[1].n == 2


@pytest.mark.asyncio
async def test_aiter_sse_lines_extracts_data_and_stops_on_done():
    async def async_lines():
        for line in ['data: {"n":1}', "", 'data: {"n":2}', "", "data: [DONE]", ""]:
            yield line

    payloads = []
    async for payload in aiter_sse_lines(async_lines()):
        payloads.append(payload)
    assert payloads == ['{"n":1}', '{"n":2}']
