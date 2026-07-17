"""Admin ``frontend`` resource namespace."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import FrontendConfigResponse


class Frontend(SyncResource):
    """Frontend configuration for an organization."""

    namespace: ClassVar[str] = "frontend"

    @operation("get_frontend_configuration_frontend_config__org_uuid__get")
    def get_config(self, org_uuid: str) -> FrontendConfigResponse:
        """Get frontend configuration for an organization."""
        return cast(
            FrontendConfigResponse,
            self._client.get(f"/frontend/config/{org_uuid}", cast_to=FrontendConfigResponse),
        )


class AsyncFrontend(AsyncResource):
    """Async counterpart of :class:`Frontend`."""

    namespace: ClassVar[str] = "frontend"

    @operation("get_frontend_configuration_frontend_config__org_uuid__get")
    async def get_config(self, org_uuid: str) -> FrontendConfigResponse:
        """Get frontend configuration for an organization."""
        return cast(
            FrontendConfigResponse,
            await self._client.get(f"/frontend/config/{org_uuid}", cast_to=FrontendConfigResponse),
        )


Galene._ADMIN_NAMESPACES.append(Frontend)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncFrontend)
