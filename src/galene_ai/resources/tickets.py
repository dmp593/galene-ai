"""`tickets` resource: platform support tickets and admin (Zammad) support tickets.

Covers the user-facing `/platform-tickets/*` endpoints (create/list/retrieve/update/
delete/reply/download) and the admin `/admin/support-tickets/*` endpoints
(list/create/detail/reply/escalate/download) which bridge to Zammad.

Several responses are enveloped (`{success, message, result}`); those are decoded with
`envelope=True` so `_core.envelope.unwrap` raises `GaleneError` on `success: false`.
Attachment-download operations have an empty (untyped) 200 schema in `spec/openapi.json`,
so they are decoded as a plain `dict` per the pre-computed directives.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    CreateTicketResponse,
    PlatformTicketDetailResponse,
    TicketListItemResponse,
    UpdateTicketRequest,
    ZammadTicketResponse,
)

# A file to upload: (filename, content) pairs, sent under the multipart `files` field.
FilePart = tuple[str, bytes]
# Module-level alias so method signatures don't reference the builtin `list` by name:
# the `list()` methods below shadow it inside the class body, breaking annotations.
FileUploads = list[FilePart]
# An httpx multipart part: text field -> (None, value); file -> (filename, content).
_MultipartPart = tuple[str, tuple[str | None, Any]]


def _multipart(fields: dict[str, Any], files: FileUploads | None) -> list[_MultipartPart]:
    """Build httpx multipart `files` entries from text fields + uploads.

    Text fields are emitted as `(name, (None, value))` parts (dropping unset `None`
    values) so the request is encoded as `multipart/form-data` even when no file is
    attached; uploads go under the repeated `files` field.
    """
    parts: list[_MultipartPart] = [(k, (None, v)) for k, v in fields.items() if v is not None]
    if files:
        parts += [("files", (name, content)) for name, content in files]
    return parts


class Tickets(SyncResource):
    """Manage platform support tickets and admin (Zammad) support tickets."""

    namespace: ClassVar[str] = "tickets"

    # -- admin / Zammad support tickets ---------------------------------
    @operation("list_organization_tickets_admin_admin_support_tickets__get")
    def list_organization(self) -> dict[str, Any]:
        """List organization support tickets (Admin)."""
        return cast(
            "dict[str, Any]",
            self._client.get("/admin/support-tickets/", cast_to=dict, envelope=True),
        )

    @operation("create_support_ticket_admin_admin_support_tickets__post")
    def create_zammad_ticket(
        self,
        *,
        title: str,
        content: str,
        category: str | None = None,
        severity: str | None = None,
        files: FileUploads | None = None,
    ) -> ZammadTicketResponse:
        """Create support ticket in Zammad (Admin)."""
        return cast(
            ZammadTicketResponse,
            self._client.post(
                "/admin/support-tickets/",
                files=_multipart(
                    {
                        "title": title,
                        "content": content,
                        "category": category,
                        "severity": severity,
                    },
                    files,
                ),
                cast_to=ZammadTicketResponse,
                envelope=True,
            ),
        )

    @operation("get_support_ticket_detail_admin_admin_support_tickets__platform_ticket_uuid__get")
    def retrieve_admin(self, platform_ticket_uuid: str) -> dict[str, Any]:
        """Get support ticket details (Admin)."""
        return cast(
            "dict[str, Any]",
            self._client.get(
                f"/admin/support-tickets/{platform_ticket_uuid}", cast_to=dict, envelope=True
            ),
        )

    @operation(
        "reply_to_support_ticket_admin_admin_support_tickets__platform_ticket_uuid__answer_post"
    )
    def reply_admin(
        self,
        platform_ticket_uuid: str,
        *,
        content: str,
        files: FileUploads | None = None,
    ) -> dict[str, Any]:
        """Reply to support ticket (Admin)."""
        return cast(
            "dict[str, Any]",
            self._client.post(
                f"/admin/support-tickets/{platform_ticket_uuid}/answer",
                files=_multipart({"content": content}, files),
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation(
        "escalate_platform_ticket_to_zammad_endpoint_admin_support_tickets_escalate__platform_ticket_uuid__post"
    )
    def escalate(self, platform_ticket_uuid: str) -> ZammadTicketResponse:
        """Escalate platform ticket to Zammad (Admin)."""
        return cast(
            ZammadTicketResponse,
            self._client.post(
                f"/admin/support-tickets/escalate/{platform_ticket_uuid}",
                cast_to=ZammadTicketResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_support_ticket_attachment_admin_support_tickets__support_ticket_uuid__attachments__attachment_uuid__get"
    )
    def download_admin_attachment(
        self, support_ticket_uuid: str, attachment_uuid: str
    ) -> dict[str, Any]:
        """Download a support ticket attachment (fast path)."""
        return cast(
            "dict[str, Any]",
            self._client.get(  # spec: untyped response
                f"/admin/support-tickets/{support_ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,
            ),
        )

    @operation(
        "download_zammad_attachment_lazy_admin_support_tickets__support_ticket_uuid__articles__article_id__zammad_attachments__zammad_attachment_id__get"
    )
    def download_zammad_attachment(
        self,
        support_ticket_uuid: str,
        article_id: str,
        zammad_attachment_id: str,
        *,
        filename: str | None = None,
        mime_type: str | None = None,
    ) -> dict[str, Any]:
        """Download a Zammad-hosted attachment (lazy cache)."""
        return cast(
            "dict[str, Any]",
            self._client.get(  # spec: untyped response
                f"/admin/support-tickets/{support_ticket_uuid}/articles/{article_id}"
                f"/zammad-attachments/{zammad_attachment_id}",
                params={"filename": filename, "mime_type": mime_type},
                cast_to=dict,
            ),
        )

    # -- platform (user) tickets ----------------------------------------
    @operation("list_user_tickets_platform_tickets__get")
    def list(self) -> list[TicketListItemResponse]:
        """Get current user's tickets."""
        return cast(
            "list[TicketListItemResponse]",
            self._client.get(
                "/platform-tickets/", cast_to=list[TicketListItemResponse], envelope=True
            ),
        )

    @operation("create_user_ticket_platform_tickets__post")
    def create(
        self,
        *,
        title: str,
        content: str,
        category: str | None = None,
        severity: str | None = None,
        conversation_id: str | None = None,
        files: FileUploads | None = None,
    ) -> CreateTicketResponse:
        """Create a new support ticket."""
        return cast(
            CreateTicketResponse,
            self._client.post(
                "/platform-tickets/",
                files=_multipart(
                    {
                        "title": title,
                        "content": content,
                        "category": category,
                        "severity": severity,
                        "conversation_id": conversation_id,
                    },
                    files,
                ),
                cast_to=CreateTicketResponse,
                envelope=True,
            ),
        )

    @operation("get_user_ticket_detail_platform_tickets__ticket_uuid__get")
    def retrieve(self, ticket_uuid: str) -> PlatformTicketDetailResponse:
        """Get ticket detail."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.get(
                f"/platform-tickets/{ticket_uuid}",
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("update_user_ticket_platform_tickets__ticket_uuid__put")
    def update(
        self, ticket_uuid: str, *, body: UpdateTicketRequest
    ) -> PlatformTicketDetailResponse:
        """Update ticket (user only)."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.put(
                f"/platform-tickets/{ticket_uuid}",
                json_body=body,
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("delete_user_ticket_platform_tickets__ticket_uuid__delete")
    def delete(self, ticket_uuid: str) -> None:
        """Delete a ticket."""
        self._client.delete(f"/platform-tickets/{ticket_uuid}", cast_to=dict, envelope=True)

    @operation("reply_to_ticket_as_user_platform_tickets__ticket_uuid__reply_post")
    def reply(
        self,
        ticket_uuid: str,
        *,
        content: str,
        files: FileUploads | None = None,
    ) -> PlatformTicketDetailResponse:
        """Reply to a ticket as user."""
        return cast(
            PlatformTicketDetailResponse,
            self._client.post(
                f"/platform-tickets/{ticket_uuid}/reply",
                files=_multipart({"content": content}, files),
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_user_ticket_attachment_platform_tickets__ticket_uuid__attachments__attachment_uuid__get"
    )
    def download_attachment(self, ticket_uuid: str, attachment_uuid: str) -> dict[str, Any]:
        """Download a ticket attachment."""
        return cast(
            "dict[str, Any]",
            self._client.get(  # spec: untyped response
                f"/platform-tickets/{ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,
            ),
        )


class AsyncTickets(AsyncResource):
    """Async counterpart of `Tickets`."""

    namespace: ClassVar[str] = "tickets"

    # -- admin / Zammad support tickets ---------------------------------
    @operation("list_organization_tickets_admin_admin_support_tickets__get")
    async def list_organization(self) -> dict[str, Any]:
        """List organization support tickets (Admin)."""
        return cast(
            "dict[str, Any]",
            await self._client.get("/admin/support-tickets/", cast_to=dict, envelope=True),
        )

    @operation("create_support_ticket_admin_admin_support_tickets__post")
    async def create_zammad_ticket(
        self,
        *,
        title: str,
        content: str,
        category: str | None = None,
        severity: str | None = None,
        files: FileUploads | None = None,
    ) -> ZammadTicketResponse:
        """Create support ticket in Zammad (Admin)."""
        return cast(
            ZammadTicketResponse,
            await self._client.post(
                "/admin/support-tickets/",
                files=_multipart(
                    {
                        "title": title,
                        "content": content,
                        "category": category,
                        "severity": severity,
                    },
                    files,
                ),
                cast_to=ZammadTicketResponse,
                envelope=True,
            ),
        )

    @operation("get_support_ticket_detail_admin_admin_support_tickets__platform_ticket_uuid__get")
    async def retrieve_admin(self, platform_ticket_uuid: str) -> dict[str, Any]:
        """Get support ticket details (Admin)."""
        return cast(
            "dict[str, Any]",
            await self._client.get(
                f"/admin/support-tickets/{platform_ticket_uuid}", cast_to=dict, envelope=True
            ),
        )

    @operation(
        "reply_to_support_ticket_admin_admin_support_tickets__platform_ticket_uuid__answer_post"
    )
    async def reply_admin(
        self,
        platform_ticket_uuid: str,
        *,
        content: str,
        files: FileUploads | None = None,
    ) -> dict[str, Any]:
        """Reply to support ticket (Admin)."""
        return cast(
            "dict[str, Any]",
            await self._client.post(
                f"/admin/support-tickets/{platform_ticket_uuid}/answer",
                files=_multipart({"content": content}, files),
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation(
        "escalate_platform_ticket_to_zammad_endpoint_admin_support_tickets_escalate__platform_ticket_uuid__post"
    )
    async def escalate(self, platform_ticket_uuid: str) -> ZammadTicketResponse:
        """Escalate platform ticket to Zammad (Admin)."""
        return cast(
            ZammadTicketResponse,
            await self._client.post(
                f"/admin/support-tickets/escalate/{platform_ticket_uuid}",
                cast_to=ZammadTicketResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_support_ticket_attachment_admin_support_tickets__support_ticket_uuid__attachments__attachment_uuid__get"
    )
    async def download_admin_attachment(
        self, support_ticket_uuid: str, attachment_uuid: str
    ) -> dict[str, Any]:
        """Download a support ticket attachment (fast path)."""
        return cast(
            "dict[str, Any]",
            await self._client.get(  # spec: untyped response
                f"/admin/support-tickets/{support_ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,
            ),
        )

    @operation(
        "download_zammad_attachment_lazy_admin_support_tickets__support_ticket_uuid__articles__article_id__zammad_attachments__zammad_attachment_id__get"
    )
    async def download_zammad_attachment(
        self,
        support_ticket_uuid: str,
        article_id: str,
        zammad_attachment_id: str,
        *,
        filename: str | None = None,
        mime_type: str | None = None,
    ) -> dict[str, Any]:
        """Download a Zammad-hosted attachment (lazy cache)."""
        return cast(
            "dict[str, Any]",
            await self._client.get(  # spec: untyped response
                f"/admin/support-tickets/{support_ticket_uuid}/articles/{article_id}"
                f"/zammad-attachments/{zammad_attachment_id}",
                params={"filename": filename, "mime_type": mime_type},
                cast_to=dict,
            ),
        )

    # -- platform (user) tickets ----------------------------------------
    @operation("list_user_tickets_platform_tickets__get")
    async def list(self) -> list[TicketListItemResponse]:
        """Get current user's tickets."""
        return cast(
            "list[TicketListItemResponse]",
            await self._client.get(
                "/platform-tickets/", cast_to=list[TicketListItemResponse], envelope=True
            ),
        )

    @operation("create_user_ticket_platform_tickets__post")
    async def create(
        self,
        *,
        title: str,
        content: str,
        category: str | None = None,
        severity: str | None = None,
        conversation_id: str | None = None,
        files: FileUploads | None = None,
    ) -> CreateTicketResponse:
        """Create a new support ticket."""
        return cast(
            CreateTicketResponse,
            await self._client.post(
                "/platform-tickets/",
                files=_multipart(
                    {
                        "title": title,
                        "content": content,
                        "category": category,
                        "severity": severity,
                        "conversation_id": conversation_id,
                    },
                    files,
                ),
                cast_to=CreateTicketResponse,
                envelope=True,
            ),
        )

    @operation("get_user_ticket_detail_platform_tickets__ticket_uuid__get")
    async def retrieve(self, ticket_uuid: str) -> PlatformTicketDetailResponse:
        """Get ticket detail."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.get(
                f"/platform-tickets/{ticket_uuid}",
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("update_user_ticket_platform_tickets__ticket_uuid__put")
    async def update(
        self, ticket_uuid: str, *, body: UpdateTicketRequest
    ) -> PlatformTicketDetailResponse:
        """Update ticket (user only)."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.put(
                f"/platform-tickets/{ticket_uuid}",
                json_body=body,
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation("delete_user_ticket_platform_tickets__ticket_uuid__delete")
    async def delete(self, ticket_uuid: str) -> None:
        """Delete a ticket."""
        await self._client.delete(f"/platform-tickets/{ticket_uuid}", cast_to=dict, envelope=True)

    @operation("reply_to_ticket_as_user_platform_tickets__ticket_uuid__reply_post")
    async def reply(
        self,
        ticket_uuid: str,
        *,
        content: str,
        files: FileUploads | None = None,
    ) -> PlatformTicketDetailResponse:
        """Reply to a ticket as user."""
        return cast(
            PlatformTicketDetailResponse,
            await self._client.post(
                f"/platform-tickets/{ticket_uuid}/reply",
                files=_multipart({"content": content}, files),
                cast_to=PlatformTicketDetailResponse,
                envelope=True,
            ),
        )

    @operation(
        "download_user_ticket_attachment_platform_tickets__ticket_uuid__attachments__attachment_uuid__get"
    )
    async def download_attachment(self, ticket_uuid: str, attachment_uuid: str) -> dict[str, Any]:
        """Download a ticket attachment."""
        return cast(
            "dict[str, Any]",
            await self._client.get(  # spec: untyped response
                f"/platform-tickets/{ticket_uuid}/attachments/{attachment_uuid}",
                cast_to=dict,
            ),
        )


Galene._NAMESPACES.append(Tickets)
AsyncGalene._NAMESPACES.append(AsyncTickets)
