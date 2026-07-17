import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models._generated import (
    KBSyncConfigurationCreateRequest,
    KBSyncConfigurationUpdateRequest,
    KBSyncDeleteRequest,
)

ORG = "org-1"
CFG = "cfg-9"


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _config_json(**overrides):
    base = {
        "id": CFG,
        "connector_uuid": "conn-1",
        "source_type": "s3",
        "include_paths": ["a/"],
        "exclude_paths": None,
        "schedule_cron": None,
        "window_timezone": "UTC",
        "window_start_local": None,
        "window_end_local": None,
        "is_active": True,
        "last_sync_status": None,
        "last_sync_started_at": None,
        "last_sync_completed_at": None,
        "created_at": 1699564800,
        "updated_at": 1699564800,
    }
    base.update(overrides)
    return base


def test_create_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync"
        assert b'"connector_uuid":"conn-1"' in req.content
        return httpx.Response(200, json=_config_json())

    body = KBSyncConfigurationCreateRequest(connector_uuid="conn-1", source_type="s3")
    result = _client(handler).kb_sync.create(ORG, body=body)
    assert result.id == CFG
    assert result.connector_uuid == "conn-1"


def test_list_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync"
        return httpx.Response(200, json=[_config_json(), _config_json(id="cfg-2")])

    result = _client(handler).kb_sync.list(ORG)
    assert [c.id for c in result] == [CFG, "cfg-2"]


def test_start_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/start"
        return httpx.Response(200, json={"started": True})

    assert _client(handler).kb_sync.start(ORG, CFG) == {"started": True}


def test_retrieve_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}"
        return httpx.Response(200, json=_config_json())

    result = _client(handler).kb_sync.retrieve(ORG, CFG)
    assert result.id == CFG


def test_update_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}"
        assert b'"is_active":false' in req.content
        return httpx.Response(200, json=_config_json(is_active=False))

    body = KBSyncConfigurationUpdateRequest(is_active=False)
    result = _client(handler).kb_sync.update(ORG, CFG, body=body)
    assert result.is_active is False


def test_delete_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}"
        return httpx.Response(200, json={"ok": True})

    assert _client(handler).kb_sync.delete(ORG, CFG) is None


def test_get_status_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/status"
        return httpx.Response(200, json={"status": "running", "progress": 50})

    result = _client(handler).kb_sync.get_status(ORG, CFG)
    assert result["status"] == "running"


def test_list_files_sends_params_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/files"
        assert req.url.params["status"] == "failed"
        assert req.url.params["limit"] == "10"
        assert req.url.params["offset"] == "5"
        return httpx.Response(
            200,
            json={
                "config_id": CFG,
                "total_files": 1,
                "files": [
                    {
                        "id": 1,
                        "external_id": "ext-1",
                        "display_path": "a/b.txt",
                        "source_type": "s3",
                        "size_bytes": 12,
                        "content_type": "text/plain",
                        "sync_status": "failed",
                        "retry_count": 2,
                        "last_attempt_at": None,
                        "last_success_at": None,
                        "last_modified": None,
                        "content_hash": None,
                        "minio_path": None,
                        "error_details": None,
                        "created_at": 1699564800,
                        "updated_at": 1699564800,
                    }
                ],
                "statistics": {"failed": 1},
            },
        )

    result = _client(handler).kb_sync.list_files(ORG, CFG, status="failed", limit=10, offset=5)
    assert result.total_files == 1
    assert result.files[0].external_id == "ext-1"


def test_list_files_omits_params_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "status" not in req.url.params
        assert "limit" not in req.url.params
        assert "offset" not in req.url.params
        return httpx.Response(
            200,
            json={"config_id": CFG, "total_files": 0, "files": [], "statistics": {}},
        )

    result = _client(handler).kb_sync.list_files(ORG, CFG)
    assert result.files == []


def test_retry_file_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/files/7/retry"
        return httpx.Response(
            200,
            json={"requested": 1, "retried": 1, "skipped": 0, "skipped_reasons": {}},
        )

    result = _client(handler).kb_sync.retry_file(ORG, CFG, "7")
    assert result.retried == 1


def test_retry_failed_files_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/failed-files/retry"
        return httpx.Response(
            200,
            json={"requested": 3, "retried": 2, "skipped": 1, "skipped_reasons": {"locked": 1}},
        )

    result = _client(handler).kb_sync.retry_failed_files(ORG, CFG)
    assert result.requested == 3
    assert result.skipped_reasons == {"locked": 1}


def test_delete_file_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/files/7"
        return httpx.Response(
            200,
            json={"requested": 1, "deleted": 1, "skipped": 0, "skipped_reasons": {}},
        )

    result = _client(handler).kb_sync.delete_file(ORG, CFG, "7")
    assert result.deleted == 1


def test_delete_selected_files_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}/files/delete"
        assert b'"file_log_ids":[1,2]' in req.content
        return httpx.Response(
            200,
            json={"requested": 2, "deleted": 2, "skipped": 0, "skipped_reasons": {}},
        )

    body = KBSyncDeleteRequest(file_log_ids=[1, 2])
    result = _client(handler).kb_sync.delete_selected_files(ORG, CFG, body=body)
    assert result.deleted == 2


async def test_async_kb_sync_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/kb-sync/{CFG}"
        return httpx.Response(200, json=_config_json())

    client = _aclient(handler)
    try:
        result = await client.kb_sync.retrieve(ORG, CFG)
        assert result.id == CFG
    finally:
        await client.aclose()
