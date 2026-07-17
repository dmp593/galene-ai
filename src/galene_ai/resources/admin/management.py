"""`admin.management` resource: superadmin organization management."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    OrganizationCreateRequest,
    OrganizationDeletedResponse,
    OrganizationResponse,
    OrganizationUpdateRequest,
)


class Management(SyncResource):
    """Create, list, retrieve, update, and delete organizations (superadmin)."""

    namespace: ClassVar[str] = "management"

    @operation("create_organization_admin_organizations_post")
    def create(self, body: OrganizationCreateRequest) -> OrganizationResponse:
        """Create a new Organization (Superadmin)."""
        return cast(
            OrganizationResponse,
            self._client.post(
                "/admin/organizations",
                json_body=body,
                cast_to=OrganizationResponse,
            ),
        )

    @operation("list_organizations_admin_organizations_get")
    def list(
        self, *, skip: int | None = None, limit: int | None = None
    ) -> list[OrganizationResponse]:
        """List all Organizations."""
        return cast(
            list[OrganizationResponse],
            self._client.get(
                "/admin/organizations",
                params={"skip": skip, "limit": limit},
                cast_to=list[OrganizationResponse],
            ),
        )

    @operation("get_organization_admin_organizations__org_uuid__get")
    def retrieve(self, org_uuid: str) -> OrganizationResponse:
        """Get a specific Organization."""
        return cast(
            OrganizationResponse,
            self._client.get(
                f"/admin/organizations/{org_uuid}",
                cast_to=OrganizationResponse,
            ),
        )

    @operation("update_organization_admin_organizations__org_uuid__put")
    def update(self, org_uuid: str, body: OrganizationUpdateRequest) -> OrganizationResponse:
        """Update an Organization."""
        return cast(
            OrganizationResponse,
            self._client.put(
                f"/admin/organizations/{org_uuid}",
                json_body=body,
                cast_to=OrganizationResponse,
            ),
        )

    @operation("delete_organization_admin_organizations__org_uuid__delete")
    def delete(self, org_uuid: str) -> OrganizationDeletedResponse:
        """Delete an Organization."""
        return cast(
            OrganizationDeletedResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}",
                cast_to=OrganizationDeletedResponse,
            ),
        )


class AsyncManagement(AsyncResource):
    """Async counterpart of `Management`."""

    namespace: ClassVar[str] = "management"

    @operation("create_organization_admin_organizations_post")
    async def create(self, body: OrganizationCreateRequest) -> OrganizationResponse:
        """Create a new Organization (Superadmin)."""
        return cast(
            OrganizationResponse,
            await self._client.post(
                "/admin/organizations",
                json_body=body,
                cast_to=OrganizationResponse,
            ),
        )

    @operation("list_organizations_admin_organizations_get")
    async def list(
        self, *, skip: int | None = None, limit: int | None = None
    ) -> list[OrganizationResponse]:
        """List all Organizations."""
        return cast(
            list[OrganizationResponse],
            await self._client.get(
                "/admin/organizations",
                params={"skip": skip, "limit": limit},
                cast_to=list[OrganizationResponse],
            ),
        )

    @operation("get_organization_admin_organizations__org_uuid__get")
    async def retrieve(self, org_uuid: str) -> OrganizationResponse:
        """Get a specific Organization."""
        return cast(
            OrganizationResponse,
            await self._client.get(
                f"/admin/organizations/{org_uuid}",
                cast_to=OrganizationResponse,
            ),
        )

    @operation("update_organization_admin_organizations__org_uuid__put")
    async def update(self, org_uuid: str, body: OrganizationUpdateRequest) -> OrganizationResponse:
        """Update an Organization."""
        return cast(
            OrganizationResponse,
            await self._client.put(
                f"/admin/organizations/{org_uuid}",
                json_body=body,
                cast_to=OrganizationResponse,
            ),
        )

    @operation("delete_organization_admin_organizations__org_uuid__delete")
    async def delete(self, org_uuid: str) -> OrganizationDeletedResponse:
        """Delete an Organization."""
        return cast(
            OrganizationDeletedResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}",
                cast_to=OrganizationDeletedResponse,
            ),
        )


Galene._ADMIN_NAMESPACES.append(Management)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncManagement)
