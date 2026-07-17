from typing import Any

import msgspec

from galene_ai.errors import GaleneError

# NOTE: this module deliberately omits `from __future__ import annotations`.
# With PEP 695 generic syntax (`class WSResponse[T]`), turning annotations
# into forward-ref strings means msgspec's runtime type resolution for
# `WSResponse[type_]` tries to `eval("T | None", ...)` and fails with
# `NameError: name 'T' is not defined`, because the PEP 695 type parameter
# `T` only lives in the class's type-param scope, not in module/class
# globals available to `eval`. Verified against msgspec 0.21.1: the
# subscripted decode `msgspec.json.decode(raw, type=WSResponse[type_])`
# raises that NameError as soon as this module has the future import, and
# succeeds once it's removed. Since target Python is 3.12+, `X | Y` unions
# work natively without the future import, so dropping it costs nothing.
#
# As an extra safety margin (and per the brief's documented fallback for
# msgspec versions that reject `WSResponse[type_]` outright), `unwrap`
# below decodes into the *untyped* `WSResponse` and then converts
# `ws.result` with `msgspec.convert(..., type_)`, rather than relying on
# the subscripted-generic decode at all.


class WSResponse[T](msgspec.Struct):
    success: bool
    message: str | None = None
    result: T | None = None
    total: int | None = None


def unwrap[T](raw: bytes, type_: type[T]) -> T | None:
    ws = msgspec.json.decode(raw, type=WSResponse[Any])
    if not ws.success:
        raise GaleneError(ws.message or "Galene request failed")
    if ws.result is None:
        # A successful response with a null result is valid for void endpoints
        # (e.g. deletes that return WSResponse[NoneType] = {success, message, result: null}).
        # Return None rather than raising — the operation succeeded.
        return None
    return msgspec.convert(ws.result, type_)
