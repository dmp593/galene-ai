"""Live integration tests against a real Galene backend.

Marked ``@pytest.mark.live`` and DESELECTED by default (`pyproject.toml` sets
``addopts = "-m 'not live'"``). Run them with::

    GALENE_AI_API_KEY=... GALENE_AI_BASE_URL=https://your-galene-instance.example make test-live

Safety: read endpoints are called freely; every write test creates its OWN
throwaway resource (named ``galene-sdk-selftest``) and deletes it in a
``finally`` — no existing/production data is ever touched. Endpoints that would
mutate shared/production state (admin/global config, user/org deletion, agent
upsert-by-type) are intentionally NOT exercised here.

These tests validated the SDK against a real Galene backend during development;
they double as a smoke test you can re-run after any change.
"""

import os

import pytest

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    DeleteApiKeyRequest,
    OrganizationRoleCreateRequest,
    VectorStoreCreate,
    VectorStoreSearchRequest,
)

pytestmark = pytest.mark.live

MODEL = os.environ.get("GALENE_TEST_MODEL", "Galene/LLM")
EMBED_MODEL = os.environ.get("GALENE_TEST_EMBED_MODEL", "Galene/Embedding")
_SELFTEST_NAME = "galene-sdk-selftest"


@pytest.fixture(scope="module")
def client():
    if not os.environ.get("GALENE_AI_API_KEY"):
        pytest.skip("GALENE_AI_API_KEY not set — live tests skipped")
    c = Galene(timeout=60)
    yield c
    c.close()


# --- read endpoints --------------------------------------------------------
def test_health(client):
    assert "status" in client.health.readiness()


def test_models_list(client):
    assert client.models.list()


def test_vector_stores_list(client):
    # decodes into typed VectorStore objects
    list(client.vector_stores.list())


def test_conversations_list(client):
    client.conversations.list()


def test_user_profile(client):
    assert client.users.get_profile() is not None


def test_observability_list_traces(client):
    client.observability.list_traces()


def test_observability_export_traces_returns_bytes(client):
    out = client.observability.export_traces(limit=1)
    assert isinstance(out, bytes)


# --- inference -------------------------------------------------------------
def test_chat_completion(client):
    reply = client.chat.create(model=MODEL, messages=[{"role": "user", "content": "Say OK"}])
    assert reply.choices


def test_embeddings(client):
    resp = client.embeddings.create(model=EMBED_MODEL, input="hello")
    assert resp.data


def test_responses(client):
    client.responses.create(model=MODEL, input="Say OK")


# --- write lifecycles (self-created, always cleaned up) --------------------
def test_vector_store_lifecycle(client):
    vs = client.vector_stores.create(body=VectorStoreCreate(name=_SELFTEST_NAME))
    try:
        assert client.vector_stores.retrieve(vs.id).id == vs.id
        result = client.vector_stores.search(vs.id, body=VectorStoreSearchRequest(query="hello"))
        assert result is not None
    finally:
        client.vector_stores.delete(vs.id)


def test_file_lifecycle(client):
    content = b"galene sdk selftest content"
    f = client.files.upload(content, filename=f"{_SELFTEST_NAME}.txt", purpose="user_data")
    try:
        assert client.files.retrieve(f.id).id == f.id
        assert client.files.content(f.id) == content
    finally:
        client.files.delete(f.id)


def test_conversation_lifecycle(client):
    conv = client.conversations.init()
    cid = conv.conversation_id
    try:
        assert client.conversations.retrieve(cid) is not None
    finally:
        # void delete: returns None on success (must not raise)
        assert client.conversations.delete(cid) is None


def _org_id(client):
    traces = client.observability.list_traces(limit=3)
    return next((t.organization_id for t in traces if getattr(t, "organization_id", None)), None)


def test_api_key_lifecycle(client):
    created = client.api_keys.create()
    key_id = None
    try:
        assert created.api_key.startswith("gln_")
        match = next(
            (
                k
                for k in client.api_keys.list().api_keys
                if k.masked_key.startswith(created.api_key[:8])
            ),
            None,
        )
        assert match is not None
        key_id = match.id
    finally:
        if key_id is not None:
            # delete returns the boolean success flag (WSResponse[bool])
            assert client.api_keys.delete(body=DeleteApiKeyRequest(api_key_id=key_id)) is True


def test_role_lifecycle(client):
    org = _org_id(client)
    if not org:
        pytest.skip("no organization id available")
    role = client.roles.create(
        org, body=OrganizationRoleCreateRequest(name=f"{_SELFTEST_NAME}-role", description="temp")
    )
    try:
        assert role.name == f"{_SELFTEST_NAME}-role"
    finally:
        client.roles.delete(org, role.id)


# --- async smoke -----------------------------------------------------------
async def test_async_chat_completion():
    if not os.environ.get("GALENE_AI_API_KEY"):
        pytest.skip("GALENE_AI_API_KEY not set")
    async with AsyncGalene(timeout=60) as client:
        reply = await client.chat.create(
            model=MODEL, messages=[{"role": "user", "content": "Say OK"}]
        )
        assert reply.choices
