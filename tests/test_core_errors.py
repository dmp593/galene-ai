import httpx
import pytest

from galene_ai.errors import (
    APIStatusError,
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    raise_for_status,
)


def _resp(status: int, json_body=None) -> httpx.Response:
    return httpx.Response(status, json=json_body or {}, request=httpx.Request("GET", "https://x/y"))


def test_success_does_not_raise():
    raise_for_status(_resp(200))


@pytest.mark.parametrize(
    "code,exc",
    [
        (401, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (503, InternalServerError),
    ],
)
def test_status_maps_to_exception(code, exc):
    with pytest.raises(exc) as ei:
        raise_for_status(_resp(code, {"detail": "boom"}))
    assert ei.value.status_code == code
    assert isinstance(ei.value, APIStatusError)
