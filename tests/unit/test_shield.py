import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import ShieldUpsert


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _shield(uuid="s1"):
    return {
        "uuid": uuid,
        "config": {"S1": True},
        "is_active": True,
        "created_at": 1699564800,
        "updated_at": None,
    }


def test_list_shields_hits_endpoint_and_decodes_items():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/shield/"
        return httpx.Response(
            200,
            json={"success": True, "message": "ok", "result": [_shield("s1"), _shield("s2")]},
        )

    shields = _client(handler).shield.list()
    assert [s.uuid for s in shields] == ["s1", "s2"]
    assert shields[0].is_active is True


def test_create_shield_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/shield"
        body = req.content
        assert b'"S1"' in body
        return httpx.Response(
            200, json={"success": True, "message": "ok", "result": _shield("new")}
        )

    result = _client(handler).shield.create(ShieldUpsert(config={"S1": True}, is_active=True))
    assert result.uuid == "new"
    assert result.config == {"S1": True}


def test_retrieve_shield_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/shield/abc"
        return httpx.Response(
            200, json={"success": True, "message": "ok", "result": _shield("abc")}
        )

    result = _client(handler).shield.retrieve("abc")
    assert result.uuid == "abc"


def test_update_shield_sends_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == "/shield/abc"
        assert b'"is_active"' in req.content
        return httpx.Response(
            200, json={"success": True, "message": "ok", "result": _shield("abc")}
        )

    result = _client(handler).shield.update("abc", ShieldUpsert(is_active=False))
    assert result.uuid == "abc"


def test_delete_shield_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/shield/abc"
        return httpx.Response(
            200, json={"success": True, "message": "ok", "result": {"deleted": True}}
        )

    result = _client(handler).shield.delete("abc")
    assert result == {"deleted": True}


def test_attach_organization_hits_endpoint_and_returns_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/shield/s1/attach/organization/o1"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": True})

    result = _client(handler).shield.attach_organization("s1", "o1")
    assert result is True


def test_attach_agent_hits_endpoint_and_returns_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/shield/s1/attach/agent/a1"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": True})

    result = _client(handler).shield.attach_agent("s1", "a1")
    assert result is True


def test_retrieve_for_organization_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/shield/organization/o1"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": _shield("s1")})

    result = _client(handler).shield.retrieve_for_organization("o1")
    assert result.uuid == "s1"


def test_retrieve_for_agent_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/shield/agent/a1"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": _shield("s1")})

    result = _client(handler).shield.retrieve_for_agent("a1")
    assert result.uuid == "s1"


async def test_async_shield_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/shield/s9"
        return httpx.Response(200, json={"success": True, "message": "ok", "result": _shield("s9")})

    client = _aclient(handler)
    try:
        result = await client.shield.retrieve("s9")
        assert result.uuid == "s9"
    finally:
        await client.aclose()
