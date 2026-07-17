import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models._generated import UpdateTicketStatusRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _detail(ticket_uuid: str = "t1", status: str = "open") -> dict:
    return {
        "ticket_uuid": ticket_uuid,
        "title": "Broken thing",
        "content": "It does not work",
        "status": status,
        "created_at": 1699564800,
        "updated_at": 1699564900,
    }


def _list_item(ticket_uuid: str = "t1") -> dict:
    return {
        "ticket_uuid": ticket_uuid,
        "title": "Broken thing",
        "status": "open",
        "created_at": 1699564800,
        "updated_at": 1699564900,
        "messages_count": 3,
    }


def test_list_hits_endpoint_and_decodes_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/admin/all"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": [_list_item("ta"), _list_item("tb")]},
        )

    tickets = _client(handler).admin.tickets.list()
    assert [t.ticket_uuid for t in tickets] == ["ta", "tb"]
    assert tickets[0].messages_count == 3


def test_retrieve_uses_path_param_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/admin/t9"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": _detail("t9")})

    ticket = _client(handler).admin.tickets.retrieve("t9")
    assert ticket.ticket_uuid == "t9"
    assert ticket.content == "It does not work"


def test_update_status_puts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/platform-tickets/admin/t1/status"
        assert b'"new_status":"resolved"' in req.content
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": _detail("t1", status="resolved")},
        )

    body = UpdateTicketStatusRequest(new_status="resolved")
    ticket = _client(handler).admin.tickets.update_status("t1", body=body)
    assert ticket.status == "resolved"


def test_delete_uses_path_param_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/platform-tickets/admin/t1"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": None})

    res = _client(handler).admin.tickets.delete("t1")
    assert res is None


def test_reply_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/platform-tickets/admin/t1/reply"
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="content"\r\n\r\nHello there' in body
        assert b'name="new_status"\r\n\r\nin_progress' in body
        assert b'name="message_uuid"\r\n\r\nm7' in body
        assert b'name="files"' in body and b"filedata" in body
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": _detail("t1", status="in_progress")},
        )

    ticket = _client(handler).admin.tickets.reply(
        "t1",
        content="Hello there",
        new_status="in_progress",
        message_uuid="m7",
        files=[b"filedata"],
    )
    assert ticket.status == "in_progress"


def test_download_attachment_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/admin/t1/attachments/a2"
        return httpx.Response(200, json={"url": "https://x/download"})

    res = _client(handler).admin.tickets.download_attachment("t1", "a2")
    assert res == {"url": "https://x/download"}


def test_export_uses_path_param_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/admin/t1/export"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"conversation": ["a", "b"]}},
        )

    res = _client(handler).admin.tickets.export("t1")
    assert res == {"conversation": ["a", "b"]}


async def test_async_tickets_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/admin/t9"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": _detail("t9")})

    client = _aclient(handler)
    try:
        ticket = await client.admin.tickets.retrieve("t9")
        assert ticket.ticket_uuid == "t9"
    finally:
        await client.aclose()
