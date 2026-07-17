# Changelog

## [1.0.0]
Initial release.

- Covers all 316 operations of the Galene.AI platform API across 37 resource
  namespaces (29 top-level + 8 nested under `client.admin.*`), including the
  OpenAI-compatible surface (`chat`, `responses`, `embeddings`, `models`,
  `moderations`, `files`, `vector_stores`, `audio`) and the platform surface
  (`agents`, `observability`, `tickets`, `users`, `auth`, `kb_sync`, `tts`,
  `database_connectors`, `kb_connectors`, `attachments`, `conversations`,
  `shield`, `mcp_servers`, `api_keys`, `groups`, `notifications`, `roles`,
  `health`, `organizations`, `release_notes`, `changelog`).
- `Galene` (sync) and `AsyncGalene` (async) clients sharing one core, with an
  identical method surface across both.
- Typed request/response models generated with `datamodel-code-generator` as
  `msgspec.Struct`s (`src/galene_ai/models/_generated.py`), plus hand-written
  models (`src/galene_ai/models/_extra.py`) for the OpenAI-compatible
  endpoints whose spec response schema is empty.
- Pluggable auth: `ApiKeyAuth` (default, static bearer token) and
  `SessionAuth` (username/password login with transparent refresh-on-401),
  both plain `httpx.Auth` implementations.
- SSE streaming (`Stream[T]` / `AsyncStream[T]`) for `chat.create(...,
  stream=True)` and `responses.create(..., stream=True)`.
- Cursor and offset pagination (`CursorPage`/`AsyncCursorPage`,
  `OffsetPage`/`AsyncOffsetPage`) with `.auto_paging_iter()`.
- Retries with exponential backoff + jitter, honoring `Retry-After`, with a
  carve-out that never retries a timed-out generation request.
- Typed error hierarchy (`GaleneError` → `APIConnectionError` /
  `APIStatusError` → per-status subclasses), mirroring the OpenAI SDK shape.
- `tests/test_drift.py`: a contract test asserting the implemented
  `operationId`s exactly match `spec/operations.json`, so any spec change
  that isn't reflected in the SDK fails CI.
- Validated live against a real Galene backend (read endpoints,
  create→use→delete lifecycles for vector stores / files / conversations, and
  inference). A re-runnable `@pytest.mark.live` suite lives in `tests/live/`
  (`make test-live`). Two spec-vs-reality bugs found and fixed there:
  - observability `.csv` export endpoints return raw CSV bytes, not JSON (the
    spec mislabels them `application/json`).
  - void endpoints returning `WSResponse[NoneType]` (`{success, result: null}`)
    now return `None` on success instead of raising, and are typed `-> None`.
  - `agents.list_organization_agents` decodes its enveloped `result` as a list
    (the API returns an array of agents), not an object.
  - `WSResponse[bool]` endpoints (`logout`, delete-api-key, disable-user, the two
    shield-attach ops, create-trace-read) return the boolean `result`, not a
    `dict` (they previously raised `Expected object, got bool`).
- Live suite additionally covers api-key and organization-role create→delete
  lifecycles, and `tests/live/conftest.py` loads `.env` so `make test-live`
  actually runs.
- A unit test for every one of the 316 endpoints (316/316 methods exercised);
  433 tests passing; `mypy --strict` clean; `ruff` lint + format clean.
- Ships library-only distributions (wheel + sdist exclude tests/spec/docs) and
  a `Makefile` (`make dev/test/check/build/publish/...`).
- Health probes (`health.readiness()` / `health.liveness()`) fail fast:
  they default to a 5s timeout and do NOT retry, so an unreachable backend
  raises promptly instead of hanging for the full 60s request timeout across
  the retry budget (~3 min worst case). Override with `timeout=`.
- Internal: `request()` gained per-call `timeout` and `max_retries` overrides
  (threaded to httpx), usable by any resource that needs non-default limits.