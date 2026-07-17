from __future__ import annotations

from typing import Any, ClassVar, Protocol

import httpx

from galene_ai._config import ClientConfig
from galene_ai._core.auth import ApiKeyAuth
from galene_ai._core.base_client import AsyncAPIClient, SyncAPIClient


class _NamespaceClass(Protocol):
    """Shape required of resource classes registered in `_NAMESPACES`."""

    namespace: ClassVar[str]

    def __init__(self, client: Any) -> None: ...


class Galene:
    _NAMESPACES: ClassVar[list[type[_NamespaceClass]]] = []
    """Resource classes; appended by each resource module."""
    _ADMIN_NAMESPACES: ClassVar[list[type[_NamespaceClass]]] = []
    """Admin sub-resource classes."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        auth: httpx.Auth | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        config = ClientConfig.resolve(
            api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries
        )
        resolved_auth = auth or ApiKeyAuth(config.api_key or "")
        self._client = SyncAPIClient(config, resolved_auth, http_client=http_client)
        self._attach_namespaces()

    def _attach_namespaces(self) -> None:
        for ns_cls in self._NAMESPACES:
            setattr(self, ns_cls.namespace, ns_cls(self._client))
        if self._ADMIN_NAMESPACES:
            self.admin = _Admin(self._client, self._ADMIN_NAMESPACES)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Galene:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class _Admin:
    def __init__(self, client: Any, namespaces: list[type[_NamespaceClass]]) -> None:
        for ns_cls in namespaces:
            setattr(self, ns_cls.namespace, ns_cls(client))


class AsyncGalene:
    _NAMESPACES: ClassVar[list[type[_NamespaceClass]]] = []
    _ADMIN_NAMESPACES: ClassVar[list[type[_NamespaceClass]]] = []

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        auth: httpx.Auth | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        config = ClientConfig.resolve(
            api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries
        )
        resolved_auth = auth or ApiKeyAuth(config.api_key or "")
        self._client = AsyncAPIClient(config, resolved_auth, http_client=http_client)
        self._attach_namespaces()

    def _attach_namespaces(self) -> None:
        for ns_cls in self._NAMESPACES:
            setattr(self, ns_cls.namespace, ns_cls(self._client))
        if self._ADMIN_NAMESPACES:
            self.admin = _Admin(self._client, self._ADMIN_NAMESPACES)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncGalene:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
