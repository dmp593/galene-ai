import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _envelope(result):
    return {"success": True, "message": "ok", "result": result}


def test_list_traces_sends_query_and_decodes_enveloped_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/observability/traces"
        assert req.url.params["organization_id"] == "org1"
        assert req.url.params["status"] == "ok"
        assert req.url.params["limit"] == "5"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "id": "t1",
                        "organization_id": "org1",
                        "started_at": "2026-01-01T00:00:00Z",
                        "status": "ok",
                        "name": "run",
                    }
                ]
            ),
        )

    traces = _client(handler).observability.list_traces(
        organization_id="org1", status="ok", limit=5
    )
    assert [t.id for t in traces] == ["t1"]
    assert traces[0].name == "run"


def test_list_traces_sends_json_body_tags():
    def handler(req: httpx.Request) -> httpx.Response:
        import json

        assert json.loads(req.content) == {"tags_any": ["a"]}
        return httpx.Response(200, json=_envelope([]))

    from galene_ai.models import BodyGetTracesObservabilityTracesGet

    body = BodyGetTracesObservabilityTracesGet(tags_any=["a"])
    result = _client(handler).observability.list_traces(body=body)
    assert result == []


def test_export_traces_returns_csv_bytes():
    # The `.csv` export endpoints return raw CSV, not JSON (the spec mislabels
    # them application/json). The SDK returns the bytes verbatim.
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/observability/traces/export.csv"
        assert req.url.params["columns"] == "id,status"
        return httpx.Response(
            200, content=b"id,status\n1,ok\n", headers={"content-type": "text/csv"}
        )

    out = _client(handler).observability.export_traces(organization_id="org1", columns="id,status")
    assert out == b"id,status\n1,ok\n"


def test_retrieve_trace_decodes_enveloped_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/observability/traces/t1"
        return httpx.Response(
            200,
            json=_envelope(
                {
                    "id": "t1",
                    "organization_id": "org1",
                    "started_at": "2026-01-01T00:00:00Z",
                    "status": "ok",
                    "total_tokens": 42,
                }
            ),
        )

    trace = _client(handler).observability.retrieve_trace("t1")
    assert trace.id == "t1"
    assert trace.total_tokens == 42


def test_list_observations_sends_type_param_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/traces/t1/observations"
        assert req.url.params["type_"] == "generation"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "id": "o1",
                        "trace_id": "t1",
                        "path": "root",
                        "type": "generation",
                        "status": "ok",
                        "started_at": "2026-01-01T00:00:00Z",
                        "model": "gpt-4",
                    }
                ]
            ),
        )

    obs = _client(handler).observability.list_observations("t1", type_="generation")
    assert obs[0].id == "o1"
    assert obs[0].model == "gpt-4"


def test_export_observations_returns_csv_bytes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/traces/t1/observations/export.csv"
        return httpx.Response(
            200, content=b"id,type\no1,llm\n", headers={"content-type": "text/csv"}
        )

    out = _client(handler).observability.export_observations("t1")
    assert out == b"id,type\no1,llm\n"


def test_create_read_posts_and_returns_bool():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/observability/traces/t1/reads"
        return httpx.Response(200, json=_envelope(True))

    out = _client(handler).observability.create_read("t1")
    assert out is True


def test_list_reads_decodes_enveloped_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/traces/t1/reads"
        assert req.url.params["user_id"] == "u1"
        return httpx.Response(
            200,
            json=_envelope(
                [
                    {
                        "id": "a1",
                        "trace_id": "t1",
                        "user_id": "u1",
                        "read_at": "2026-01-01T00:00:00Z",
                    }
                ]
            ),
        )

    reads = _client(handler).observability.list_reads("t1", user_id="u1")
    assert reads[0].id == "a1"
    assert reads[0].user_id == "u1"


def test_export_reads_returns_csv_bytes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/traces/t1/reads/export.csv"
        return httpx.Response(
            200, content=b"id,read_at\na1,2026\n", headers={"content-type": "text/csv"}
        )

    out = _client(handler).observability.export_reads("t1")
    assert out == b"id,read_at\na1,2026\n"


def test_metrics_overview_decodes_model():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/overview"
        assert req.url.params["organization_id"] == "org1"
        return httpx.Response(
            200,
            json={
                "traces": 10,
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "shield_tokens": 5,
                "blocks": 1,
                "warns": 2,
                "avg_duration_ms": 123,
            },
        )

    ov = _client(handler).observability.metrics_overview(organization_id="org1")
    assert ov.traces == 10
    assert ov.avg_duration_ms == 123


def test_top_agents_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/agents"
        assert req.url.params["order"] == "count"
        return httpx.Response(200, json=[{"name": "agent-a", "count": 7, "tokens": 99}])

    items = _client(handler).observability.top_agents(organization_id="org1", order="count")
    assert items[0].name == "agent-a"
    assert items[0].count == 7


def test_top_users_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/users"
        return httpx.Response(200, json=[{"name": "u1", "count": 3}])

    items = _client(handler).observability.top_users(organization_id="org1")
    assert items[0].name == "u1"


def test_top_tools_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/tools"
        return httpx.Response(
            200, json=[{"tool_name": "search", "calls": 4, "total_duration_ms": 200}]
        )

    items = _client(handler).observability.top_tools(organization_id="org1")
    assert items[0].tool_name == "search"
    assert items[0].calls == 4


def test_models_usage_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/models"
        return httpx.Response(
            200,
            json=[
                {
                    "model": "gpt-4",
                    "generations": 5,
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                }
            ],
        )

    items = _client(handler).observability.models_usage(organization_id="org1")
    assert items[0].model == "gpt-4"
    assert items[0].generations == 5


def test_guardrail_filters_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/guardrail/filters"
        return httpx.Response(200, json=[{"filter_ref": "pii", "hits": 9}])

    items = _client(handler).observability.guardrail_filters(organization_id="org1")
    assert items[0].filter_ref == "pii"
    assert items[0].hits == 9


def test_shield_tokens_daily_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/shield/tokens_daily"
        return httpx.Response(
            200,
            json=[{"day": "2026-01-01", "shield_tokens": 3, "blocks": 1, "warns": 0}],
        )

    items = _client(handler).observability.shield_tokens_daily(organization_id="org1")
    assert items[0].day == "2026-01-01"
    assert items[0].shield_tokens == 3


def test_active_users_daily_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/active-users-daily"
        assert req.url.params["organization_id"] == "org1"
        assert req.url.params["from_ts"] == "2026-01-01T00:00:00Z"
        return httpx.Response(
            200,
            json=[{"day": "2026-01-01T00:00:00Z", "active_users": 4, "traces": 12}],
        )

    items = _client(handler).observability.active_users_daily(
        organization_id="org1", from_ts="2026-01-01T00:00:00Z"
    )
    assert items[0].day == "2026-01-01T00:00:00Z"
    assert items[0].active_users == 4
    assert items[0].traces == 12


def test_rag_similarity_decodes_list():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/rag/similarity"
        return httpx.Response(
            200,
            json=[
                {
                    "avg_similarity": 0.8,
                    "min_similarity": 0.5,
                    "max_similarity": 0.95,
                    "samples": 12,
                }
            ],
        )

    items = _client(handler).observability.rag_similarity(organization_id="org1")
    assert items[0].samples == 12
    assert items[0].avg_similarity == 0.8


async def test_async_metrics_overview_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.url.path == "/observability/metrics/overview"
        return httpx.Response(
            200,
            json={
                "traces": 1,
                "prompt_tokens": 2,
                "completion_tokens": 3,
                "shield_tokens": 4,
                "blocks": 0,
                "warns": 0,
            },
        )

    client = _aclient(handler)
    try:
        ov = await client.observability.metrics_overview(organization_id="org1")
        assert ov.traces == 1
        assert ov.completion_tokens == 3
    finally:
        await client.aclose()
