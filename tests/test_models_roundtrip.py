import msgspec

from galene_ai.models import LoginRequest


def test_login_request_roundtrip():
    obj = LoginRequest(username="a@b.com", password="pw")
    raw = msgspec.json.encode(obj)
    back = msgspec.json.decode(raw, type=LoginRequest)
    assert back.username == "a@b.com"


def test_decoding_ignores_unknown_fields():
    # msgspec ignores unknown fields by default → forward-compatible
    raw = b'{"username":"a@b.com","password":"pw","future_field":123}'
    back = msgspec.json.decode(raw, type=LoginRequest)
    assert back.password == "pw"
