import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import ConversationUpdate


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _envelope(result):
    return {"success": True, "message": "ok", "result": result}


def test_list_conversations_returns_decoded_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversations"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "conversation_id": "c1",
                        "created_at": 1699564800,
                        "updated_at": 1699564900,
                        "title": "First chat",
                    }
                ]
            ),
        )

    items = _client(handler).conversations.list()
    assert [c.conversation_id for c in items] == ["c1"]
    assert items[0].title == "First chat"


def test_init_conversation_returns_new_id():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/init"
        return httpx.Response(200, json=_envelope({"conversation_id": "new-1"}))

    result = _client(handler).conversations.init()
    assert result.conversation_id == "new-1"


def test_retrieve_conversation_details():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1"
        return httpx.Response(
            200,
            json=_envelope(
                {
                    "conversation_id": "c1",
                    "updated_at": 1699564900,
                    "created_at": 1699564800,
                    "title": "Details",
                }
            ),
        )

    conv = _client(handler).conversations.retrieve("c1")
    assert conv.conversation_id == "c1"
    assert conv.title == "Details"


def test_update_conversation_sends_body_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PATCH"
        assert req.url.path == "/conversation/c1"
        assert b'"title":"Renamed"' in req.content
        return httpx.Response(200, json=_envelope({"updated": True}))

    out = _client(handler).conversations.update("c1", body=ConversationUpdate(title="Renamed"))
    assert out == {"updated": True}


def test_delete_conversation_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/conversation/c1"
        return httpx.Response(200, json=_envelope(None))

    out = _client(handler).conversations.delete("c1")
    assert out is None


def test_attachments_returns_decoded_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1/attachments"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "file_id": "f1",
                        "file_name": "a.txt",
                        "mime_type": "text/plain",
                        "is_active": True,
                    }
                ]
            ),
        )

    atts = _client(handler).conversations.attachments("c1")
    assert atts[0].file_id == "f1"
    assert atts[0].file_name == "a.txt"


def test_add_references_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1/message/0/add_references"
        return httpx.Response(200, json=_envelope({"added": 2}))

    out = _client(handler).conversations.add_references("c1", "0")
    assert out == {"added": 2}


def test_delete_message_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/conversation/c1/message/m1"
        return httpx.Response(200, json=_envelope(None))

    out = _client(handler).conversations.delete_message("c1", "m1")
    assert out is None


def test_sanitize_message_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1/message/m1/sanitize"
        return httpx.Response(200, json=_envelope({"content": "clean"}))

    out = _client(handler).conversations.sanitize_message("c1", "m1")
    assert out == {"content": "clean"}


def test_sql_results_returns_decoded_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1/sql-results/r1"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "id": 1,
                        "kind": "sql",
                        "csv_ref": "ref-1",
                        "code": "SELECT 1",
                        "explanation": "one",
                    }
                ]
            ),
        )

    results = _client(handler).conversations.sql_results("c1", "r1")
    assert results[0].id == 1
    assert results[0].code == "SELECT 1"


async def test_async_conversations_init_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/init"
        return httpx.Response(200, json=_envelope({"conversation_id": "async-1"}))

    client = _aclient(handler)
    try:
        result = await client.conversations.init()
        assert result.conversation_id == "async-1"
    finally:
        await client.aclose()
