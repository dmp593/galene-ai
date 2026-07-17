"""`admin.search` resource: cross-organization search (Superadmin)."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import CrossOrgUserSearchResponse


class Search(SyncResource):
    """Search across all organizations."""

    namespace: ClassVar[str] = "search"

    @operation("_search_users_admin_search_users_get")
    def users(
        self,
        *,
        q: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        organization_id: str | None = None,
        is_active: bool | None = None,
        role: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> CrossOrgUserSearchResponse:
        """Search users across all organizations (Superadmin)."""
        return cast(
            CrossOrgUserSearchResponse,
            self._client.get(
                "/admin/search/users",
                params={
                    "q": q,
                    "page": page,
                    "page_size": page_size,
                    "organization_id": organization_id,
                    "is_active": is_active,
                    "role": role,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                },
                cast_to=CrossOrgUserSearchResponse,
                envelope=True,
            ),
        )


class AsyncSearch(AsyncResource):
    """Async counterpart of `Search`."""

    namespace: ClassVar[str] = "search"

    @operation("_search_users_admin_search_users_get")
    async def users(
        self,
        *,
        q: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        organization_id: str | None = None,
        is_active: bool | None = None,
        role: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> CrossOrgUserSearchResponse:
        """Search users across all organizations (Superadmin)."""
        return cast(
            CrossOrgUserSearchResponse,
            await self._client.get(
                "/admin/search/users",
                params={
                    "q": q,
                    "page": page,
                    "page_size": page_size,
                    "organization_id": organization_id,
                    "is_active": is_active,
                    "role": role,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                },
                cast_to=CrossOrgUserSearchResponse,
                envelope=True,
            ),
        )


Galene._ADMIN_NAMESPACES.append(Search)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncSearch)
