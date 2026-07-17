import httpx
import msgspec
import pytest

from galene_ai import errors
from galene_ai._config import ClientConfig
from galene_ai._core.auth import ApiKeyAuth
from galene_ai._core.base_client import SyncAPIClient


class _Item(msgspec.Struct):
    id: str


def _client(handler) -> SyncAPIClient:
    cfg = ClientConfig.resolve(api_key="k", base_url="https://x")
    http = httpx.Client(
        transport=httpx.MockTransport(handler), base_url=cfg.base_url, auth=ApiKeyAuth("k")
    )
    return SyncAPIClient(cfg, ApiKeyAuth("k"), http_client=http)


def test_get_decodes_cast_to():
    def handler(req):
        assert req.headers["Authorization"] == "Bearer k"
        assert req.url.path == "/v1/thing"
        return httpx.Response(200, json={"id": "abc"})

    item = _client(handler).get("/v1/thing", cast_to=_Item)
    assert item.id == "abc"


def test_envelope_unwrap():
    def handler(req):
        return httpx.Response(200, json={"success": True, "result": {"id": "z"}})

    item = _client(handler).get("/thing", cast_to=_Item, envelope=True)
    assert item.id == "z"


def test_retries_then_succeeds():
    calls = {"n": 0}

    def handler(req):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"id": "ok"})

    item = _client(handler).get("/thing", cast_to=_Item)
    assert item.id == "ok"
    assert calls["n"] == 2


def test_stream_error_raises_typed_error_not_response_not_read():
    # Simulate a *real* streaming response whose body has not been eagerly
    # buffered (unlike `httpx.Response(status, json=...)`, which reads the
    # body immediately). `stream=httpx.ByteStream(...)` bypasses that eager
    # read, exactly like a genuine network transport would.
    def handler(req):
        return httpx.Response(
            404,
            stream=httpx.ByteStream(b'{"detail": "nope"}'),
            headers={"content-type": "application/json"},
        )

    with pytest.raises(errors.NotFoundError):
        _client(handler).get("/v1/thing", stream_type=_Item)
