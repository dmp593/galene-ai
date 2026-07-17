"""`files` resource: OpenAI-compatible file upload, listing, and management.

`/v1/files/*` mirrors OpenAI's Files API (`tag: "OpenAI API"` in `spec/openapi.json`).
None of these 6 operations' response schemas reference a `WSResponse_*` component — every
200 response in `spec/openapi.json` for these paths has the empty schema `{}` (only a
documentation `example` is given, no `$ref`). Because the schema is empty,
`datamodel-code-generator` emitted no dedicated file-object model in
`galene_ai.models._generated`, so responses are decoded with the hand-written models in
`galene_ai.models._extra` (`File`, `FileMetadata`, `FileList`, `UploadedFileResult`) instead.

Per-operation shape, and where we deliberately depart from the spec's static examples:
- `list`/`retrieve` return the flat OpenAI file object (`File`/`FileMetadata`) — see the
  `_list_files_v1_files_get` and `_retrieve_file_v1_files__file_id__get` examples. These are
  decoded un-enveloped (`envelope=False`), matching their examples.
- `retry`'s spec example IS enveloped: `{success, message, result: {attachment_id, ...}}`.
- `upload`'s spec example, by contrast, is a FLAT `File`-shaped object
  (`{id, object, filename, bytes, purpose, created_at}`) with no `success`/`result`
  wrapper — i.e. the spec's static examples disagree with each other on whether `upload`
  is enveloped. We do NOT trust the flat example here: verified against a live backend,
  the `/v1/files` POST response is in fact enveloped — `{success, message,
  result: {attachment_id, ...}}`, the same shape as `retry`. Modeling `upload`'s
  response as a flat file object (or as a struct with a plain `success: bool` field that
  callers must remember to check) would silently swallow an HTTP-200
  `{"success": false, ...}` failure response instead of raising, unlike every other
  enveloped namespace in this SDK. We therefore follow the proven live behavior for BOTH
  `upload` and `retry`: decode with `envelope=True, cast_to=UploadedFileResult`, so
  `_core.envelope.unwrap` raises `GaleneError` on `success: false` and returns the
  `UploadedFileResult` from `result` on success. This is flagged for re-verification once
  the backend is reachable again (see `scripts/probe_shapes.py`, to be added).
"""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.pagination import AsyncCursorPage, CursorPage
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models import File, FileList, FileMetadata, UploadedFileResult


def _upload_form(purpose: str, filename: str | None) -> dict[str, str]:
    form = {"purpose": purpose}
    if filename is not None:
        # `original_filename` (per `BodyUploadFileV1FilesPost`) is the name the backend
        # keeps on record even if the multipart transport filename below gets mangled.
        form["original_filename"] = filename
    return form


class Files(SyncResource):
    """Upload, list, retrieve, retry, and download OpenAI-compatible files."""

    namespace: ClassVar[str] = "files"

    @operation("_upload_file_v1_files_post")
    def upload(
        self, file: bytes, *, purpose: str = "user_data", filename: str | None = None
    ) -> UploadedFileResult:
        """Upload a file.

        Returns the uploaded file object; raises `GaleneError` on failure.
        """
        files = {"file": (filename or "upload", file)}
        form = _upload_form(purpose, filename)
        return cast(
            UploadedFileResult,
            self._client.post(
                "/v1/files",
                data=form,
                files=files,
                cast_to=UploadedFileResult,
                envelope=True,
            ),
        )

    @operation("_list_files_v1_files_get")
    def list(self, *, purpose: str | None = None) -> CursorPage[File]:
        """List files."""
        page: FileList = self._client.get(
            "/v1/files", params={"purpose": purpose}, cast_to=FileList
        )

        def _fetch(_after: str | None) -> CursorPage[File]:
            # `/v1/files` takes no cursor parameter and always returns everything in a
            # single page (`has_more` is never true in practice); re-fetching just
            # repeats the same request, kept only to satisfy the `CursorPage` interface.
            return self.list(purpose=purpose)

        return CursorPage(data=page.data, has_more=bool(page.has_more), last_id=None, _fetch=_fetch)

    @operation("_retrieve_file_v1_files__file_id__get")
    def retrieve(self, file_id: str) -> FileMetadata:
        """Retrieve file metadata."""
        return cast(FileMetadata, self._client.get(f"/v1/files/{file_id}", cast_to=FileMetadata))

    @operation("_delete_file_v1_files__file_id__delete")
    def delete(self, file_id: str) -> None:
        """Delete a file."""
        self._client.delete(f"/v1/files/{file_id}", cast_to=None)

    @operation("_retry_file_v1_files__file_id__retry_post")
    def retry(self, file_id: str) -> UploadedFileResult:
        """Retry file ingestion.

        Returns the uploaded file object; raises `GaleneError` on failure.
        """
        return cast(
            UploadedFileResult,
            self._client.post(
                f"/v1/files/{file_id}/retry", cast_to=UploadedFileResult, envelope=True
            ),
        )

    @operation("_retrieve_file_content_v1_files__file_id__content_get")
    def content(self, file_id: str) -> bytes:
        """Download file content."""
        return cast(bytes, self._client.get(f"/v1/files/{file_id}/content", cast_to=bytes))


class AsyncFiles(AsyncResource):
    """Async counterpart of `Files`."""

    namespace: ClassVar[str] = "files"

    @operation("_upload_file_v1_files_post")
    async def upload(
        self, file: bytes, *, purpose: str = "user_data", filename: str | None = None
    ) -> UploadedFileResult:
        """Upload a file.

        Returns the uploaded file object; raises `GaleneError` on failure.
        """
        files = {"file": (filename or "upload", file)}
        form = _upload_form(purpose, filename)
        return cast(
            UploadedFileResult,
            await self._client.post(
                "/v1/files",
                data=form,
                files=files,
                cast_to=UploadedFileResult,
                envelope=True,
            ),
        )

    @operation("_list_files_v1_files_get")
    async def list(self, *, purpose: str | None = None) -> AsyncCursorPage[File]:
        """List files."""
        page: FileList = await self._client.get(
            "/v1/files", params={"purpose": purpose}, cast_to=FileList
        )

        async def _fetch(_after: str | None) -> AsyncCursorPage[File]:
            return await self.list(purpose=purpose)

        return AsyncCursorPage(
            data=page.data, has_more=bool(page.has_more), last_id=None, _fetch=_fetch
        )

    @operation("_retrieve_file_v1_files__file_id__get")
    async def retrieve(self, file_id: str) -> FileMetadata:
        """Retrieve file metadata."""
        return cast(
            FileMetadata,
            await self._client.get(f"/v1/files/{file_id}", cast_to=FileMetadata),
        )

    @operation("_delete_file_v1_files__file_id__delete")
    async def delete(self, file_id: str) -> None:
        """Delete a file."""
        await self._client.delete(f"/v1/files/{file_id}", cast_to=None)

    @operation("_retry_file_v1_files__file_id__retry_post")
    async def retry(self, file_id: str) -> UploadedFileResult:
        """Retry file ingestion.

        Returns the uploaded file object; raises `GaleneError` on failure.
        """
        return cast(
            UploadedFileResult,
            await self._client.post(
                f"/v1/files/{file_id}/retry", cast_to=UploadedFileResult, envelope=True
            ),
        )

    @operation("_retrieve_file_content_v1_files__file_id__content_get")
    async def content(self, file_id: str) -> bytes:
        """Download file content."""
        return cast(bytes, await self._client.get(f"/v1/files/{file_id}/content", cast_to=bytes))


Galene._NAMESPACES.append(Files)
AsyncGalene._NAMESPACES.append(AsyncFiles)
