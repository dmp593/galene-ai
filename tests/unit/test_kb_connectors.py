import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    KBConnectorCreateRequest,
    KBConnectorTestRequest,
    ModelsAdminModelsKbConnectorKBConnectorUpdateRequest,
    ScopedDiscoveryPreviewRequest,
)

ORG = "org-1"
KBC = "kbc-1"
BASE = f"/admin/organizations/{ORG}/kb-connectors"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _connector_json(uuid="kbc-1", title="Docs"):
    return {
        "connector_uuid": uuid,
        "title": title,
        "type": "google_drive",
        "permission_type": "organization_wide",
    }


def test_create_posts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == BASE
        assert b'"title":"Docs"' in req.content
        return httpx.Response(200, json=_connector_json())

    body = KBConnectorCreateRequest(
        title="Docs", type="google_drive", permission_type="organization_wide"
    )
    result = _client(handler).kb_connectors.create(ORG, body=body)
    assert result.connector_uuid == "kbc-1"
    assert result.title == "Docs"


def test_list_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == BASE
        return httpx.Response(200, json={"connectors": [_connector_json()]})

    result = _client(handler).kb_connectors.list(ORG)
    assert result.connectors[0].connector_uuid == "kbc-1"


def test_retrieve_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{KBC}"
        return httpx.Response(200, json=_connector_json())

    result = _client(handler).kb_connectors.retrieve(ORG, KBC)
    assert result.connector_uuid == "kbc-1"
    assert result.type == "google_drive"


def test_update_puts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/{KBC}"
        assert b'"title":"New"' in req.content
        return httpx.Response(200, json=_connector_json(title="New"))

    body = ModelsAdminModelsKbConnectorKBConnectorUpdateRequest(title="New")
    result = _client(handler).kb_connectors.update(ORG, KBC, body=body)
    assert result.title == "New"


def test_delete_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"{BASE}/{KBC}"
        return httpx.Response(200, json={"ok": True})

    assert _client(handler).kb_connectors.delete(ORG, KBC) is None


def test_retrieve_discovery_cache_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{KBC}/discovery-cache"
        return httpx.Response(200, json={"available": True, "valid": True, "items_count": 2})

    result = _client(handler).kb_connectors.retrieve_discovery_cache(ORG, KBC)
    assert result.available is True
    assert result.items_count == 2


def test_list_drives_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{KBC}/drives"
        return httpx.Response(200, json={"drives": [{"id": "d1"}]})

    result = _client(handler).kb_connectors.list_drives(ORG, KBC)
    assert result["drives"][0]["id"] == "d1"


def test_browse_passes_path_param_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{KBC}/browse"
        assert req.url.params["path"] == "HR/"
        return httpx.Response(200, json={"items": []})

    result = _client(handler).kb_connectors.browse(ORG, KBC, path="HR/")
    assert result == {"items": []}


def test_browse_omits_path_when_not_given():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "path" not in req.url.params
        return httpx.Response(200, json={"items": []})

    _client(handler).kb_connectors.browse(ORG, KBC)


def test_preview_scoped_discovery_posts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{KBC}/scoped-discovery-preview"
        assert b'"paths":["HR/"]' in req.content
        return httpx.Response(200, json={"success": True, "total_count": 3})

    body = ScopedDiscoveryPreviewRequest(paths=["HR/"])
    result = _client(handler).kb_connectors.preview_scoped_discovery(ORG, KBC, body=body)
    assert result.success is True
    assert result.total_count == 3


def test_test_posts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{KBC}/test"
        assert b'"connector_uuid":"kbc-1"' in req.content
        return httpx.Response(
            200,
            json={
                "success": True,
                "connector_uuid": "kbc-1",
                "test_type": "connection",
                "message": "ok",
            },
        )

    body = KBConnectorTestRequest(connector_uuid="kbc-1")
    result = _client(handler).kb_connectors.test(ORG, KBC, body=body)
    assert result.success is True
    assert result.message == "ok"


def test_list_for_organization_unwraps_envelope():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb_connectors"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "connectors": [
                        {
                            "connector_uuid": "kbc-1",
                            "name": "Docs",
                            "organization_kb_connector_uuid": "okbc-1",
                            "created_at": 1699564800,
                            "updated_at": 1699564800,
                        }
                    ]
                },
            },
        )

    result = _client(handler).kb_connectors.list_for_organization(ORG)
    assert result.connectors[0].connector_uuid == "kbc-1"
    assert result.connectors[0].name == "Docs"


async def test_async_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{KBC}"
        return httpx.Response(200, json=_connector_json())

    client = _aclient(handler)
    try:
        result = await client.kb_connectors.retrieve(ORG, KBC)
        assert result.connector_uuid == "kbc-1"
    finally:
        await client.aclose()
