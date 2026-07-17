"""`groups` resource: SSO connector group import, reconciliation, and consent."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AvailableGroupsResult,
    ConsentStatus,
    ImportedGroupResponse,
    ResyncSummary,
    UpdateImportsRequest,
    UpdateImportsResult,
)


class Groups(SyncResource):
    """List, import, reconcile SSO groups and probe admin consent."""

    namespace: ClassVar[str] = "groups"

    @operation(
        "get_available_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__available_groups_get"
    )
    def available(self, organization_uuid: str, connector_uuid: str) -> AvailableGroupsResult:
        """List groups available for import on the IdP side."""
        return cast(
            AvailableGroupsResult,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/available-groups",
                cast_to=AvailableGroupsResult,
            ),
        )

    @operation(
        "get_imported_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__imported_groups_get"
    )
    def imported(self, organization_uuid: str, connector_uuid: str) -> list[ImportedGroupResponse]:
        """List imported groups (DB-only view)."""
        return cast(
            list[ImportedGroupResponse],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/imported-groups",
                cast_to=list[ImportedGroupResponse],
            ),
        )

    @operation(
        "update_imported_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__imported_groups_put"
    )
    def update_imports(
        self, organization_uuid: str, connector_uuid: str, *, body: UpdateImportsRequest
    ) -> UpdateImportsResult:
        """Reconcile the imported-groups list (declarative)."""
        return cast(
            UpdateImportsResult,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/imported-groups",
                json_body=body,
                cast_to=UpdateImportsResult,
            ),
        )

    @operation(
        "resync_organization_admin_organizations__organization_uuid__sso_connectors__connector_uuid__resync_post"
    )
    def resync(self, organization_uuid: str, connector_uuid: str) -> ResyncSummary:
        """Resync every SSO user in the organization."""
        return cast(
            ResyncSummary,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/resync",
                cast_to=ResyncSummary,
            ),
        )

    @operation(
        "get_consent_status_admin_organizations__organization_uuid__sso_connectors__connector_uuid__consent_status_get"
    )
    def consent_status(self, organization_uuid: str, connector_uuid: str) -> ConsentStatus:
        """Probe Microsoft Graph admin consent for this connector."""
        return cast(
            ConsentStatus,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/consent-status",
                cast_to=ConsentStatus,
            ),
        )

    @operation(
        "get_admin_consent_url_admin_organizations__organization_uuid__sso_connectors__connector_uuid__admin_consent_url_get"
    )
    def admin_consent_url(self, organization_uuid: str, connector_uuid: str) -> dict[str, Any]:
        """Generate a Microsoft adminconsent URL with HMAC-signed state."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/admin-consent-url",
                cast_to=dict,  # spec: untyped response
            ),
        )


class AsyncGroups(AsyncResource):
    """Async counterpart of `Groups`."""

    namespace: ClassVar[str] = "groups"

    @operation(
        "get_available_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__available_groups_get"
    )
    async def available(self, organization_uuid: str, connector_uuid: str) -> AvailableGroupsResult:
        """List groups available for import on the IdP side."""
        return cast(
            AvailableGroupsResult,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/available-groups",
                cast_to=AvailableGroupsResult,
            ),
        )

    @operation(
        "get_imported_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__imported_groups_get"
    )
    async def imported(
        self, organization_uuid: str, connector_uuid: str
    ) -> list[ImportedGroupResponse]:
        """List imported groups (DB-only view)."""
        return cast(
            list[ImportedGroupResponse],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/imported-groups",
                cast_to=list[ImportedGroupResponse],
            ),
        )

    @operation(
        "update_imported_groups_admin_organizations__organization_uuid__sso_connectors__connector_uuid__imported_groups_put"
    )
    async def update_imports(
        self, organization_uuid: str, connector_uuid: str, *, body: UpdateImportsRequest
    ) -> UpdateImportsResult:
        """Reconcile the imported-groups list (declarative)."""
        return cast(
            UpdateImportsResult,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/imported-groups",
                json_body=body,
                cast_to=UpdateImportsResult,
            ),
        )

    @operation(
        "resync_organization_admin_organizations__organization_uuid__sso_connectors__connector_uuid__resync_post"
    )
    async def resync(self, organization_uuid: str, connector_uuid: str) -> ResyncSummary:
        """Resync every SSO user in the organization."""
        return cast(
            ResyncSummary,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/resync",
                cast_to=ResyncSummary,
            ),
        )

    @operation(
        "get_consent_status_admin_organizations__organization_uuid__sso_connectors__connector_uuid__consent_status_get"
    )
    async def consent_status(self, organization_uuid: str, connector_uuid: str) -> ConsentStatus:
        """Probe Microsoft Graph admin consent for this connector."""
        return cast(
            ConsentStatus,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/consent-status",
                cast_to=ConsentStatus,
            ),
        )

    @operation(
        "get_admin_consent_url_admin_organizations__organization_uuid__sso_connectors__connector_uuid__admin_consent_url_get"
    )
    async def admin_consent_url(
        self, organization_uuid: str, connector_uuid: str
    ) -> dict[str, Any]:
        """Generate a Microsoft adminconsent URL with HMAC-signed state."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}/admin-consent-url",
                cast_to=dict,  # spec: untyped response
            ),
        )


Galene._NAMESPACES.append(Groups)
AsyncGalene._NAMESPACES.append(AsyncGroups)
