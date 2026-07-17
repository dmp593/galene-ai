"""`admin.tickets` resource: platform support ticket administration."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    PlatformTicketDetailResponse,
    TicketListItemResponse,
    UpdateTicketStatusRequest,
)


def _reply_form(content: str, new_status: str, message_uuid: str | None) -> dict[str, str]:
    form = {"content": content, "new_status": new_status}
    if message_uuid is not None:
        form["message_uuid"] = message_uuid
    return form


def _reply_files(files: Sequence[bytes] | None) -> list[tuple[str, tuple[str, bytes]]]:
    if not files:
        return []
    return [("files", (f"attachment-{i}", content)) for i, content in enumerate(files)]


class Tickets(SyncResource):
    """Administer platform support tickets."""

    namespace: ClassVar[str] = "tickets"

    @operation("list_all_tickets_admin_platform_tickets_admin_all_get")
    def list(self) -> list[TicketListItemResponse]:
        """Get all tickets (Admin only)."""
        return cast(
            list[TicketListItemResponse],
            self._client.get(
                "/platform-tickets/admin/all",
                cast_to=list[TicketListItemResponse],
                envelope=True,
            ),
        )

    @operation("get_ticket_detail_admin_platform_tickets_admin__ticket_uuid__get")
    def retrieve(self, ticket_uuid: str) -> PlatformTicketDetailResponse:
        """Get ticket detail as admin."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}",
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("update_ticket_status_admin_platform_tickets_admin__ticket_uuid__status_put")
    def update_status(
        self, ticket_uuid: str, *, body: UpdateTicketStatusRequest
    ) -> PlatformTicketDetailResponse:
        """Update ticket status (Admin only)."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.put(
                f"/platform-tickets/admin/{ticket_uuid}/status",
                json_body=body,
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("delete_ticket_admin_platform_tickets_admin__ticket_uuid__delete")
    def delete(self, ticket_uuid: str) -> None:
        """Delete ticket as admin."""
        self._client.delete(
            f"/platform-tickets/admin/{ticket_uuid}",
            cast_to=dict,
            envelope=True,
        )

    @operation("admin_reply_ticket_platform_tickets_admin__ticket_uuid__reply_post")
    def reply(
        self,
        ticket_uuid: str,
        *,
        content: str,
        new_status: str,
        message_uuid: str | None = None,
        files: Sequence[bytes] | None = None,
    ) -> PlatformTicketDetailResponse:
        """Reply to ticket as admin."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.post(
                f"/platform-tickets/admin/{ticket_uuid}/reply",
                data=_reply_form(content, new_status, message_uuid),
                files=_reply_files(files),
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_admin_ticket_attachment_platform_tickets_admin"
        "__ticket_uuid__attachments__attachment_uuid__get"
    )
    def download_attachment(self, ticket_uuid: str, attachment_uuid: str) -> dict[str, Any]:
        """Download a ticket attachment (Admin)."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("export_ticket_conversation_platform_tickets_admin__ticket_uuid__export_get")
    def export(self, ticket_uuid: str) -> dict[str, Any]:
        """Export ticket conversation (Admin only)."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}/export",
                cast_to=dict,
                envelope=True,
            ),
        )


class AsyncTickets(AsyncResource):
    """Async counterpart of `Tickets`."""

    namespace: ClassVar[str] = "tickets"

    @operation("list_all_tickets_admin_platform_tickets_admin_all_get")
    async def list(self) -> list[TicketListItemResponse]:
        """Get all tickets (Admin only)."""
        return cast(
            list[TicketListItemResponse],
            await self._client.get(
                "/platform-tickets/admin/all",
                cast_to=list[TicketListItemResponse],
                envelope=True,
            ),
        )

    @operation("get_ticket_detail_admin_platform_tickets_admin__ticket_uuid__get")
    async def retrieve(self, ticket_uuid: str) -> PlatformTicketDetailResponse:
        """Get ticket detail as admin."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}",
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("update_ticket_status_admin_platform_tickets_admin__ticket_uuid__status_put")
    async def update_status(
        self, ticket_uuid: str, *, body: UpdateTicketStatusRequest
    ) -> PlatformTicketDetailResponse:
        """Update ticket status (Admin only)."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.put(
                f"/platform-tickets/admin/{ticket_uuid}/status",
                json_body=body,
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("delete_ticket_admin_platform_tickets_admin__ticket_uuid__delete")
    async def delete(self, ticket_uuid: str) -> None:
        """Delete ticket as admin."""
        await self._client.delete(
            f"/platform-tickets/admin/{ticket_uuid}",
            cast_to=dict,
            envelope=True,
        )

    @operation("admin_reply_ticket_platform_tickets_admin__ticket_uuid__reply_post")
    async def reply(
        self,
        ticket_uuid: str,
        *,
        content: str,
        new_status: str,
        message_uuid: str | None = None,
        files: Sequence[bytes] | None = None,
    ) -> PlatformTicketDetailResponse:
        """Reply to ticket as admin."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.post(
                f"/platform-tickets/admin/{ticket_uuid}/reply",
                data=_reply_form(content, new_status, message_uuid),
                files=_reply_files(files),
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_admin_ticket_attachment_platform_tickets_admin"
        "__ticket_uuid__attachments__attachment_uuid__get"
    )
    async def download_attachment(self, ticket_uuid: str, attachment_uuid: str) -> dict[str, Any]:
        """Download a ticket attachment (Admin)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("export_ticket_conversation_platform_tickets_admin__ticket_uuid__export_get")
    async def export(self, ticket_uuid: str) -> dict[str, Any]:
        """Export ticket conversation (Admin only)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/platform-tickets/admin/{ticket_uuid}/export",
                cast_to=dict,
                envelope=True,
            ),
        )


Galene._ADMIN_NAMESPACES.append(Tickets)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncTickets)
