import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


ORG = "org-1"


def _config_payload() -> dict:
    return {
        "colors": {"primary": "#111111", "secondary": "#222222"},
        "assets": {"folder": "acme"},
        "endpoints": {"baseUrl": "https://acme.example", "socketPath": "/acme.sio"},
        "sso": {"keycloakRealm": "acme", "keycloakClientId": "web"},
        "settings": {"agentName": "Acme Bot", "supportEmail": "help@acme.example", "orgUuid": ORG},
        "features": {"webSearch": False, "imageGen": True},
    }


def test_get_config():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/frontend/config/{ORG}"
        return httpx.Response(200, json=_config_payload())

    result = _client(handler).admin.frontend.get_config(ORG)
    assert result.settings.orgUuid == ORG
    assert result.settings.agentName == "Acme Bot"
    assert result.colors.primary == "#111111"
    assert result.features.imageGen is True


async def test_async_get_config_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/frontend/config/{ORG}"
        return httpx.Response(200, json=_config_payload())

    client = _aclient(handler)
    try:
        result = await client.admin.frontend.get_config(ORG)
        assert result.settings.orgUuid == ORG
        assert result.endpoints.baseUrl == "https://acme.example"
    finally:
        await client.aclose()
