import httpx
import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai.errors import GaleneError
from galene_ai.models._generated import MarkSeenRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_unseen_hits_endpoint_with_audience_param_and_unwraps_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/release-notes/unseen"
        assert req.url.params["audience"] == "user"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": {
                    "has_unseen": True,
                    "latest_version": "1.2.0",
                    "releases": [{"version": "1.2.0", "date": "2023-11-10", "content": "x"}],
                },
            },
        )

    result = _client(handler).release_notes.unseen(audience="user")
    assert result["has_unseen"] is True
    assert result["latest_version"] == "1.2.0"


def test_unseen_omits_audience_param_when_not_given():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "audience" not in req.url.params
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"has_unseen": False}},
        )

    result = _client(handler).release_notes.unseen()
    assert result["has_unseen"] is False


def test_unseen_raises_galene_error_on_http_200_success_false():
    def handler(req: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"success": False, "message": "boom", "result": None},
        )

    with pytest.raises(GaleneError, match="boom"):
        _client(handler).release_notes.unseen()


def test_seen_posts_version_body_and_returns_none():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/release-notes/seen"
        assert b'"version":"1.2.0"' in req.content
        return httpx.Response(
            200,
            json={"success": True, "message": "seen", "result": None},
        )

    result = _client(handler).release_notes.seen(MarkSeenRequest(version="1.2.0"))
    assert result is None


async def test_async_release_notes_unseen_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/release-notes/unseen"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": {"has_unseen": True}},
        )

    client = _aclient(handler)
    try:
        result = await client.release_notes.unseen()
        assert result["has_unseen"] is True
    finally:
        await client.aclose()
