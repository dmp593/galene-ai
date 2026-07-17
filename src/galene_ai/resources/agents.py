"""`agents` resource: user agents, personal-agent knowledge (files/URLs/website
scraping), MCP servers, database/knowledge-base connectors, permissions,
invitations, sharing, and catalog templates.

Every 200 response for these operations has the empty schema `{}` in
`spec/openapi.json` (only a documentation `example`, no `$ref`), so
`datamodel-code-generator` emitted no dedicated response model. We therefore
decode them un-typed as `dict[str, Any]` (`cast_to=dict`), matching the
`files.py` exemplar's handling of empty-schema responses. The single exception
is `list_organization_agents`, whose response is the standard
`{success, message, result}` envelope wrapping an ARRAY of agent objects
(verified live). It is decoded with `envelope=True, cast_to=list[...]`, so
`_core.envelope.unwrap` raises `GaleneError` on `success: false`.
"""

from __future__ import annotations

import builtins
from collections.abc import Sequence
from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
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


class Agents(SyncResource):
    """User agents, personal-agent knowledge, connectors, and sharing."""

    namespace: ClassVar[str] = "agents"

    @operation("_list_agents_get")
    def list(self) -> dict[str, Any]:
        """List user agents."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.get("/agents", cast_to=dict))

    @operation("_detail_agent__agent_id__get")
    def retrieve(self, agent_id: str) -> dict[str, Any]:
        """Get agent details."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.get(f"/agent/{agent_id}", cast_to=dict))

    @operation("_delete_agent_agent__agent_id__delete")
    def delete(self, agent_id: str) -> dict[str, Any]:
        """Delete agent."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.delete(f"/agent/{agent_id}", cast_to=dict))

    @operation("_set_agent_pin_agent__agent_id__pin_post")
    def pin(self, agent_id: str, *, body: AgentPinRequest) -> dict[str, Any]:
        """Pin or unpin an agent for the current user."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/{agent_id}/pin", json_body=body, cast_to=dict),
        )

    @operation("_upsert_agent_agent__agent_type__post")
    def upsert(self, agent_type: str) -> dict[str, Any]:
        """Create or update agent."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.post(f"/agent/{agent_type}", cast_to=dict))

    @operation(
        "_share_agent_with_organization_agent_share__agent_id__organization__organization_id__post"
    )
    def share_with_organization(self, agent_id: str, organization_id: str) -> dict[str, Any]:
        """Share agent with organization."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/share/{agent_id}/organization/{organization_id}", cast_to=dict
            ),
        )

    @operation("_personal_upload_file_agent_personal__agent_id__files_post")
    def upload_file(
        self, agent_id: str, file: bytes, *, filename: str | None = None
    ) -> dict[str, Any]:
        """Upload file to personal agent."""
        files = {"file": (filename or "upload", file)}
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/personal/{agent_id}/files", files=files, cast_to=dict),
        )

    @operation("_batch_delete_files_agent_personal__agent_id__files_delete")
    def batch_delete_files(
        self, agent_id: str, *, body: PersonalAgentAttachmentBatchDeleteRequest
    ) -> dict[str, Any]:
        """Delete multiple personal agent files."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(f"/agent/personal/{agent_id}/files", json_body=body, cast_to=dict),
        )

    @operation("_del_file_agent_personal__agent_id__file__file_id__delete")
    def delete_file(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Delete file from personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(f"/agent/personal/{agent_id}/file/{file_id}", cast_to=dict),
        )

    @operation("_retry_file_agent_personal__agent_id__file__file_id__retry_post")
    def retry_file(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Retry file ingestion for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/personal/{agent_id}/file/{file_id}/retry", cast_to=dict),
        )

    @operation("_personal_add_urls_agent_personal__agent_id__urls_post")
    def add_urls(self, agent_id: str, *, body: PersonalAgentUrlListRequest) -> dict[str, Any]:
        """Add URLs to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/personal/{agent_id}/urls", json_body=body, cast_to=dict),
        )

    @operation("_delete_all_files_agent_personal__agent_id__all_files_delete")
    def delete_all_files(self, agent_id: str) -> dict[str, Any]:
        """Delete all personal agent files."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(f"/agent/personal/{agent_id}/all_files", cast_to=dict),
        )

    @operation("_get_sitemap_agent_personal_get_sitemap_post")
    def get_sitemap(self, *, body: SiteampRequest) -> dict[str, Any]:
        """Discover a website's sitemap URLs."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post("/agent/personal/get_sitemap", json_body=body, cast_to=dict),
        )

    @operation("_scrape_website_agent_personal__agent_id__scrape_website_post")
    def scrape_website(
        self, agent_id: str, *, body: PersonalAgentWebsiteScrapeRequest
    ) -> dict[str, Any]:
        """Scrape website for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/scrape_website", json_body=body, cast_to=dict
            ),
        )

    @operation("_scrape_website_documents_agent_personal__agent_id__scrape_website_documents_post")
    def scrape_website_documents(
        self, agent_id: str, *, body: PersonalAgentWebsiteDocumentsScrapeRequest
    ) -> dict[str, Any]:
        """Discover website documents for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/scrape_website_documents",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_ingest_website_documents_agent_personal__agent_id__documents_post")
    def ingest_website_documents(
        self, agent_id: str, *, body: PersonalAgentDocumentUrlListRequest
    ) -> dict[str, Any]:
        """Ingest discovered website documents for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/documents", json_body=body, cast_to=dict
            ),
        )

    @operation("_del_url_agent_personal__agent_id__url__file_id__delete")
    def delete_url(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Delete URL content from personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(f"/agent/personal/{agent_id}/url/{file_id}", cast_to=dict),
        )

    @operation("_retry_url_agent_personal__agent_id__url__file_id__retry_post")
    def retry_url(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Retry URL ingestion for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/personal/{agent_id}/url/{file_id}/retry", cast_to=dict),
        )

    @operation("_add_mcp_server_agent_personal__agent_id__mcp_servers_post")
    def add_mcp_server(self, agent_id: str, *, body: MCPServerAddRequest) -> dict[str, Any]:
        """Add MCP server to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/mcp_servers", json_body=body, cast_to=dict
            ),
        )

    @operation("_get_user_available_mcp_servers_agents_mcp_servers_get")
    def list_available_mcp_servers(self, *, org_id: str | None = None) -> dict[str, Any]:
        """List available MCP servers."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get("/agents/mcp_servers", params={"org_id": org_id}, cast_to=dict),
        )

    @operation("_get_user_mcp_server_agents_mcp_servers__server_id__get")
    def retrieve_mcp_server(self, server_id: str) -> dict[str, Any]:
        """Get MCP server details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/mcp_servers/{server_id}", cast_to=dict),
        )

    @operation("_ingest_mcp_resources_agent_personal__agent_id__mcp_resources_ingest_post")
    def ingest_mcp_resources(
        self, agent_id: str, *, body: MCPResourcesIngestRequest
    ) -> dict[str, Any]:
        """Ingest MCP direct resources into a conversation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/mcp_resources/ingest",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_mcp_prompt_agent_personal__agent_id__mcp_prompts_post")
    def get_mcp_prompt(self, agent_id: str, *, body: MCPPromptFetchRequest) -> dict[str, Any]:
        """Fetch an MCP prompt for a conversation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/mcp_prompts", json_body=body, cast_to=dict
            ),
        )

    @operation("_delete_mcp_server_agent_personal__agent_id__mcp_servers__server_id__delete")
    def delete_mcp_server(self, agent_id: str, server_id: str) -> dict[str, Any]:
        """Remove MCP server from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(
                f"/agent/personal/{agent_id}/mcp_servers/{server_id}", cast_to=dict
            ),
        )

    @operation("_update_personal_mcp_server_agent_personal__agent_id__mcp_servers__server_id__put")
    def update_mcp_server(
        self, agent_id: str, server_id: str, *, body: MCPServerUpdateRequest
    ) -> dict[str, Any]:
        """Update MCP server for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.put(
                f"/agent/personal/{agent_id}/mcp_servers/{server_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_add_database_connector_agent_personal__agent_id__database_connectors_post")
    def add_database_connector(
        self, agent_id: str, *, body: DatabaseConnectorAddRequest
    ) -> dict[str, Any]:
        """Add database connector to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/database_connectors",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_agent_database_connectors_agent_personal__agent_id__database_connectors_get")
    def list_database_connectors(self, agent_id: str) -> dict[str, Any]:
        """List agent's database connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agent/personal/{agent_id}/database_connectors", cast_to=dict),
        )

    @operation("_get_user_available_database_connectors_agents_database_connectors_get")
    def list_available_database_connectors(self, *, org_id: str | None = None) -> dict[str, Any]:
        """List available database connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(
                "/agents/database_connectors", params={"org_id": org_id}, cast_to=dict
            ),
        )

    @operation("_get_user_database_connector_agents_database_connectors__connector_id__get")
    def retrieve_database_connector(self, connector_id: str) -> dict[str, Any]:
        """Get database connector details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/database_connectors/{connector_id}", cast_to=dict),
        )

    @operation(
        "_delete_database_connector_agent_personal__agent_id__database_connectors__connector_id__delete"
    )
    def delete_database_connector(self, agent_id: str, connector_id: str) -> dict[str, Any]:
        """Remove database connector from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(
                f"/agent/personal/{agent_id}/database_connectors/{connector_id}", cast_to=dict
            ),
        )

    @operation(
        "_update_personal_database_connector_agent_personal__agent_id__database_connectors__connector_id__put"
    )
    def update_database_connector(
        self,
        agent_id: str,
        connector_id: str,
        *,
        body: ModelsConnectorsDatabaseConnectorUpdateRequest,
    ) -> dict[str, Any]:
        """Update database connector for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.put(
                f"/agent/personal/{agent_id}/database_connectors/{connector_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_add_kb_connector_agent_personal__agent_id__kb_connectors_post")
    def add_kb_connector(self, agent_id: str, *, body: KBConnectorAddRequest) -> dict[str, Any]:
        """Add knowledge base connector to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agent/personal/{agent_id}/kb_connectors", json_body=body, cast_to=dict
            ),
        )

    @operation("_get_agent_kb_connectors_agent_personal__agent_id__kb_connectors_get")
    def list_kb_connectors(self, agent_id: str) -> dict[str, Any]:
        """List agent's knowledge base connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agent/personal/{agent_id}/kb_connectors", cast_to=dict),
        )

    @operation("_get_user_available_kb_connectors_agents_kb_connectors_get")
    def list_available_kb_connectors(self, *, org_id: str | None = None) -> dict[str, Any]:
        """List available knowledge base connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get("/agents/kb_connectors", params={"org_id": org_id}, cast_to=dict),
        )

    @operation("_get_user_kb_connector_agents_kb_connectors__connector_id__get")
    def retrieve_kb_connector(self, connector_id: str) -> dict[str, Any]:
        """Get knowledge base connector details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/kb_connectors/{connector_id}", cast_to=dict),
        )

    @operation("_delete_kb_connector_agent_personal__agent_id__kb_connectors__connector_id__delete")
    def delete_kb_connector(self, agent_id: str, connector_id: str) -> dict[str, Any]:
        """Remove knowledge base connector from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.delete(
                f"/agent/personal/{agent_id}/kb_connectors/{connector_id}", cast_to=dict
            ),
        )

    @operation(
        "_update_personal_kb_connector_agent_personal__agent_id__kb_connectors__connector_id__put"
    )
    def update_kb_connector(
        self,
        agent_id: str,
        connector_id: str,
        *,
        body: ModelsConnectorsKBConnectorUpdateRequest,
    ) -> dict[str, Any]:
        """Update knowledge base connector for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.put(
                f"/agent/personal/{agent_id}/kb_connectors/{connector_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_agent_permissions_agent__agent_id__permissions_get")
    def get_permissions(self, agent_id: str) -> dict[str, Any]:
        """Get agent permissions."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agent/{agent_id}/permissions", cast_to=dict),
        )

    @operation("_set_agent_permissions_agent__agent_id__permissions_post")
    def set_permissions(self, agent_id: str, *, body: AgentRolePermissionRequest) -> dict[str, Any]:
        """Set agent permissions."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/{agent_id}/permissions", json_body=body, cast_to=dict),
        )

    @operation("_get_pending_agent_invitations_agents_invitations_get")
    def list_invitations(self) -> dict[str, Any]:
        """Get pending agent invitations."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.get("/agents/invitations", cast_to=dict))

    @operation("_accept_agent_invitation_agents__agent_id__approve_get")
    def accept_invitation(self, agent_id: str) -> dict[str, Any]:
        """Accept agent invitation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/{agent_id}/approve", cast_to=dict),
        )

    @operation("_deny_agent_invitation_agents__agent_id__deny_get")
    def deny_invitation(self, agent_id: str) -> dict[str, Any]:
        """Deny agent invitation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/{agent_id}/deny", cast_to=dict),
        )

    @operation("_share_agent_with_user_agent_share__agent_id__user_id__user_id__post")
    def share_with_user(self, agent_id: str, user_id: str) -> dict[str, Any]:
        """Share agent with specific user."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(f"/agent/share/{agent_id}/user_id/{user_id}", cast_to=dict),
        )

    @operation("_create_agent_from_catalog_agents_personal_from_catalog__catalog_id__post")
    def create_from_catalog(
        self, catalog_id: str, *, inputs: str, files: Sequence[bytes] | None = None
    ) -> dict[str, Any]:
        """Create agent from catalog template."""
        upload = [("files", ("upload", f)) for f in files] if files else None
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.post(
                f"/agents/personal/from_catalog/{catalog_id}",
                data={"inputs": inputs},
                files=upload,
                cast_to=dict,
            ),
        )

    @operation("_get_catalog_template_agents_personal_catalog__catalog_id__get")
    def get_catalog_template(self, catalog_id: str) -> dict[str, Any]:
        """Get catalog template details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            self._client.get(f"/agents/personal/catalog/{catalog_id}", cast_to=dict),
        )

    @operation("list_organization_agents_admin_organizations__organization_uuid__agents_get")
    def list_organization_agents(self, organization_uuid: str) -> builtins.list[dict[str, Any]]:
        """List All Agents in an Organization."""
        return cast(
            builtins.list[dict[str, Any]],
            self._client.get(
                f"/admin/organizations/{organization_uuid}/agents",
                envelope=True,
                cast_to=builtins.list[dict[str, Any]],
            ),
        )


class AsyncAgents(AsyncResource):
    """Async counterpart of `Agents`."""

    namespace: ClassVar[str] = "agents"

    @operation("_list_agents_get")
    async def list(self) -> dict[str, Any]:
        """List user agents."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.get("/agents", cast_to=dict))

    @operation("_detail_agent__agent_id__get")
    async def retrieve(self, agent_id: str) -> dict[str, Any]:
        """Get agent details."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.get(f"/agent/{agent_id}", cast_to=dict))

    @operation("_delete_agent_agent__agent_id__delete")
    async def delete(self, agent_id: str) -> dict[str, Any]:
        """Delete agent."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.delete(f"/agent/{agent_id}", cast_to=dict))

    @operation("_set_agent_pin_agent__agent_id__pin_post")
    async def pin(self, agent_id: str, *, body: AgentPinRequest) -> dict[str, Any]:
        """Pin or unpin an agent for the current user."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(f"/agent/{agent_id}/pin", json_body=body, cast_to=dict),
        )

    @operation("_upsert_agent_agent__agent_type__post")
    async def upsert(self, agent_type: str) -> dict[str, Any]:
        """Create or update agent."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.post(f"/agent/{agent_type}", cast_to=dict))

    @operation(
        "_share_agent_with_organization_agent_share__agent_id__organization__organization_id__post"
    )
    async def share_with_organization(self, agent_id: str, organization_id: str) -> dict[str, Any]:
        """Share agent with organization."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/share/{agent_id}/organization/{organization_id}", cast_to=dict
            ),
        )

    @operation("_personal_upload_file_agent_personal__agent_id__files_post")
    async def upload_file(
        self, agent_id: str, file: bytes, *, filename: str | None = None
    ) -> dict[str, Any]:
        """Upload file to personal agent."""
        files = {"file": (filename or "upload", file)}
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(f"/agent/personal/{agent_id}/files", files=files, cast_to=dict),
        )

    @operation("_batch_delete_files_agent_personal__agent_id__files_delete")
    async def batch_delete_files(
        self, agent_id: str, *, body: PersonalAgentAttachmentBatchDeleteRequest
    ) -> dict[str, Any]:
        """Delete multiple personal agent files."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(
                f"/agent/personal/{agent_id}/files", json_body=body, cast_to=dict
            ),
        )

    @operation("_del_file_agent_personal__agent_id__file__file_id__delete")
    async def delete_file(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Delete file from personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(f"/agent/personal/{agent_id}/file/{file_id}", cast_to=dict),
        )

    @operation("_retry_file_agent_personal__agent_id__file__file_id__retry_post")
    async def retry_file(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Retry file ingestion for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/file/{file_id}/retry", cast_to=dict
            ),
        )

    @operation("_personal_add_urls_agent_personal__agent_id__urls_post")
    async def add_urls(self, agent_id: str, *, body: PersonalAgentUrlListRequest) -> dict[str, Any]:
        """Add URLs to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/urls", json_body=body, cast_to=dict
            ),
        )

    @operation("_delete_all_files_agent_personal__agent_id__all_files_delete")
    async def delete_all_files(self, agent_id: str) -> dict[str, Any]:
        """Delete all personal agent files."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(f"/agent/personal/{agent_id}/all_files", cast_to=dict),
        )

    @operation("_get_sitemap_agent_personal_get_sitemap_post")
    async def get_sitemap(self, *, body: SiteampRequest) -> dict[str, Any]:
        """Discover a website's sitemap URLs."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post("/agent/personal/get_sitemap", json_body=body, cast_to=dict),
        )

    @operation("_scrape_website_agent_personal__agent_id__scrape_website_post")
    async def scrape_website(
        self, agent_id: str, *, body: PersonalAgentWebsiteScrapeRequest
    ) -> dict[str, Any]:
        """Scrape website for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/scrape_website", json_body=body, cast_to=dict
            ),
        )

    @operation("_scrape_website_documents_agent_personal__agent_id__scrape_website_documents_post")
    async def scrape_website_documents(
        self, agent_id: str, *, body: PersonalAgentWebsiteDocumentsScrapeRequest
    ) -> dict[str, Any]:
        """Discover website documents for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/scrape_website_documents",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_ingest_website_documents_agent_personal__agent_id__documents_post")
    async def ingest_website_documents(
        self, agent_id: str, *, body: PersonalAgentDocumentUrlListRequest
    ) -> dict[str, Any]:
        """Ingest discovered website documents for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/documents", json_body=body, cast_to=dict
            ),
        )

    @operation("_del_url_agent_personal__agent_id__url__file_id__delete")
    async def delete_url(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Delete URL content from personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(f"/agent/personal/{agent_id}/url/{file_id}", cast_to=dict),
        )

    @operation("_retry_url_agent_personal__agent_id__url__file_id__retry_post")
    async def retry_url(self, agent_id: str, file_id: str) -> dict[str, Any]:
        """Retry URL ingestion for personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/url/{file_id}/retry", cast_to=dict
            ),
        )

    @operation("_add_mcp_server_agent_personal__agent_id__mcp_servers_post")
    async def add_mcp_server(self, agent_id: str, *, body: MCPServerAddRequest) -> dict[str, Any]:
        """Add MCP server to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/mcp_servers", json_body=body, cast_to=dict
            ),
        )

    @operation("_get_user_available_mcp_servers_agents_mcp_servers_get")
    async def list_available_mcp_servers(self, *, org_id: str | None = None) -> dict[str, Any]:
        """List available MCP servers."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get("/agents/mcp_servers", params={"org_id": org_id}, cast_to=dict),
        )

    @operation("_get_user_mcp_server_agents_mcp_servers__server_id__get")
    async def retrieve_mcp_server(self, server_id: str) -> dict[str, Any]:
        """Get MCP server details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/mcp_servers/{server_id}", cast_to=dict),
        )

    @operation("_ingest_mcp_resources_agent_personal__agent_id__mcp_resources_ingest_post")
    async def ingest_mcp_resources(
        self, agent_id: str, *, body: MCPResourcesIngestRequest
    ) -> dict[str, Any]:
        """Ingest MCP direct resources into a conversation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/mcp_resources/ingest",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_mcp_prompt_agent_personal__agent_id__mcp_prompts_post")
    async def get_mcp_prompt(self, agent_id: str, *, body: MCPPromptFetchRequest) -> dict[str, Any]:
        """Fetch an MCP prompt for a conversation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/mcp_prompts", json_body=body, cast_to=dict
            ),
        )

    @operation("_delete_mcp_server_agent_personal__agent_id__mcp_servers__server_id__delete")
    async def delete_mcp_server(self, agent_id: str, server_id: str) -> dict[str, Any]:
        """Remove MCP server from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(
                f"/agent/personal/{agent_id}/mcp_servers/{server_id}", cast_to=dict
            ),
        )

    @operation("_update_personal_mcp_server_agent_personal__agent_id__mcp_servers__server_id__put")
    async def update_mcp_server(
        self, agent_id: str, server_id: str, *, body: MCPServerUpdateRequest
    ) -> dict[str, Any]:
        """Update MCP server for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.put(
                f"/agent/personal/{agent_id}/mcp_servers/{server_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_add_database_connector_agent_personal__agent_id__database_connectors_post")
    async def add_database_connector(
        self, agent_id: str, *, body: DatabaseConnectorAddRequest
    ) -> dict[str, Any]:
        """Add database connector to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/database_connectors",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_agent_database_connectors_agent_personal__agent_id__database_connectors_get")
    async def list_database_connectors(self, agent_id: str) -> dict[str, Any]:
        """List agent's database connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agent/personal/{agent_id}/database_connectors", cast_to=dict),
        )

    @operation("_get_user_available_database_connectors_agents_database_connectors_get")
    async def list_available_database_connectors(
        self, *, org_id: str | None = None
    ) -> dict[str, Any]:
        """List available database connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(
                "/agents/database_connectors", params={"org_id": org_id}, cast_to=dict
            ),
        )

    @operation("_get_user_database_connector_agents_database_connectors__connector_id__get")
    async def retrieve_database_connector(self, connector_id: str) -> dict[str, Any]:
        """Get database connector details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/database_connectors/{connector_id}", cast_to=dict),
        )

    @operation(
        "_delete_database_connector_agent_personal__agent_id__database_connectors__connector_id__delete"
    )
    async def delete_database_connector(self, agent_id: str, connector_id: str) -> dict[str, Any]:
        """Remove database connector from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(
                f"/agent/personal/{agent_id}/database_connectors/{connector_id}", cast_to=dict
            ),
        )

    @operation(
        "_update_personal_database_connector_agent_personal__agent_id__database_connectors__connector_id__put"
    )
    async def update_database_connector(
        self,
        agent_id: str,
        connector_id: str,
        *,
        body: ModelsConnectorsDatabaseConnectorUpdateRequest,
    ) -> dict[str, Any]:
        """Update database connector for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.put(
                f"/agent/personal/{agent_id}/database_connectors/{connector_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_add_kb_connector_agent_personal__agent_id__kb_connectors_post")
    async def add_kb_connector(
        self, agent_id: str, *, body: KBConnectorAddRequest
    ) -> dict[str, Any]:
        """Add knowledge base connector to personal agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agent/personal/{agent_id}/kb_connectors", json_body=body, cast_to=dict
            ),
        )

    @operation("_get_agent_kb_connectors_agent_personal__agent_id__kb_connectors_get")
    async def list_kb_connectors(self, agent_id: str) -> dict[str, Any]:
        """List agent's knowledge base connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agent/personal/{agent_id}/kb_connectors", cast_to=dict),
        )

    @operation("_get_user_available_kb_connectors_agents_kb_connectors_get")
    async def list_available_kb_connectors(self, *, org_id: str | None = None) -> dict[str, Any]:
        """List available knowledge base connectors."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(
                "/agents/kb_connectors", params={"org_id": org_id}, cast_to=dict
            ),
        )

    @operation("_get_user_kb_connector_agents_kb_connectors__connector_id__get")
    async def retrieve_kb_connector(self, connector_id: str) -> dict[str, Any]:
        """Get knowledge base connector details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/kb_connectors/{connector_id}", cast_to=dict),
        )

    @operation("_delete_kb_connector_agent_personal__agent_id__kb_connectors__connector_id__delete")
    async def delete_kb_connector(self, agent_id: str, connector_id: str) -> dict[str, Any]:
        """Remove knowledge base connector from agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.delete(
                f"/agent/personal/{agent_id}/kb_connectors/{connector_id}", cast_to=dict
            ),
        )

    @operation(
        "_update_personal_kb_connector_agent_personal__agent_id__kb_connectors__connector_id__put"
    )
    async def update_kb_connector(
        self,
        agent_id: str,
        connector_id: str,
        *,
        body: ModelsConnectorsKBConnectorUpdateRequest,
    ) -> dict[str, Any]:
        """Update knowledge base connector for agent."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.put(
                f"/agent/personal/{agent_id}/kb_connectors/{connector_id}",
                json_body=body,
                cast_to=dict,
            ),
        )

    @operation("_get_agent_permissions_agent__agent_id__permissions_get")
    async def get_permissions(self, agent_id: str) -> dict[str, Any]:
        """Get agent permissions."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agent/{agent_id}/permissions", cast_to=dict),
        )

    @operation("_set_agent_permissions_agent__agent_id__permissions_post")
    async def set_permissions(
        self, agent_id: str, *, body: AgentRolePermissionRequest
    ) -> dict[str, Any]:
        """Set agent permissions."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(f"/agent/{agent_id}/permissions", json_body=body, cast_to=dict),
        )

    @operation("_get_pending_agent_invitations_agents_invitations_get")
    async def list_invitations(self) -> dict[str, Any]:
        """Get pending agent invitations."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.get("/agents/invitations", cast_to=dict))

    @operation("_accept_agent_invitation_agents__agent_id__approve_get")
    async def accept_invitation(self, agent_id: str) -> dict[str, Any]:
        """Accept agent invitation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/{agent_id}/approve", cast_to=dict),
        )

    @operation("_deny_agent_invitation_agents__agent_id__deny_get")
    async def deny_invitation(self, agent_id: str) -> dict[str, Any]:
        """Deny agent invitation."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/{agent_id}/deny", cast_to=dict),
        )

    @operation("_share_agent_with_user_agent_share__agent_id__user_id__user_id__post")
    async def share_with_user(self, agent_id: str, user_id: str) -> dict[str, Any]:
        """Share agent with specific user."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(f"/agent/share/{agent_id}/user_id/{user_id}", cast_to=dict),
        )

    @operation("_create_agent_from_catalog_agents_personal_from_catalog__catalog_id__post")
    async def create_from_catalog(
        self, catalog_id: str, *, inputs: str, files: Sequence[bytes] | None = None
    ) -> dict[str, Any]:
        """Create agent from catalog template."""
        upload = [("files", ("upload", f)) for f in files] if files else None
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.post(
                f"/agents/personal/from_catalog/{catalog_id}",
                data={"inputs": inputs},
                files=upload,
                cast_to=dict,
            ),
        )

    @operation("_get_catalog_template_agents_personal_catalog__catalog_id__get")
    async def get_catalog_template(self, catalog_id: str) -> dict[str, Any]:
        """Get catalog template details."""
        # spec: untyped response
        return cast(
            dict[str, Any],
            await self._client.get(f"/agents/personal/catalog/{catalog_id}", cast_to=dict),
        )

    @operation("list_organization_agents_admin_organizations__organization_uuid__agents_get")
    async def list_organization_agents(
        self, organization_uuid: str
    ) -> builtins.list[dict[str, Any]]:
        """List All Agents in an Organization."""
        return cast(
            builtins.list[dict[str, Any]],
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/agents",
                envelope=True,
                cast_to=builtins.list[dict[str, Any]],
            ),
        )


Galene._NAMESPACES.append(Agents)
AsyncGalene._NAMESPACES.append(AsyncAgents)
