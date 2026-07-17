import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    ApplicationMaintenanceWindowCreateRequest,
    BackupDestinationCreateRequest,
    BackupNotificationCreateRequest,
    BackupScheduleCreateRequest,
    BackupTimeSlot,
    DomainSettingsUpdateRequest,
    InfrastructureUpdateWindowCreateRequest,
    PlatformManualWindowRequest,
    PlatformUpdateSettingsRequest,
    ScheduledTimeMoment,
    SMTPSettingsCreateRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _smtp_body() -> SMTPSettingsCreateRequest:
    return SMTPSettingsCreateRequest(
        endpoint="smtp.example.com",
        port=587,
        username="mailer",
        sender_email="no-reply@example.com",
        password="secret",
    )


def test_test_smtp_posts_body_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/smtp/test"
        assert b'"endpoint":"smtp.example.com"' in req.content
        return httpx.Response(200, json={"success": True, "message": "ok"})

    result = _client(handler).admin.global_config.test_smtp(_smtp_body())
    assert result["success"] is True


def test_retrieve_smtp_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/smtp"
        return httpx.Response(
            200,
            json={
                "endpoint": "smtp.example.com",
                "port": 587,
                "username": "mailer",
                "sender_email": "no-reply@example.com",
                "has_password": True,
            },
        )

    res = _client(handler).admin.global_config.retrieve_smtp()
    assert res.endpoint == "smtp.example.com"
    assert res.port == 587
    assert res.has_password is True


def _global_config_json(value: dict, name: str) -> dict:
    return {
        "id": 1,
        "created_at": 1699564800,
        "updated_at": 1699564800,
        "name": name,
        "value": value,
    }


def test_set_smtp_posts_body_and_decodes_config():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/smtp"
        assert b'"port":587' in req.content
        return httpx.Response(
            200,
            json=_global_config_json(
                {
                    "endpoint": "smtp.example.com",
                    "port": 587,
                    "username": "mailer",
                    "sender_email": "no-reply@example.com",
                    "password": "secret",
                },
                name="smtp_settings",
            ),
        )

    res = _client(handler).admin.global_config.set_smtp(_smtp_body())
    assert res.id == 1
    assert res.value.endpoint == "smtp.example.com"


def test_retrieve_domain_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/domain"
        return httpx.Response(200, json={"domain_name": "acme.example.com"})

    res = _client(handler).admin.global_config.retrieve_domain()
    assert res.domain_name == "acme.example.com"


def test_set_domain_posts_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/domain"
        assert b'"domain_name":"acme.example.com"' in req.content
        return httpx.Response(
            200,
            json=_global_config_json({"domain_name": "acme.example.com"}, name="domain_settings"),
        )

    body = DomainSettingsUpdateRequest(domain_name="acme.example.com")
    res = _client(handler).admin.global_config.set_domain(body)
    assert res.value.domain_name == "acme.example.com"


def test_retrieve_platform_updates_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/platform_updates"
        return httpx.Response(200, json={"automatic_update": False})

    res = _client(handler).admin.global_config.retrieve_platform_updates()
    assert res.automatic_update is False


def test_set_platform_updates_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/platform_updates"
        assert b'"automatic_update":false' in req.content
        return httpx.Response(200, json={"automatic_update": False})

    body = PlatformUpdateSettingsRequest(automatic_update=False)
    res = _client(handler).admin.global_config.set_platform_updates(body)
    assert res.automatic_update is False


def test_request_platform_manual_window_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/platform_updates/manual-window"
        assert b'"manual_window_start":100' in req.content
        return httpx.Response(
            200,
            json={"message": "scheduled", "manual_window_start": 100, "manual_window_end": 200},
        )

    body = PlatformManualWindowRequest(manual_window_start=100, manual_window_end=200)
    res = _client(handler).admin.global_config.request_platform_manual_window(body)
    assert res.message == "scheduled"
    assert res.manual_window_end == 200


def test_retrieve_pending_platform_updates_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/platform_updates/pending-updates"
        return httpx.Response(200, json={"pending_updates": ["a", "b"]})

    res = _client(handler).admin.global_config.retrieve_pending_platform_updates()
    assert res.pending_updates == ["a", "b"]


def test_retrieve_app_maintenance_window_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/application_maintenance_window"
        return httpx.Response(200, json={"windows": []})

    res = _client(handler).admin.global_config.retrieve_app_maintenance_window()
    assert res.windows == []


def test_set_app_maintenance_window_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/application_maintenance_window"
        assert b'"hour":2' in req.content
        return httpx.Response(
            200,
            json=_global_config_json(
                {"windows": [{"hour": 2, "minute": 30, "days_of_week": ["Monday"]}]},
                name="application_maintenance_window",
            ),
        )

    body = ApplicationMaintenanceWindowCreateRequest(
        windows=[ScheduledTimeMoment(hour=2, minute=30, days_of_week=["monday"])]
    )
    res = _client(handler).admin.global_config.set_app_maintenance_window(body)
    assert res.value.windows[0].hour == 2


def test_retrieve_infra_update_window_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/infrastructure_update_window"
        return httpx.Response(200, json={"windows": []})

    res = _client(handler).admin.global_config.retrieve_infra_update_window()
    assert res.windows == []


def test_set_infra_update_window_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/infrastructure_update_window"
        assert b'"hour":3' in req.content
        return httpx.Response(
            200,
            json=_global_config_json(
                {"windows": [{"hour": 3, "minute": 0, "days_of_week": ["Tuesday"]}]},
                name="infrastructure_update_window",
            ),
        )

    body = InfrastructureUpdateWindowCreateRequest(
        windows=[ScheduledTimeMoment(hour=3, minute=0, days_of_week=["tuesday"])]
    )
    res = _client(handler).admin.global_config.set_infra_update_window(body)
    assert res.value.windows[0].hour == 3


def test_retrieve_backup_destination_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/backup_destination"
        return httpx.Response(200, json={"type": "s3", "enabled": True})

    res = _client(handler).admin.global_config.retrieve_backup_destination()
    assert res.type == "s3"
    assert res.enabled is True


def test_set_backup_destination_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_destination"
        assert b'"type":"s3"' in req.content
        return httpx.Response(
            200,
            json=_global_config_json({"type": "s3", "enabled": True}, name="backup_destination"),
        )

    body = BackupDestinationCreateRequest(type="s3", enabled=True)
    res = _client(handler).admin.global_config.set_backup_destination(body)
    assert res.value.type == "s3"


def _backup_slot() -> BackupTimeSlot:
    return BackupTimeSlot(
        hour=1,
        minute=15,
        recurring_frequency=1,
        recurring_type="day",
        retention_length=30,
        retention_type="day",
    )


def test_retrieve_backup_schedule_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/backup_schedule"
        return httpx.Response(
            200,
            json={
                "schedules": [
                    {
                        "hour": 1,
                        "minute": 15,
                        "recurring_frequency": 1,
                        "recurring_type": "day",
                        "retention_length": 30,
                        "retention_type": "day",
                    }
                ]
            },
        )

    res = _client(handler).admin.global_config.retrieve_backup_schedule()
    assert res.schedules[0].hour == 1


def test_set_backup_schedule_posts_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_schedule"
        assert b'"hour":1' in req.content
        return httpx.Response(
            200,
            json=_global_config_json(
                {
                    "schedules": [
                        {
                            "hour": 1,
                            "minute": 15,
                            "recurring_frequency": 1,
                            "recurring_type": "day",
                            "retention_length": 30,
                            "retention_type": "day",
                        }
                    ]
                },
                name="backup_schedule",
            ),
        )

    body = BackupScheduleCreateRequest(schedules=[_backup_slot()])
    res = _client(handler).admin.global_config.set_backup_schedule(body)
    assert res.value.schedules[0].hour == 1


def test_retrieve_backup_notification_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/admin/settings/backup_notification"
        return httpx.Response(200, json={"enabled": True, "recipients": ["a@x.com"]})

    res = _client(handler).admin.global_config.retrieve_backup_notification()
    assert res.enabled is True
    assert res.recipients == ["a@x.com"]


def test_set_backup_notification_posts_body_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_notification"
        assert b'"enabled":true' in req.content
        return httpx.Response(200, json={"status": "saved"})

    body = BackupNotificationCreateRequest(enabled=True, recipients=["a@x.com"])
    res = _client(handler).admin.global_config.set_backup_notification(body)
    assert res["status"] == "saved"


def test_check_smtp_configured_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/smtp_configured"
        return httpx.Response(200, json={"configured": True})

    res = _client(handler).admin.global_config.check_smtp_configured()
    assert res["configured"] is True


def test_list_backup_logs_passes_query_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/backup_logs"
        assert req.url.params["page"] == "2"
        assert req.url.params["page_size"] == "10"
        return httpx.Response(
            200,
            json={
                "page": 2,
                "page_size": 10,
                "total": 0,
                "total_pages": 0,
                "has_next": False,
                "has_prev": True,
                "logs": [],
            },
        )

    res = _client(handler).admin.global_config.list_backup_logs(page=2, page_size=10)
    assert res.page == 2
    assert res.logs == []


def test_list_backup_logs_omits_query_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "page" not in req.url.params
        assert "page_size" not in req.url.params
        return httpx.Response(
            200,
            json={
                "page": 1,
                "page_size": 20,
                "total": 0,
                "total_pages": 0,
                "has_next": False,
                "has_prev": False,
                "logs": [],
            },
        )

    res = _client(handler).admin.global_config.list_backup_logs()
    assert res.page == 1


def test_trigger_backup_run_posts_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_run"
        return httpx.Response(200, json={"message": "started", "workflow_id": "wf1"})

    res = _client(handler).admin.global_config.trigger_backup_run()
    assert res.workflow_id == "wf1"


def test_cancel_backup_run_uses_path_param_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_logs/42/cancel"
        return httpx.Response(
            200,
            json={
                "message": "cancelled",
                "log_id": 42,
                "workflow_id": "wf1",
                "status": "cancelled",
            },
        )

    res = _client(handler).admin.global_config.cancel_backup_run("42")
    assert res.log_id == 42
    assert res.status == "cancelled"


def test_trigger_backup_cleanup_posts_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/settings/backup_cleanup"
        return httpx.Response(200, json={"message": "cleaned", "workflow_id": "wf2"})

    res = _client(handler).admin.global_config.trigger_backup_cleanup()
    assert res.workflow_id == "wf2"


def test_get_n8n_credentials_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/n8n-credentials"
        return httpx.Response(200, json={"email": "admin@x.com", "password": "pw"})

    res = _client(handler).admin.global_config.get_n8n_credentials()
    assert res.email == "admin@x.com"
    assert res.password == "pw"


async def test_async_global_config_retrieve_smtp_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/settings/smtp"
        return httpx.Response(
            200,
            json={
                "endpoint": "smtp.example.com",
                "port": 25,
                "username": "mailer",
                "sender_email": "no-reply@example.com",
                "has_password": False,
            },
        )

    client = _aclient(handler)
    try:
        res = await client.admin.global_config.retrieve_smtp()
        assert res.endpoint == "smtp.example.com"
        assert res.port == 25
    finally:
        await client.aclose()
