import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import UpdateImportItem, UpdateImportsRequest

ORG = "org-1"
CONN = "conn-9"
BASE = f"/admin/organizations/{ORG}/sso-connectors/{CONN}"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_available_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/available-groups"
        return httpx.Response(
            200,
            json={
                "fetched_at": 1699564800,
                "tenant_id": "t-1",
                "groups": [
                    {
                        "idp_group_id": "g1",
                        "idp_group_name": "Engineering",
                        "member_count": 12,
                        "is_imported": False,
                    }
                ],
            },
        )

    result = _client(handler).groups.available(ORG, CONN)
    assert result.fetched_at == 1699564800
    assert result.tenant_id == "t-1"
    assert result.groups[0].idp_group_id == "g1"


def test_imported_hits_endpoint_and_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/imported-groups"
        return httpx.Response(
            200,
            json=[
                {
                    "idp_group_id": "g1",
                    "idp_group_name": "Engineering",
                    "role_id": 7,
                    "role_name": "eng",
                    "is_active": True,
                    "created_at": 1699564800,
                    "updated_at": 1699564900,
                }
            ],
        )

    groups = _client(handler).groups.imported(ORG, CONN)
    assert len(groups) == 1
    assert groups[0].role_id == 7
    assert groups[0].idp_group_name == "Engineering"


def test_update_imports_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/imported-groups"
        import json

        payload = json.loads(req.content)
        assert payload["items"][0]["idp_group_id"] == "g1"
        return httpx.Response(
            200,
            json={
                "imported_count": 1,
                "deactivated_count": 0,
                "reactivated_count": 2,
            },
        )

    body = UpdateImportsRequest(
        items=[UpdateImportItem(idp_group_id="g1", idp_group_name="Engineering")]
    )
    result = _client(handler).groups.update_imports(ORG, CONN, body=body)
    assert result.imported_count == 1
    assert result.reactivated_count == 2


def test_resync_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/resync"
        return httpx.Response(
            200,
            json={"users_processed": 10, "users_updated": 3, "errors": []},
        )

    result = _client(handler).groups.resync(ORG, CONN)
    assert result.users_processed == 10
    assert result.users_updated == 3


def test_consent_status_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/consent-status"
        return httpx.Response(
            200,
            json={
                "granted": True,
                "granted_at": 1699564800,
                "tenant_id": "t-1",
                "missing_permissions": [],
            },
        )

    result = _client(handler).groups.consent_status(ORG, CONN)
    assert result.granted is True
    assert result.tenant_id == "t-1"


def test_admin_consent_url_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/admin-consent-url"
        return httpx.Response(200, json={"url": "https://consent.example/adminconsent"})

    result = _client(handler).groups.admin_consent_url(ORG, CONN)
    assert result["url"] == "https://consent.example/adminconsent"


async def test_async_groups_consent_status_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/consent-status"
        return httpx.Response(200, json={"granted": False})

    client = _aclient(handler)
    try:
        result = await client.groups.consent_status(ORG, CONN)
        assert result.granted is False
    finally:
        await client.aclose()
