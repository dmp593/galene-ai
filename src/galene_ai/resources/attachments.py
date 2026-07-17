"""`attachments` resource: attachment chunks, conversation attach/detach, and lifecycle.

Every operation in this namespace has an empty (`{}`) 200 response schema in
`spec/openapi.json`, so responses are decoded untyped as `dict[str, Any]`.
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation


class Attachments(SyncResource):
    """Attachment chunks, conversation attach/detach, and lifecycle controls."""

    namespace: ClassVar[str] = "attachments"

    @operation(
        "_get_chunk_in_conversation_conversation__conversation_id__attachment_chunk__chunk_id__get"
    )
    def get_chunk_in_conversation(self, conversation_id: str, chunk_id: str) -> dict[str, Any]:
        """Get attachment chunk within conversation context (SECURE)."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/conversation/{conversation_id}/attachment/chunk/{chunk_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_get_chunk_attachment_chunk__chunk_id__get")
    def get_chunk(self, chunk_id: str) -> dict[str, Any]:
        """Get attachment chunk."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/chunk/{chunk_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_attach_to_conversation_attachment__file_id__attach_conversation__conversation_id__get"
    )
    def attach(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Attach file to conversation."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/attach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_detach_from_conversation_attachment__file_id__detach_conversation__conversation_id__get"
    )
    def detach(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Detach file from conversation."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/detach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_detach_from_conversation_delete_attachment__file_id__detach_conversation"
        "__conversation_id__delete"
    )
    def detach_delete(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Detach file from conversation (DELETE)."""
        return cast(
            dict[str, Any],
            self._client.delete(
                f"/attachment/{file_id}/detach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_enable_attachment__file_id__status_enable_get")
    def enable(self, file_id: str) -> dict[str, Any]:
        """Enable attachment."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/status/enable",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_disable_attachment__file_id__status_disable_get")
    def disable(self, file_id: str) -> dict[str, Any]:
        """Disable attachment."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/status/disable",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_presigned_attachment__file_id__presignedurl_get")
    def presigned_url(self, file_id: str) -> dict[str, Any]:
        """Get presigned download URL."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/presignedurl",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_download_media_transcription_attachment__file_id__transcription_get")
    def transcription(self, file_id: str) -> dict[str, Any]:
        """Download media transcription."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/attachment/{file_id}/transcription",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_retry_attachment_attachment__file_id__retry_post")
    def retry(self, file_id: str) -> dict[str, Any]:
        """Retry attachment ingestion."""
        return cast(
            dict[str, Any],
            self._client.post(
                f"/attachment/{file_id}/retry",
                cast_to=dict,  # spec: untyped response
            ),
        )


class AsyncAttachments(AsyncResource):
    """Async counterpart of `Attachments`."""

    namespace: ClassVar[str] = "attachments"

    @operation(
        "_get_chunk_in_conversation_conversation__conversation_id__attachment_chunk__chunk_id__get"
    )
    async def get_chunk_in_conversation(
        self, conversation_id: str, chunk_id: str
    ) -> dict[str, Any]:
        """Get attachment chunk within conversation context (SECURE)."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/conversation/{conversation_id}/attachment/chunk/{chunk_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_get_chunk_attachment_chunk__chunk_id__get")
    async def get_chunk(self, chunk_id: str) -> dict[str, Any]:
        """Get attachment chunk."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/chunk/{chunk_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_attach_to_conversation_attachment__file_id__attach_conversation__conversation_id__get"
    )
    async def attach(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Attach file to conversation."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/attach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_detach_from_conversation_attachment__file_id__detach_conversation__conversation_id__get"
    )
    async def detach(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Detach file from conversation."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/detach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation(
        "_detach_from_conversation_delete_attachment__file_id__detach_conversation"
        "__conversation_id__delete"
    )
    async def detach_delete(self, file_id: str, conversation_id: str) -> dict[str, Any]:
        """Detach file from conversation (DELETE)."""
        return cast(
            dict[str, Any],
            await self._client.delete(
                f"/attachment/{file_id}/detach/conversation/{conversation_id}",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_enable_attachment__file_id__status_enable_get")
    async def enable(self, file_id: str) -> dict[str, Any]:
        """Enable attachment."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/status/enable",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_disable_attachment__file_id__status_disable_get")
    async def disable(self, file_id: str) -> dict[str, Any]:
        """Disable attachment."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/status/disable",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_presigned_attachment__file_id__presignedurl_get")
    async def presigned_url(self, file_id: str) -> dict[str, Any]:
        """Get presigned download URL."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/presignedurl",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_download_media_transcription_attachment__file_id__transcription_get")
    async def transcription(self, file_id: str) -> dict[str, Any]:
        """Download media transcription."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/attachment/{file_id}/transcription",
                cast_to=dict,  # spec: untyped response
            ),
        )

    @operation("_retry_attachment_attachment__file_id__retry_post")
    async def retry(self, file_id: str) -> dict[str, Any]:
        """Retry attachment ingestion."""
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/attachment/{file_id}/retry",
                cast_to=dict,  # spec: untyped response
            ),
        )


Galene._NAMESPACES.append(Attachments)
AsyncGalene._NAMESPACES.append(AsyncAttachments)
