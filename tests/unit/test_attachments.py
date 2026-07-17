import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_get_chunk_in_conversation_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/conversation/c1/attachment/chunk/ch1"
        return httpx.Response(200, json={"chunk_id": "ch1", "text": "hello"})

    out = _client(handler).attachments.get_chunk_in_conversation("c1", "ch1")
    assert out["chunk_id"] == "ch1"
    assert out["text"] == "hello"


def test_get_chunk_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/chunk/ch1"
        return httpx.Response(200, json={"chunk_id": "ch1", "text": "body"})

    out = _client(handler).attachments.get_chunk("ch1")
    assert out["chunk_id"] == "ch1"


def test_attach_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/attach/conversation/c1"
        return httpx.Response(200, json={"attached": True})

    out = _client(handler).attachments.attach("f1", "c1")
    assert out["attached"] is True


def test_detach_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/detach/conversation/c1"
        return httpx.Response(200, json={"detached": True})

    out = _client(handler).attachments.detach("f1", "c1")
    assert out["detached"] is True


def test_detach_delete_uses_delete_method():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/attachment/f1/detach/conversation/c1"
        return httpx.Response(200, json={"detached": True})

    out = _client(handler).attachments.detach_delete("f1", "c1")
    assert out["detached"] is True


def test_enable_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/status/enable"
        return httpx.Response(200, json={"status": "enabled"})

    out = _client(handler).attachments.enable("f1")
    assert out["status"] == "enabled"


def test_disable_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/status/disable"
        return httpx.Response(200, json={"status": "disabled"})

    out = _client(handler).attachments.disable("f1")
    assert out["status"] == "disabled"


def test_presigned_url_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/presignedurl"
        return httpx.Response(200, json={"url": "https://s3/x"})

    out = _client(handler).attachments.presigned_url("f1")
    assert out["url"] == "https://s3/x"


def test_transcription_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f1/transcription"
        return httpx.Response(200, json={"transcript": "spoken words"})

    out = _client(handler).attachments.transcription("f1")
    assert out["transcript"] == "spoken words"


def test_retry_uses_post_method_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/attachment/f1/retry"
        return httpx.Response(200, json={"status": "scheduled"})

    out = _client(handler).attachments.retry("f1")
    assert out["status"] == "scheduled"


async def test_async_attachments_enable_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/attachment/f9/status/enable"
        return httpx.Response(200, json={"status": "enabled"})

    client = _aclient(handler)
    try:
        out = await client.attachments.enable("f9")
        assert out["status"] == "enabled"
    finally:
        await client.aclose()
