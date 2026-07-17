from __future__ import annotations

from typing import Any

import httpx


class GaleneError(Exception):
    """Base class for every error raised by the SDK."""


class APIConnectionError(GaleneError):
    def __init__(self, message: str = "Connection error", *, request: httpx.Request | None = None):
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    def __init__(self, *, request: httpx.Request | None = None):
        super().__init__("Request timed out", request=request)


class APIStatusError(GaleneError):
    status_code: int = 0

    def __init__(self, message: str, *, response: httpx.Response, body: Any = None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.body = body
        self.request_id = response.headers.get("x-request-id")


class BadRequestError(APIStatusError):
    status_code = 400


class AuthenticationError(APIStatusError):
    status_code = 401


class PermissionDeniedError(APIStatusError):
    status_code = 403


class NotFoundError(APIStatusError):
    status_code = 404


class ConflictError(APIStatusError):
    status_code = 409


class UnprocessableEntityError(APIStatusError):
    status_code = 422


class RateLimitError(APIStatusError):
    status_code = 429


class InternalServerError(APIStatusError):
    status_code = 500


_STATUS_MAP: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def _extract_message(body: Any, response: httpx.Response) -> str:
    if isinstance(body, dict):
        for key in ("message", "detail", "error"):
            val = body.get(key)
            if isinstance(val, str):
                return val
    return f"HTTP {response.status_code}"


def raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text
    cls = _STATUS_MAP.get(response.status_code)
    if cls is None:
        cls = InternalServerError if response.status_code >= 500 else APIStatusError
    raise cls(_extract_message(body, response), response=response, body=body)
