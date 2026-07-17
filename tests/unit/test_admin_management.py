import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


ORG = "550e8400-e29b-41d4-a716-446655440000"


def _org_json(name: str = "Acme Corporation") -> dict:
    return {
        "name": name,
        "uuid": ORG,
        "created_at": 1699564800,
        "updated_at": 1699564800,
    }


def test_create_organization_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations"
        assert b"Acme Corporation" in req.content
        return httpx.Response(200, json=_org_json())

    result = _client(handler).admin.management.create(
        OrganizationCreateRequest(name="Acme Corporation")
    )
    assert result.name == "Acme Corporation"
    assert result.uuid == ORG


def test_list_organizations_passes_pagination_params():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations"
        assert req.url.params["skip"] == "5"
        assert req.url.params["limit"] == "10"
        return httpx.Response(200, json=[_org_json("A"), _org_json("B")])

    result = _client(handler).admin.management.list(skip=5, limit=10)
    assert [o.name for o in result] == ["A", "B"]


def test_list_organizations_omits_params_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "skip" not in req.url.params
        assert "limit" not in req.url.params
        return httpx.Response(200, json=[])

    result = _client(handler).admin.management.list()
    assert result == []


def test_retrieve_organization_hits_endpoint():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}"
        return httpx.Response(200, json=_org_json())

    result = _client(handler).admin.management.retrieve(ORG)
    assert result.uuid == ORG


def test_update_organization_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"/admin/organizations/{ORG}"
        assert b"Renamed Corp" in req.content
        return httpx.Response(200, json=_org_json("Renamed Corp"))

    result = _client(handler).admin.management.update(
        ORG, OrganizationUpdateRequest(name="Renamed Corp")
    )
    assert result.name == "Renamed Corp"


def test_delete_organization_returns_summary():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}"
        return httpx.Response(
            200,
            json={
                "uuid": ORG,
                "name": "Acme Corporation",
                "deleted_users_count": 15,
                "deleted_agents_count": 8,
                "deleted_roles_count": 3,
            },
        )

    result = _client(handler).admin.management.delete(ORG)
    assert result.uuid == ORG
    assert result.deleted_users_count == 15
    assert result.deleted_agents_count == 8


async def test_async_management_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}"
        return httpx.Response(200, json=_org_json("Async Org"))

    client = _aclient(handler)
    try:
        result = await client.admin.management.retrieve(ORG)
        assert result.name == "Async Org"
        assert result.uuid == ORG
    finally:
        await client.aclose()
