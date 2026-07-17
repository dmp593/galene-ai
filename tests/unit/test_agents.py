import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    AgentPinRequest,
    AgentRolePermissionRequest,
    DatabaseConnectorAddRequest,
    KBConnectorAddRequest,
    MCPPromptFetchRequest,
    MCPResourcesIngestRequest,
    MCPServerAddRequest,
    MCPServerUpdateRequest,
    ModelsConnectorsDatabaseConnectorUpdateRequest,
    ModelsConnectorsKBConnectorUpdateRequest,
    PersonalAgentAttachmentBatchDeleteRequest,
    PersonalAgentDocumentUrlListRequest,
    PersonalAgentUrlListRequest,
    PersonalAgentWebsiteDocumentsScrapeRequest,
    PersonalAgentWebsiteScrapeRequest,
    SiteampRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _ok(expect_method, expect_path, *, body_check=None, param_check=None, json_out=None):
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == expect_method
        assert req.url.path == expect_path
        if body_check is not None:
            body_check(req.content)
        if param_check is not None:
            param_check(req.url.params)
        return httpx.Response(200, json=json_out if json_out is not None else {"ok": True})

    return handler


def test_list():
    r = _client(_ok("GET", "/agents", json_out={"agents": []})).agents.list()
    assert r == {"agents": []}


def test_retrieve():
    r = _client(_ok("GET", "/agent/a1", json_out={"id": "a1"})).agents.retrieve("a1")
    assert r["id"] == "a1"


def test_delete():
    r = _client(_ok("DELETE", "/agent/a1")).agents.delete("a1")
    assert r == {"ok": True}


def test_pin():
    def check(content):
        assert b'"pinned":true' in content

    r = _client(_ok("POST", "/agent/a1/pin", body_check=check)).agents.pin(
        "a1", body=AgentPinRequest(pinned=True)
    )
    assert r == {"ok": True}


def test_upsert():
    r = _client(_ok("POST", "/agent/assistant")).agents.upsert("assistant")
    assert r == {"ok": True}


def test_share_with_organization():
    r = _client(_ok("POST", "/agent/share/a1/organization/o1")).agents.share_with_organization(
        "a1", "o1"
    )
    assert r == {"ok": True}


def test_upload_file():
    def check(content):
        assert b'name="file"; filename="doc.pdf"' in content
        assert b"PDFDATA" in content

    r = _client(_ok("POST", "/agent/personal/a1/files", body_check=check)).agents.upload_file(
        "a1", b"PDFDATA", filename="doc.pdf"
    )
    assert r == {"ok": True}


def test_batch_delete_files():
    def check(content):
        assert b'"ids"' in content
        assert b"f1" in content

    r = _client(
        _ok("DELETE", "/agent/personal/a1/files", body_check=check)
    ).agents.batch_delete_files(
        "a1", body=PersonalAgentAttachmentBatchDeleteRequest(ids=["f1", "f2"])
    )
    assert r == {"ok": True}


def test_delete_file():
    r = _client(_ok("DELETE", "/agent/personal/a1/file/f1")).agents.delete_file("a1", "f1")
    assert r == {"ok": True}


def test_retry_file():
    r = _client(_ok("POST", "/agent/personal/a1/file/f1/retry")).agents.retry_file("a1", "f1")
    assert r == {"ok": True}


def test_add_urls():
    def check(content):
        assert b"https://example.com" in content

    r = _client(_ok("POST", "/agent/personal/a1/urls", body_check=check)).agents.add_urls(
        "a1", body=PersonalAgentUrlListRequest(urls=["https://example.com"])
    )
    assert r == {"ok": True}


def test_delete_all_files():
    r = _client(_ok("DELETE", "/agent/personal/a1/all_files")).agents.delete_all_files("a1")
    assert r == {"ok": True}


def test_get_sitemap():
    r = _client(_ok("POST", "/agent/personal/get_sitemap")).agents.get_sitemap(
        body=SiteampRequest(url="https://example.com")
    )
    assert r == {"ok": True}


def test_scrape_website():
    r = _client(_ok("POST", "/agent/personal/a1/scrape_website")).agents.scrape_website(
        "a1", body=PersonalAgentWebsiteScrapeRequest(url="https://example.com")
    )
    assert r == {"ok": True}


def test_scrape_website_documents():
    r = _client(
        _ok("POST", "/agent/personal/a1/scrape_website_documents")
    ).agents.scrape_website_documents(
        "a1", body=PersonalAgentWebsiteDocumentsScrapeRequest(domain="example.com", file_type="pdf")
    )
    assert r == {"ok": True}


def test_ingest_website_documents():
    r = _client(_ok("POST", "/agent/personal/a1/documents")).agents.ingest_website_documents(
        "a1", body=PersonalAgentDocumentUrlListRequest(urls=["https://example.com/a.pdf"])
    )
    assert r == {"ok": True}


def test_delete_url():
    r = _client(_ok("DELETE", "/agent/personal/a1/url/u1")).agents.delete_url("a1", "u1")
    assert r == {"ok": True}


def test_retry_url():
    r = _client(_ok("POST", "/agent/personal/a1/url/u1/retry")).agents.retry_url("a1", "u1")
    assert r == {"ok": True}


def test_add_mcp_server():
    r = _client(_ok("POST", "/agent/personal/a1/mcp_servers")).agents.add_mcp_server(
        "a1", body=MCPServerAddRequest(name="srv", organization_mcp_server_uuid="s1")
    )
    assert r == {"ok": True}


def test_list_available_mcp_servers():
    def pcheck(params):
        assert params["org_id"] == "o1"

    r = _client(
        _ok("GET", "/agents/mcp_servers", param_check=pcheck)
    ).agents.list_available_mcp_servers(org_id="o1")
    assert r == {"ok": True}


def test_retrieve_mcp_server():
    r = _client(_ok("GET", "/agents/mcp_servers/s1")).agents.retrieve_mcp_server("s1")
    assert r == {"ok": True}


def test_ingest_mcp_resources():
    r = _client(_ok("POST", "/agent/personal/a1/mcp_resources/ingest")).agents.ingest_mcp_resources(
        "a1", body=MCPResourcesIngestRequest(conversation_id="c1", uris=["mcp://x"])
    )
    assert r == {"ok": True}


def test_get_mcp_prompt():
    r = _client(_ok("POST", "/agent/personal/a1/mcp_prompts")).agents.get_mcp_prompt(
        "a1", body=MCPPromptFetchRequest(conversation_id="c1", server_uuid="s1", prompt_name="p")
    )
    assert r == {"ok": True}


def test_delete_mcp_server():
    r = _client(_ok("DELETE", "/agent/personal/a1/mcp_servers/s1")).agents.delete_mcp_server(
        "a1", "s1"
    )
    assert r == {"ok": True}


def test_update_mcp_server():
    r = _client(_ok("PUT", "/agent/personal/a1/mcp_servers/s1")).agents.update_mcp_server(
        "a1", "s1", body=MCPServerUpdateRequest()
    )
    assert r == {"ok": True}


def test_add_database_connector():
    r = _client(
        _ok("POST", "/agent/personal/a1/database_connectors")
    ).agents.add_database_connector(
        "a1", body=DatabaseConnectorAddRequest(name="db", organization_db_connector_uuid="c1")
    )
    assert r == {"ok": True}


def test_list_database_connectors():
    r = _client(
        _ok("GET", "/agent/personal/a1/database_connectors")
    ).agents.list_database_connectors("a1")
    assert r == {"ok": True}


def test_list_available_database_connectors():
    r = _client(
        _ok("GET", "/agents/database_connectors")
    ).agents.list_available_database_connectors()
    assert r == {"ok": True}


def test_retrieve_database_connector():
    r = _client(_ok("GET", "/agents/database_connectors/c1")).agents.retrieve_database_connector(
        "c1"
    )
    assert r == {"ok": True}


def test_delete_database_connector():
    r = _client(
        _ok("DELETE", "/agent/personal/a1/database_connectors/c1")
    ).agents.delete_database_connector("a1", "c1")
    assert r == {"ok": True}


def test_update_database_connector():
    def check(content):
        assert b"renamed" in content

    r = _client(
        _ok("PUT", "/agent/personal/a1/database_connectors/c1", body_check=check)
    ).agents.update_database_connector(
        "a1", "c1", body=ModelsConnectorsDatabaseConnectorUpdateRequest(name="renamed")
    )
    assert r == {"ok": True}


def test_add_kb_connector():
    r = _client(_ok("POST", "/agent/personal/a1/kb_connectors")).agents.add_kb_connector(
        "a1", body=KBConnectorAddRequest(name="kb", organization_kb_connector_uuid="k1")
    )
    assert r == {"ok": True}


def test_list_kb_connectors():
    r = _client(_ok("GET", "/agent/personal/a1/kb_connectors")).agents.list_kb_connectors("a1")
    assert r == {"ok": True}


def test_list_available_kb_connectors():
    r = _client(_ok("GET", "/agents/kb_connectors")).agents.list_available_kb_connectors()
    assert r == {"ok": True}


def test_retrieve_kb_connector():
    r = _client(_ok("GET", "/agents/kb_connectors/k1")).agents.retrieve_kb_connector("k1")
    assert r == {"ok": True}


def test_delete_kb_connector():
    r = _client(_ok("DELETE", "/agent/personal/a1/kb_connectors/k1")).agents.delete_kb_connector(
        "a1", "k1"
    )
    assert r == {"ok": True}


def test_update_kb_connector():
    r = _client(_ok("PUT", "/agent/personal/a1/kb_connectors/k1")).agents.update_kb_connector(
        "a1", "k1", body=ModelsConnectorsKBConnectorUpdateRequest(name="renamed")
    )
    assert r == {"ok": True}


def test_get_permissions():
    r = _client(_ok("GET", "/agent/a1/permissions")).agents.get_permissions("a1")
    assert r == {"ok": True}


def test_set_permissions():
    def check(content):
        assert b"role_ids" in content

    r = _client(_ok("POST", "/agent/a1/permissions", body_check=check)).agents.set_permissions(
        "a1", body=AgentRolePermissionRequest(role_ids=[1, 2])
    )
    assert r == {"ok": True}


def test_list_invitations():
    r = _client(_ok("GET", "/agents/invitations")).agents.list_invitations()
    assert r == {"ok": True}


def test_accept_invitation():
    r = _client(_ok("GET", "/agents/a1/approve")).agents.accept_invitation("a1")
    assert r == {"ok": True}


def test_deny_invitation():
    r = _client(_ok("GET", "/agents/a1/deny")).agents.deny_invitation("a1")
    assert r == {"ok": True}


def test_share_with_user():
    r = _client(_ok("POST", "/agent/share/a1/user_id/u1")).agents.share_with_user("a1", "u1")
    assert r == {"ok": True}


def test_create_from_catalog():
    def check(content):
        assert b'name="inputs"' in content
        assert b"CATALOGDATA" in content

    r = _client(
        _ok("POST", "/agents/personal/from_catalog/cat1", body_check=check)
    ).agents.create_from_catalog("cat1", inputs="{}", files=[b"CATALOGDATA"])
    assert r == {"ok": True}


def test_get_catalog_template():
    r = _client(_ok("GET", "/agents/personal/catalog/cat1")).agents.get_catalog_template("cat1")
    assert r == {"ok": True}


def test_list_organization_agents_unwraps_envelope_list():
    # The enveloped `result` is an ARRAY of agent objects (verified live), not an object.
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org1/agents"
        return httpx.Response(
            200,
            json={
                "success": True,
                "message": "ok",
                "result": [{"id": "a1", "name": "one"}, {"id": "a2", "name": "two"}],
            },
        )

    r = _client(handler).agents.list_organization_agents("org1")
    assert isinstance(r, list)
    assert [a["id"] for a in r] == ["a1", "a2"]


async def test_async_agents_retrieve_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/agent/a9"
        return httpx.Response(200, json={"id": "a9"})

    client = _aclient(handler)
    try:
        result = await client.agents.retrieve("a9")
        assert result["id"] == "a9"
    finally:
        await client.aclose()
