"""Hand-written msgspec models for response shapes the OpenAPI spec leaves untyped.

These cover the OpenAI-compatible surface (files, vector stores, embeddings,
moderations) whose `/v1/*` responses are empty `{}` in the spec. Ported from the
proven galene integration + OpenAI conventions. Kept separate from the generated
`_generated.py`. agents/attachments shapes remain `dict` until they can be probed.

Timestamp fields (`created_at`, `expires_at`) are typed `int` (Unix epoch seconds),
not `datetime`, even though the pydantic reference this was ported from uses
`datetime` (pydantic silently coerces int/float epoch values on validation, so
that worked there). msgspec's stdlib `datetime` decoder does *not* accept ints —
only RFC3339 strings — and every documented `example` for these endpoints in
`spec/openapi.json` (e.g. `_upload_file_v1_files_post`, `_retry_file_...`) shows
`"created_at": 1699564800`, an int. `int` also matches how `_generated.py` already
types timestamp fields elsewhere in this same spec (e.g. `AdminApiKeyItem.created_at`)
and how OpenAI's own official SDK types `FileObject.created_at`/`VectorStore.created_at`.
"""

from typing import Any

import msgspec

__all__ = [
    "Embedding",
    "EmbeddingResponse",
    "EmbeddingUsage",
    "File",
    "FileList",
    "FileMetadata",
    "ModerationResponse",
    "ModerationResult",
    "Transcription",
    "UploadedFile",
    "UploadedFileResult",
    "VectorStore",
    "VectorStoreFile",
    "VectorStoreFileCounts",
    "VectorStoreFileList",
    "VectorStoreList",
    "VectorStoreSearchItem",
    "VectorStoreSearchItemContent",
    "VectorStoreSearchResult",
]


# --- Files -----------------------------------------------------------------
class File(msgspec.Struct):
    id: str
    filename: str
    purpose: str
    bytes: int
    # `/v1/files` list items carry `created_at` (Unix epoch seconds) as of the
    # paginated Files API; older backends omitted it, so it stays optional here.
    created_at: int | None = None


class FileMetadata(File):
    # `GET /v1/files/{id}` always includes `created_at`, so it is required on
    # the single-file metadata shape (this re-declaration narrows the optional
    # base field to a required one).
    created_at: int


class UploadedFileResult(msgspec.Struct):
    id: str = msgspec.field(name="attachment_id")
    object: str = ""
    filename: str = ""
    size: int = 0
    mime_type: str = ""
    created_at: int | None = None
    purpose: str = ""
    error_code: int | None = None
    error_phase: str | None = None
    warnings: list[Any] = []


class UploadedFile(msgspec.Struct):
    success: bool
    message: str = ""
    result: UploadedFileResult | None = None


class FileList(msgspec.Struct):
    data: list[File]
    has_more: bool | None = None
    total: int | None = None


# --- Vector stores ---------------------------------------------------------
class VectorStoreFileCounts(msgspec.Struct):
    total: int = 0
    in_progress: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0


class VectorStore(msgspec.Struct):
    id: str
    name: str | None = None
    created_at: int | None = None
    last_active_at: int | None = None
    usage_bytes: int = 0
    status: str = ""
    file_counts: VectorStoreFileCounts | None = None
    metadata: dict[str, str] = {}
    expires_at: int | None = None
    expires_after: dict[str, Any] | None = None


class VectorStoreList(msgspec.Struct):
    data: list[VectorStore]
    first_id: str | None = None
    last_id: str | None = None
    has_more: bool = False


class VectorStoreFile(msgspec.Struct):
    id: str
    usage_bytes: int = 0
    created_at: int | None = None
    vector_store_id: str = ""
    status: str = ""
    last_error: dict[str, Any] | None = None


class VectorStoreFileList(msgspec.Struct):
    data: list[VectorStoreFile]
    first_id: str | None = None
    last_id: str | None = None
    has_more: bool = False


class VectorStoreSearchItemContent(msgspec.Struct):
    type: str
    text: str


class VectorStoreSearchItem(msgspec.Struct):
    content: list[VectorStoreSearchItemContent]
    score: float
    file_id: str | None = None
    filename: str | None = None
    attributes: dict[str, Any] | None = None


class VectorStoreSearchResult(msgspec.Struct):
    search_query: str
    data: list[VectorStoreSearchItem]
    has_more: bool = False


# --- Embeddings (OpenAI-standard) ------------------------------------------
class Embedding(msgspec.Struct):
    embedding: list[float]
    index: int
    object: str = "embedding"


class EmbeddingUsage(msgspec.Struct):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingResponse(msgspec.Struct):
    data: list[Embedding]
    model: str = ""
    object: str = "list"
    usage: EmbeddingUsage | None = None


# --- Moderations (OpenAI-standard) -----------------------------------------
class ModerationResult(msgspec.Struct):
    flagged: bool = False
    categories: dict[str, bool] = {}
    category_scores: dict[str, float] = {}


class ModerationResponse(msgspec.Struct):
    id: str = ""
    model: str = ""
    results: list[ModerationResult] = []


# --- Audio transcription/translation ---------------------------------------
class Transcription(msgspec.Struct):
    text: str
