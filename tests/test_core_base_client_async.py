import httpx
import msgspec
import pytest

from galene_ai import errors
from galene_ai._config import ClientConfig
from galene_ai._core.auth import ApiKeyAuth
from galene_ai._core.base_client import AsyncAPIClient


class _Item(msgspec.Struct):
    id: str


async def test_async_get_decodes():
    def handler(req):
        return httpx.Response(200, json={"id": "async-ok"})

    cfg = ClientConfig.resolve(api_key="k", base_url="https://x")
    http = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url=cfg.base_url, auth=ApiKeyAuth("k")
    )
    client = AsyncAPIClient(cfg, ApiKeyAuth("k"), http_client=http)
    item = await client.get("/thing", cast_to=_Item)
    assert item.id == "async-ok"
    await client.aclose()


async def test_async_stream_error_raises_typed_error_not_response_not_read():
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

    cfg = ClientConfig.resolve(api_key="k", base_url="https://x")
    http = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url=cfg.base_url, auth=ApiKeyAuth("k")
    )
    client = AsyncAPIClient(cfg, ApiKeyAuth("k"), http_client=http)
    with pytest.raises(errors.NotFoundError):
        await client.get("/v1/thing", stream_type=_Item)
    await client.aclose()
