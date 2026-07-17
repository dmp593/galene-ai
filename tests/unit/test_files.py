import httpx
import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai.errors import GaleneError


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_upload_sends_multipart_with_purpose_and_returns_decoded_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/files"
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="purpose"\r\n\r\nuser_data' in body
        assert b'name="original_filename"\r\n\r\nd.txt' in body
        assert b'name="file"; filename="d.txt"' in body and b"abc" in body
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "attachment_id": "f9",
                    "object": "file",
                    "filename": "d.txt",
                    "size": 3,
                    "mime_type": "text/plain",
                    "created_at": 1699564800,
                    "purpose": "user_data",
                    "error_code": None,
                    "error_phase": None,
                    "warnings": [],
                },
            },
        )

    result = _client(handler).files.upload(b"abc", filename="d.txt")
    assert result.id == "f9"
    assert result.filename == "d.txt"
    assert result.purpose == "user_data"


def test_upload_defaults_purpose_and_omits_original_filename_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        body = req.content
        assert b'name="purpose"\r\n\r\nuser_data' in body
        assert b"original_filename" not in body
        assert b'name="file"; filename="upload"' in body
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {"attachment_id": "f0", "object": "file"},
            },
        )

    result = _client(handler).files.upload(b"xyz")
    assert result.id == "f0"


def test_upload_raises_galene_error_on_http_200_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"success": False, "message": "quota exceeded", "result": None},
        )

    with pytest.raises(GaleneError, match="quota exceeded"):
        _client(handler).files.upload(b"abc", filename="d.txt")


def test_list_files_hits_endpoint_with_purpose_param_and_decodes_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/files"
        assert req.url.params["purpose"] == "user_data"
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "f1",
                        "object": "file",
                        "filename": "a.txt",
                        "purpose": "user_data",
                        "bytes": 3,
                    }
                ],
                "object": "list",
            },
        )

    page = _client(handler).files.list(purpose="user_data")
    assert [f.id for f in page] == ["f1"]
    assert page.data[0].filename == "a.txt"
    assert page.data[0].bytes == 3
    assert page.has_more is False


def test_list_files_omits_purpose_param_when_not_given():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "purpose" not in req.url.params
        return httpx.Response(200, json={"data": [], "object": "list"})

    page = _client(handler).files.list()
    assert page.data == []


def test_retrieve_file_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/files/f1"
        return httpx.Response(
            200,
            json={
                "id": "f1",
                "object": "file",
                "filename": "a.txt",
                "purpose": "user_data",
                "bytes": 3,
                "created_at": 1699564800,
            },
        )

    meta = _client(handler).files.retrieve("f1")
    assert meta.filename == "a.txt"
    assert meta.bytes == 3
    assert meta.created_at == 1699564800


def test_retry_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/files/f1/retry"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "Attachment retry scheduled successfully",
                "result": {
                    "attachment_id": "f1",
                    "object": "file",
                    "filename": "a.txt",
                    "size": 3,
                    "mime_type": "text/plain",
                    "created_at": 1699564800,
                    "purpose": "user_data",
                    "error_code": None,
                    "error_phase": None,
                    "warnings": [],
                    "status": "in_progress",
                },
            },
        )

    result = _client(handler).files.retry("f1")
    assert result.id == "f1"
    assert result.filename == "a.txt"


def test_retry_raises_galene_error_on_http_200_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"success": False, "message": "quota exceeded", "result": None},
        )

    with pytest.raises(GaleneError, match="quota exceeded"):
        _client(handler).files.retry("f1")


def test_content_returns_raw_bytes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/files/f1/content"
        return httpx.Response(200, content=b"\x00\x01raw")

    assert _client(handler).files.content("f1") == b"\x00\x01raw"


def test_delete_hits_endpoint_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/v1/files/f1"
        return httpx.Response(200, json={"id": "f1", "object": "file", "deleted": True})

    assert _client(handler).files.delete("f1") is None


async def test_async_files_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/files/f9"
        return httpx.Response(
            200,
            json={
                "id": "f9",
                "object": "file",
                "filename": "z.txt",
                "purpose": "user_data",
                "bytes": 9,
                "created_at": 1699564800,
            },
        )

    client = _aclient(handler)
    try:
        result = await client.files.retrieve("f9")
        assert result.id == "f9"
        assert result.filename == "z.txt"
    finally:
        await client.aclose()
