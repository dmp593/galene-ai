"""`kb_connectors` resource: admin management of organization knowledge-base connectors."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    KBConnectorCreateRequest,
    KBConnectorDetailResponse,
    KBConnectorDiscoveryCacheResponse,
    KBConnectorListResponse,
    KBConnectorsResponse,
    KBConnectorTestRequest,
    KBConnectorTestResponse,
    ModelsAdminModelsKbConnectorKBConnectorResponse,
    ModelsAdminModelsKbConnectorKBConnectorUpdateRequest,
    ScopedDiscoveryPreviewRequest,
    ScopedDiscoveryPreviewResponse,
)


class KbConnectors(SyncResource):
    """Create, manage, test, and browse organization KB connectors."""

    namespace: ClassVar[str] = "kb_connectors"

    @operation("create_kb_connector_admin_organizations__organization_uuid__kb_connectors_post")
    def create(
        self, organization_uuid: str, *, body: KBConnectorCreateRequest
    ) -> ModelsAdminModelsKbConnectorKBConnectorResponse:
        """Create a KB Connector for an Organization."""
        return cast(
            ModelsAdminModelsKbConnectorKBConnectorResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors",
                json_body=body,
                cast_to=ModelsAdminModelsKbConnectorKBConnectorResponse,
            ),
        )

    @operation("list_kb_connectors_admin_organizations__organization_uuid__kb_connectors_get")
    def list(self, organization_uuid: str) -> KBConnectorListResponse:
        """List KB Connectors for an Organization."""
        return cast(
            KBConnectorListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors",
                cast_to=KBConnectorListResponse,
            ),
        )

    @operation(
        "get_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__get"
    )
    def retrieve(self, organization_uuid: str, kb_connector_uuid: str) -> KBConnectorDetailResponse:
        """Get a Specific KB Connector for an Organization."""
        return cast(
            KBConnectorDetailResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
                cast_to=KBConnectorDetailResponse,
            ),
        )

    @operation(
        "update_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__put"
    )
    def update(
        self,
        organization_uuid: str,
        kb_connector_uuid: str,
        *,
        body: ModelsAdminModelsKbConnectorKBConnectorUpdateRequest,
    ) -> ModelsAdminModelsKbConnectorKBConnectorResponse:
        """Update a KB Connector for an Organization."""
        return cast(
            ModelsAdminModelsKbConnectorKBConnectorResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
                json_body=body,
                cast_to=ModelsAdminModelsKbConnectorKBConnectorResponse,
            ),
        )

    @operation(
        "delete_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__delete"
    )
    def delete(self, organization_uuid: str, kb_connector_uuid: str) -> None:
        """Delete a KB Connector for an Organization."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
            cast_to=None,
        )

    @operation(
        "get_kb_connector_discovery_cache_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__discovery_cache_get"
    )
    def retrieve_discovery_cache(
        self, organization_uuid: str, kb_connector_uuid: str
    ) -> KBConnectorDiscoveryCacheResponse:
        """Get cached full discovery for a KB Connector."""
        return cast(
            KBConnectorDiscoveryCacheResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/discovery-cache",
                cast_to=KBConnectorDiscoveryCacheResponse,
            ),
        )

    @operation(
        "list_kb_connector_drives_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__drives_get"
    )
    def list_drives(self, organization_uuid: str, kb_connector_uuid: str) -> dict[str, Any]:
        """List available document libraries (drives) for a SharePoint KB Connector."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/drives",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "browse_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__browse_get"
    )
    def browse(
        self, organization_uuid: str, kb_connector_uuid: str, *, path: str | None = None
    ) -> dict[str, Any]:
        """Browse folder contents of a SharePoint document library."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/browse",
                params={"path": path},
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "scoped_discovery_preview_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__scoped_discovery_preview_post"
    )
    def preview_scoped_discovery(
        self,
        organization_uuid: str,
        kb_connector_uuid: str,
        *,
        body: ScopedDiscoveryPreviewRequest,
    ) -> ScopedDiscoveryPreviewResponse:
        """Preview files that would be discovered from the given paths."""
        return cast(
            ScopedDiscoveryPreviewResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/scoped-discovery-preview",
                json_body=body,
                cast_to=ScopedDiscoveryPreviewResponse,
            ),
        )

    @operation(
        "test_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__test_post"
    )
    def test(
        self, organization_uuid: str, kb_connector_uuid: str, *, body: KBConnectorTestRequest
    ) -> KBConnectorTestResponse:
        """Test KB Connector Connection."""
        return cast(
            KBConnectorTestResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/test",
                json_body=body,
                cast_to=KBConnectorTestResponse,
            ),
        )

    @operation(
        "_get_organization_kb_connectors_admin_organizations__organization_uuid__kb_connectors_get"
    )
    def list_for_organization(self, organization_uuid: str) -> KBConnectorsResponse:
        """List KB Connectors for Organization (Admin)."""
        return cast(
            KBConnectorsResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb_connectors",
                cast_to=KBConnectorsResponse,
                envelope=True,
            ),
        )


class AsyncKbConnectors(AsyncResource):
    """Async counterpart of `KbConnectors`."""

    namespace: ClassVar[str] = "kb_connectors"

    @operation("create_kb_connector_admin_organizations__organization_uuid__kb_connectors_post")
    async def create(
        self, organization_uuid: str, *, body: KBConnectorCreateRequest
    ) -> ModelsAdminModelsKbConnectorKBConnectorResponse:
        """Create a KB Connector for an Organization."""
        return cast(
            ModelsAdminModelsKbConnectorKBConnectorResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors",
                json_body=body,
                cast_to=ModelsAdminModelsKbConnectorKBConnectorResponse,
            ),
        )

    @operation("list_kb_connectors_admin_organizations__organization_uuid__kb_connectors_get")
    async def list(self, organization_uuid: str) -> KBConnectorListResponse:
        """List KB Connectors for an Organization."""
        return cast(
            KBConnectorListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors",
                cast_to=KBConnectorListResponse,
            ),
        )

    @operation(
        "get_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__get"
    )
    async def retrieve(
        self, organization_uuid: str, kb_connector_uuid: str
    ) -> KBConnectorDetailResponse:
        """Get a Specific KB Connector for an Organization."""
        return cast(
            KBConnectorDetailResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
                cast_to=KBConnectorDetailResponse,
            ),
        )

    @operation(
        "update_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__put"
    )
    async def update(
        self,
        organization_uuid: str,
        kb_connector_uuid: str,
        *,
        body: ModelsAdminModelsKbConnectorKBConnectorUpdateRequest,
    ) -> ModelsAdminModelsKbConnectorKBConnectorResponse:
        """Update a KB Connector for an Organization."""
        return cast(
            ModelsAdminModelsKbConnectorKBConnectorResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
                json_body=body,
                cast_to=ModelsAdminModelsKbConnectorKBConnectorResponse,
            ),
        )

    @operation(
        "delete_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__delete"
    )
    async def delete(self, organization_uuid: str, kb_connector_uuid: str) -> None:
        """Delete a KB Connector for an Organization."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}",
            cast_to=None,
        )

    @operation(
        "get_kb_connector_discovery_cache_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__discovery_cache_get"
    )
    async def retrieve_discovery_cache(
        self, organization_uuid: str, kb_connector_uuid: str
    ) -> KBConnectorDiscoveryCacheResponse:
        """Get cached full discovery for a KB Connector."""
        return cast(
            KBConnectorDiscoveryCacheResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/discovery-cache",
                cast_to=KBConnectorDiscoveryCacheResponse,
            ),
        )

    @operation(
        "list_kb_connector_drives_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__drives_get"
    )
    async def list_drives(self, organization_uuid: str, kb_connector_uuid: str) -> dict[str, Any]:
        """List available document libraries (drives) for a SharePoint KB Connector."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/drives",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "browse_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__browse_get"
    )
    async def browse(
        self, organization_uuid: str, kb_connector_uuid: str, *, path: str | None = None
    ) -> dict[str, Any]:
        """Browse folder contents of a SharePoint document library."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/browse",
                params={"path": path},
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "scoped_discovery_preview_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__scoped_discovery_preview_post"
    )
    async def preview_scoped_discovery(
        self,
        organization_uuid: str,
        kb_connector_uuid: str,
        *,
        body: ScopedDiscoveryPreviewRequest,
    ) -> ScopedDiscoveryPreviewResponse:
        """Preview files that would be discovered from the given paths."""
        return cast(
            ScopedDiscoveryPreviewResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/scoped-discovery-preview",
                json_body=body,
                cast_to=ScopedDiscoveryPreviewResponse,
            ),
        )

    @operation(
        "test_kb_connector_admin_organizations__organization_uuid__kb_connectors__kb_connector_uuid__test_post"
    )
    async def test(
        self, organization_uuid: str, kb_connector_uuid: str, *, body: KBConnectorTestRequest
    ) -> KBConnectorTestResponse:
        """Test KB Connector Connection."""
        return cast(
            KBConnectorTestResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-connectors/{kb_connector_uuid}/test",
                json_body=body,
                cast_to=KBConnectorTestResponse,
            ),
        )

    @operation(
        "_get_organization_kb_connectors_admin_organizations__organization_uuid__kb_connectors_get"
    )
    async def list_for_organization(self, organization_uuid: str) -> KBConnectorsResponse:
        """List KB Connectors for Organization (Admin)."""
        return cast(
            KBConnectorsResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb_connectors",
                cast_to=KBConnectorsResponse,
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(KbConnectors)
AsyncGalene._NAMESPACES.append(AsyncKbConnectors)
