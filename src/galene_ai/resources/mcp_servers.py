"""`mcp_servers` resource: admin management of an organization's MCP servers."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    MCPServerActiveItemsUpdateRequest,
    MCPServerDetailResponse,
    MCPServerListResponse,
    MCPServersResponse,
    MCPServerTestRequest,
    MCPServerTestResponse,
    ModelsAdminModelsMcpMCPServerResponse,
)


def _mcp_form(fields: dict[str, Any]) -> dict[str, Any]:
    """Drop `None` form values so only supplied fields are sent."""
    return {k: v for k, v in fields.items() if v is not None}


class McpServers(SyncResource):
    """Create, list, retrieve, update, delete, and test an organization's MCP servers (admin)."""

    namespace: ClassVar[str] = "mcp_servers"

    @operation("create_mcp_server_admin_organizations__organization_uuid__mcp_servers_post")
    def create(
        self,
        organization_uuid: str,
        *,
        name: str,
        server_type: str,
        permission_type: str,
        description: str | None = None,
        allowed_role_ids: list[str] | None = None,
        endpoint_url: str | None = None,
        headers: str | None = None,
        context_headers: str | None = None,
        runtime_language: str | None = None,
        runtime_version: str | None = None,
        memory_mb: int | None = None,
        timeout_seconds: int | None = None,
        environment_variables: str | None = None,
        zip_file: bytes | None = None,
        zip_filename: str | None = None,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Create an MCP Server for an Organization."""
        data = _mcp_form(
            {
                "name": name,
                "server_type": server_type,
                "permission_type": permission_type,
                "description": description,
                "allowed_role_ids": allowed_role_ids,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "context_headers": context_headers,
                "runtime_language": runtime_language,
                "runtime_version": runtime_version,
                "memory_mb": memory_mb,
                "timeout_seconds": timeout_seconds,
                "environment_variables": environment_variables,
            }
        )
        files = {"zip_file": (zip_filename or "server.zip", zip_file)} if zip_file else {}
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/mcp-servers",
                data=data,
                files=files,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation(
        "get_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__get"
    )
    def retrieve(
        self, organization_uuid: str, server_uuid: str, *, include_tools: bool | None = None
    ) -> MCPServerDetailResponse:
        """Get a Specific MCP Server for an Organization."""
        return cast(
            MCPServerDetailResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
                params={"include_tools": include_tools},
                cast_to=MCPServerDetailResponse,
            ),
        )

    @operation(
        "update_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__put"
    )
    def update(
        self,
        organization_uuid: str,
        server_uuid: str,
        *,
        name: str | None = None,
        description: str | None = None,
        permission_type: str | None = None,
        allowed_role_ids: list[str] | None = None,
        endpoint_url: str | None = None,
        headers: str | None = None,
        context_headers: str | None = None,
        runtime_language: str | None = None,
        runtime_version: str | None = None,
        memory_mb: int | None = None,
        timeout_seconds: int | None = None,
        environment_variables: str | None = None,
        zip_file: bytes | None = None,
        zip_filename: str | None = None,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Update an MCP Server for an Organization."""
        data = _mcp_form(
            {
                "name": name,
                "description": description,
                "permission_type": permission_type,
                "allowed_role_ids": allowed_role_ids,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "context_headers": context_headers,
                "runtime_language": runtime_language,
                "runtime_version": runtime_version,
                "memory_mb": memory_mb,
                "timeout_seconds": timeout_seconds,
                "environment_variables": environment_variables,
            }
        )
        files = {"zip_file": (zip_filename or "server.zip", zip_file)} if zip_file else {}
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
                data=data,
                files=files,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation(
        "delete_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__delete"
    )
    def delete(self, organization_uuid: str, server_uuid: str) -> None:
        """Delete an MCP Server for an Organization."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
            cast_to=None,
        )

    @operation(
        "test_mcp_server_connection_admin_organizations__organization_uuid__mcp_servers__server_uuid__test_connection_post"
    )
    def test_connection(
        self, organization_uuid: str, server_uuid: str, *, body: MCPServerTestRequest
    ) -> MCPServerTestResponse:
        """Test MCP Server Connection."""
        return cast(
            MCPServerTestResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}/test-connection",
                json_body=body,
                cast_to=MCPServerTestResponse,
            ),
        )

    @operation(
        "update_mcp_server_active_items_admin_organizations__organization_uuid__mcp_servers__server_uuid__active_items_put"
    )
    def update_active_items(
        self,
        organization_uuid: str,
        server_uuid: str,
        *,
        body: MCPServerActiveItemsUpdateRequest,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Update Active MCP Tools and Resources."""
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}/active-items",
                json_body=body,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation("list_mcp_servers_admin_organizations__organization_uuid__mcp_servers_get")
    def list(
        self, organization_uuid: str, *, include_tools: bool | None = None
    ) -> MCPServerListResponse:
        """List MCP Servers for an Organization."""
        return cast(
            MCPServerListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp-servers",
                params={"include_tools": include_tools},
                cast_to=MCPServerListResponse,
            ),
        )

    @operation(
        "_get_organization_mcp_servers_admin_organizations__organization_uuid__mcp_servers_get"
    )
    def list_organization_servers(self, organization_uuid: str) -> MCPServersResponse:
        """List MCP Servers for Organization (Admin)."""
        return cast(
            MCPServersResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp_servers",
                cast_to=MCPServersResponse,
                envelope=True,
            ),
        )


class AsyncMcpServers(AsyncResource):
    """Async counterpart of `McpServers`."""

    namespace: ClassVar[str] = "mcp_servers"

    @operation("create_mcp_server_admin_organizations__organization_uuid__mcp_servers_post")
    async def create(
        self,
        organization_uuid: str,
        *,
        name: str,
        server_type: str,
        permission_type: str,
        description: str | None = None,
        allowed_role_ids: list[str] | None = None,
        endpoint_url: str | None = None,
        headers: str | None = None,
        context_headers: str | None = None,
        runtime_language: str | None = None,
        runtime_version: str | None = None,
        memory_mb: int | None = None,
        timeout_seconds: int | None = None,
        environment_variables: str | None = None,
        zip_file: bytes | None = None,
        zip_filename: str | None = None,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Create an MCP Server for an Organization."""
        data = _mcp_form(
            {
                "name": name,
                "server_type": server_type,
                "permission_type": permission_type,
                "description": description,
                "allowed_role_ids": allowed_role_ids,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "context_headers": context_headers,
                "runtime_language": runtime_language,
                "runtime_version": runtime_version,
                "memory_mb": memory_mb,
                "timeout_seconds": timeout_seconds,
                "environment_variables": environment_variables,
            }
        )
        files = {"zip_file": (zip_filename or "server.zip", zip_file)} if zip_file else {}
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/mcp-servers",
                data=data,
                files=files,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation(
        "get_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__get"
    )
    async def retrieve(
        self, organization_uuid: str, server_uuid: str, *, include_tools: bool | None = None
    ) -> MCPServerDetailResponse:
        """Get a Specific MCP Server for an Organization."""
        return cast(
            MCPServerDetailResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
                params={"include_tools": include_tools},
                cast_to=MCPServerDetailResponse,
            ),
        )

    @operation(
        "update_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__put"
    )
    async def update(
        self,
        organization_uuid: str,
        server_uuid: str,
        *,
        name: str | None = None,
        description: str | None = None,
        permission_type: str | None = None,
        allowed_role_ids: list[str] | None = None,
        endpoint_url: str | None = None,
        headers: str | None = None,
        context_headers: str | None = None,
        runtime_language: str | None = None,
        runtime_version: str | None = None,
        memory_mb: int | None = None,
        timeout_seconds: int | None = None,
        environment_variables: str | None = None,
        zip_file: bytes | None = None,
        zip_filename: str | None = None,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Update an MCP Server for an Organization."""
        data = _mcp_form(
            {
                "name": name,
                "description": description,
                "permission_type": permission_type,
                "allowed_role_ids": allowed_role_ids,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "context_headers": context_headers,
                "runtime_language": runtime_language,
                "runtime_version": runtime_version,
                "memory_mb": memory_mb,
                "timeout_seconds": timeout_seconds,
                "environment_variables": environment_variables,
            }
        )
        files = {"zip_file": (zip_filename or "server.zip", zip_file)} if zip_file else {}
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
                data=data,
                files=files,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation(
        "delete_mcp_server_admin_organizations__organization_uuid__mcp_servers__server_uuid__delete"
    )
    async def delete(self, organization_uuid: str, server_uuid: str) -> None:
        """Delete an MCP Server for an Organization."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}",
            cast_to=None,
        )

    @operation(
        "test_mcp_server_connection_admin_organizations__organization_uuid__mcp_servers__server_uuid__test_connection_post"
    )
    async def test_connection(
        self, organization_uuid: str, server_uuid: str, *, body: MCPServerTestRequest
    ) -> MCPServerTestResponse:
        """Test MCP Server Connection."""
        return cast(
            MCPServerTestResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}/test-connection",
                json_body=body,
                cast_to=MCPServerTestResponse,
            ),
        )

    @operation(
        "update_mcp_server_active_items_admin_organizations__organization_uuid__mcp_servers__server_uuid__active_items_put"
    )
    async def update_active_items(
        self,
        organization_uuid: str,
        server_uuid: str,
        *,
        body: MCPServerActiveItemsUpdateRequest,
    ) -> ModelsAdminModelsMcpMCPServerResponse:
        """Update Active MCP Tools and Resources."""
        return cast(
            ModelsAdminModelsMcpMCPServerResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/mcp-servers/{server_uuid}/active-items",
                json_body=body,
                cast_to=ModelsAdminModelsMcpMCPServerResponse,
            ),
        )

    @operation("list_mcp_servers_admin_organizations__organization_uuid__mcp_servers_get")
    async def list(
        self, organization_uuid: str, *, include_tools: bool | None = None
    ) -> MCPServerListResponse:
        """List MCP Servers for an Organization."""
        return cast(
            MCPServerListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp-servers",
                params={"include_tools": include_tools},
                cast_to=MCPServerListResponse,
            ),
        )

    @operation(
        "_get_organization_mcp_servers_admin_organizations__organization_uuid__mcp_servers_get"
    )
    async def list_organization_servers(self, organization_uuid: str) -> MCPServersResponse:
        """List MCP Servers for Organization (Admin)."""
        return cast(
            MCPServersResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/mcp_servers",
                cast_to=MCPServersResponse,
                envelope=True,
            ),
        )


Galene._NAMESPACES.append(McpServers)
AsyncGalene._NAMESPACES.append(AsyncMcpServers)
