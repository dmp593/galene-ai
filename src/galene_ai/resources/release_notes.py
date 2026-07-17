"""`release_notes` resource: fetch unseen release notes and mark them seen."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import MarkSeenRequest


class ReleaseNotes(SyncResource):
    """Retrieve unseen release notes and record the last seen version."""

    namespace: ClassVar[str] = "release_notes"

    @operation("get_unseen_release_notes_release_notes_unseen_get")
    def unseen(self, *, audience: str | None = None) -> dict[str, Any]:
        """Get unseen release notes."""
        return cast(
            "dict[str, Any]",
            self._client.get(
                "/release-notes/unseen",
                params={"audience": audience},
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("mark_release_notes_seen_release_notes_seen_post")
    def seen(self, body: MarkSeenRequest) -> None:
        """Mark release notes as seen."""
        self._client.post(
            "/release-notes/seen",
            json_body=body,
            cast_to=dict,
            envelope=True,
        )


class AsyncReleaseNotes(AsyncResource):
    """Async counterpart of `ReleaseNotes`."""

    namespace: ClassVar[str] = "release_notes"

    @operation("get_unseen_release_notes_release_notes_unseen_get")
    async def unseen(self, *, audience: str | None = None) -> dict[str, Any]:
        """Get unseen release notes."""
        return cast(
            "dict[str, Any]",
            await self._client.get(
                "/release-notes/unseen",
                params={"audience": audience},
                cast_to=dict,
                envelope=True,
            ),
        )

    @operation("mark_release_notes_seen_release_notes_seen_post")
    async def seen(self, body: MarkSeenRequest) -> None:
        """Mark release notes as seen."""
        await self._client.post(
            "/release-notes/seen",
            json_body=body,
            cast_to=dict,
            envelope=True,
        )


Galene._NAMESPACES.append(ReleaseNotes)
AsyncGalene._NAMESPACES.append(AsyncReleaseNotes)
