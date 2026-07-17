import httpx
import msgspec

from galene_ai import AsyncGalene, Galene
from galene_ai._core.streaming import AsyncStream, Stream

_SSE = {"content-type": "text/event-stream"}


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _response_json(rid: str = "resp_1") -> dict:
    return {
        "id": rid,
        "created_at": 1699564800,
        "status": "completed",
        "model": "Galene/LLM",
        "output": [],
        "object": "response",
    }


def test_create_posts_body_and_decodes_response():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/responses"
        body = msgspec.json.decode(req.content)
        assert body["model"] == "Galene/LLM"
        assert body["input"] == "What is the capital of France?"
        assert "stream" not in body
        return httpx.Response(200, json=_response_json())

    result = _client(handler).responses.create(
        model="Galene/LLM", input="What is the capital of France?"
    )
    assert result.id == "resp_1"
    assert result.status == "completed"
    assert result.model == "Galene/LLM"


def test_create_passes_extra_kwargs_into_body():
    def handler(req: httpx.Request) -> httpx.Response:
        body = msgspec.json.decode(req.content)
        assert body["temperature"] == 0.5
        assert body["enable_thinking"] is True
        return httpx.Response(200, json=_response_json())

    result = _client(handler).responses.create(
        model="Galene/LLM", input="hi", temperature=0.5, enable_thinking=True
    )
    assert result.id == "resp_1"


def test_create_streaming_returns_stream_of_dict_chunks():
    def handler(req: httpx.Request) -> httpx.Response:
        body = msgspec.json.decode(req.content)
        assert body["stream"] is True
        sse = 'data: {"type": "chunk", "n": 1}\n\ndata: [DONE]\n\n'
        return httpx.Response(200, content=sse.encode(), headers=_SSE)

    stream = _client(handler).responses.create(model="Galene/LLM", input="hi", stream=True)
    assert isinstance(stream, Stream)
    chunks = list(stream)
    assert chunks == [{"type": "chunk", "n": 1}]


def test_create_with_mode_uses_mode_prefixed_path():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/shield/v1/responses"
        body = msgspec.json.decode(req.content)
        assert body["model"] == "Galene/LLM"
        assert body["input"] == "hi"
        return httpx.Response(200, json=_response_json("resp_shield"))

    result = _client(handler).responses.create_with_mode("shield", model="Galene/LLM", input="hi")
    assert result.id == "resp_shield"
    assert result.status == "completed"


def test_create_with_mode_streaming_returns_stream():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/direct/v1/responses"
        body = msgspec.json.decode(req.content)
        assert body["stream"] is True
        sse = 'data: {"delta": "x"}\n\ndata: [DONE]\n\n'
        return httpx.Response(200, content=sse.encode(), headers=_SSE)

    stream = _client(handler).responses.create_with_mode(
        "direct", model="Galene/LLM", input="hi", stream=True
    )
    assert isinstance(stream, Stream)
    assert list(stream) == [{"delta": "x"}]


async def test_async_create_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/responses"
        return httpx.Response(200, json=_response_json("resp_async"))

    client = _aclient(handler)
    try:
        result = await client.responses.create(model="Galene/LLM", input="hi")
        assert result.id == "resp_async"
        assert result.status == "completed"
    finally:
        await client.aclose()


async def test_async_create_streaming_returns_async_stream():
    def handler(req: httpx.Request) -> httpx.Response:
        sse = 'data: {"n": 2}\n\ndata: [DONE]\n\n'
        return httpx.Response(200, content=sse.encode(), headers=_SSE)

    client = _aclient(handler)
    try:
        stream = await client.responses.create(model="Galene/LLM", input="hi", stream=True)
        assert isinstance(stream, AsyncStream)
        chunks = [c async for c in stream]
        assert chunks == [{"n": 2}]
    finally:
        await client.aclose()
