"""`organizations` resource: admin management of users within an organization.

Covers the admin endpoints under `/admin/organizations/{organization_uuid}/users`:
list the users in an organization and invite/create a new user. Both responses are
plain (un-enveloped) models per the pre-computed directives.
"""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AdminUserCreateRequest,
    AdminUserCreateResponse,
    OrganizationUserListResponse,
)


class Organizations(SyncResource):
    """List and invite/create users within an organization (Admin)."""

    namespace: ClassVar[str] = "organizations"

    @operation("list_organization_users_admin_organizations__organization_uuid__users_get")
    def list_users(self, organization_uuid: str) -> OrganizationUserListResponse:
        """List Users in an Organization."""
        return cast(
            OrganizationUserListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/users",
                cast_to=OrganizationUserListResponse,
            ),
        )

    @operation("admin_create_invite_user_admin_organizations__organization_uuid__users_post")
    def create_user(
        self, organization_uuid: str, body: AdminUserCreateRequest
    ) -> AdminUserCreateResponse:
        """Admin Invites/Creates a User in an Organization."""
        return cast(
            AdminUserCreateResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/users",
                json_body=body,
                cast_to=AdminUserCreateResponse,
            ),
        )


class AsyncOrganizations(AsyncResource):
    """Async counterpart of `Organizations`."""

    namespace: ClassVar[str] = "organizations"

    @operation("list_organization_users_admin_organizations__organization_uuid__users_get")
    async def list_users(self, organization_uuid: str) -> OrganizationUserListResponse:
        """List Users in an Organization."""
        return cast(
            OrganizationUserListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/users",
                cast_to=OrganizationUserListResponse,
            ),
        )

    @operation("admin_create_invite_user_admin_organizations__organization_uuid__users_post")
    async def create_user(
        self, organization_uuid: str, body: AdminUserCreateRequest
    ) -> AdminUserCreateResponse:
        """Admin Invites/Creates a User in an Organization."""
        return cast(
            AdminUserCreateResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/users",
                json_body=body,
                cast_to=AdminUserCreateResponse,
            ),
        )


Galene._NAMESPACES.append(Organizations)
AsyncGalene._NAMESPACES.append(AsyncOrganizations)
