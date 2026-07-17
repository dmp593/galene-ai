import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models._generated import AdminUserCreateRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_list_users_hits_endpoint_and_decodes_users():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org-1/users"
        return httpx.Response(
            200,
            json={
                "users": [
                    {
                        "uuid": "u1",
                        "role": {"names": ["admin"]},
                        "created_at": 1699564800,
                        "updated_at": 1699564900,
                        "firstname": "John",
                        "lastname": "Doe",
                        "email": "john.doe@company.com",
                        "status": True,
                    }
                ]
            },
        )

    resp = _client(handler).organizations.list_users("org-1")
    assert len(resp.users) == 1
    assert resp.users[0].uuid == "u1"
    assert resp.users[0].email == "john.doe@company.com"
    assert resp.users[0].role.names == ["admin"]


def test_create_user_posts_body_and_decodes_response():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org-1/users"
        assert b'"email":"john.doe@company.com"' in req.content
        assert b'"role_name":"user"' in req.content
        return httpx.Response(
            200,
            json={
                "user_uuid": "user-uuid-123456",
                "email": "john.doe@company.com",
                "role_name": "user",
                "is_active": False,
                "organization_id": "org-1",
                "message": "User invited. Registration email sent.",
                "registration_link_sent": True,
                "firstname": "John",
                "lastname": "Doe",
            },
        )

    body = AdminUserCreateRequest(email="john.doe@company.com", role_name="user", firstname="John")
    resp = _client(handler).organizations.create_user("org-1", body)
    assert resp.user_uuid == "user-uuid-123456"
    assert resp.is_active is False
    assert resp.registration_link_sent is True


async def test_async_organizations_list_users_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org-9/users"
        return httpx.Response(
            200,
            json={
                "users": [
                    {
                        "uuid": "u9",
                        "role": {"names": ["viewer"]},
                        "created_at": 1699564800,
                        "updated_at": 1699564900,
                    }
                ]
            },
        )

    client = _aclient(handler)
    try:
        resp = await client.organizations.list_users("org-9")
        assert resp.users[0].uuid == "u9"
        assert resp.users[0].role.names == ["viewer"]
    finally:
        await client.aclose()
