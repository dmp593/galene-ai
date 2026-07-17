import httpx
import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai._core.errors import APIConnectionError


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_readiness_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/readiness"
        return httpx.Response(200, json={"status": "ready"})

    result = _client(handler).health.readiness()
    assert result == {"status": "ready"}


def test_liveness_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/liveness"
        return httpx.Response(200, json={"status": "alive"})

    result = _client(handler).health.liveness()
    assert result == {"status": "alive"}


def test_health_uses_short_timeout_and_allows_override():
    seen: list[dict | None] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req.extensions.get("timeout"))
        return httpx.Response(200, json={"status": "alive"})

    client = _client(handler)
    # default fast-fail timeout (5s) is applied to the probe, not the 60s client default
    client.health.liveness()
    assert seen[-1] == {"connect": 5.0, "read": 5.0, "write": 5.0, "pool": 5.0}
    # caller can override
    client.health.liveness(timeout=1.5)
    assert seen[-1] == {"connect": 1.5, "read": 1.5, "write": 1.5, "pool": 1.5}


def test_health_does_not_retry_when_backend_is_down():
    # When Galene is unreachable, a health probe should fail after ONE attempt
    # (max_retries=0) instead of retrying with backoff and hanging.
    calls = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ConnectError("connection refused", request=req)

    with pytest.raises(APIConnectionError):
        _client(handler).health.liveness()
    assert calls["n"] == 1


def test_ordinary_get_still_retries_on_connection_error():
    # Contrast: a normal idempotent GET keeps the default retry budget (2 retries
    # -> 3 attempts), proving the health carve-out is a per-call override.
    calls = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ConnectError("connection refused", request=req)

    client = _client(handler)
    with pytest.raises(APIConnectionError):
        client._client.get("/readiness", cast_to=dict)
    assert calls["n"] == 3


async def test_async_health_liveness_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/liveness"
        return httpx.Response(200, json={"status": "alive"})

    client = _aclient(handler)
    try:
        result = await client.health.liveness()
        assert result == {"status": "alive"}
    finally:
        await client.aclose()
