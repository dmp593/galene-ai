import httpx

from galene_ai._core.auth import ApiKeyAuth


def test_api_key_auth_sets_bearer_header():
    auth = ApiKeyAuth("sk-123")
    request = httpx.Request("GET", "https://x/y")
    flow = auth.auth_flow(request)
    req = next(flow)
    assert req.headers["Authorization"] == "Bearer sk-123"


def test_session_auth_refreshes_on_401():
    # Transport: first login → tokens; a protected GET returns 401 once, then 200 after refresh.
    state = {"access": "a1", "refreshed": False}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/login":
            return httpx.Response(
                200,
                json={
                    "success": True,
                    "result": {"user_id": "u", "access_token": "a1", "refresh_token": "r1"},
                },
            )
        if request.url.path == "/refresh-token":
            state["refreshed"] = True
            return httpx.Response(
                200,
                json={
                    "success": True,
                    "result": {"user_id": "u", "access_token": "a2", "refresh_token": "r2"},
                },
            )
        # protected endpoint
        token = request.headers.get("Authorization")
        if token == "Bearer a1" and not state["refreshed"]:
            return httpx.Response(401)
        return httpx.Response(200, json={"ok": True})

    from galene_ai._core.auth import SessionAuth

    auth = SessionAuth("user", "pw")
    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x", auth=auth)
    resp = client.get("/protected")
    assert resp.status_code == 200
    assert state["refreshed"] is True
