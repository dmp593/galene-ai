"""`conversations` resource: manage user conversations, messages, and results."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AttachmentListResponse,
    ConversationModel,
    ConversationUpdate,
    CreateConversationResponse,
    ItemConversationResponse,
    SQLResultResponse,
)

# Module-scope aliases: the `list` method below shadows the builtin `list` inside the
# class namespace, so annotations like `list[AttachmentListResponse]` on *other* methods
# would resolve to the method. These aliases are evaluated in module scope where `list`
# is the builtin.
_AttachmentList = list[AttachmentListResponse]
_SQLResultList = list[SQLResultResponse]


class Conversations(SyncResource):
    """List, create, retrieve, update, and delete conversations and their messages."""

    namespace: ClassVar[str] = "conversations"

    @operation("_list_conversations_get")
    def list(self) -> list[ItemConversationResponse]:
        """List User Conversations."""
        return cast(
            list[ItemConversationResponse],
            self._client.get(
                "/conversations",
                cast_to=list[ItemConversationResponse],
                envelope=True,
            ),
        )

    @operation("_init_conversation_init_get")
    def init(self) -> CreateConversationResponse:
        """Initialize New Conversation."""
        return cast(
            CreateConversationResponse,
            self._client.get(
                "/conversation/init",
                cast_to=CreateConversationResponse,
                envelope=True,
            ),
        )

    @operation("_get_conversation__conversation_id__get")
    def retrieve(self, conversation_id: str) -> ConversationModel:
        """Get Conversation Details."""
        return cast(
            ConversationModel,
            self._client.get(
                f"/conversation/{conversation_id}",
                cast_to=ConversationModel,
                envelope=True,
            ),
        )

    @operation("_update_conversation__conversation_id__patch")
    def update(self, conversation_id: str, *, body: ConversationUpdate) -> dict[str, Any]:
        """Update Conversation Settings."""
        return cast(
            dict[str, Any],
            self._client.patch(
                f"/conversation/{conversation_id}",
                json_body=body,
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_delete_conversation__conversation_id__delete")
    def delete(self, conversation_id: str) -> None:
        """Delete Conversation."""
        self._client.delete(
            f"/conversation/{conversation_id}",
            cast_to=dict,
            envelope=True,
        )

    @operation("_attachments_conversation__conversation_id__attachments_get")
    def attachments(self, conversation_id: str) -> _AttachmentList:
        """Get Conversation Attachments."""
        return cast(
            list[AttachmentListResponse],
            self._client.get(
                f"/conversation/{conversation_id}/attachments",
                cast_to=list[AttachmentListResponse],
                envelope=True,
            ),
        )

    @operation("_reference_conversation__conversation_id__message__index__add_references_get")
    def add_references(self, conversation_id: str, index: str) -> dict[str, Any]:
        """Add References to Message."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/conversation/{conversation_id}/message/{index}/add_references",
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_delete_message_conversation__conversation_id__message__message_id__delete")
    def delete_message(self, conversation_id: str, message_id: str) -> None:
        """Delete Message."""
        self._client.delete(
            f"/conversation/{conversation_id}/message/{message_id}",
            cast_to=dict,
            envelope=True,
        )

    @operation("_sanitize_message_conversation__conversation_id__message__message_id__sanitize_get")
    def sanitize_message(self, conversation_id: str, message_id: str) -> dict[str, Any]:
        """Sanitize Message Content."""
        return cast(
            dict[str, Any],
            self._client.get(
                f"/conversation/{conversation_id}/message/{message_id}/sanitize",
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_get_sql_results_conversation__conversation_id__sql_results__result_id__get")
    def sql_results(self, conversation_id: str, result_id: str) -> _SQLResultList:
        """Get SQL / Data Analysis Results."""
        return cast(
            list[SQLResultResponse],
            self._client.get(
                f"/conversation/{conversation_id}/sql-results/{result_id}",
                cast_to=list[SQLResultResponse],
                envelope=True,
            ),
        )


class AsyncConversations(AsyncResource):
    """Async counterpart of `Conversations`."""

    namespace: ClassVar[str] = "conversations"

    @operation("_list_conversations_get")
    async def list(self) -> list[ItemConversationResponse]:
        """List User Conversations."""
        return cast(
            list[ItemConversationResponse],
            await self._client.get(
                "/conversations",
                cast_to=list[ItemConversationResponse],
                envelope=True,
            ),
        )

    @operation("_init_conversation_init_get")
    async def init(self) -> CreateConversationResponse:
        """Initialize New Conversation."""
        return cast(
            CreateConversationResponse,
            await self._client.get(
                "/conversation/init",
                cast_to=CreateConversationResponse,
                envelope=True,
            ),
        )

    @operation("_get_conversation__conversation_id__get")
    async def retrieve(self, conversation_id: str) -> ConversationModel:
        """Get Conversation Details."""
        return cast(
            ConversationModel,
            await self._client.get(
                f"/conversation/{conversation_id}",
                cast_to=ConversationModel,
                envelope=True,
            ),
        )

    @operation("_update_conversation__conversation_id__patch")
    async def update(self, conversation_id: str, *, body: ConversationUpdate) -> dict[str, Any]:
        """Update Conversation Settings."""
        return cast(
            dict[str, Any],
            await self._client.patch(
                f"/conversation/{conversation_id}",
                json_body=body,
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_delete_conversation__conversation_id__delete")
    async def delete(self, conversation_id: str) -> None:
        """Delete Conversation."""
        await self._client.delete(
            f"/conversation/{conversation_id}",
            cast_to=dict,
            envelope=True,
        )

    @operation("_attachments_conversation__conversation_id__attachments_get")
    async def attachments(self, conversation_id: str) -> _AttachmentList:
        """Get Conversation Attachments."""
        return cast(
            list[AttachmentListResponse],
            await self._client.get(
                f"/conversation/{conversation_id}/attachments",
                cast_to=list[AttachmentListResponse],
                envelope=True,
            ),
        )

    @operation("_reference_conversation__conversation_id__message__index__add_references_get")
    async def add_references(self, conversation_id: str, index: str) -> dict[str, Any]:
        """Add References to Message."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/conversation/{conversation_id}/message/{index}/add_references",
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_delete_message_conversation__conversation_id__message__message_id__delete")
    async def delete_message(self, conversation_id: str, message_id: str) -> None:
        """Delete Message."""
        await self._client.delete(
            f"/conversation/{conversation_id}/message/{message_id}",
            cast_to=dict,
            envelope=True,
        )

    @operation("_sanitize_message_conversation__conversation_id__message__message_id__sanitize_get")
    async def sanitize_message(self, conversation_id: str, message_id: str) -> dict[str, Any]:
        """Sanitize Message Content."""
        return cast(
            dict[str, Any],
            await self._client.get(
                f"/conversation/{conversation_id}/message/{message_id}/sanitize",
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("_get_sql_results_conversation__conversation_id__sql_results__result_id__get")
    async def sql_results(self, conversation_id: str, result_id: str) -> _SQLResultList:
        """Get SQL / Data Analysis Results."""
        return cast(
            list[SQLResultResponse],
            await self._client.get(
                f"/conversation/{conversation_id}/sql-results/{result_id}",
                cast_to=list[SQLResultResponse],
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(Conversations)
AsyncGalene._NAMESPACES.append(AsyncConversations)
