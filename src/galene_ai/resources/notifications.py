"""`notifications` resource: delivery/read state and summaries for user and
platform-ticket notifications.

Every operation's 200 response is an enveloped `WSResponse_*`-style payload
(`{success, message, result}`), so each is decoded with `envelope=True,
cast_to=dict` (raising `GaleneError` on `success: false`). The summary
operations return the unwrapped `result` as a `dict[str, Any]`; the
mark-delivered/mark-read operations have a `null` result (`WSResponse[NoneType]`)
and return `None`.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation


class Notifications(SyncResource):
    """User and platform-ticket notification delivery, read state, and summaries."""

    namespace: ClassVar[str] = "notifications"

    @operation("_delivered_notification__notification_id__delivered_get")
    def mark_delivered(self, notification_id: str) -> None:
        """Mark Notification as Delivered."""
        self._client.get(f"/notification/{notification_id}/delivered", cast_to=dict, envelope=True)

    @operation("get_user_notifications_summary_notifications__mode__summary_get")
    def summary(self, mode: str) -> dict[str, Any]:
        """Get notifications summary."""
        return cast(
            "dict[str, Any]",
            self._client.get(f"/notifications/{mode}/summary", cast_to=dict, envelope=True),
        )

    @operation("mark_user_notifications_as_read_notifications_mark_read_post")
    def mark_read(self, body: list[str]) -> None:
        """Mark notifications as read."""
        self._client.post("/notifications/mark-read", json_body=body, cast_to=dict, envelope=True)

    @operation("get_user_notifications_summary_platform_tickets_notifications_summary_get")
    def platform_summary(self) -> dict[str, Any]:
        """Get notifications summary."""
        return cast(
            "dict[str, Any]",
            self._client.get(
                "/platform-tickets/notifications/summary", cast_to=dict, envelope=True
            ),
        )

    @operation("mark_user_notifications_as_read_platform_tickets_notifications_mark_read_post")
    def platform_mark_read(self, body: list[str]) -> None:
        """Mark notifications as read."""
        self._client.post(
            "/platform-tickets/notifications/mark-read",
            json_body=body,
            cast_to=dict,
            envelope=True,
        )


class AsyncNotifications(AsyncResource):
    """Async counterpart of `Notifications`."""

    namespace: ClassVar[str] = "notifications"

    @operation("_delivered_notification__notification_id__delivered_get")
    async def mark_delivered(self, notification_id: str) -> None:
        """Mark Notification as Delivered."""
        await self._client.get(
            f"/notification/{notification_id}/delivered", cast_to=dict, envelope=True
        )

    @operation("get_user_notifications_summary_notifications__mode__summary_get")
    async def summary(self, mode: str) -> dict[str, Any]:
        """Get notifications summary."""
        return cast(
            "dict[str, Any]",
            await self._client.get(f"/notifications/{mode}/summary", cast_to=dict, envelope=True),
        )

    @operation("mark_user_notifications_as_read_notifications_mark_read_post")
    async def mark_read(self, body: list[str]) -> None:
        """Mark notifications as read."""
        await self._client.post(
            "/notifications/mark-read", json_body=body, cast_to=dict, envelope=True
        )

    @operation("get_user_notifications_summary_platform_tickets_notifications_summary_get")
    async def platform_summary(self) -> dict[str, Any]:
        """Get notifications summary."""
        return cast(
            "dict[str, Any]",
            await self._client.get(
                "/platform-tickets/notifications/summary", cast_to=dict, envelope=True
            ),
        )

    @operation("mark_user_notifications_as_read_platform_tickets_notifications_mark_read_post")
    async def platform_mark_read(self, body: list[str]) -> None:
        """Mark notifications as read."""
        await self._client.post(
            "/platform-tickets/notifications/mark-read",
            json_body=body,
            cast_to=dict,
            envelope=True,
        )


Galene._NAMESPACES.append(Notifications)
AsyncGalene._NAMESPACES.append(AsyncNotifications)
