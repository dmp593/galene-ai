import json

import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _response() -> dict:
    return {
        "id": "modr-1",
        "model": "shield-uuid",
        "results": [
            {
                "flagged": True,
                "categories": {"violence": True, "hate": False},
                "category_scores": {"violence": 0.98, "hate": 0.01},
            }
        ],
    }


def test_create_sends_input_and_model_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/moderations"
        body = json.loads(req.content)
        assert body["input"] == "I hate you"
        assert body["model"] == "shield-uuid"
        return httpx.Response(200, json=_response())

    result = _client(handler).moderations.create(input="I hate you", model="shield-uuid")
    assert result.id == "modr-1"
    assert result.model == "shield-uuid"
    assert result.results[0].flagged is True
    assert result.results[0].categories["violence"] is True
    assert result.results[0].category_scores["violence"] == 0.98


def test_create_omits_model_when_absent_and_forwards_extra():
    def handler(req: httpx.Request) -> httpx.Response:
        body = json.loads(req.content)
        assert "model" not in body
        assert body["input"] == ["a", "b"]
        assert body["custom_flag"] is True
        return httpx.Response(200, json=_response())

    result = _client(handler).moderations.create(input=["a", "b"], custom_flag=True)
    assert result.results[0].flagged is True


async def test_async_create_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/moderations"
        body = json.loads(req.content)
        assert body["input"] == "hello"
        return httpx.Response(200, json=_response())

    client = _aclient(handler)
    try:
        result = await client.moderations.create(input="hello", model="shield-uuid")
        assert result.id == "modr-1"
        assert result.results[0].flagged is True
    finally:
        await client.aclose()
