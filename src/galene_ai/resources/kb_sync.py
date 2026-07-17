"""`kb_sync` resource: knowledge-base sync configuration and file management.

Admin endpoints under `/admin/organizations/{organization_uuid}/kb-sync/*` for
creating and running knowledge-base sync configurations and inspecting/retrying
their synced files.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    KBSyncConfigurationCreateRequest,
    KBSyncConfigurationResponse,
    KBSyncConfigurationUpdateRequest,
    KBSyncDeleteRequest,
    KBSyncDeleteResponse,
    KBSyncFilesListResponse,
    KBSyncRetryResponse,
)


class KbSync(SyncResource):
    """Manage knowledge-base sync configurations and their synced files."""

    namespace: ClassVar[str] = "kb_sync"

    @operation("create_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync_post")
    def create(
        self, organization_uuid: str, *, body: KBSyncConfigurationCreateRequest
    ) -> KBSyncConfigurationResponse:
        """Create Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync",
                json_body=body,
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation("list_kb_sync_configurations_admin_organizations__organization_uuid__kb_sync_get")
    def list(self, organization_uuid: str) -> list[KBSyncConfigurationResponse]:
        """List Kb Sync Configurations."""
        return cast(
            list[KBSyncConfigurationResponse],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync",
                cast_to=list[KBSyncConfigurationResponse],
            ),
        )

    @operation(
        "start_kb_sync_admin_organizations__organization_uuid__kb_sync__sync_config_id__start_post"
    )
    def start(self, organization_uuid: str, sync_config_id: str) -> dict[str, Any]:
        """Start Kb Sync."""
        return cast(
            dict[str, Any],
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/start",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "get_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__get"
    )
    def retrieve(self, organization_uuid: str, sync_config_id: str) -> KBSyncConfigurationResponse:
        """Get Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation(
        "update_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__put"
    )
    def update(
        self,
        organization_uuid: str,
        sync_config_id: str,
        *,
        body: KBSyncConfigurationUpdateRequest,
    ) -> KBSyncConfigurationResponse:
        """Update Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
                json_body=body,
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation(
        "delete_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__delete"
    )
    def delete(self, organization_uuid: str, sync_config_id: str) -> None:
        """Delete Kb Sync Configuration."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
            cast_to=None,
        )

    @operation(
        "get_kb_sync_status_admin_organizations__organization_uuid__kb_sync__sync_config_id__status_get"
    )
    def get_status(self, organization_uuid: str, sync_config_id: str) -> dict[str, Any]:
        """Get Kb Sync Status."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/status",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "list_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__files_get"
    )
    def list_files(
        self,
        organization_uuid: str,
        sync_config_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> KBSyncFilesListResponse:
        """List Kb Sync Files."""
        return cast(
            KBSyncFilesListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/files",
                params={"status": status, "limit": limit, "offset": offset},
                cast_to=KBSyncFilesListResponse,
            ),
        )

    @operation(
        "retry_kb_sync_file_admin_organizations__organization_uuid__kb_sync__sync_config_id__files__file_log_id__retry_post"
    )
    def retry_file(
        self, organization_uuid: str, sync_config_id: str, file_log_id: str
    ) -> KBSyncRetryResponse:
        """Retry Kb Sync File."""
        return cast(
            KBSyncRetryResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/files/{file_log_id}/retry",
                cast_to=KBSyncRetryResponse,
            ),
        )

    @operation(
        "retry_failed_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__failed_files_retry_post"
    )
    def retry_failed_files(
        self, organization_uuid: str, sync_config_id: str
    ) -> KBSyncRetryResponse:
        """Retry Failed Kb Sync Files."""
        return cast(
            KBSyncRetryResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/failed-files/retry",
                cast_to=KBSyncRetryResponse,
            ),
        )

    @operation(
        "delete_kb_sync_file_admin_organizations__organization_uuid__kb_sync__sync_config_id__files__file_log_id__delete"
    )
    def delete_file(
        self, organization_uuid: str, sync_config_id: str, file_log_id: str
    ) -> KBSyncDeleteResponse:
        """Delete Kb Sync File."""
        return cast(
            KBSyncDeleteResponse,
            self._client.delete(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/files/{file_log_id}",
                cast_to=KBSyncDeleteResponse,
            ),
        )

    @operation(
        "delete_selected_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__files_delete_post"
    )
    def delete_selected_files(
        self, organization_uuid: str, sync_config_id: str, *, body: KBSyncDeleteRequest
    ) -> KBSyncDeleteResponse:
        """Delete Selected Kb Sync Files."""
        return cast(
            KBSyncDeleteResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/files/delete",
                json_body=body,
                cast_to=KBSyncDeleteResponse,
            ),
        )


class AsyncKbSync(AsyncResource):
    """Async counterpart of `KbSync`."""

    namespace: ClassVar[str] = "kb_sync"

    @operation("create_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync_post")
    async def create(
        self, organization_uuid: str, *, body: KBSyncConfigurationCreateRequest
    ) -> KBSyncConfigurationResponse:
        """Create Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync",
                json_body=body,
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation("list_kb_sync_configurations_admin_organizations__organization_uuid__kb_sync_get")
    async def list(self, organization_uuid: str) -> list[KBSyncConfigurationResponse]:
        """List Kb Sync Configurations."""
        return cast(
            list[KBSyncConfigurationResponse],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync",
                cast_to=list[KBSyncConfigurationResponse],
            ),
        )

    @operation(
        "start_kb_sync_admin_organizations__organization_uuid__kb_sync__sync_config_id__start_post"
    )
    async def start(self, organization_uuid: str, sync_config_id: str) -> dict[str, Any]:
        """Start Kb Sync."""
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/start",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "get_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__get"
    )
    async def retrieve(
        self, organization_uuid: str, sync_config_id: str
    ) -> KBSyncConfigurationResponse:
        """Get Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation(
        "update_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__put"
    )
    async def update(
        self,
        organization_uuid: str,
        sync_config_id: str,
        *,
        body: KBSyncConfigurationUpdateRequest,
    ) -> KBSyncConfigurationResponse:
        """Update Kb Sync Configuration."""
        return cast(
            KBSyncConfigurationResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
                json_body=body,
                cast_to=KBSyncConfigurationResponse,
            ),
        )

    @operation(
        "delete_kb_sync_configuration_admin_organizations__organization_uuid__kb_sync__sync_config_id__delete"
    )
    async def delete(self, organization_uuid: str, sync_config_id: str) -> None:
        """Delete Kb Sync Configuration."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}",
            cast_to=None,
        )

    @operation(
        "get_kb_sync_status_admin_organizations__organization_uuid__kb_sync__sync_config_id__status_get"
    )
    async def get_status(self, organization_uuid: str, sync_config_id: str) -> dict[str, Any]:
        """Get Kb Sync Status."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/status",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "list_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__files_get"
    )
    async def list_files(
        self,
        organization_uuid: str,
        sync_config_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> KBSyncFilesListResponse:
        """List Kb Sync Files."""
        return cast(
            KBSyncFilesListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/files",
                params={"status": status, "limit": limit, "offset": offset},
                cast_to=KBSyncFilesListResponse,
            ),
        )

    @operation(
        "retry_kb_sync_file_admin_organizations__organization_uuid__kb_sync__sync_config_id__files__file_log_id__retry_post"
    )
    async def retry_file(
        self, organization_uuid: str, sync_config_id: str, file_log_id: str
    ) -> KBSyncRetryResponse:
        """Retry Kb Sync File."""
        return cast(
            KBSyncRetryResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/files/{file_log_id}/retry",
                cast_to=KBSyncRetryResponse,
            ),
        )

    @operation(
        "retry_failed_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__failed_files_retry_post"
    )
    async def retry_failed_files(
        self, organization_uuid: str, sync_config_id: str
    ) -> KBSyncRetryResponse:
        """Retry Failed Kb Sync Files."""
        return cast(
            KBSyncRetryResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/failed-files/retry",
                cast_to=KBSyncRetryResponse,
            ),
        )

    @operation(
        "delete_kb_sync_file_admin_organizations__organization_uuid__kb_sync__sync_config_id__files__file_log_id__delete"
    )
    async def delete_file(
        self, organization_uuid: str, sync_config_id: str, file_log_id: str
    ) -> KBSyncDeleteResponse:
        """Delete Kb Sync File."""
        return cast(
            KBSyncDeleteResponse,
            await self._client.delete(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}"
                f"/files/{file_log_id}",
                cast_to=KBSyncDeleteResponse,
            ),
        )

    @operation(
        "delete_selected_kb_sync_files_admin_organizations__organization_uuid__kb_sync__sync_config_id__files_delete_post"
    )
    async def delete_selected_files(
        self, organization_uuid: str, sync_config_id: str, *, body: KBSyncDeleteRequest
    ) -> KBSyncDeleteResponse:
        """Delete Selected Kb Sync Files."""
        return cast(
            KBSyncDeleteResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/kb-sync/{sync_config_id}/files/delete",
                json_body=body,
                cast_to=KBSyncDeleteResponse,
            ),
        )


Galene._NAMESPACES.append(KbSync)
AsyncGalene._NAMESPACES.append(AsyncKbSync)
