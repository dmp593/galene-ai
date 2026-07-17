import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _result() -> dict:
    return {
        "success": True,
        "message": "ok",
        "result": {
            "users": [
                {
                    "uuid": "u1",
                    "organization_id": "o1",
                    "organization_name": "Acme",
                    "roles": ["admin"],
                    "is_active": True,
                    "created_at": 1699564800,
                    "firstname": "Ada",
                    "lastname": "Lovelace",
                    "email": "ada@example.com",
                }
            ],
            "page": 1,
            "page_size": 20,
            "total_pages": 3,
        },
    }


def test_search_users_hits_endpoint_with_query_params_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/search/users"
        assert req.url.params["q"] == "ada"
        assert req.url.params["page"] == "2"
        assert req.url.params["page_size"] == "20"
        assert req.url.params["organization_id"] == "o1"
        assert req.url.params["is_active"] == "true"
        assert req.url.params["role"] == "admin"
        assert req.url.params["sort_by"] == "created_at"
        assert req.url.params["sort_order"] == "desc"
        return httpx.Response(200, json=_result())

    resp = _client(handler).admin.search.users(
        q="ada",
        page=2,
        page_size=20,
        organization_id="o1",
        is_active=True,
        role="admin",
        sort_by="created_at",
        sort_order="desc",
    )
    assert resp.page == 1
    assert resp.total_pages == 3
    assert resp.users[0].uuid == "u1"
    assert resp.users[0].email == "ada@example.com"
    assert resp.users[0].roles == ["admin"]


def test_search_users_omits_unset_params():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "q" not in req.url.params
        assert "page" not in req.url.params
        assert "is_active" not in req.url.params
        return httpx.Response(200, json=_result())

    resp = _client(handler).admin.search.users()
    assert resp.page_size == 20


async def test_async_search_users_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/search/users"
        return httpx.Response(200, json=_result())

    client = _aclient(handler)
    try:
        resp = await client.admin.search.users(q="ada")
        assert resp.users[0].organization_name == "Acme"
    finally:
        await client.aclose()
