"""`admin.global_config` resource: superadmin-only global platform configuration.

Covers `/admin/settings/*` — SMTP, domain, platform update, maintenance/infra
windows, and backup (destination/schedule/notification/logs/runs) settings.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    ApplicationMaintenanceWindowCreateRequest,
    ApplicationMaintenanceWindowValue,
    BackupDestinationCreateRequest,
    BackupDestinationValue,
    BackupExecutionLogListResponse,
    BackupNotificationCreateRequest,
    BackupNotificationValue,
    BackupScheduleCreateRequest,
    BackupScheduleValue,
    DomainSettingsUpdateRequest,
    DomainSettingsValue,
    GlobalAppMaintenanceWindowConfigResponse,
    GlobalBackupDestinationConfigResponse,
    GlobalBackupScheduleConfigResponse,
    GlobalDomainConfigResponse,
    GlobalInfraUpdateWindowConfigResponse,
    GlobalSMTPConfigResponse,
    InfrastructureUpdateWindowCreateRequest,
    InfrastructureUpdateWindowValue,
    ManualBackupCancelResponse,
    ManualBackupTriggerResponse,
    ManualRetentionCleanupTriggerResponse,
    N8NCredentialsResponse,
    PendingPlatformUpdatesResponse,
    PlatformManualWindowRequest,
    PlatformManualWindowResponse,
    PlatformUpdateSettingsRequest,
    PlatformUpdateSettingsResponse,
    SMTPSettingsCreateRequest,
    SMTPSettingsPublicResponse,
)


class GlobalConfig(SyncResource):
    """Superadmin global platform configuration under `/admin/settings/*`."""

    namespace: ClassVar[str] = "global_config"

    @operation("test_smtp_connection_admin_settings_smtp_test_post")
    def test_smtp(self, body: SMTPSettingsCreateRequest) -> dict[str, Any]:
        """Test SMTP Connection (Superadmin)."""
        return cast(
            dict[str, Any],
            self._client.post(
                "/admin/settings/smtp/test",
                json_body=body,
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("retrieve_global_smtp_settings_admin_settings_smtp_get")
    def retrieve_smtp(self) -> SMTPSettingsPublicResponse:
        """Get Global SMTP Settings (Superadmin)."""
        return cast(
            SMTPSettingsPublicResponse,
            self._client.get("/admin/settings/smtp", cast_to=SMTPSettingsPublicResponse),
        )

    @operation("set_global_smtp_settings_admin_settings_smtp_post")
    def set_smtp(self, body: SMTPSettingsCreateRequest) -> GlobalSMTPConfigResponse:
        """Set Global SMTP Settings (Superadmin)."""
        return cast(
            GlobalSMTPConfigResponse,
            self._client.post(
                "/admin/settings/smtp", json_body=body, cast_to=GlobalSMTPConfigResponse
            ),
        )

    @operation("retrieve_global_domain_settings_admin_settings_domain_get")
    def retrieve_domain(self) -> DomainSettingsValue:
        """Get Global Domain Settings (Superadmin)."""
        return cast(
            DomainSettingsValue,
            self._client.get("/admin/settings/domain", cast_to=DomainSettingsValue),
        )

    @operation("set_global_domain_settings_admin_settings_domain_post")
    def set_domain(self, body: DomainSettingsUpdateRequest) -> GlobalDomainConfigResponse:
        """Set Global Domain Settings (Superadmin)."""
        return cast(
            GlobalDomainConfigResponse,
            self._client.post(
                "/admin/settings/domain", json_body=body, cast_to=GlobalDomainConfigResponse
            ),
        )

    @operation("retrieve_platform_update_settings_admin_settings_platform_updates_get")
    def retrieve_platform_updates(self) -> PlatformUpdateSettingsResponse:
        """Get Platform Update Settings (Superadmin)."""
        return cast(
            PlatformUpdateSettingsResponse,
            self._client.get(
                "/admin/settings/platform_updates", cast_to=PlatformUpdateSettingsResponse
            ),
        )

    @operation("set_platform_update_settings_admin_settings_platform_updates_post")
    def set_platform_updates(
        self, body: PlatformUpdateSettingsRequest
    ) -> PlatformUpdateSettingsResponse:
        """Set Platform Update Settings (Superadmin)."""
        return cast(
            PlatformUpdateSettingsResponse,
            self._client.post(
                "/admin/settings/platform_updates",
                json_body=body,
                cast_to=PlatformUpdateSettingsResponse,
            ),
        )

    @operation("request_platform_manual_window_admin_settings_platform_updates_manual_window_post")
    def request_platform_manual_window(
        self, body: PlatformManualWindowRequest
    ) -> PlatformManualWindowResponse:
        """Request One-Time Platform Update Window (Superadmin)."""
        return cast(
            PlatformManualWindowResponse,
            self._client.post(
                "/admin/settings/platform_updates/manual-window",
                json_body=body,
                cast_to=PlatformManualWindowResponse,
            ),
        )

    @operation(
        "retrieve_pending_platform_updates_admin_settings_platform_updates_pending_updates_get"
    )
    def retrieve_pending_platform_updates(self) -> PendingPlatformUpdatesResponse:
        """Get Pending Platform Updates (Superadmin)."""
        return cast(
            PendingPlatformUpdatesResponse,
            self._client.get(
                "/admin/settings/platform_updates/pending-updates",
                cast_to=PendingPlatformUpdatesResponse,
            ),
        )

    @operation(
        "retrieve_global_app_maintenance_window_settings_admin_settings_application_maintenance_window_get"
    )
    def retrieve_app_maintenance_window(self) -> ApplicationMaintenanceWindowValue:
        """Get Global Application Maintenance Window Settings (Superadmin)."""
        return cast(
            ApplicationMaintenanceWindowValue,
            self._client.get(
                "/admin/settings/application_maintenance_window",
                cast_to=ApplicationMaintenanceWindowValue,
            ),
        )

    @operation(
        "set_global_app_maintenance_window_settings_admin_settings_application_maintenance_window_post"
    )
    def set_app_maintenance_window(
        self, body: ApplicationMaintenanceWindowCreateRequest
    ) -> GlobalAppMaintenanceWindowConfigResponse:
        """Set Global Application Maintenance Window Settings (Superadmin)."""
        return cast(
            GlobalAppMaintenanceWindowConfigResponse,
            self._client.post(
                "/admin/settings/application_maintenance_window",
                json_body=body,
                cast_to=GlobalAppMaintenanceWindowConfigResponse,
            ),
        )

    @operation(
        "retrieve_global_infra_update_window_settings_admin_settings_infrastructure_update_window_get"
    )
    def retrieve_infra_update_window(self) -> InfrastructureUpdateWindowValue:
        """Get Global Infrastructure Update Window Settings (Superadmin)."""
        return cast(
            InfrastructureUpdateWindowValue,
            self._client.get(
                "/admin/settings/infrastructure_update_window",
                cast_to=InfrastructureUpdateWindowValue,
            ),
        )

    @operation(
        "set_global_infra_update_window_settings_admin_settings_infrastructure_update_window_post"
    )
    def set_infra_update_window(
        self, body: InfrastructureUpdateWindowCreateRequest
    ) -> GlobalInfraUpdateWindowConfigResponse:
        """Set Global Infrastructure Update Window Settings (Superadmin)."""
        return cast(
            GlobalInfraUpdateWindowConfigResponse,
            self._client.post(
                "/admin/settings/infrastructure_update_window",
                json_body=body,
                cast_to=GlobalInfraUpdateWindowConfigResponse,
            ),
        )

    @operation("retrieve_global_backup_destination_settings_admin_settings_backup_destination_get")
    def retrieve_backup_destination(self) -> BackupDestinationValue:
        """Get Global Backup Destination Settings (Superadmin)."""
        return cast(
            BackupDestinationValue,
            self._client.get("/admin/settings/backup_destination", cast_to=BackupDestinationValue),
        )

    @operation("set_global_backup_destination_settings_admin_settings_backup_destination_post")
    def set_backup_destination(
        self, body: BackupDestinationCreateRequest
    ) -> GlobalBackupDestinationConfigResponse:
        """Set Global Backup Destination Settings (Superadmin)."""
        return cast(
            GlobalBackupDestinationConfigResponse,
            self._client.post(
                "/admin/settings/backup_destination",
                json_body=body,
                cast_to=GlobalBackupDestinationConfigResponse,
            ),
        )

    @operation("retrieve_global_backup_schedule_settings_admin_settings_backup_schedule_get")
    def retrieve_backup_schedule(self) -> BackupScheduleValue:
        """Get Global Backup Schedule Settings (Superadmin)."""
        return cast(
            BackupScheduleValue,
            self._client.get("/admin/settings/backup_schedule", cast_to=BackupScheduleValue),
        )

    @operation("set_global_backup_schedule_settings_admin_settings_backup_schedule_post")
    def set_backup_schedule(
        self, body: BackupScheduleCreateRequest
    ) -> GlobalBackupScheduleConfigResponse:
        """Set Global Backup Schedule Settings (Superadmin)."""
        return cast(
            GlobalBackupScheduleConfigResponse,
            self._client.post(
                "/admin/settings/backup_schedule",
                json_body=body,
                cast_to=GlobalBackupScheduleConfigResponse,
            ),
        )

    @operation(
        "retrieve_global_backup_notification_settings_admin_settings_backup_notification_get"
    )
    def retrieve_backup_notification(self) -> BackupNotificationValue:
        """Get Global Backup Notification Settings (Superadmin)."""
        return cast(
            BackupNotificationValue,
            self._client.get(
                "/admin/settings/backup_notification", cast_to=BackupNotificationValue
            ),
        )

    @operation("set_global_backup_notification_settings_admin_settings_backup_notification_post")
    def set_backup_notification(self, body: BackupNotificationCreateRequest) -> dict[str, Any]:
        """Set Global Backup Notification Settings (Superadmin)."""
        return cast(
            dict[str, Any],
            self._client.post(
                "/admin/settings/backup_notification",
                json_body=body,
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("check_smtp_configured_admin_settings_smtp_configured_get")
    def check_smtp_configured(self) -> dict[str, Any]:
        """Check if SMTP is configured (Superadmin)."""
        return cast(
            dict[str, Any],
            self._client.get(
                "/admin/settings/smtp_configured",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("retrieve_backup_execution_logs_admin_settings_backup_logs_get")
    def list_backup_logs(
        self, *, page: int | None = None, page_size: int | None = None
    ) -> BackupExecutionLogListResponse:
        """List Backup Execution Logs (Superadmin)."""
        return cast(
            BackupExecutionLogListResponse,
            self._client.get(
                "/admin/settings/backup_logs",
                params={"page": page, "page_size": page_size},
                cast_to=BackupExecutionLogListResponse,
            ),
        )

    @operation("trigger_manual_backup_run_admin_settings_backup_run_post")
    def trigger_backup_run(self) -> ManualBackupTriggerResponse:
        """Trigger Manual Backup Run (Superadmin)."""
        return cast(
            ManualBackupTriggerResponse,
            self._client.post("/admin/settings/backup_run", cast_to=ManualBackupTriggerResponse),
        )

    @operation("cancel_running_backup_run_admin_settings_backup_logs__log_id__cancel_post")
    def cancel_backup_run(self, log_id: str) -> ManualBackupCancelResponse:
        """Cancel Running Backup Run (Superadmin)."""
        return cast(
            ManualBackupCancelResponse,
            self._client.post(
                f"/admin/settings/backup_logs/{log_id}/cancel",
                cast_to=ManualBackupCancelResponse,
            ),
        )

    @operation("trigger_manual_backup_retention_cleanup_admin_settings_backup_cleanup_post")
    def trigger_backup_cleanup(self) -> ManualRetentionCleanupTriggerResponse:
        """Trigger Retention Cleanup (Superadmin)."""
        return cast(
            ManualRetentionCleanupTriggerResponse,
            self._client.post(
                "/admin/settings/backup_cleanup", cast_to=ManualRetentionCleanupTriggerResponse
            ),
        )

    @operation("get_n8n_credentials_admin_settings_n8n_credentials_get")
    def get_n8n_credentials(self) -> N8NCredentialsResponse:
        """Get N8N Admin Credentials (Superadmin)."""
        return cast(
            N8NCredentialsResponse,
            self._client.get("/admin/settings/n8n-credentials", cast_to=N8NCredentialsResponse),
        )


class AsyncGlobalConfig(AsyncResource):
    """Async counterpart of `GlobalConfig`."""

    namespace: ClassVar[str] = "global_config"

    @operation("test_smtp_connection_admin_settings_smtp_test_post")
    async def test_smtp(self, body: SMTPSettingsCreateRequest) -> dict[str, Any]:
        """Test SMTP Connection (Superadmin)."""
        return cast(
            dict[str, Any],
            await self._client.post(
                "/admin/settings/smtp/test",
                json_body=body,
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("retrieve_global_smtp_settings_admin_settings_smtp_get")
    async def retrieve_smtp(self) -> SMTPSettingsPublicResponse:
        """Get Global SMTP Settings (Superadmin)."""
        return cast(
            SMTPSettingsPublicResponse,
            await self._client.get("/admin/settings/smtp", cast_to=SMTPSettingsPublicResponse),
        )

    @operation("set_global_smtp_settings_admin_settings_smtp_post")
    async def set_smtp(self, body: SMTPSettingsCreateRequest) -> GlobalSMTPConfigResponse:
        """Set Global SMTP Settings (Superadmin)."""
        return cast(
            GlobalSMTPConfigResponse,
            await self._client.post(
                "/admin/settings/smtp", json_body=body, cast_to=GlobalSMTPConfigResponse
            ),
        )

    @operation("retrieve_global_domain_settings_admin_settings_domain_get")
    async def retrieve_domain(self) -> DomainSettingsValue:
        """Get Global Domain Settings (Superadmin)."""
        return cast(
            DomainSettingsValue,
            await self._client.get("/admin/settings/domain", cast_to=DomainSettingsValue),
        )

    @operation("set_global_domain_settings_admin_settings_domain_post")
    async def set_domain(self, body: DomainSettingsUpdateRequest) -> GlobalDomainConfigResponse:
        """Set Global Domain Settings (Superadmin)."""
        return cast(
            GlobalDomainConfigResponse,
            await self._client.post(
                "/admin/settings/domain", json_body=body, cast_to=GlobalDomainConfigResponse
            ),
        )

    @operation("retrieve_platform_update_settings_admin_settings_platform_updates_get")
    async def retrieve_platform_updates(self) -> PlatformUpdateSettingsResponse:
        """Get Platform Update Settings (Superadmin)."""
        return cast(
            PlatformUpdateSettingsResponse,
            await self._client.get(
                "/admin/settings/platform_updates", cast_to=PlatformUpdateSettingsResponse
            ),
        )

    @operation("set_platform_update_settings_admin_settings_platform_updates_post")
    async def set_platform_updates(
        self, body: PlatformUpdateSettingsRequest
    ) -> PlatformUpdateSettingsResponse:
        """Set Platform Update Settings (Superadmin)."""
        return cast(
            PlatformUpdateSettingsResponse,
            await self._client.post(
                "/admin/settings/platform_updates",
                json_body=body,
                cast_to=PlatformUpdateSettingsResponse,
            ),
        )

    @operation("request_platform_manual_window_admin_settings_platform_updates_manual_window_post")
    async def request_platform_manual_window(
        self, body: PlatformManualWindowRequest
    ) -> PlatformManualWindowResponse:
        """Request One-Time Platform Update Window (Superadmin)."""
        return cast(
            PlatformManualWindowResponse,
            await self._client.post(
                "/admin/settings/platform_updates/manual-window",
                json_body=body,
                cast_to=PlatformManualWindowResponse,
            ),
        )

    @operation(
        "retrieve_pending_platform_updates_admin_settings_platform_updates_pending_updates_get"
    )
    async def retrieve_pending_platform_updates(self) -> PendingPlatformUpdatesResponse:
        """Get Pending Platform Updates (Superadmin)."""
        return cast(
            PendingPlatformUpdatesResponse,
            await self._client.get(
                "/admin/settings/platform_updates/pending-updates",
                cast_to=PendingPlatformUpdatesResponse,
            ),
        )

    @operation(
        "retrieve_global_app_maintenance_window_settings_admin_settings_application_maintenance_window_get"
    )
    async def retrieve_app_maintenance_window(self) -> ApplicationMaintenanceWindowValue:
        """Get Global Application Maintenance Window Settings (Superadmin)."""
        return cast(
            ApplicationMaintenanceWindowValue,
            await self._client.get(
                "/admin/settings/application_maintenance_window",
                cast_to=ApplicationMaintenanceWindowValue,
            ),
        )

    @operation(
        "set_global_app_maintenance_window_settings_admin_settings_application_maintenance_window_post"
    )
    async def set_app_maintenance_window(
        self, body: ApplicationMaintenanceWindowCreateRequest
    ) -> GlobalAppMaintenanceWindowConfigResponse:
        """Set Global Application Maintenance Window Settings (Superadmin)."""
        return cast(
            GlobalAppMaintenanceWindowConfigResponse,
            await self._client.post(
                "/admin/settings/application_maintenance_window",
                json_body=body,
                cast_to=GlobalAppMaintenanceWindowConfigResponse,
            ),
        )

    @operation(
        "retrieve_global_infra_update_window_settings_admin_settings_infrastructure_update_window_get"
    )
    async def retrieve_infra_update_window(self) -> InfrastructureUpdateWindowValue:
        """Get Global Infrastructure Update Window Settings (Superadmin)."""
        return cast(
            InfrastructureUpdateWindowValue,
            await self._client.get(
                "/admin/settings/infrastructure_update_window",
                cast_to=InfrastructureUpdateWindowValue,
            ),
        )

    @operation(
        "set_global_infra_update_window_settings_admin_settings_infrastructure_update_window_post"
    )
    async def set_infra_update_window(
        self, body: InfrastructureUpdateWindowCreateRequest
    ) -> GlobalInfraUpdateWindowConfigResponse:
        """Set Global Infrastructure Update Window Settings (Superadmin)."""
        return cast(
            GlobalInfraUpdateWindowConfigResponse,
            await self._client.post(
                "/admin/settings/infrastructure_update_window",
                json_body=body,
                cast_to=GlobalInfraUpdateWindowConfigResponse,
            ),
        )

    @operation("retrieve_global_backup_destination_settings_admin_settings_backup_destination_get")
    async def retrieve_backup_destination(self) -> BackupDestinationValue:
        """Get Global Backup Destination Settings (Superadmin)."""
        return cast(
            BackupDestinationValue,
            await self._client.get(
                "/admin/settings/backup_destination", cast_to=BackupDestinationValue
            ),
        )

    @operation("set_global_backup_destination_settings_admin_settings_backup_destination_post")
    async def set_backup_destination(
        self, body: BackupDestinationCreateRequest
    ) -> GlobalBackupDestinationConfigResponse:
        """Set Global Backup Destination Settings (Superadmin)."""
        return cast(
            GlobalBackupDestinationConfigResponse,
            await self._client.post(
                "/admin/settings/backup_destination",
                json_body=body,
                cast_to=GlobalBackupDestinationConfigResponse,
            ),
        )

    @operation("retrieve_global_backup_schedule_settings_admin_settings_backup_schedule_get")
    async def retrieve_backup_schedule(self) -> BackupScheduleValue:
        """Get Global Backup Schedule Settings (Superadmin)."""
        return cast(
            BackupScheduleValue,
            await self._client.get("/admin/settings/backup_schedule", cast_to=BackupScheduleValue),
        )

    @operation("set_global_backup_schedule_settings_admin_settings_backup_schedule_post")
    async def set_backup_schedule(
        self, body: BackupScheduleCreateRequest
    ) -> GlobalBackupScheduleConfigResponse:
        """Set Global Backup Schedule Settings (Superadmin)."""
        return cast(
            GlobalBackupScheduleConfigResponse,
            await self._client.post(
                "/admin/settings/backup_schedule",
                json_body=body,
                cast_to=GlobalBackupScheduleConfigResponse,
            ),
        )

    @operation(
        "retrieve_global_backup_notification_settings_admin_settings_backup_notification_get"
    )
    async def retrieve_backup_notification(self) -> BackupNotificationValue:
        """Get Global Backup Notification Settings (Superadmin)."""
        return cast(
            BackupNotificationValue,
            await self._client.get(
                "/admin/settings/backup_notification", cast_to=BackupNotificationValue
            ),
        )

    @operation("set_global_backup_notification_settings_admin_settings_backup_notification_post")
    async def set_backup_notification(
        self, body: BackupNotificationCreateRequest
    ) -> dict[str, Any]:
        """Set Global Backup Notification Settings (Superadmin)."""
        return cast(
            dict[str, Any],
            await self._client.post(
                "/admin/settings/backup_notification",
                json_body=body,
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("check_smtp_configured_admin_settings_smtp_configured_get")
    async def check_smtp_configured(self) -> dict[str, Any]:
        """Check if SMTP is configured (Superadmin)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                "/admin/settings/smtp_configured",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("retrieve_backup_execution_logs_admin_settings_backup_logs_get")
    async def list_backup_logs(
        self, *, page: int | None = None, page_size: int | None = None
    ) -> BackupExecutionLogListResponse:
        """List Backup Execution Logs (Superadmin)."""
        return cast(
            BackupExecutionLogListResponse,
            await self._client.get(
                "/admin/settings/backup_logs",
                params={"page": page, "page_size": page_size},
                cast_to=BackupExecutionLogListResponse,
            ),
        )

    @operation("trigger_manual_backup_run_admin_settings_backup_run_post")
    async def trigger_backup_run(self) -> ManualBackupTriggerResponse:
        """Trigger Manual Backup Run (Superadmin)."""
        return cast(
            ManualBackupTriggerResponse,
            await self._client.post(
                "/admin/settings/backup_run", cast_to=ManualBackupTriggerResponse
            ),
        )

    @operation("cancel_running_backup_run_admin_settings_backup_logs__log_id__cancel_post")
    async def cancel_backup_run(self, log_id: str) -> ManualBackupCancelResponse:
        """Cancel Running Backup Run (Superadmin)."""
        return cast(
            ManualBackupCancelResponse,
            await self._client.post(
                f"/admin/settings/backup_logs/{log_id}/cancel",
                cast_to=ManualBackupCancelResponse,
            ),
        )

    @operation("trigger_manual_backup_retention_cleanup_admin_settings_backup_cleanup_post")
    async def trigger_backup_cleanup(self) -> ManualRetentionCleanupTriggerResponse:
        """Trigger Retention Cleanup (Superadmin)."""
        return cast(
            ManualRetentionCleanupTriggerResponse,
            await self._client.post(
                "/admin/settings/backup_cleanup",
                cast_to=ManualRetentionCleanupTriggerResponse,
            ),
        )

    @operation("get_n8n_credentials_admin_settings_n8n_credentials_get")
    async def get_n8n_credentials(self) -> N8NCredentialsResponse:
        """Get N8N Admin Credentials (Superadmin)."""
        return cast(
            N8NCredentialsResponse,
            await self._client.get(
                "/admin/settings/n8n-credentials", cast_to=N8NCredentialsResponse
            ),
        )


Galene._ADMIN_NAMESPACES.append(GlobalConfig)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncGlobalConfig)
