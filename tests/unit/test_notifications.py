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


def test_mark_delivered_hits_endpoint_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/notification/n1/delivered"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": None},
        )

    result = _client(handler).notifications.mark_delivered("n1")
    assert result is None


def test_summary_uses_mode_path_param_and_unwraps_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/notifications/personal/summary"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"unread": 3, "total": 5}},
        )

    result = _client(handler).notifications.summary("personal")
    assert result == {"unread": 3, "total": 5}


def test_mark_read_posts_id_list_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/notifications/mark-read"
        import json

        assert json.loads(req.content) == ["a", "b"]
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": None},
        )

    result = _client(handler).notifications.mark_read(["a", "b"])
    assert result is None


def test_mark_read_raises_galene_error_on_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"success": False, "message": "nope", "result": None},
        )

    with pytest.raises(GaleneError, match="nope"):
        _client(handler).notifications.mark_read(["a"])


def test_platform_summary_hits_endpoint_and_unwraps_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/platform-tickets/notifications/summary"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"unread": 1}},
        )

    result = _client(handler).notifications.platform_summary()
    assert result == {"unread": 1}


def test_platform_mark_read_posts_id_list_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/platform-tickets/notifications/mark-read"
        import json

        assert json.loads(req.content) == ["t1"]
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": None},
        )

    result = _client(handler).notifications.platform_mark_read(["t1"])
    assert result is None


async def test_async_notifications_summary_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/notifications/team/summary"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"unread": 7}},
        )

    client = _aclient(handler)
    try:
        result = await client.notifications.summary("team")
        assert result == {"unread": 7}
    finally:
        await client.aclose()
