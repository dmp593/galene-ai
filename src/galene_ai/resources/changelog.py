"""Changelog resource."""

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation


class Changelog(SyncResource):
    """Get application changelog."""

    namespace: ClassVar[str] = "changelog"

    @operation("_changelog_changelog_get")
    def get(self, *, lang: str | None = None, include_admin: bool | None = None) -> dict[str, Any]:
        """Get application changelog."""
        return cast(
            dict[str, Any],
            self._client.get(
                "/changelog",
                params={"lang": lang, "include_admin": include_admin},
                cast_to=dict,
                envelope=True,
            ),
        )


class AsyncChangelog(AsyncResource):
    """Async counterpart of `Changelog`."""

    namespace: ClassVar[str] = "changelog"

    @operation("_changelog_changelog_get")
    async def get(
        self, *, lang: str | None = None, include_admin: bool | None = None
    ) -> dict[str, Any]:
        """Get application changelog."""
        return cast(
            dict[str, Any],
            await self._client.get(
                "/changelog",
                params={"lang": lang, "include_admin": include_admin},
                cast_to=dict,
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(Changelog)
AsyncGalene._NAMESPACES.append(AsyncChangelog)
