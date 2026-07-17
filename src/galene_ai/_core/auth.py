from __future__ import annotations

from collections.abc import Generator

import httpx
import msgspec


class ApiKeyAuth(httpx.Auth):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self._api_key}"
        yield request


class _Tokens(msgspec.Struct):
    access_token: str | None = None
    refresh_token: str | None = None


class SessionAuth(httpx.Auth):
    """Username/password login with transparent refresh-on-401.

    httpx calls auth_flow() as a generator: we may `yield` a request and inspect
    the response before yielding a follow-up (login or refresh, then retry).
    """

    requires_response_body = True

    def __init__(
        self,
        username: str,
        password: str,
        *,
        login_path: str = "/login",
        refresh_path: str = "/refresh-token",
    ) -> None:
        self._username = username
        self._password = password
        self._login_path = login_path
        self._refresh_path = refresh_path
        self._access: str | None = None
        self._refresh: str | None = None

    def _login_request(self, base: httpx.URL) -> httpx.Request:
        return httpx.Request(
            "POST",
            base.join(self._login_path),
            json={"username": self._username, "password": self._password},
        )

    def _refresh_request(self, base: httpx.URL) -> httpx.Request:
        return httpx.Request(
            "POST",
            base.join(self._refresh_path),
            json={"refresh_token": self._refresh},
        )

    def _read_tokens(self, response: httpx.Response) -> None:
        body = msgspec.json.decode(response.content)
        result = body.get("result") if isinstance(body, dict) else None
        tokens = msgspec.convert(result or {}, _Tokens)
        self._access = tokens.access_token
        self._refresh = tokens.refresh_token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        if self._access is None:
            login_resp = yield self._login_request(request.url)
            login_resp.read()
            self._read_tokens(login_resp)

        request.headers["Authorization"] = f"Bearer {self._access}"
        response = yield request

        if response.status_code == 401 and self._refresh is not None:
            refresh_resp = yield self._refresh_request(request.url)
            refresh_resp.read()
            self._read_tokens(refresh_resp)
            request.headers["Authorization"] = f"Bearer {self._access}"
            yield request
