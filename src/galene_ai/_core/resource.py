from __future__ import annotations

from collections.abc import Callable
from typing import Any


def operation[F: Callable[..., Any]](operation_id: str) -> Callable[[F], F]:
    def deco(func: F) -> F:
        func.__galene_operation__ = operation_id  # type: ignore[attr-defined]
        return func

    return deco


class SyncResource:
    def __init__(self, client: Any) -> None:
        self._client = client


class AsyncResource:
    def __init__(self, client: Any) -> None:
        self._client = client
