import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models._generated import (
    MCPServerActiveItemsUpdateRequest,
    MCPServerTestRequest,
)

ORG = "org-1"
SRV = "srv-1"
BASE = f"/admin/organizations/{ORG}/mcp-servers"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _server_obj(uuid: str = SRV, name: str = "srv") -> dict:
    return {
        "server_uuid": uuid,
        "name": name,
        "server_type": "self_hosted",
        "permission_type": "organization_wide",
        "status": "ready",
        "created_at": 1699564800,
        "updated_at": 1699564900,
    }


def test_create_sends_multipart_form_and_zip_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == BASE
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="name"\r\n\r\nmy-server' in body
        assert b'name="server_type"\r\n\r\nself_hosted' in body
        assert b'name="permission_type"\r\n\r\norganization_wide' in body
        assert b'name="zip_file"; filename="s.zip"' in body
        assert b"ZIPDATA" in body
        return httpx.Response(200, json=_server_obj(name="my-server"))

    result = _client(handler).mcp_servers.create(
        ORG,
        name="my-server",
        server_type="self_hosted",
        permission_type="organization_wide",
        zip_file=b"ZIPDATA",
        zip_filename="s.zip",
    )
    assert result.server_uuid == SRV
    assert result.name == "my-server"
    assert result.status.value == "ready"


def test_list_hits_endpoint_with_include_tools_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == BASE
        assert req.url.params["include_tools"] == "true"
        return httpx.Response(200, json={"servers": [_server_obj()]})

    result = _client(handler).mcp_servers.list(ORG, include_tools=True)
    assert [s.server_uuid for s in result.servers] == [SRV]


def test_list_omits_include_tools_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "include_tools" not in req.url.params
        return httpx.Response(200, json={"servers": []})

    result = _client(handler).mcp_servers.list(ORG)
    assert result.servers == []


def test_retrieve_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{SRV}"
        return httpx.Response(200, json=_server_obj())

    result = _client(handler).mcp_servers.retrieve(ORG, SRV)
    assert result.server_uuid == SRV


def test_update_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/{SRV}"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="name"\r\n\r\nrenamed' in req.content
        return httpx.Response(200, json=_server_obj(name="renamed"))

    result = _client(handler).mcp_servers.update(
        ORG, SRV, name="renamed", zip_file=b"Z", zip_filename="u.zip"
    )
    assert result.name == "renamed"


def test_delete_hits_endpoint_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"{BASE}/{SRV}"
        return httpx.Response(204)

    assert _client(handler).mcp_servers.delete(ORG, SRV) is None


def test_test_connection_sends_json_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{SRV}/test-connection"
        assert req.headers["content-type"] == "application/json"
        import json

        payload = json.loads(req.content)
        assert payload["test_type"] == "tools"
        return httpx.Response(
            200,
            json={
                "success": True,
                "server_uuid": SRV,
                "test_type": "tools",
                "message": "ok",
                "duration_ms": 42,
            },
        )

    result = _client(handler).mcp_servers.test_connection(
        ORG, SRV, body=MCPServerTestRequest(test_type="tools")
    )
    assert result.success is True
    assert result.duration_ms == 42


def test_update_active_items_sends_json_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/{SRV}/active-items"
        import json

        payload = json.loads(req.content)
        assert payload["active_tools"] == ["a", "b"]
        return httpx.Response(200, json=_server_obj())

    result = _client(handler).mcp_servers.update_active_items(
        ORG, SRV, body=MCPServerActiveItemsUpdateRequest(active_tools=["a", "b"])
    )
    assert result.server_uuid == SRV


def test_list_organization_servers_unwraps_envelope_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/mcp_servers"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "servers": [
                        {
                            "server_uuid": SRV,
                            "name": "srv",
                            "server_type": "self_hosted",
                            "status": "ready",
                            "permission_type": "organization_wide",
                            "created_at": 1699564800,
                            "updated_at": 1699564900,
                            "memory_mb": 256,
                        }
                    ]
                },
            },
        )

    result = _client(handler).mcp_servers.list_organization_servers(ORG)
    assert [s.server_uuid for s in result.servers] == [SRV]
    assert result.servers[0].memory_mb == 256


async def test_async_mcp_servers_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{SRV}"
        return httpx.Response(200, json=_server_obj(name="async-srv"))

    client = _aclient(handler)
    try:
        result = await client.mcp_servers.retrieve(ORG, SRV)
        assert result.name == "async-srv"
    finally:
        await client.aclose()
