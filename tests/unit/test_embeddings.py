import json

import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _embedding_payload() -> dict:
    return {
        "object": "list",
        "model": "Galene/Embedding",
        "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}],
        "usage": {"prompt_tokens": 5, "total_tokens": 5},
    }


def test_create_posts_body_and_decodes_response():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/embeddings"
        body = json.loads(req.content)
        assert body["model"] == "Galene/Embedding"
        assert body["input"] == "hello world"
        return httpx.Response(200, json=_embedding_payload())

    resp = _client(handler).embeddings.create(model="Galene/Embedding", input="hello world")
    assert resp.model == "Galene/Embedding"
    assert resp.data[0].embedding == [0.1, 0.2, 0.3]
    assert resp.data[0].index == 0
    assert resp.usage is not None
    assert resp.usage.total_tokens == 5


def test_create_with_mode_uses_prefixed_path_and_passes_extra():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/proxy/v1/embeddings"
        body = json.loads(req.content)
        assert body["input"] == ["a", "b"]
        assert body["encoding_format"] == "float"
        return httpx.Response(200, json=_embedding_payload())

    resp = _client(handler).embeddings.create(
        model="Galene/Embedding",
        input=["a", "b"],
        mode="proxy",
        encoding_format="float",
    )
    assert resp.object == "list"
    assert len(resp.data) == 1


def test_create_with_mode_method_hits_prefixed_path():
    # The explicit create_with_mode() method carries the distinct operationId for
    # POST /{mode}/v1/embeddings.
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/shield/v1/embeddings"
        assert json.loads(req.content)["input"] == "hi"
        return httpx.Response(200, json=_embedding_payload())

    resp = _client(handler).embeddings.create_with_mode(
        "shield", model="Galene/Embedding", input="hi"
    )
    assert resp.model == "Galene/Embedding"
    assert resp.data[0].index == 0


async def test_async_create_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/embeddings"
        return httpx.Response(200, json=_embedding_payload())

    client = _aclient(handler)
    try:
        resp = await client.embeddings.create(model="Galene/Embedding", input="hi")
        assert resp.model == "Galene/Embedding"
        assert resp.data[0].embedding == [0.1, 0.2, 0.3]
    finally:
        await client.aclose()
