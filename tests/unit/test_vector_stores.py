import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models._generated import (
    VectorStoreCreate,
    VectorStoreFileAdd,
    VectorStoreFileBatchCreate,
    VectorStoreSearchRequest,
    VectorStoreUpdate,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _store_json(vs_id="vs_1", name="Docs"):
    return {
        "id": vs_id,
        "name": name,
        "created_at": 1699564800,
        "usage_bytes": 12,
        "status": "completed",
        "file_counts": {"total": 1, "completed": 1},
        "metadata": {"k": "v"},
    }


def test_create_sends_json_body_and_decodes_store():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/vector_stores"
        assert b'"name":"My Store"' in req.content
        return httpx.Response(200, json=_store_json(name="My Store"))

    vs = _client(handler).vector_stores.create(VectorStoreCreate(name="My Store"))
    assert vs.id == "vs_1"
    assert vs.name == "My Store"
    assert vs.file_counts.completed == 1


def test_list_hits_endpoint_with_params_and_paginates():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/vector_stores"
        assert req.url.params["limit"] == "5"
        assert req.url.params["order"] == "desc"
        return httpx.Response(
            200,
            json={"data": [_store_json()], "last_id": "vs_1", "has_more": False},
        )

    page = _client(handler).vector_stores.list(limit=5, order="desc")
    assert [v.id for v in page] == ["vs_1"]
    assert page.last_id == "vs_1"
    assert page.has_more is False


def test_list_omits_none_params():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "limit" not in req.url.params
        assert "order" not in req.url.params
        return httpx.Response(200, json={"data": [], "has_more": False})

    page = _client(handler).vector_stores.list()
    assert page.data == []


def test_retrieve_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/vector_stores/vs_9"
        return httpx.Response(200, json=_store_json(vs_id="vs_9"))

    vs = _client(handler).vector_stores.retrieve("vs_9")
    assert vs.id == "vs_9"


def test_update_sends_json_body_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/vector_stores/vs_1"
        assert b'"name":"Renamed"' in req.content
        return httpx.Response(200, json=_store_json(name="Renamed"))

    vs = _client(handler).vector_stores.update("vs_1", VectorStoreUpdate(name="Renamed"))
    assert vs.name == "Renamed"


def test_delete_returns_status_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/v1/vector_stores/vs_1"
        return httpx.Response(
            200, json={"id": "vs_1", "object": "vector_store.deleted", "deleted": True}
        )

    result = _client(handler).vector_stores.delete("vs_1")
    assert result["deleted"] is True
    assert result["id"] == "vs_1"


def test_add_file_sends_json_body_and_decodes_file():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/vector_stores/vs_1/files"
        assert b'"file_id":"file-abc"' in req.content
        return httpx.Response(
            200,
            json={
                "id": "file-abc",
                "usage_bytes": 5,
                "created_at": 1699564800,
                "vector_store_id": "vs_1",
                "status": "completed",
            },
        )

    f = _client(handler).vector_stores.add_file("vs_1", VectorStoreFileAdd(file_id="file-abc"))
    assert f.id == "file-abc"
    assert f.vector_store_id == "vs_1"
    assert f.status == "completed"


def test_list_files_hits_endpoint_with_filter_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/vector_stores/vs_1/files"
        assert req.url.params["filter"] == "completed"
        return httpx.Response(
            200,
            json={
                "data": [{"id": "file-abc", "vector_store_id": "vs_1", "status": "completed"}],
                "last_id": "file-abc",
                "has_more": False,
            },
        )

    page = _client(handler).vector_stores.list_files("vs_1", filter="completed")
    assert [f.id for f in page] == ["file-abc"]
    assert page.last_id == "file-abc"


def test_retrieve_file_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/vector_stores/vs_1/files/file-abc"
        return httpx.Response(
            200,
            json={"id": "file-abc", "vector_store_id": "vs_1", "status": "completed"},
        )

    f = _client(handler).vector_stores.retrieve_file("vs_1", "file-abc")
    assert f.id == "file-abc"


def test_delete_file_returns_status_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/v1/vector_stores/vs_1/files/file-abc"
        return httpx.Response(
            200, json={"id": "file-abc", "object": "vector_store.file.deleted", "deleted": True}
        )

    result = _client(handler).vector_stores.delete_file("vs_1", "file-abc")
    assert result["deleted"] is True


def test_create_file_batch_sends_json_body_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/vector_stores/vs_1/file_batches"
        assert b'"file_ids":["file-a","file-b"]' in req.content
        return httpx.Response(
            200,
            json={
                "id": "vsfb_1",
                "object": "vector_store.file_batch",
                "vector_store_id": "vs_1",
                "status": "in_progress",
                "file_counts": {"total": 2, "in_progress": 2},
            },
        )

    batch = _client(handler).vector_stores.create_file_batch(
        "vs_1", VectorStoreFileBatchCreate(file_ids=["file-a", "file-b"])
    )
    assert batch["id"] == "vsfb_1"
    assert batch["status"] == "in_progress"


def test_search_sends_json_body_and_decodes_result():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/vector_stores/vs_1/search"
        assert b'"query":"neural networks"' in req.content
        return httpx.Response(
            200,
            json={
                "search_query": "neural networks",
                "data": [
                    {
                        "content": [{"type": "text", "text": "a result"}],
                        "score": 0.9,
                        "file_id": "file-abc",
                        "filename": "doc.pdf",
                    }
                ],
                "has_more": False,
            },
        )

    res = _client(handler).vector_stores.search(
        "vs_1", VectorStoreSearchRequest(query="neural networks")
    )
    assert res.search_query == "neural networks"
    assert res.data[0].score == 0.9
    assert res.data[0].content[0].text == "a result"


async def test_async_vector_stores_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/vector_stores/vs_9"
        return httpx.Response(200, json=_store_json(vs_id="vs_9", name="Async"))

    client = _aclient(handler)
    try:
        vs = await client.vector_stores.retrieve("vs_9")
        assert vs.id == "vs_9"
        assert vs.name == "Async"
    finally:
        await client.aclose()
