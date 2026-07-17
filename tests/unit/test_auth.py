import httpx
import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai.errors import GaleneError
from galene_ai.models import (
    KeycloakSSORequest,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    SignupRequest,
    SSOConnectorCreateRequest,
    SSOConnectorUpdateRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_signup_posts_body_and_decodes_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/signup"
        body = req.content
        assert b'"username":"jdoe"' in body
        assert b'"email":"jdoe@example.com"' in body
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"user_id": "u1"}},
        )

    result = _client(handler).auth.signup(
        SignupRequest(
            username="jdoe",
            email="jdoe@example.com",
            first_name="John",
            last_name="Doe",
            password="hunter2secure",
        )
    )
    assert result.user_id == "u1"


def test_signup_raises_on_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"success": False, "message": "email taken", "result": None}
        )

    with pytest.raises(GaleneError, match="email taken"):
        _client(handler).auth.signup(
            SignupRequest(
                username="jdoe",
                email="jdoe@example.com",
                first_name="John",
                last_name="Doe",
                password="hunter2secure",
            )
        )


def test_login_posts_credentials_and_decodes_tokens():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/login"
        assert b'"username":"jdoe"' in req.content
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "user_id": "u1",
                    "access_token": "at",
                    "refresh_token": "rt",
                },
            },
        )

    result = _client(handler).auth.login(LoginRequest(username="jdoe", password="pw"))
    assert result.access_token == "at"
    assert result.refresh_token == "rt"


def test_logout_returns_result_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/logout"
        assert b'"refresh_token":"rt"' in req.content
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": True},
        )

    result = _client(handler).auth.logout(LogoutRequest(refresh_token="rt"))
    assert result is True


def test_refresh_token_decodes_new_tokens():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/refresh-token"
        assert b'"refresh_token":"rt"' in req.content
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"access_token": "at2", "refresh_token": "rt2"},
            },
        )

    result = _client(handler).auth.refresh_token(RefreshTokenRequest(refresh_token="rt"))
    assert result.access_token == "at2"


def test_reset_password_decodes_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/reset-password"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"username": "jdoe", "success": True},
            },
        )

    result = _client(handler).auth.reset_password(
        ResetPasswordRequest(username="jdoe", actual_password="old", new_password="brandnew1")
    )
    assert result.username == "jdoe"
    assert result.success is True


def test_sso_posts_code_with_frontend_url_param_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/auth/sso/org7"
        assert req.url.params["frontend_url"] == "https://app.example.com"
        assert b'"code":"xyz"' in req.content
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"user_id": "u1", "access_token": "at"},
            },
        )

    result = _client(handler).auth.sso(
        "org7",
        KeycloakSSORequest(code="xyz"),
        frontend_url="https://app.example.com",
    )
    assert result.access_token == "at"


def test_sso_omits_frontend_url_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "frontend_url" not in req.url.params
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"access_token": "at"}},
        )

    result = _client(handler).auth.sso("org7", KeycloakSSORequest(code="xyz"))
    assert result.access_token == "at"


def test_get_sso_config_returns_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/auth/sso/org7/config"
        return httpx.Response(
            200,
            json=[
                {
                    "url": "https://kc",
                    "realm": "r",
                    "client_id": "c",
                    "callback_route": "/cb",
                    "idp_hint": "google",
                    "name": "Google",
                    "logo": "https://logo",
                }
            ],
        )

    configs = _client(handler).auth.get_sso_config("org7")
    assert len(configs) == 1
    assert configs[0].realm == "r"
    assert configs[0].name == "Google"


def test_create_sso_connector_posts_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org7/sso-connectors"
        assert b'"title":"Company Google"' in req.content
        return httpx.Response(
            200,
            json={
                "connector_uuid": "c1",
                "title": "Company Google",
                "type": "google_workspace",
            },
        )

    result = _client(handler).auth.create_sso_connector(
        "org7",
        SSOConnectorCreateRequest(title="Company Google", type="google_workspace", sso_uuid="s1"),
    )
    assert result.connector_uuid == "c1"
    assert result.type == "google_workspace"


def test_list_sso_connectors_decodes_wrapper():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org7/sso-connectors"
        return httpx.Response(
            200,
            json={
                "connectors": [{"connector_uuid": "c1", "title": "G", "type": "google_workspace"}]
            },
        )

    result = _client(handler).auth.list_sso_connectors("org7")
    assert result.connectors[0].connector_uuid == "c1"


def test_get_sso_connector_decodes_detail():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org7/sso-connectors/c1"
        return httpx.Response(
            200,
            json={
                "connector_uuid": "c1",
                "title": "G",
                "type": "google_workspace",
                "users_count": 5,
                "roles_count": 2,
                "accesses_count": 3,
            },
        )

    result = _client(handler).auth.get_sso_connector("org7", "c1")
    assert result.connector_uuid == "c1"
    assert result.users_count == 5


def test_update_sso_connector_puts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/admin/organizations/org7/sso-connectors/c1"
        assert b'"title":"Renamed"' in req.content
        return httpx.Response(
            200,
            json={
                "connector_uuid": "c1",
                "title": "Renamed",
                "type": "google_workspace",
            },
        )

    result = _client(handler).auth.update_sso_connector(
        "org7", "c1", SSOConnectorUpdateRequest(title="Renamed")
    )
    assert result.title == "Renamed"


def test_delete_sso_connector_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/organizations/org7/sso-connectors/c1"
        return httpx.Response(204)

    assert _client(handler).auth.delete_sso_connector("org7", "c1") is None


async def test_async_auth_login_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/login"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"access_token": "at", "refresh_token": "rt"},
            },
        )

    client = _aclient(handler)
    try:
        result = await client.auth.login(LoginRequest(username="jdoe", password="pw"))
        assert result.access_token == "at"
    finally:
        await client.aclose()
