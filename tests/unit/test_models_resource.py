import httpx

from galene_ai import AsyncGalene, Galene

_MODEL_LIST = {
    "object": "list",
    "data": [
        {"id": "gpt-4o", "object": "model", "created": 1699564800, "owned_by": "galene"},
        {"id": "gpt-4o-mini", "object": "model", "created": 1699564800, "owned_by": "galene"},
    ],
}


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_list_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/models"
        return httpx.Response(200, json=_MODEL_LIST)

    result = _client(handler).models.list()
    assert isinstance(result, dict)
    assert result["object"] == "list"
    assert [m["id"] for m in result["data"]] == ["gpt-4o", "gpt-4o-mini"]


def test_list_with_mode_prefixes_path():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/openai/v1/models"
        return httpx.Response(200, json=_MODEL_LIST)

    result = _client(handler).models.list_with_mode("openai")
    assert isinstance(result, dict)
    assert result["data"][0]["id"] == "gpt-4o"


async def test_async_models_list_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/models"
        return httpx.Response(200, json=_MODEL_LIST)

    client = _aclient(handler)
    try:
        result = await client.models.list()
        assert result["data"][1]["id"] == "gpt-4o-mini"
    finally:
        await client.aclose()
