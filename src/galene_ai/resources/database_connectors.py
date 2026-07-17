"""`database_connectors` resource: admin management of organization database connectors."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    DatabaseConnectorCreateRequest,
    DatabaseConnectorDetailResponse,
    DatabaseConnectorListResponse,
    DatabaseConnectorsResponse,
    DatabasePropertiesBatchUpdateRequest,
    DatabasePropertiesBatchUpdateResponse,
    DatabaseTablesConfigurationUploadResponse,
    ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
    ModelsAdminModelsDatabaseConnectorDatabaseConnectorUpdateRequest,
)


class DatabaseConnectors(SyncResource):
    """Manage an organization's database connectors (admin)."""

    namespace: ClassVar[str] = "database_connectors"

    @operation("create_db_connector_admin_organizations__organization_uuid__db_connectors_post")
    def create(
        self, organization_uuid: str, *, body: DatabaseConnectorCreateRequest
    ) -> ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse:
        """Create a Database Connector for an Organization."""
        return cast(
            ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors",
                json_body=body,
                cast_to=ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            ),
        )

    @operation("list_db_connectors_admin_organizations__organization_uuid__db_connectors_get")
    def list(self, organization_uuid: str) -> DatabaseConnectorListResponse:
        """List Database Connectors for an Organization."""
        return cast(
            DatabaseConnectorListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors",
                cast_to=DatabaseConnectorListResponse,
            ),
        )

    @operation(
        "get_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__get"
    )
    def retrieve(
        self, organization_uuid: str, db_connector_uuid: str
    ) -> DatabaseConnectorDetailResponse:
        """Get a Specific Database Connector for an Organization."""
        return cast(
            DatabaseConnectorDetailResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
                cast_to=DatabaseConnectorDetailResponse,
            ),
        )

    @operation(
        "update_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__put"
    )
    def update(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        *,
        body: ModelsAdminModelsDatabaseConnectorDatabaseConnectorUpdateRequest,
    ) -> ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse:
        """Update a Database Connector for an Organization."""
        return cast(
            ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
                json_body=body,
                cast_to=ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            ),
        )

    @operation(
        "delete_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__delete"
    )
    def delete(self, organization_uuid: str, db_connector_uuid: str) -> None:
        """Delete a Database Connector for an Organization."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
            cast_to=None,
        )

    @operation(
        "trigger_database_discovery_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__discover_post"
    )
    def discover(self, organization_uuid: str, db_connector_uuid: str) -> dict[str, Any]:
        """Trigger Database Discovery for a Connector."""
        return cast(
            "dict[str, Any]",
            self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/discover",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "update_database_properties_batch_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__properties_put"
    )
    def update_properties(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        *,
        body: DatabasePropertiesBatchUpdateRequest,
    ) -> DatabasePropertiesBatchUpdateResponse:
        """Update Multiple Table and Column Properties in Database Connector."""
        return cast(
            DatabasePropertiesBatchUpdateResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/properties",
                json_body=body,
                cast_to=DatabasePropertiesBatchUpdateResponse,
            ),
        )

    @operation(
        "test_database_connection_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__test_connection_post"
    )
    def test_connection(self, organization_uuid: str, db_connector_uuid: str) -> dict[str, Any]:
        """Test Database Connection."""
        return cast(
            "dict[str, Any]",
            self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/test-connection",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "download_tables_configuration_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__tables_config_get"
    )
    def download_tables_config(
        self, organization_uuid: str, db_connector_uuid: str
    ) -> dict[str, Any]:
        """Download Database Tables Configuration as JSON File."""
        return cast(
            "dict[str, Any]",
            self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/tables-config",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "upload_tables_configuration_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__tables_config_post"
    )
    def upload_tables_config(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        file: bytes,
        *,
        filename: str | None = None,
    ) -> DatabaseTablesConfigurationUploadResponse:
        """Upload Database Tables Configuration from JSON File."""
        files = {"file": (filename or "tables-config.json", file)}
        return cast(
            DatabaseTablesConfigurationUploadResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/tables-config",
                files=files,
                cast_to=DatabaseTablesConfigurationUploadResponse,
            ),
        )

    @operation(
        "_get_organization_database_connectors_admin_organizations__organization_uuid__database_connectors_get"
    )
    def list_organization_connectors(self, organization_uuid: str) -> DatabaseConnectorsResponse:
        """List Database Connectors for Organization (Admin)."""
        return cast(
            DatabaseConnectorsResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/database_connectors",
                cast_to=DatabaseConnectorsResponse,
                envelope=True,
            ),
        )


class AsyncDatabaseConnectors(AsyncResource):
    """Async counterpart of `DatabaseConnectors`."""

    namespace: ClassVar[str] = "database_connectors"

    @operation("create_db_connector_admin_organizations__organization_uuid__db_connectors_post")
    async def create(
        self, organization_uuid: str, *, body: DatabaseConnectorCreateRequest
    ) -> ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse:
        """Create a Database Connector for an Organization."""
        return cast(
            ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors",
                json_body=body,
                cast_to=ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            ),
        )

    @operation("list_db_connectors_admin_organizations__organization_uuid__db_connectors_get")
    async def list(self, organization_uuid: str) -> DatabaseConnectorListResponse:
        """List Database Connectors for an Organization."""
        return cast(
            DatabaseConnectorListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors",
                cast_to=DatabaseConnectorListResponse,
            ),
        )

    @operation(
        "get_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__get"
    )
    async def retrieve(
        self, organization_uuid: str, db_connector_uuid: str
    ) -> DatabaseConnectorDetailResponse:
        """Get a Specific Database Connector for an Organization."""
        return cast(
            DatabaseConnectorDetailResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
                cast_to=DatabaseConnectorDetailResponse,
            ),
        )

    @operation(
        "update_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__put"
    )
    async def update(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        *,
        body: ModelsAdminModelsDatabaseConnectorDatabaseConnectorUpdateRequest,
    ) -> ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse:
        """Update a Database Connector for an Organization."""
        return cast(
            ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
                json_body=body,
                cast_to=ModelsAdminModelsDatabaseConnectorDatabaseConnectorResponse,
            ),
        )

    @operation(
        "delete_db_connector_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__delete"
    )
    async def delete(self, organization_uuid: str, db_connector_uuid: str) -> None:
        """Delete a Database Connector for an Organization."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}",
            cast_to=None,
        )

    @operation(
        "trigger_database_discovery_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__discover_post"
    )
    async def discover(self, organization_uuid: str, db_connector_uuid: str) -> dict[str, Any]:
        """Trigger Database Discovery for a Connector."""
        return cast(
            "dict[str, Any]",
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/discover",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "update_database_properties_batch_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__properties_put"
    )
    async def update_properties(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        *,
        body: DatabasePropertiesBatchUpdateRequest,
    ) -> DatabasePropertiesBatchUpdateResponse:
        """Update Multiple Table and Column Properties in Database Connector."""
        return cast(
            DatabasePropertiesBatchUpdateResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/properties",
                json_body=body,
                cast_to=DatabasePropertiesBatchUpdateResponse,
            ),
        )

    @operation(
        "test_database_connection_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__test_connection_post"
    )
    async def test_connection(
        self, organization_uuid: str, db_connector_uuid: str
    ) -> dict[str, Any]:
        """Test Database Connection."""
        return cast(
            "dict[str, Any]",
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/test-connection",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "download_tables_configuration_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__tables_config_get"
    )
    async def download_tables_config(
        self, organization_uuid: str, db_connector_uuid: str
    ) -> dict[str, Any]:
        """Download Database Tables Configuration as JSON File."""
        return cast(
            "dict[str, Any]",
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/tables-config",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "upload_tables_configuration_admin_organizations__organization_uuid__db_connectors__db_connector_uuid__tables_config_post"
    )
    async def upload_tables_config(
        self,
        organization_uuid: str,
        db_connector_uuid: str,
        file: bytes,
        *,
        filename: str | None = None,
    ) -> DatabaseTablesConfigurationUploadResponse:
        """Upload Database Tables Configuration from JSON File."""
        files = {"file": (filename or "tables-config.json", file)}
        return cast(
            DatabaseTablesConfigurationUploadResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/db-connectors/{db_connector_uuid}/tables-config",
                files=files,
                cast_to=DatabaseTablesConfigurationUploadResponse,
            ),
        )

    @operation(
        "_get_organization_database_connectors_admin_organizations__organization_uuid__database_connectors_get"
    )
    async def list_organization_connectors(
        self, organization_uuid: str
    ) -> DatabaseConnectorsResponse:
        """List Database Connectors for Organization (Admin)."""
        return cast(
            DatabaseConnectorsResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/database_connectors",
                cast_to=DatabaseConnectorsResponse,
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(DatabaseConnectors)
AsyncGalene._NAMESPACES.append(AsyncDatabaseConnectors)
