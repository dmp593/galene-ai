"""Probe response shapes for endpoints the OpenAPI spec leaves untyped.

Read-only dev tool. `spec/openapi.json` gives an empty `{}` 200-response schema
for a number of GET operations (see the README's "Typing note" section) — most
notably the entire `agents` and `attachments` namespaces. This script hits
those endpoints on a real, reachable Galene instance to capture what they
actually return, so a follow-up task can replace their `dict` returns with
real `msgspec.Struct` models in `src/galene_ai/models/_extra.py`.

Usage
-----

    GALENE_AI_API_KEY=sk-... python scripts/probe_shapes.py
    # optionally target a non-default host:
    GALENE_AI_API_KEY=sk-... GALENE_AI_BASE_URL=https://staging.example.com \\
        python scripts/probe_shapes.py

Safety
------
This script is GET-only by construction: it selects operations straight from
`spec["paths"][path]["get"]` and never looks at (or calls) `post`/`put`/
`patch`/`delete` for any path. `_request()` additionally asserts the HTTP
method is `"GET"` before every call, as a second line of defense. No request
ever carries a body. Nothing is created, modified, or deleted on the target
instance — this only ever reads.

What it does
------------
1. Loads `spec/openapi.json` and selects every GET operation whose 200
   response has an empty JSON schema (`{}` — no `$ref`), i.e. the operations
   this SDK currently types as `dict[str, Any]`.
2. Phase 1: calls every such operation that takes no path parameters (list
   endpoints), and harvests string values found under id-shaped keys (`id`,
   `*_id`, `*_uuid`) anywhere in the response.
3. Phase 2: for operations that take exactly one path parameter, looks for a
   harvested id whose source key plausibly matches that parameter (by name,
   or by the resource segment preceding it in the path) and calls the
   endpoint with it substituted in. Operations with no matching harvested id
   are skipped and reported as such, not treated as errors. Operations with
   more than one path parameter are also skipped (no attempt to guess
   combinations).
4. Writes each successful response body to `probe_output/<operationId>.json`
   and prints a summary table (operationId, status, top-level shape).

Next step
---------
Hand the contents of `probe_output/` to a follow-up task that adds concrete
`msgspec.Struct` models to `src/galene_ai/models/_extra.py` for shapes that
turn out to be stable, then updates the corresponding resource method's
`cast_to=` argument to the new model (see the README's "Typing note").

This script is never invoked by CI or tests — it talks to a live backend and
is meant to be run by hand when that backend is reachable.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "spec" / "openapi.json"
OUTPUT_DIR = ROOT / "probe_output"
DEFAULT_BASE_URL = "https://api.playground.galene.ai"
TIMEOUT_SECONDS = 20.0

_ID_KEY_RE = re.compile(r"^(id|.*_id|.*_uuid)$")
_PATH_PARAM_RE = re.compile(r"\{([^{}]+)\}")


class Operation:
    """A GET operation with an empty (untyped) 200 response schema."""

    __slots__ = ("operation_id", "path", "path_params")

    def __init__(self, operation_id: str, path: str, path_params: list[str]) -> None:
        self.operation_id = operation_id
        self.path = path
        self.path_params = path_params


def _load_untyped_get_operations(spec: dict[str, Any]) -> list[Operation]:
    """Every GET operation whose 200 response schema is the empty object `{}`."""
    ops: list[Operation] = []
    for path, item in spec.get("paths", {}).items():
        for method, op in item.items():
            if method.lower() != "get":
                continue  # by construction: never even look at non-GET methods
            responses = op.get("responses", {})
            ok_response = responses.get("200", {})
            content = ok_response.get("content", {})
            schema = content.get("application/json", {}).get("schema")
            if schema != {}:
                continue  # typed (or no 200 response) — not our concern here
            operation_id = op.get("operationId") or f"GET {path}"
            path_params = _PATH_PARAM_RE.findall(path)
            ops.append(Operation(operation_id, path, path_params))
    return ops


def _normalize(name: str) -> str:
    name = name.lower()
    for suffix in ("_uuid", "_id"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def _resource_hint(path: str, param: str) -> str:
    """Best-effort resource name for a path param, from the path segment before it."""
    segments = [s for s in path.split("/") if s]
    placeholder = "{" + param + "}"
    if placeholder in segments:
        idx = segments.index(placeholder)
        if idx > 0:
            return _normalize(segments[idx - 1].rstrip("s"))
    return _normalize(param)


def _harvest_ids(value: Any, into: dict[str, list[str]], *, depth: int = 0) -> None:
    """Recursively collect string values found under id-shaped keys.

    Matches keys literally named `id`, or ending in `_id` / `_uuid` (case-insensitive).
    """
    if depth > 6:
        return
    if isinstance(value, dict):
        for key, val in value.items():
            if isinstance(val, str) and val and _ID_KEY_RE.match(key.lower()):
                bucket = into.setdefault(key.lower(), [])
                if val not in bucket:
                    bucket.append(val)
            _harvest_ids(val, into, depth=depth + 1)
    elif isinstance(value, list):
        for item in value:
            _harvest_ids(item, into, depth=depth + 1)


def _find_id_for(param: str, path: str, harvested: dict[str, list[str]]) -> str | None:
    """Find a harvested id that plausibly belongs to `param` on `path`."""
    exact = harvested.get(param.lower())
    if exact:
        return exact[0]

    hint = _resource_hint(path, param)
    candidates: list[str] = []
    for key, values in harvested.items():
        if not values:
            continue
        norm_key = _normalize(key)
        if norm_key == hint or hint in norm_key or norm_key in hint:
            candidates.extend(values)
    return candidates[0] if candidates else None


def _request(client: httpx.Client, method: str, path: str) -> tuple[int | None, Any, str | None]:
    """Issue one GET request. Returns `(status_code, decoded_json, error_message)`."""
    assert method.upper() == "GET", "probe_shapes.py is GET-only by design"
    try:
        response = client.request(method, path, timeout=TIMEOUT_SECONDS)
    except httpx.HTTPError as exc:
        return None, None, f"{type(exc).__name__}: {exc}"
    try:
        body = response.json()
    except ValueError:
        body = None
    return response.status_code, body, None


def _shape_summary(body: Any) -> str:
    if isinstance(body, list):
        return f"list[{len(body)}]"
    if isinstance(body, dict):
        keys = list(body.keys())
        shown = ", ".join(keys[:8])
        more = "" if len(keys) <= 8 else f", +{len(keys) - 8} more"
        return f"dict{{{shown}{more}}}"
    return type(body).__name__


def _write_capture(operation_id: str, body: Any) -> None:
    path = OUTPUT_DIR / f"{operation_id}.json"
    path.write_text(json.dumps(body, indent=2, default=str))


def _print_summary(rows: list[tuple[str, int | None, str]]) -> None:
    op_width = max((len(op_id) for op_id, _, _ in rows), default=11)
    op_width = max(op_width, len("operationId"))
    print()
    print(f"{'operationId':<{op_width}}  {'status':<6}  shape")
    print("-" * (op_width + 6 + 40))
    for operation_id, status, shape in rows:
        status_str = str(status) if status is not None else "-"
        print(f"{operation_id:<{op_width}}  {status_str:<6}  {shape}")


def main() -> int:
    api_key = os.environ.get("GALENE_AI_API_KEY")
    if not api_key:
        print("GALENE_AI_API_KEY is required.", file=sys.stderr)
        return 1
    base_url = os.environ.get("GALENE_AI_BASE_URL", DEFAULT_BASE_URL)

    spec = json.loads(SPEC_PATH.read_text())
    operations = _load_untyped_get_operations(spec)
    parameterless = [op for op in operations if not op.path_params]
    single_param = [op for op in operations if len(op.path_params) == 1]
    multi_param = [op for op in operations if len(op.path_params) > 1]

    print(f"{len(operations)} untyped GET operations found in the spec:")
    print(f"  {len(parameterless)} parameterless (phase 1)")
    print(f"  {len(single_param)} single-path-param (phase 2)")
    print(f"  {len(multi_param)} multi-path-param (skipped, not attempted)")

    OUTPUT_DIR.mkdir(exist_ok=True)

    rows: list[tuple[str, int | None, str]] = []
    harvested: dict[str, list[str]] = {}

    with httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {api_key}"}) as client:
        # Phase 1: parameterless GETs (list endpoints) — also harvest ids from them.
        for op in parameterless:
            status, body, error = _request(client, "GET", op.path)
            if error is not None:
                rows.append((op.operation_id, None, error))
                continue
            if status == 200 and body is not None:
                _harvest_ids(body, harvested)
                _write_capture(op.operation_id, body)
            rows.append((op.operation_id, status, _shape_summary(body)))

        # Phase 2: single-path-param GETs, substituting a harvested id when we have one.
        for op in single_param:
            param = op.path_params[0]
            resolved_id = _find_id_for(param, op.path, harvested)
            if resolved_id is None:
                rows.append((op.operation_id, None, "skipped: no id harvested"))
                continue
            resolved_path = op.path.replace("{" + param + "}", resolved_id)
            status, body, error = _request(client, "GET", resolved_path)
            if error is not None:
                rows.append((op.operation_id, None, error))
                continue
            if status == 200 and body is not None:
                _write_capture(op.operation_id, body)
            rows.append((op.operation_id, status, _shape_summary(body)))

    for op in multi_param:
        rows.append((op.operation_id, None, f"skipped: {len(op.path_params)} path params"))

    _print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
