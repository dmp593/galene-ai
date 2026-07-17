import msgspec
import pytest

from galene_ai._core.envelope import unwrap
from galene_ai.errors import GaleneError


class _Item(msgspec.Struct):
    id: str


def test_unwrap_returns_result():
    raw = b'{"success":true,"message":null,"result":{"id":"x"},"total":1}'
    item = unwrap(raw, _Item)
    assert item.id == "x"


def test_unwrap_raises_on_failure():
    raw = b'{"success":false,"message":"nope","result":null}'
    with pytest.raises(GaleneError, match="nope"):
        unwrap(raw, _Item)


def test_unwrap_returns_none_on_successful_void_result():
    # Void endpoints (deletes) return {success: true, result: null} — a success,
    # not an error. unwrap must return None here, never raise.
    raw = b'{"success":true,"message":"Conversation deleted successfully","result":null}'
    assert unwrap(raw, _Item) is None
