import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    DatabaseConnectorCreateRequest,
    DatabasePropertiesBatchUpdateRequest,
    ModelsAdminModelsDatabaseConnectorDatabaseConnectorUpdateRequest,
)

ORG = "org-1"
CONN = "conn-1"
BASE = f"/admin/organizations/{ORG}/db-connectors"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _connector_json(uuid=CONN):
    return {
        "connector_uuid": uuid,
        "connection_name": "main_prod_db",
        "title": "Prod DB",
        "type": "pgsql",
        "permission_type": "organization_wide",
    }


def test_create_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == BASE
        import json

        payload = json.loads(req.content)
        assert payload["connection_name"] == "main_prod_db"
        assert payload["type"] == "pgsql"
        return httpx.Response(200, json=_connector_json())

    body = DatabaseConnectorCreateRequest(
        connection_name="main_prod_db", title="Prod DB", type="pgsql"
    )
    result = _client(handler).database_connectors.create(ORG, body=body)
    assert result.connector_uuid == CONN
    assert result.title == "Prod DB"


def test_list_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == BASE
        return httpx.Response(200, json={"connectors": [_connector_json()]})

    result = _client(handler).database_connectors.list(ORG)
    assert [c.connector_uuid for c in result.connectors] == [CONN]


def test_retrieve_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{CONN}"
        return httpx.Response(200, json=_connector_json())

    result = _client(handler).database_connectors.retrieve(ORG, CONN)
    assert result.connector_uuid == CONN
    assert result.connection_name == "main_prod_db"


def test_update_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/{CONN}"
        import json

        assert json.loads(req.content)["title"] == "Renamed"
        return httpx.Response(200, json=_connector_json())

    body = ModelsAdminModelsDatabaseConnectorDatabaseConnectorUpdateRequest(title="Renamed")
    result = _client(handler).database_connectors.update(ORG, CONN, body=body)
    assert result.connector_uuid == CONN


def test_delete_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"{BASE}/{CONN}"
        return httpx.Response(200, json={})

    assert _client(handler).database_connectors.delete(ORG, CONN) is None


def test_discover_posts_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{CONN}/discover"
        return httpx.Response(200, json={"status": "started"})

    result = _client(handler).database_connectors.discover(ORG, CONN)
    assert result == {"status": "started"}


def test_update_properties_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"{BASE}/{CONN}/properties"
        return httpx.Response(
            200,
            json={
                "overall_success": True,
                "total_updates": 2,
                "successful_updates": 2,
                "failed_updates": 0,
                "results": [],
                "message": "ok",
            },
        )

    body = DatabasePropertiesBatchUpdateRequest()
    result = _client(handler).database_connectors.update_properties(ORG, CONN, body=body)
    assert result.overall_success is True
    assert result.total_updates == 2
    assert result.successful_updates == 2


def test_test_connection_posts_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{CONN}/test-connection"
        return httpx.Response(200, json={"ok": True})

    result = _client(handler).database_connectors.test_connection(ORG, CONN)
    assert result == {"ok": True}


def test_download_tables_config_gets_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{CONN}/tables-config"
        return httpx.Response(200, json={"tables": []})

    result = _client(handler).database_connectors.download_tables_config(ORG, CONN)
    assert result == {"tables": []}


def test_upload_tables_config_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"{BASE}/{CONN}/tables-config"
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="file"; filename="cfg.json"' in body
        assert b"{}" in body
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "applied",
                "tables_processed": 3,
                "columns_processed": 12,
            },
        )

    result = _client(handler).database_connectors.upload_tables_config(
        ORG, CONN, b"{}", filename="cfg.json"
    )
    assert result.success is True
    assert result.tables_processed == 3
    assert result.columns_processed == 12


def test_list_organization_connectors_unwraps_envelope():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/database_connectors"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "connectors": [
                        {
                            "connector_uuid": CONN,
                            "name": "main",
                            "organization_db_connector_uuid": "odc-1",
                            "created_at": 1699564800,
                            "updated_at": 1699564900,
                        }
                    ]
                },
            },
        )

    result = _client(handler).database_connectors.list_organization_connectors(ORG)
    assert result.connectors[0].connector_uuid == CONN
    assert result.connectors[0].name == "main"


async def test_async_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"{BASE}/{CONN}"
        return httpx.Response(200, json=_connector_json())

    client = _aclient(handler)
    try:
        result = await client.database_connectors.retrieve(ORG, CONN)
        assert result.connector_uuid == CONN
    finally:
        await client.aclose()
