import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import OrganizationRoleCreateRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _role(role_id: int = 1, name: str = "admin") -> dict:
    return {
        "id": role_id,
        "name": name,
        "created_at": 1699564800,
        "description": "Organization administrator",
        "organization_id": "org-uuid-123",
        "is_active": True,
        "source": "manual",
    }


def test_list_all_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/roles"
        return httpx.Response(200, json={"roles": [_role(1, "admin"), _role(2, "user")]})

    resp = _client(handler).roles.list_all()
    assert [r.id for r in resp.roles] == [1, 2]
    assert resp.roles[0].name == "admin"


def test_list_organization_roles_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org-1/roles"
        return httpx.Response(200, json={"roles": [_role(5, "team_lead")]})

    resp = _client(handler).roles.list("org-1")
    assert resp.roles[0].id == 5
    assert resp.roles[0].name == "team_lead"


def test_create_organization_role_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org-1/roles"
        body = req.content
        assert b'"name":"team_lead"' in body.replace(b" ", b"")
        return httpx.Response(200, json=_role(7, "team_lead"))

    resp = _client(handler).roles.create(
        "org-1",
        body=OrganizationRoleCreateRequest(name="team_lead", description="Team leader"),
    )
    assert resp.id == 7
    assert resp.name == "team_lead"


def test_delete_organization_role_hits_endpoint_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/organizations/org-1/roles/9"
        return httpx.Response(200, json={"deleted": True})

    assert _client(handler).roles.delete("org-1", "9") is None


async def test_async_roles_list_all_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/roles"
        return httpx.Response(200, json={"roles": [_role(1, "admin")]})

    client = _aclient(handler)
    try:
        resp = await client.roles.list_all()
        assert resp.roles[0].id == 1
    finally:
        await client.aclose()
