import httpx

from galene_ai import AsyncGalene, Galene

USER = "11111111-2222-3333-4444-555555555555"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _payload() -> dict:
    return {
        "id": 42,
        "api_key": "sk-live-abc123",
        "is_active": True,
        "created_at": 1699564800,
        "user_uuid": USER,
        "user_email": "u@example.com",
    }


def test_create_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/users/{USER}/api-keys"
        return httpx.Response(200, json=_payload())

    result = _client(handler).admin.user_api_keys.create(USER)
    assert result.id == 42
    assert result.api_key == "sk-live-abc123"
    assert result.is_active is True
    assert result.user_email == "u@example.com"


async def test_async_create_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/users/{USER}/api-keys"
        return httpx.Response(200, json=_payload())

    client = _aclient(handler)
    try:
        result = await client.admin.user_api_keys.create(USER)
        assert result.id == 42
        assert result.user_uuid == USER
    finally:
        await client.aclose()
