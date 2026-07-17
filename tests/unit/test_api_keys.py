import json

import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import AdminToggleApiKeyRequest, DeleteApiKeyRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_list_hits_endpoint_and_decodes_enveloped_keys():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/auth/config/api-key"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "api_keys": [
                        {
                            "id": 1,
                            "masked_key": "sk-abcd...wxyz",
                            "is_active": True,
                            "created_at": 1699564800,
                            "last_used": 1699568400,
                        }
                    ]
                },
            },
        )

    result = _client(handler).api_keys.list()
    assert result.api_keys[0].id == 1
    assert result.api_keys[0].masked_key == "sk-abcd...wxyz"


def test_create_posts_and_decodes_enveloped_key():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/auth/config/api-key"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "api_key": "sk-secret-123",
                    "message": "Save this key securely.",
                },
            },
        )

    result = _client(handler).api_keys.create()
    assert result.api_key == "sk-secret-123"


def test_delete_sends_body_and_returns_envelope_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/auth/config/api-key"
        assert json.loads(req.content) == {"api_key_id": 7}
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": True},
        )

    result = _client(handler).api_keys.delete(DeleteApiKeyRequest(api_key_id=7))
    assert result is True


def test_get_user_keys_hits_admin_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/users/u-42/api-keys"
        return httpx.Response(
            200,
            json={
                "user_uuid": "u-42",
                "user_email": "jane@example.com",
                "user_name": "Jane Doe",
                "api_keys": [
                    {
                        "id": 5,
                        "masked_key": "sk-1234...abcd",
                        "is_active": True,
                        "created_at": 1699564800,
                        "updated_at": 1699568400,
                        "last_used_at": None,
                    }
                ],
            },
        )

    result = _client(handler).api_keys.get_user_keys("u-42")
    assert result.user_uuid == "u-42"
    assert result.api_keys[0].id == 5


def test_toggle_status_patches_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PATCH"
        assert req.url.path == "/admin/api-keys/9/status"
        assert json.loads(req.content) == {"is_active": False}
        return httpx.Response(
            200,
            json={"id": 9, "is_active": False, "updated_at": 1699568400},
        )

    result = _client(handler).api_keys.toggle_status("9", AdminToggleApiKeyRequest(is_active=False))
    assert result.id == 9
    assert result.is_active is False


def test_delete_admin_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/api-keys/9"
        return httpx.Response(
            200,
            json={"message": "API key deleted", "deleted_key_id": 9},
        )

    result = _client(handler).api_keys.delete_admin("9")
    assert result.deleted_key_id == 9
    assert result.message == "API key deleted"


async def test_async_list_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/auth/config/api-key"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "api_keys": [
                        {
                            "id": 1,
                            "masked_key": "sk-abcd...wxyz",
                            "is_active": True,
                            "created_at": 1699564800,
                            "last_used": 1699568400,
                        }
                    ]
                },
            },
        )

    client = _aclient(handler)
    try:
        result = await client.api_keys.list()
        assert result.api_keys[0].id == 1
    finally:
        await client.aclose()
