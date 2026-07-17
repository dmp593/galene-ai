import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_changelog_get_hits_endpoint_with_no_params():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/changelog"
        assert "lang" not in req.url.params
        assert "include_admin" not in req.url.params
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "version": "1.0.0",
                    "release_date": "2024-01-01",
                    "changes": ["Initial release"],
                },
            },
        )

    result = _client(handler).changelog.get()
    assert isinstance(result, dict)
    assert result["version"] == "1.0.0"
    assert result["release_date"] == "2024-01-01"


def test_changelog_get_hits_endpoint_with_lang_param():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/changelog"
        assert req.url.params["lang"] == "fr"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"version": "1.0.0", "content": "Contenu en français"},
            },
        )

    result = _client(handler).changelog.get(lang="fr")
    assert result["content"] == "Contenu en français"


def test_changelog_get_hits_endpoint_with_include_admin_param():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/changelog"
        assert req.url.params["include_admin"] == "true"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"version": "1.0.0", "admin_notes": "Internal notes"},
            },
        )

    result = _client(handler).changelog.get(include_admin=True)
    assert result["admin_notes"] == "Internal notes"


async def test_async_changelog_get_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/changelog"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"version": "1.0.0"},
            },
        )

    client = _aclient(handler)
    try:
        result = await client.changelog.get()
        assert result["version"] == "1.0.0"
    finally:
        await client.aclose()
