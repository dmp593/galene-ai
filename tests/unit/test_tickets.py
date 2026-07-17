import httpx
import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai.errors import GaleneError
from galene_ai.models._generated import UpdateTicketRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _env(result):
    return {"success": True, "message": "ok", "result": result}


# -- admin / Zammad -----------------------------------------------------
def test_list_organization_unwraps_envelope_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/support-tickets/"
        return httpx.Response(200, json=_env({"tickets": [], "total": 0}))

    out = _client(handler).tickets.list_organization()
    assert out == {"tickets": [], "total": 0}


def test_create_zammad_ticket_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/support-tickets/"
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="title"\r\n\r\nBroken' in body
        assert b'name="content"\r\n\r\nDetails' in body
        assert b'name="files"; filename="log.txt"' in body and b"LOGDATA" in body
        return httpx.Response(
            200,
            json=_env(
                {
                    "zammad_ticket_id": 42,
                    "title": "Broken",
                    "status": "open",
                    "ticket_uuid": "u1",
                    "created_at": 1699564800,
                    "category": "bug",
                    "severity": "high",
                }
            ),
        )

    out = _client(handler).tickets.create_zammad_ticket(
        title="Broken",
        content="Details",
        category="bug",
        severity="high",
        files=[("log.txt", b"LOGDATA")],
    )
    assert out.zammad_ticket_id == 42
    assert out.ticket_uuid == "u1"


def test_retrieve_admin_hits_path_and_unwraps():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/support-tickets/u1"
        return httpx.Response(200, json=_env({"ticket_uuid": "u1", "status": "open"}))

    out = _client(handler).tickets.retrieve_admin("u1")
    assert out == {"ticket_uuid": "u1", "status": "open"}


def test_reply_admin_sends_content_and_unwraps():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/support-tickets/u1/answer"
        assert b'name="content"\r\n\r\nThanks' in req.content
        return httpx.Response(200, json=_env({"article_id": 7}))

    out = _client(handler).tickets.reply_admin("u1", content="Thanks")
    assert out == {"article_id": 7}


def test_escalate_hits_path_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/support-tickets/escalate/u1"
        return httpx.Response(
            200,
            json=_env(
                {
                    "zammad_ticket_id": 9,
                    "title": "Esc",
                    "status": "in_progress",
                    "ticket_uuid": "u1",
                    "created_at": 1699564800,
                }
            ),
        )

    out = _client(handler).tickets.escalate("u1")
    assert out.zammad_ticket_id == 9
    assert out.status == "in_progress"


def test_download_admin_attachment_hits_path():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/support-tickets/t1/attachments/a1"
        return httpx.Response(200, json={"url": "https://d/a1"})

    out = _client(handler).tickets.download_admin_attachment("t1", "a1")
    assert out == {"url": "https://d/a1"}


def test_download_zammad_attachment_passes_query_params():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/support-tickets/t1/articles/5/zammad-attachments/z9"
        assert req.url.params["filename"] == "f.pdf"
        assert req.url.params["mime_type"] == "application/pdf"
        return httpx.Response(200, json={"cached": True})

    out = _client(handler).tickets.download_zammad_attachment(
        "t1", "5", "z9", filename="f.pdf", mime_type="application/pdf"
    )
    assert out == {"cached": True}


def test_download_zammad_attachment_omits_query_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "filename" not in req.url.params
        assert "mime_type" not in req.url.params
        return httpx.Response(200, json={"cached": False})

    out = _client(handler).tickets.download_zammad_attachment("t1", "5", "z9")
    assert out == {"cached": False}


# -- platform (user) tickets -------------------------------------------
def test_list_user_tickets_unwraps_envelope_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/"
        return httpx.Response(
            200,
            json=_env(
                [
                    {
                        "ticket_uuid": "u1",
                        "title": "Help",
                        "status": "open",
                        "created_at": 1,
                        "updated_at": 2,
                        "messages_count": 3,
                    }
                ]
            ),
        )

    out = _client(handler).tickets.list()
    assert [t.ticket_uuid for t in out] == ["u1"]
    assert out[0].messages_count == 3


def test_create_user_ticket_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/platform-tickets/"
        body = req.content
        assert b'name="title"\r\n\r\nHi' in body
        assert b'name="content"\r\n\r\nBody' in body
        assert b'name="conversation_id"\r\n\r\nc1' in body
        assert b'name="files"; filename="a.png"' in body
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u2",
                    "title": "Hi",
                    "content": "Body",
                    "status": "open",
                    "created_at": 5,
                }
            ),
        )

    out = _client(handler).tickets.create(
        title="Hi",
        content="Body",
        conversation_id="c1",
        files=[("a.png", b"PNG")],
    )
    assert out.ticket_uuid == "u2"
    assert out.status == "open"


def test_create_user_ticket_omits_optional_form_fields():
    def handler(req: httpx.Request) -> httpx.Response:
        body = req.content
        assert b"category" not in body
        assert b"conversation_id" not in body
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u3",
                    "title": "T",
                    "content": "C",
                    "status": "open",
                    "created_at": 5,
                }
            ),
        )

    out = _client(handler).tickets.create(title="T", content="C")
    assert out.ticket_uuid == "u3"


def test_retrieve_user_ticket_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/u1"
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u1",
                    "title": "T",
                    "content": "C",
                    "status": "open",
                    "created_at": 1,
                    "updated_at": 2,
                }
            ),
        )

    out = _client(handler).tickets.retrieve("u1")
    assert out.ticket_uuid == "u1"
    assert out.title == "T"


def test_update_user_ticket_sends_json_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/platform-tickets/u1"
        assert b'"title":"New"' in req.content
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u1",
                    "title": "New",
                    "content": "C",
                    "status": "open",
                    "created_at": 1,
                    "updated_at": 3,
                }
            ),
        )

    out = _client(handler).tickets.update("u1", body=UpdateTicketRequest(title="New"))
    assert out.title == "New"
    assert out.updated_at == 3


def test_delete_user_ticket_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/platform-tickets/u1"
        return httpx.Response(200, json=_env(None))

    out = _client(handler).tickets.delete("u1")
    assert out is None


def test_reply_user_ticket_sends_content_and_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/platform-tickets/u1/reply"
        assert b'name="content"\r\n\r\nReplying' in req.content
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u1",
                    "title": "T",
                    "content": "C",
                    "status": "in_progress",
                    "created_at": 1,
                    "updated_at": 4,
                }
            ),
        )

    out = _client(handler).tickets.reply("u1", content="Replying")
    assert out.status == "in_progress"


def test_download_user_ticket_attachment_hits_path():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/u1/attachments/a1"
        return httpx.Response(200, json={"url": "https://d/a1"})

    out = _client(handler).tickets.download_attachment("u1", "a1")
    assert out == {"url": "https://d/a1"}


def test_create_raises_galene_error_on_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"success": False, "message": "denied", "result": None})

    with pytest.raises(GaleneError, match="denied"):
        _client(handler).tickets.create(title="T", content="C")


async def test_async_tickets_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/u9"
        return httpx.Response(
            200,
            json=_env(
                {
                    "ticket_uuid": "u9",
                    "title": "T",
                    "content": "C",
                    "status": "open",
                    "created_at": 1,
                    "updated_at": 2,
                }
            ),
        )

    client = _aclient(handler)
    try:
        out = await client.tickets.retrieve("u9")
        assert out.ticket_uuid == "u9"
    finally:
        await client.aclose()
