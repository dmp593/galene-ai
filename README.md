# galene-ai

Python SDK for the [Galene.AI](https://api.playground.galene.ai) platform — a single,
typed client covering all 317 REST operations of the API, generated and
hand-crafted from the vendored OpenAPI spec (`spec/openapi.json`).

- **Familiar ergonomics** — `client.chat.create(...)`, `client.files.upload(...)`,
  OpenAI-SDK-style.
- **Sync and async** — `Galene` and `AsyncGalene` share one core and expose an
  identical API.
- **Typed** — [`msgspec`](https://jcristharif.com/msgspec/) models generated from
  the spec; `mypy --strict` clean.
- **Slim** — two runtime dependencies: `httpx` and `msgspec`.
- **Production-ready** — retries with backoff, pluggable auth (API key or
  username/password with auto-refresh), SSE streaming, cursor pagination.

## Install

```bash
pip install galene-ai
```

Requires Python 3.12+.

## Quickstart

```python
from galene_ai import Galene
from galene_ai.models._generated import VectorStoreCreate, VectorStoreFileAdd, VectorStoreSearchRequest

client = Galene(api_key="sk-...")  # or set GALENE_AI_API_KEY in the environment

# Chat completion
reply = client.chat.create(
    model="Galene/LLM",
    messages=[{"role": "user", "content": "Hi"}],
)
print(reply.choices[0].message.content)

# Upload a file
uploaded = client.files.upload(b"some file bytes", purpose="user_data", filename="doc.txt")

# Vector stores (RAG)
vector_store = client.vector_stores.create(VectorStoreCreate(name="kb"))
client.vector_stores.add_file(vector_store.id, VectorStoreFileAdd(file_id=uploaded.id))
results = client.vector_stores.search(vector_store.id, VectorStoreSearchRequest(query="pricing"))

client.close()
```

`VectorStoreCreate`, `VectorStoreFileAdd`, and `VectorStoreSearchRequest` are
generated request models (see
[examples/vector_store_rag.py](examples/vector_store_rag.py) for the full,
runnable version). `Galene` is also a context manager:

```python
with Galene(api_key="sk-...") as client:
    ...  # client.close() is called automatically
```

## Authentication

The default is a static API key, supplied explicitly or via environment
variable:

```python
from galene_ai import Galene

client = Galene(api_key="sk-...")   # explicit
client = Galene()                   # reads GALENE_AI_API_KEY from the environment
```

Environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `GALENE_AI_API_KEY` | API key used by the default `ApiKeyAuth` | — |
| `GALENE_AI_BASE_URL` | API base URL | `https://api.playground.galene.ai` |

Both are optional — the base URL defaults to the public playground, so point it
at your own deployment via the env var or the `base_url=` argument. The SDK also **auto-loads a `.env` file** from the
working directory (real environment variables always win). Copy `.env.example`
to `.env` and fill it in:

```bash
cp .env.example .env   # then set GALENE_AI_API_KEY / GALENE_AI_BASE_URL
```

For username/password login with transparent token refresh, pass a
`SessionAuth` instance as `auth=`:

```python
from galene_ai import Galene, SessionAuth

client = Galene(auth=SessionAuth(username="me@example.com", password="hunter2"))
```

`SessionAuth` logs in via `POST /login` on the first request, attaches the
resulting access token to every request, and — on a `401` — transparently
calls `POST /refresh-token` and retries once. Auth is pluggable: any
`httpx.Auth` subclass can be passed as `auth=`.

## Async usage

`AsyncGalene` mirrors `Galene` method-for-method:

```python
import asyncio
from galene_ai import AsyncGalene


async def main() -> None:
    async with AsyncGalene(api_key="sk-...") as client:
        reply = await client.chat.create(
            model="Galene/LLM",
            messages=[{"role": "user", "content": "Hi"}],
        )
        print(reply.choices[0].message.content)


asyncio.run(main())
```

## Streaming

Pass `stream=True` to `chat.create` (or `responses.create`) to get a
`Stream[dict]` (or `AsyncStream[dict]`) of raw SSE chunks — the spec defines no
fixed chunk schema, so chunks decode as plain dicts in the standard OpenAI
delta shape:

```python
with client.chat.create(
    model="Galene/LLM",
    messages=[{"role": "user", "content": "Count to five."}],
    stream=True,
) as stream:
    for chunk in stream:
        delta = (chunk.get("choices") or [{}])[0].get("delta") or {}
        print(delta.get("content") or "", end="", flush=True)
```

The async equivalent uses `async for chunk in stream:` inside `async with`.

## Pagination

List methods on cursor-paginated namespaces (`files`, `vector_stores`, ...)
return a `CursorPage[T]` (or `AsyncCursorPage[T]`) with `.data`, `.has_more`,
and `.auto_paging_iter()`:

```python
for vector_store in client.vector_stores.list().auto_paging_iter():
    print(vector_store.id, vector_store.name)
```

Async (`async for` on an `AsyncCursorPage` already walks every page — no
separate `auto_paging_iter()` call needed):

```python
async for vector_store in await client.vector_stores.list():
    print(vector_store.id)
```

Namespaces that use offset pagination (e.g. `observability`) instead expose
plain `limit`/`offset` keyword arguments and return a `list[...]` directly.

## Error handling

Every error raised by the SDK subclasses `GaleneError`. HTTP error responses
raise a status-specific subclass of `APIStatusError`, mirroring the OpenAI SDK
hierarchy:

```python
from galene_ai import GaleneError, NotFoundError

try:
    client.files.retrieve("file-does-not-exist")
except NotFoundError as e:
    print(e.status_code, e.request_id, e.body)
except GaleneError as e:
    print("Galene API error:", e)
```

```
GaleneError
├─ APIConnectionError            (network failure)
│  └─ APITimeoutError
└─ APIStatusError                (.status_code, .request_id, .response, .body)
   ├─ BadRequestError            400
   ├─ AuthenticationError        401
   ├─ PermissionDeniedError      403
   ├─ NotFoundError              404
   ├─ ConflictError              409
   ├─ UnprocessableEntityError   422
   ├─ RateLimitError             429
   └─ InternalServerError        5xx
```

Connection failures and `408/409/429/500/502/503/504` responses are retried
automatically with exponential backoff (`max_retries=2` by default,
configurable via `Galene(max_retries=...)`); non-idempotent generation
requests are never retried on a read timeout, since a timed-out generation
keeps running server-side.

## Namespaces

Every operation is reachable as `client.<namespace>.<method>(...)`
(async: `AsyncGalene`, identical shape). Admin operations nest under
`client.admin.<namespace>.<method>(...)`.

**OpenAI-compatible surface** (30 ops):

| Namespace | Ops | Namespace | Ops |
|---|--:|---|--:|
| `chat` | 2 | `files` | 6 |
| `responses` | 2 | `vector_stores` | 11 |
| `embeddings` | 2 | `audio` | 4 |
| `models` | 2 | `moderations` | 1 |

**Platform surface** (212 ops):

| Namespace | Ops | Namespace | Ops | Namespace | Ops |
|---|--:|---|--:|---|--:|
| `agents` | 46 | `attachments` | 10 | `api_keys` | 6 |
| `observability` | 16 | `conversations` | 10 | `groups` | 6 |
| `tickets` | 14 | `shield` | 9 | `notifications` | 5 |
| `users` | 13 | `mcp_servers` | 8 | `roles` | 4 |
| `auth` | 12 | | | `health` | 2 |
| `kb_sync` | 12 | | | `organizations` | 2 |
| `tts` | 12 | | | `release_notes` | 2 |
| `database_connectors` | 11 | | | `changelog` | 1 |
| `kb_connectors` | 11 | | | | |

**Admin surface**, nested under `client.admin.*` (74 ops):

| Namespace | Ops | Namespace | Ops |
|---|--:|---|--:|
| `admin.org_config` | 33 | `admin.tickets` | 7 |
| `admin.global_config` | 25 | `admin.management` | 5 |
| | | `admin.deployment` | 1 |
| | | `admin.frontend` | 1 |
| | | `admin.search` | 1 |
| | | `admin.user_api_keys` | 1 |

For example:

```python
client.agents.list()
client.observability.list_traces(status="running")
client.admin.org_config.set_favicon(org_uuid, favicon_png_bytes)
```

`observability` exposes trace/observation listing, read-audit trails, CSV
exports, and aggregate metrics directly (no further sub-resource nesting);
`conversations` exposes message- and attachment-related helpers the same way.
Endpoints with mode-prefixed variants (`chat`, `responses`, `embeddings`,
`models`; mode ∈ `direct`/`shield`/`appliance_shield`) expose a
`create_with_mode(mode, ...)` (or `list_with_mode(mode)`) sibling method
alongside the plain `/v1/...` one.

The full, machine-readable operation → namespace/method mapping lives in
`spec/operations.json`.

### Typing note: a handful of endpoints return `dict`

`spec/openapi.json` leaves the 200 response schema empty (`{}`, no `$ref`) for
a number of operations — most notably the entire `agents` namespace (46 ops)
and `attachments` namespace (10 ops), plus a few others scattered across the
SDK (`models.list`, `audio.voices`, the `observability` `.csv` export
endpoints, some `vector_stores` delete/batch responses). `datamodel-code-generator`
has nothing to generate a model from in those cases, so the SDK decodes the
response as a plain `dict[str, Any]` rather than guessing a shape that might
not match production.

To upgrade one of these to a typed `msgspec.Struct`:

1. Run `scripts/probe_shapes.py` against a reachable Galene instance
   (`GALENE_AI_API_KEY=... python scripts/probe_shapes.py`). It only issues GET
   requests — it never mutates data — and writes the observed JSON shapes to
   `probe_output/<operationId>.json`, plus a summary table to stdout.
2. Add a hand-written `msgspec.Struct` for the observed shape to
   `src/galene_ai/models/_extra.py` (see that module's docstring for the
   existing pattern used for `File`, `VectorStore`, etc.).
3. Update the resource method's `cast_to=` argument to the new model.

## Development

```bash
uv sync --extra dev
```

- **Regenerate models** (dev-only, output is committed):
  `uv run python scripts/generate_models.py`
- **Regenerate the operation registry** (dev-only, output is committed, drives
  the drift test): `uv run python scripts/build_registry.py`
- **Tests**: `uv run pytest`
- **Type-check**: `uv run mypy`
- **Lint / format**: `uv run ruff check .` / `uv run ruff format .`

`tests/test_drift.py` asserts that the set of `operationId`s implemented by
resource methods equals the set in `spec/operations.json` exactly — any API
addition, removal, or rename that isn't reflected in the SDK fails CI.

## License

MIT
