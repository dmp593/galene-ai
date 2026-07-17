import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _completion_json() -> dict:
    return {
        "id": "chatcmpl-1",
        "created": 1699564800,
        "model": "Galene/LLM",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Hi there"},
                "finish_reason": "stop",
            }
        ],
    }


def test_create_posts_direct_endpoint_with_model_and_messages():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/chat/completions"
        body = req.content
        assert b'"model":"Galene/LLM"' in body
        assert b'"stream":false' in body
        assert b"Hello" in body
        return httpx.Response(200, json=_completion_json())

    resp = _client(handler).chat.create(
        model="Galene/LLM",
        messages=[{"role": "user", "content": "Hello"}],
    )
    assert resp.id == "chatcmpl-1"
    assert resp.model == "Galene/LLM"
    assert resp.choices[0].message.content == "Hi there"
    assert resp.choices[0].finish_reason == "stop"


def test_create_passes_extra_kwargs_into_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert b'"temperature":0.5' in req.content
        return httpx.Response(200, json=_completion_json())

    resp = _client(handler).chat.create(
        model="Galene/LLM",
        messages=[{"role": "user", "content": "Hi"}],
        temperature=0.5,
    )
    assert resp.id == "chatcmpl-1"


def test_create_with_mode_targets_mode_prefixed_path():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/agent/v1/chat/completions"
        assert b'"model":"Galene/LLM"' in req.content
        return httpx.Response(200, json=_completion_json())

    resp = _client(handler).chat.create_with_mode(
        "agent",
        model="Galene/LLM",
        messages=[{"role": "user", "content": "Hello"}],
    )
    assert resp.id == "chatcmpl-1"


def test_create_streaming_yields_dict_chunks():
    def handler(req: httpx.Request) -> httpx.Response:
        assert b'"stream":true' in req.content
        sse = (
            b'data: {"id": "chatcmpl-1", "choices": [{"delta": {"content": "Hi"}}]}\n\n'
            b"data: [DONE]\n\n"
        )
        return httpx.Response(200, content=sse, headers={"content-type": "text/event-stream"})

    stream = _client(handler).chat.create(
        model="Galene/LLM",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True,
    )
    chunks = list(stream)
    assert chunks[0]["id"] == "chatcmpl-1"
    assert chunks[0]["choices"][0]["delta"]["content"] == "Hi"


async def test_async_chat_create_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/chat/completions"
        return httpx.Response(200, json=_completion_json())

    client = _aclient(handler)
    try:
        resp = await client.chat.create(
            model="Galene/LLM",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert resp.id == "chatcmpl-1"
        assert resp.choices[0].message.content == "Hi there"
    finally:
        await client.aclose()
