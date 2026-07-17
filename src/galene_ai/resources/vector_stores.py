"""`vector_stores` resource: create, manage, and search vector stores.

`/v1/vector_stores/*` provides an OpenAI-compatible Vector Stores API. Vector stores
group uploaded files for retrieval; files can be attached individually or in batches,
and the store can be searched with a natural-language query.

Response shapes follow the pre-computed directives:
- store CRUD returns the hand-written `VectorStore` model (`galene_ai.models._extra`);
- list operations paginate with a cursor (`VectorStoreList` / `VectorStoreFileList`);
- file attach/retrieve return `VectorStoreFile`;
- delete and file-batch operations return the raw status/batch `dict`;
- search returns `VectorStoreSearchResult`.
Request bodies use the generated `VectorStore*` request models from
`galene_ai.models._generated` (imported there rather than via the package root because
the generated names are not `mypy --strict`-visible through `galene_ai.models`).
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.pagination import AsyncCursorPage, CursorPage
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models import (
    VectorStore,
    VectorStoreFile,
    VectorStoreFileList,
    VectorStoreList,
    VectorStoreSearchResult,
)
from galene_ai.models._generated import (
    VectorStoreCreate,
    VectorStoreFileAdd,
    VectorStoreFileBatchCreate,
    VectorStoreSearchRequest,
    VectorStoreUpdate,
)

_BASE = "/v1/vector_stores"


class VectorStores(SyncResource):
    """Create, manage, and search vector stores and their files."""

    namespace: ClassVar[str] = "vector_stores"

    @operation("_create_vector_store_v1_vector_stores_post")
    def create(self, body: VectorStoreCreate) -> VectorStore:
        """Create a vector store."""
        return cast(
            VectorStore,
            self._client.post(_BASE, json_body=body, cast_to=VectorStore),
        )

    @operation("_list_vector_stores_v1_vector_stores_get")
    def list(
        self,
        *,
        limit: int | None = None,
        order: str | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> CursorPage[VectorStore]:
        """List vector stores."""
        page = cast(
            VectorStoreList,
            self._client.get(
                _BASE,
                params={"limit": limit, "order": order, "after": after, "before": before},
                cast_to=VectorStoreList,
            ),
        )

        def _fetch(cursor: str | None) -> CursorPage[VectorStore]:
            return self.list(limit=limit, order=order, after=cursor, before=before)

        return CursorPage(
            data=page.data, has_more=page.has_more, last_id=page.last_id, _fetch=_fetch
        )

    @operation("_get_vector_store_v1_vector_stores__vector_store_id__get")
    def retrieve(self, vector_store_id: str) -> VectorStore:
        """Retrieve a vector store."""
        return cast(
            VectorStore,
            self._client.get(f"{_BASE}/{vector_store_id}", cast_to=VectorStore),
        )

    @operation("_update_vector_store_v1_vector_stores__vector_store_id__post")
    def update(self, vector_store_id: str, body: VectorStoreUpdate) -> VectorStore:
        """Update a vector store."""
        return cast(
            VectorStore,
            self._client.post(f"{_BASE}/{vector_store_id}", json_body=body, cast_to=VectorStore),
        )

    @operation("_delete_vector_store_v1_vector_stores__vector_store_id__delete")
    def delete(self, vector_store_id: str) -> dict[str, Any]:
        """Delete a vector store."""
        return cast(
            dict[str, Any],
            self._client.delete(f"{_BASE}/{vector_store_id}", cast_to=dict),
        )

    @operation("_add_file_to_vector_store_v1_vector_stores__vector_store_id__files_post")
    def add_file(self, vector_store_id: str, body: VectorStoreFileAdd) -> VectorStoreFile:
        """Add file to vector store."""
        return cast(
            VectorStoreFile,
            self._client.post(
                f"{_BASE}/{vector_store_id}/files", json_body=body, cast_to=VectorStoreFile
            ),
        )

    @operation("_list_vector_store_files_v1_vector_stores__vector_store_id__files_get")
    def list_files(
        self,
        vector_store_id: str,
        *,
        limit: int | None = None,
        order: str | None = None,
        after: str | None = None,
        before: str | None = None,
        filter: str | None = None,
    ) -> CursorPage[VectorStoreFile]:
        """List vector store files."""
        page = cast(
            VectorStoreFileList,
            self._client.get(
                f"{_BASE}/{vector_store_id}/files",
                params={
                    "limit": limit,
                    "order": order,
                    "after": after,
                    "before": before,
                    "filter": filter,
                },
                cast_to=VectorStoreFileList,
            ),
        )

        def _fetch(cursor: str | None) -> CursorPage[VectorStoreFile]:
            return self.list_files(
                vector_store_id,
                limit=limit,
                order=order,
                after=cursor,
                before=before,
                filter=filter,
            )

        return CursorPage(
            data=page.data, has_more=page.has_more, last_id=page.last_id, _fetch=_fetch
        )

    @operation(
        "_delete_vector_store_file_v1_vector_stores__vector_store_id__files__file_id__delete"
    )
    def delete_file(self, vector_store_id: str, file_id: str) -> dict[str, Any]:
        """Delete vector store file."""
        return cast(
            dict[str, Any],
            self._client.delete(f"{_BASE}/{vector_store_id}/files/{file_id}", cast_to=dict),
        )

    @operation("_get_vector_store_file_v1_vector_stores__vector_store_id__files__file_id__get")
    def retrieve_file(self, vector_store_id: str, file_id: str) -> VectorStoreFile:
        """Retrieve a vector store file."""
        return cast(
            VectorStoreFile,
            self._client.get(f"{_BASE}/{vector_store_id}/files/{file_id}", cast_to=VectorStoreFile),
        )

    @operation(
        "_create_vector_store_file_batch_v1_vector_stores__vector_store_id__file_batches_post"
    )
    def create_file_batch(
        self, vector_store_id: str, body: VectorStoreFileBatchCreate
    ) -> dict[str, Any]:
        """Create vector store file batch."""
        return cast(
            dict[str, Any],
            self._client.post(
                f"{_BASE}/{vector_store_id}/file_batches", json_body=body, cast_to=dict
            ),
        )

    @operation("_search_vector_store_v1_vector_stores__vector_store_id__search_post")
    def search(
        self, vector_store_id: str, body: VectorStoreSearchRequest
    ) -> VectorStoreSearchResult:
        """Search in vector store."""
        return cast(
            VectorStoreSearchResult,
            self._client.post(
                f"{_BASE}/{vector_store_id}/search",
                json_body=body,
                cast_to=VectorStoreSearchResult,
            ),
        )


class AsyncVectorStores(AsyncResource):
    """Async counterpart of `VectorStores`."""

    namespace: ClassVar[str] = "vector_stores"

    @operation("_create_vector_store_v1_vector_stores_post")
    async def create(self, body: VectorStoreCreate) -> VectorStore:
        """Create a vector store."""
        return cast(
            VectorStore,
            await self._client.post(_BASE, json_body=body, cast_to=VectorStore),
        )

    @operation("_list_vector_stores_v1_vector_stores_get")
    async def list(
        self,
        *,
        limit: int | None = None,
        order: str | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncCursorPage[VectorStore]:
        """List vector stores."""
        page = cast(
            VectorStoreList,
            await self._client.get(
                _BASE,
                params={"limit": limit, "order": order, "after": after, "before": before},
                cast_to=VectorStoreList,
            ),
        )

        async def _fetch(cursor: str | None) -> AsyncCursorPage[VectorStore]:
            return await self.list(limit=limit, order=order, after=cursor, before=before)

        return AsyncCursorPage(
            data=page.data, has_more=page.has_more, last_id=page.last_id, _fetch=_fetch
        )

    @operation("_get_vector_store_v1_vector_stores__vector_store_id__get")
    async def retrieve(self, vector_store_id: str) -> VectorStore:
        """Retrieve a vector store."""
        return cast(
            VectorStore,
            await self._client.get(f"{_BASE}/{vector_store_id}", cast_to=VectorStore),
        )

    @operation("_update_vector_store_v1_vector_stores__vector_store_id__post")
    async def update(self, vector_store_id: str, body: VectorStoreUpdate) -> VectorStore:
        """Update a vector store."""
        return cast(
            VectorStore,
            await self._client.post(
                f"{_BASE}/{vector_store_id}", json_body=body, cast_to=VectorStore
            ),
        )

    @operation("_delete_vector_store_v1_vector_stores__vector_store_id__delete")
    async def delete(self, vector_store_id: str) -> dict[str, Any]:
        """Delete a vector store."""
        return cast(
            dict[str, Any],
            await self._client.delete(f"{_BASE}/{vector_store_id}", cast_to=dict),
        )

    @operation("_add_file_to_vector_store_v1_vector_stores__vector_store_id__files_post")
    async def add_file(self, vector_store_id: str, body: VectorStoreFileAdd) -> VectorStoreFile:
        """Add file to vector store."""
        return cast(
            VectorStoreFile,
            await self._client.post(
                f"{_BASE}/{vector_store_id}/files", json_body=body, cast_to=VectorStoreFile
            ),
        )

    @operation("_list_vector_store_files_v1_vector_stores__vector_store_id__files_get")
    async def list_files(
        self,
        vector_store_id: str,
        *,
        limit: int | None = None,
        order: str | None = None,
        after: str | None = None,
        before: str | None = None,
        filter: str | None = None,
    ) -> AsyncCursorPage[VectorStoreFile]:
        """List vector store files."""
        page = cast(
            VectorStoreFileList,
            await self._client.get(
                f"{_BASE}/{vector_store_id}/files",
                params={
                    "limit": limit,
                    "order": order,
                    "after": after,
                    "before": before,
                    "filter": filter,
                },
                cast_to=VectorStoreFileList,
            ),
        )

        async def _fetch(cursor: str | None) -> AsyncCursorPage[VectorStoreFile]:
            return await self.list_files(
                vector_store_id,
                limit=limit,
                order=order,
                after=cursor,
                before=before,
                filter=filter,
            )

        return AsyncCursorPage(
            data=page.data, has_more=page.has_more, last_id=page.last_id, _fetch=_fetch
        )

    @operation(
        "_delete_vector_store_file_v1_vector_stores__vector_store_id__files__file_id__delete"
    )
    async def delete_file(self, vector_store_id: str, file_id: str) -> dict[str, Any]:
        """Delete vector store file."""
        return cast(
            dict[str, Any],
            await self._client.delete(f"{_BASE}/{vector_store_id}/files/{file_id}", cast_to=dict),
        )

    @operation("_get_vector_store_file_v1_vector_stores__vector_store_id__files__file_id__get")
    async def retrieve_file(self, vector_store_id: str, file_id: str) -> VectorStoreFile:
        """Retrieve a vector store file."""
        return cast(
            VectorStoreFile,
            await self._client.get(
                f"{_BASE}/{vector_store_id}/files/{file_id}", cast_to=VectorStoreFile
            ),
        )

    @operation(
        "_create_vector_store_file_batch_v1_vector_stores__vector_store_id__file_batches_post"
    )
    async def create_file_batch(
        self, vector_store_id: str, body: VectorStoreFileBatchCreate
    ) -> dict[str, Any]:
        """Create vector store file batch."""
        return cast(
            dict[str, Any],
            await self._client.post(
                f"{_BASE}/{vector_store_id}/file_batches", json_body=body, cast_to=dict
            ),
        )

    @operation("_search_vector_store_v1_vector_stores__vector_store_id__search_post")
    async def search(
        self, vector_store_id: str, body: VectorStoreSearchRequest
    ) -> VectorStoreSearchResult:
        """Search in vector store."""
        return cast(
            VectorStoreSearchResult,
            await self._client.post(
                f"{_BASE}/{vector_store_id}/search",
                json_body=body,
                cast_to=VectorStoreSearchResult,
            ),
        )


Galene._NAMESPACES.append(VectorStores)
AsyncGalene._NAMESPACES.append(AsyncVectorStores)
