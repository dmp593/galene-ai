from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx
import msgspec
from httpx import USE_CLIENT_DEFAULT

from galene_ai._config import ClientConfig
from galene_ai._core.envelope import unwrap
from galene_ai._core.errors import APIConnectionError, APITimeoutError, raise_for_status
from galene_ai._core.retry import RetryPolicy
from galene_ai._core.streaming import AsyncStream, Stream


def _encode_json(json_body: Any) -> bytes | None:
    if json_body is None:
        return None
    return msgspec.json.encode(json_body)


def _decode(response: httpx.Response, cast_to: Any, envelope: bool) -> Any:
    if cast_to is None:
        return None
    if cast_to is bytes:
        return response.content
    if envelope:
        return unwrap(response.content, cast_to)
    return msgspec.json.decode(response.content, type=cast_to)


def _parse_retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


class SyncAPIClient:
    def __init__(
        self,
        config: ClientConfig,
        auth: httpx.Auth,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._retry = RetryPolicy(config.max_retries)
        self._http = http_client or httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            auth=auth,
            headers=config.default_headers,
        )

    # -- public helpers -------------------------------------------------
    def get(self, path: str, **kw: Any) -> Any:
        return self.request("GET", path, **kw)

    def post(self, path: str, **kw: Any) -> Any:
        return self.request("POST", path, **kw)

    def put(self, path: str, **kw: Any) -> Any:
        return self.request("PUT", path, **kw)

    def patch(self, path: str, **kw: Any) -> Any:
        return self.request("PATCH", path, **kw)

    def delete(self, path: str, **kw: Any) -> Any:
        return self.request("DELETE", path, **kw)

    # -- core -----------------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        files: Any = None,
        data: Any = None,
        cast_to: Any = None,
        envelope: bool = False,
        stream_type: Any = None,
        timeout: Any = USE_CLIENT_DEFAULT,
        max_retries: int | None = None,
    ) -> Any:
        content = _encode_json(json_body) if files is None else None
        headers = {"Content-Type": "application/json"} if content is not None else None
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        # Per-call retry budget (e.g. health probes pass max_retries=0 to fail fast).
        retry = self._retry if max_retries is None else RetryPolicy(max_retries)

        if stream_type is not None:
            req = self._http.build_request(
                method, path, params=clean_params, content=content, headers=headers, timeout=timeout
            )
            response = self._http.send(req, stream=True)
            if not response.is_success:
                response.read()
                raise_for_status(response)
            return Stream(response, stream_type)

        attempt = 0
        while True:
            try:
                response = self._http.request(
                    method,
                    path,
                    params=clean_params,
                    content=content,
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                )
            except httpx.TimeoutException as exc:
                if retry.should_retry(attempt, status=None, method=method, is_timeout=True):
                    time.sleep(retry.backoff_seconds(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(request=exc.request) from exc
            except httpx.HTTPError as exc:
                if retry.should_retry(attempt, status=None, method=method, is_timeout=False):
                    time.sleep(retry.backoff_seconds(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc)) from exc

            if response.is_success:
                return _decode(response, cast_to, envelope)

            if retry.should_retry(
                attempt, status=response.status_code, method=method, is_timeout=False
            ):
                retry_after = _parse_retry_after(response)
                time.sleep(retry.backoff_seconds(attempt, retry_after))
                attempt += 1
                continue

            raise_for_status(response)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> SyncAPIClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class AsyncAPIClient:
    def __init__(
        self,
        config: ClientConfig,
        auth: httpx.Auth,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._retry = RetryPolicy(config.max_retries)
        self._http = http_client or httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            auth=auth,
            headers=config.default_headers,
        )

    # -- public helpers -------------------------------------------------
    async def get(self, path: str, **kw: Any) -> Any:
        return await self.request("GET", path, **kw)

    async def post(self, path: str, **kw: Any) -> Any:
        return await self.request("POST", path, **kw)

    async def put(self, path: str, **kw: Any) -> Any:
        return await self.request("PUT", path, **kw)

    async def patch(self, path: str, **kw: Any) -> Any:
        return await self.request("PATCH", path, **kw)

    async def delete(self, path: str, **kw: Any) -> Any:
        return await self.request("DELETE", path, **kw)

    # -- core -----------------------------------------------------------
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        files: Any = None,
        data: Any = None,
        cast_to: Any = None,
        envelope: bool = False,
        stream_type: Any = None,
        timeout: Any = USE_CLIENT_DEFAULT,
        max_retries: int | None = None,
    ) -> Any:
        content = _encode_json(json_body) if files is None else None
        headers = {"Content-Type": "application/json"} if content is not None else None
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        # Per-call retry budget (e.g. health probes pass max_retries=0 to fail fast).
        retry = self._retry if max_retries is None else RetryPolicy(max_retries)

        if stream_type is not None:
            req = self._http.build_request(
                method, path, params=clean_params, content=content, headers=headers, timeout=timeout
            )
            response = await self._http.send(req, stream=True)
            if not response.is_success:
                await response.aread()
                raise_for_status(response)
            return AsyncStream(response, stream_type)

        attempt = 0
        while True:
            try:
                response = await self._http.request(
                    method,
                    path,
                    params=clean_params,
                    content=content,
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                )
            except httpx.TimeoutException as exc:
                if retry.should_retry(attempt, status=None, method=method, is_timeout=True):
                    await asyncio.sleep(retry.backoff_seconds(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(request=exc.request) from exc
            except httpx.HTTPError as exc:
                if retry.should_retry(attempt, status=None, method=method, is_timeout=False):
                    await asyncio.sleep(retry.backoff_seconds(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc)) from exc

            if response.is_success:
                return _decode(response, cast_to, envelope)

            if retry.should_retry(
                attempt, status=response.status_code, method=method, is_timeout=False
            ):
                retry_after = _parse_retry_after(response)
                await asyncio.sleep(retry.backoff_seconds(attempt, retry_after))
                attempt += 1
                continue

            raise_for_status(response)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncAPIClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
