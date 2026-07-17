"""`roles` resource: admin role listing and organization role management."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    OrganizationRoleCreateRequest,
    RoleDetailResponse,
    RoleListResponse,
)


class Roles(SyncResource):
    """Admin role listing and organization role management."""

    namespace: ClassVar[str] = "roles"

    @operation("admin_list_all_roles_admin_roles_get")
    def list_all(self) -> RoleListResponse:
        """Admin Lists All Available Roles."""
        return cast(
            RoleListResponse,
            self._client.get("/admin/roles", cast_to=RoleListResponse),
        )

    @operation("list_organization_roles_admin_organizations__organization_uuid__roles_get")
    def list(self, organization_uuid: str) -> RoleListResponse:
        """List Roles for a Specific Organization."""
        return cast(
            RoleListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/roles",
                cast_to=RoleListResponse,
            ),
        )

    @operation("create_organization_role_admin_organizations__organization_uuid__roles_post")
    def create(
        self, organization_uuid: str, *, body: OrganizationRoleCreateRequest
    ) -> RoleDetailResponse:
        """Create a Role for a Specific Organization."""
        return cast(
            RoleDetailResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/roles",
                json_body=body,
                cast_to=RoleDetailResponse,
            ),
        )

    @operation(
        "delete_organization_role_admin_organizations__organization_uuid__roles__role_id__delete"
    )
    def delete(self, organization_uuid: str, role_id: str) -> None:
        """Delete an Organization Role."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/roles/{role_id}", cast_to=None
        )


class AsyncRoles(AsyncResource):
    """Async counterpart of `Roles`."""

    namespace: ClassVar[str] = "roles"

    @operation("admin_list_all_roles_admin_roles_get")
    async def list_all(self) -> RoleListResponse:
        """Admin Lists All Available Roles."""
        return cast(
            RoleListResponse,
            await self._client.get("/admin/roles", cast_to=RoleListResponse),
        )

    @operation("list_organization_roles_admin_organizations__organization_uuid__roles_get")
    async def list(self, organization_uuid: str) -> RoleListResponse:
        """List Roles for a Specific Organization."""
        return cast(
            RoleListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/roles",
                cast_to=RoleListResponse,
            ),
        )

    @operation("create_organization_role_admin_organizations__organization_uuid__roles_post")
    async def create(
        self, organization_uuid: str, *, body: OrganizationRoleCreateRequest
    ) -> RoleDetailResponse:
        """Create a Role for a Specific Organization."""
        return cast(
            RoleDetailResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/roles",
                json_body=body,
                cast_to=RoleDetailResponse,
            ),
        )

    @operation(
        "delete_organization_role_admin_organizations__organization_uuid__roles__role_id__delete"
    )
    async def delete(self, organization_uuid: str, role_id: str) -> None:
        """Delete an Organization Role."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/roles/{role_id}", cast_to=None
        )


Galene._NAMESPACES.append(Roles)
AsyncGalene._NAMESPACES.append(AsyncRoles)
