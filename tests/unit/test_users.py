import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    AdminChangeUserRoleRequest,
    AdminEditUserInfoRequest,
    AdminSetUserActiveStatusRequest,
    AdminSetUserPasswordRequest,
    EditUserProfileRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _envelope(result):
    return {"success": True, "message": "ok", "result": result}


def test_disable_hits_endpoint_and_returns_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/user/u1/delete"
        return httpx.Response(200, json=_envelope(True))

    out = _client(handler).users.disable("u1")
    assert out is True


def test_get_profile_decodes_enveloped_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/user/profile"
        return httpx.Response(
            200,
            json=_envelope(
                {
                    "uuid": "u1",
                    "is_admin": True,
                    "has_sso_identity": False,
                    "has_local_password": True,
                    "is_sso_only": False,
                    "email": "a@b.com",
                }
            ),
        )

    prof = _client(handler).users.get_profile()
    assert prof.uuid == "u1"
    assert prof.is_admin is True
    assert prof.email == "a@b.com"


def test_update_profile_sends_body_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/user/profile"
        assert b"Jane" in req.content
        return httpx.Response(200, json={"status": "ok"})

    out = _client(handler).users.update_profile(EditUserProfileRequest(firstname="Jane"))
    assert out == {"status": "ok"}


def test_search_returns_enveloped_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/user/search"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {"uuid": "u1", "email": "a@b.com", "firstname": "Al"},
                    {"uuid": "u2", "email": "c@d.com"},
                ]
            ),
        )

    out = _client(handler).users.search()
    assert [u.uuid for u in out] == ["u1", "u2"]
    assert out[0].email == "a@b.com"


def test_retrieve_decodes_enveloped_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/user/uuid-1"
        return httpx.Response(
            200,
            json=_envelope(
                {
                    "uuid": "uuid-1",
                    "organization_id": "org-1",
                    "role_id": 3,
                    "role_name": "user",
                    "is_active": True,
                    "created_at": 1699564800,
                    "updated_at": 1699564900,
                    "email": "a@b.com",
                }
            ),
        )

    u = _client(handler).users.retrieve("uuid-1")
    assert u.uuid == "uuid-1"
    assert u.role_name == "user"
    assert u.role_id == 3


def test_set_password_sends_body_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/users/uuid-1/set-password"
        assert b"SecurePassword123!" in req.content
        return httpx.Response(
            200,
            json={"user_uuid": "uuid-1", "email": "a@b.com", "message": "done"},
        )

    out = _client(handler).users.set_password(
        "uuid-1", AdminSetUserPasswordRequest(password="SecurePassword123!")
    )
    assert out.user_uuid == "uuid-1"
    assert out.message == "done"


def test_get_auth_status_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/users/uuid-1/auth-status"
        return httpx.Response(
            200,
            json={
                "has_sso_identity": True,
                "has_local_password": False,
                "is_sso_only": True,
            },
        )

    out = _client(handler).users.get_auth_status("uuid-1")
    assert out.has_sso_identity is True
    assert out.is_sso_only is True


def test_change_role_sends_body_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/admin/users/uuid-1/role"
        assert b"admin" in req.content
        return httpx.Response(
            200,
            json={
                "user_uuid": "uuid-1",
                "email": "a@b.com",
                "old_role_name": "user",
                "new_role_name": "admin",
            },
        )

    out = _client(handler).users.change_role(
        "uuid-1", AdminChangeUserRoleRequest(new_role_name="admin")
    )
    assert out.new_role_name == "admin"
    assert out.old_role_name == "user"


def test_remove_role_hits_endpoint_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/users/uuid-1/roles/editor"
        return httpx.Response(204)

    assert _client(handler).users.remove_role("uuid-1", "editor") is None


def test_list_roles_returns_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/users/uuid-1/roles"
        return httpx.Response(
            200,
            json=[
                {"id": 1, "name": "admin", "created_at": 1699564800},
                {"id": 2, "name": "user", "created_at": 1699564900},
            ],
        )

    out = _client(handler).users.list_roles("uuid-1")
    assert [r.name for r in out] == ["admin", "user"]
    assert out[0].id == 1


def test_update_info_sends_body_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/admin/users/uuid-1/info"
        assert b"newmail@x.com" in req.content
        return httpx.Response(
            200,
            json={
                "user_uuid": "uuid-1",
                "email": "newmail@x.com",
                "role_name": "user",
                "is_active": True,
                "organization_id": "org-1",
            },
        )

    out = _client(handler).users.update_info(
        "uuid-1", AdminEditUserInfoRequest(email="newmail@x.com")
    )
    assert out.email == "newmail@x.com"
    assert out.is_active is True


def test_set_active_status_sends_body_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/admin/users/uuid-1/status"
        assert b"false" in req.content
        return httpx.Response(
            200,
            json={
                "user_uuid": "uuid-1",
                "email": "a@b.com",
                "is_active": False,
                "message": "disabled",
            },
        )

    out = _client(handler).users.set_active_status(
        "uuid-1", AdminSetUserActiveStatusRequest(is_active=False)
    )
    assert out.is_active is False
    assert out.message == "disabled"


def test_delete_sends_query_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/users/uuid-1"
        assert req.url.params["reassign_agents_to"] == "uuid-2"
        return httpx.Response(
            200,
            json={"user_uuid": "uuid-1", "email": "a@b.com", "message": "gone"},
        )

    out = _client(handler).users.delete("uuid-1", reassign_agents_to="uuid-2")
    assert out.user_uuid == "uuid-1"
    assert out.message == "gone"


def test_delete_omits_query_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "reassign_agents_to" not in req.url.params
        return httpx.Response(
            200,
            json={"user_uuid": "uuid-1", "email": "a@b.com"},
        )

    out = _client(handler).users.delete("uuid-1")
    assert out.user_uuid == "uuid-1"


async def test_async_users_get_profile_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/user/profile"
        return httpx.Response(
            200,
            json=_envelope(
                {
                    "uuid": "u9",
                    "is_admin": False,
                    "has_sso_identity": False,
                    "has_local_password": True,
                    "is_sso_only": False,
                }
            ),
        )

    client = _aclient(handler)
    try:
        prof = await client.users.get_profile()
        assert prof.uuid == "u9"
        assert prof.is_admin is False
    finally:
        await client.aclose()
