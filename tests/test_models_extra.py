"""Round-trip decode tests for the hand-written `_extra` models.

These exercise representative JSON payloads (OpenAI-compatible `files`/
`vector_stores`/`embeddings` shapes) to lock in the field mapping — in
particular the `UploadedFileResult.id` <- `attachment_id` alias.
"""

import msgspec

from galene_ai.models import (
    EmbeddingResponse,
    File,
    UploadedFile,
    VectorStore,
    VectorStoreSearchResult,
)


def test_file_decodes_from_representative_json() -> None:
    raw = b"""
    {
        "id": "file-abc123",
        "object": "file",
        "filename": "report.pdf",
        "purpose": "user_data",
        "bytes": 4096
    }
    """
    f = msgspec.json.decode(raw, type=File)
    assert f.id == "file-abc123"
    assert f.filename == "report.pdf"
    assert f.purpose == "user_data"
    assert f.bytes == 4096


def test_vector_store_decodes_with_file_counts() -> None:
    raw = b"""
    {
        "id": "vs_abc123",
        "object": "vector_store",
        "name": "Support FAQ",
        "created_at": 1768473000,
        "last_active_at": 1768473600,
        "usage_bytes": 12345,
        "status": "completed",
        "file_counts": {
            "total": 3,
            "in_progress": 0,
            "completed": 3,
            "failed": 0,
            "cancelled": 0
        },
        "metadata": {"team": "support"},
        "expires_at": null,
        "expires_after": null
    }
    """
    vs = msgspec.json.decode(raw, type=VectorStore)
    assert vs.id == "vs_abc123"
    assert vs.name == "Support FAQ"
    assert vs.created_at == 1768473000
    assert vs.last_active_at == 1768473600
    assert vs.usage_bytes == 12345
    assert vs.status == "completed"
    assert vs.file_counts is not None
    assert vs.file_counts.total == 3
    assert vs.file_counts.completed == 3
    assert vs.metadata == {"team": "support"}
    assert vs.expires_at is None


def test_vector_store_search_result_decodes_data_items() -> None:
    raw = b"""
    {
        "search_query": "how to reset password",
        "data": [
            {
                "content": [
                    {"type": "text", "text": "Go to settings and click reset."}
                ],
                "score": 0.87,
                "file_id": "file-abc123",
                "filename": "faq.md",
                "attributes": {"category": "auth"}
            }
        ],
        "has_more": false
    }
    """
    result = msgspec.json.decode(raw, type=VectorStoreSearchResult)
    assert result.search_query == "how to reset password"
    assert result.has_more is False
    assert len(result.data) == 1
    item = result.data[0]
    assert item.score == 0.87
    assert item.file_id == "file-abc123"
    assert item.filename == "faq.md"
    assert item.attributes == {"category": "auth"}
    assert len(item.content) == 1
    assert item.content[0].type == "text"
    assert item.content[0].text == "Go to settings and click reset."


def test_embedding_response_decodes_vectors_and_usage() -> None:
    raw = b"""
    {
        "object": "list",
        "model": "text-embedding-3-small",
        "data": [
            {"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]},
            {"object": "embedding", "index": 1, "embedding": [0.4, 0.5, 0.6]}
        ],
        "usage": {"prompt_tokens": 8, "total_tokens": 8}
    }
    """
    resp = msgspec.json.decode(raw, type=EmbeddingResponse)
    assert resp.model == "text-embedding-3-small"
    assert len(resp.data) == 2
    assert resp.data[0].index == 0
    assert resp.data[0].embedding == [0.1, 0.2, 0.3]
    assert resp.data[1].embedding == [0.4, 0.5, 0.6]
    assert resp.usage is not None
    assert resp.usage.prompt_tokens == 8
    assert resp.usage.total_tokens == 8


def test_uploaded_file_decodes_attachment_id_alias_into_result_id() -> None:
    raw = b"""
    {
        "success": true,
        "message": "File uploaded successfully.",
        "result": {
            "attachment_id": "att_9f8e7d",
            "object": "attachment",
            "filename": "notes.txt",
            "size": 128,
            "mime_type": "text/plain",
            "created_at": 1769947200,
            "purpose": "user_data",
            "error_code": null,
            "error_phase": null,
            "warnings": []
        }
    }
    """
    uploaded = msgspec.json.decode(raw, type=UploadedFile)
    assert uploaded.success is True
    assert uploaded.message == "File uploaded successfully."
    assert uploaded.result is not None
    assert uploaded.result.id == "att_9f8e7d"
    assert uploaded.result.filename == "notes.txt"
    assert uploaded.result.size == 128
    assert uploaded.result.mime_type == "text/plain"
    assert uploaded.result.created_at == 1769947200
    assert uploaded.result.error_code is None
    assert uploaded.result.warnings == []
