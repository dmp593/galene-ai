# scripts/build_registry.py
"""Build the operation registry (spec/operations.json) from the vendored OpenAPI spec.

Dev-only. Output is committed. Regenerate with: python scripts/build_registry.py
CI asserts the committed spec/operations.json is byte-identical to a fresh run.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RANK = {
    "KB Connectors": 100,
    "KB Sync": 100,
    "Database Connectors": 100,
    "MCP Servers": 100,
    "Groups": 100,
    "Roles": 95,
    "TTS Language Samples": 100,
    "Audio Sample Management": 100,
    "Agents": 100,
    "API Keys": 100,
    "Api-Keys": 100,
    "Deployment": 100,
    "SSO": 80,
    "Conversations": 60,
    "Attachments": 60,
    "Shield": 60,
    "Observability": 60,
    "Notifications": 60,
    "Support Tickets (Zammad)": 60,
    "User Ticket Operations": 60,
    "Admin Ticket Management": 60,
    "Admin - Search": 60,
    "Admin - User API Keys": 60,
    "Frontend": 60,
    "Changelog": 60,
    "Release Notes": 60,
    "Health Checks": 60,
    "OpenAI API": 60,
    "Authentication": 70,
    "Users": 50,
    "User": 50,
    "Admin Management": 40,
    "Admin - Organization Specific Configuration Settings": 20,
    "Admin - Global Configuration Settings": 20,
    "Organizations": 10,
}
ADMIN = {
    "Admin - Global Configuration Settings": "admin.global_config",
    "Admin - Organization Specific Configuration Settings": "admin.org_config",
    "Admin Ticket Management": "admin.tickets",
    "Admin Management": "admin.management",
    "Admin - Search": "admin.search",
    "Admin - User API Keys": "admin.user_api_keys",
    "Deployment": "admin.deployment",
    "Frontend": "admin.frontend",
}
MERGE = {
    "Api-Keys": "api_keys",
    "API Keys": "api_keys",
    "User": "users",
    "Users": "users",
    "Support Tickets (Zammad)": "tickets",
    "User Ticket Operations": "tickets",
    "TTS Language Samples": "tts",
    "Audio Sample Management": "tts",
    "Health Checks": "health",
    "Authentication": "auth",
    "SSO": "auth",
    "KB Connectors": "kb_connectors",
    "KB Sync": "kb_sync",
    "Database Connectors": "database_connectors",
    "MCP Servers": "mcp_servers",
    "Groups": "groups",
    "Roles": "roles",
    "Agents": "agents",
    "Conversations": "conversations",
    "Attachments": "attachments",
    "Shield": "shield",
    "Observability": "observability",
    "Notifications": "notifications",
    "Organizations": "organizations",
    "Changelog": "changelog",
    "Release Notes": "release_notes",
}


def _openai_ns(path: str) -> str:
    p = re.sub(r"^/\{mode\}", "", path)
    for pre, ns in [
        ("/v1/chat", "chat"),
        ("/v1/responses", "responses"),
        ("/v1/embeddings", "embeddings"),
        ("/v1/models", "models"),
        ("/v1/moderations", "moderations"),
        ("/v1/files", "files"),
        ("/v1/vector_stores", "vector_stores"),
        ("/v1/audio", "audio"),
    ]:
        if p.startswith(pre):
            return ns
    return "openai_misc"


def _ns_for(tag: str, path: str) -> str:
    if tag == "OpenAI API":
        return _openai_ns(path)
    if tag in ADMIN:
        return ADMIN[tag]
    if tag in MERGE:
        return MERGE[tag]
    return re.sub(r"[^a-z0-9]+", "_", tag.lower()).strip("_")


def build_registry(spec: dict) -> list[dict]:
    rows = []
    for p, item in spec["paths"].items():
        for m, op in item.items():
            if m not in ("get", "post", "put", "patch", "delete"):
                continue
            tags = list(dict.fromkeys(op.get("tags") or ["untagged"]))
            best = max(tags, key=lambda t: RANK.get(t, 55))
            rows.append(
                {
                    "namespace": _ns_for(best, p),
                    "method": m.upper(),
                    "path": p,
                    "operationId": op.get("operationId", ""),
                    "summary": (op.get("summary") or "").strip(),
                    "tag": best,
                }
            )
    return rows


def main() -> None:
    spec = json.loads((ROOT / "spec" / "openapi.json").read_text())
    rows = build_registry(spec)
    with open(ROOT / "spec" / "operations.json", "w") as f:
        json.dump(rows, f, indent=1)  # NO trailing newline — matches the committed file
    print(f"wrote {len(rows)} operations")


if __name__ == "__main__":
    main()
