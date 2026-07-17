"""`admin.deployment` resource: trigger frontend deployment workflows."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation


class Deployment(SyncResource):
    """Trigger frontend deployment workflows for organizations (admin)."""

    namespace: ClassVar[str] = "deployment"

    @operation(
        "deploy_organization_updates_admin_organizations__organization_uuid__deploy_updates_post"
    )
    def deploy_updates(self, organization_uuid: str) -> dict[str, Any]:
        """Deploy Frontend Updates for Organization."""
        return cast(
            dict[str, Any],
            self._client.post(
                f"/admin/organizations/{organization_uuid}/deploy-updates",
                cast_to=dict,  # spec: untyped response
            ),
        )


class AsyncDeployment(AsyncResource):
    """Async counterpart of `Deployment`."""

    namespace: ClassVar[str] = "deployment"

    @operation(
        "deploy_organization_updates_admin_organizations__organization_uuid__deploy_updates_post"
    )
    async def deploy_updates(self, organization_uuid: str) -> dict[str, Any]:
        """Deploy Frontend Updates for Organization."""
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/deploy-updates",
                cast_to=dict,  # spec: untyped response
            ),
        )


Galene._ADMIN_NAMESPACES.append(Deployment)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncDeployment)
