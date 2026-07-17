"""`api_keys` resource: user-facing API key management plus admin key operations.

The user endpoints under `/auth/config/api-key` return the backend's `WSResponse_*`
envelope (`{success, message, result}`), so they are decoded with `envelope=True` — the
`result` payload is returned on success and `GaleneError` is raised on `success:false`.
The admin endpoints under `/admin/...` return their models un-enveloped.
"""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AdminDeleteApiKeyResponse,
    AdminToggleApiKeyRequest,
    AdminToggleApiKeyResponse,
    AdminUserApiKeysResponse,
    CreateApiKeyResponse,
    DeleteApiKeyRequest,
    GetApiKeysResponse,
)


class ApiKeys(SyncResource):
    """User API key management and admin key operations."""

    namespace: ClassVar[str] = "api_keys"

    @operation("_get_api_keys_auth_config_api_key_get")
    def list(self) -> GetApiKeysResponse:
        """List User API Keys."""
        return cast(
            GetApiKeysResponse,
            self._client.get("/auth/config/api-key", cast_to=GetApiKeysResponse, envelope=True),
        )

    @operation("_create_api_key_auth_config_api_key_post")
    def create(self) -> CreateApiKeyResponse:
        """Create New API Key."""
        return cast(
            CreateApiKeyResponse,
            self._client.post("/auth/config/api-key", cast_to=CreateApiKeyResponse, envelope=True),
        )

    @operation("_delete_api_key_auth_config_api_key_delete")
    def delete(self, body: DeleteApiKeyRequest) -> bool:
        """Delete API Key."""
        return cast(
            bool,
            self._client.delete(
                "/auth/config/api-key", json_body=body, cast_to=bool, envelope=True
            ),
        )

    @operation("get_user_api_keys_admin_users__user_uuid__api_keys_get")
    def get_user_keys(self, user_uuid: str) -> AdminUserApiKeysResponse:
        """Get user's API keys (Admin)."""
        return cast(
            AdminUserApiKeysResponse,
            self._client.get(
                f"/admin/users/{user_uuid}/api-keys", cast_to=AdminUserApiKeysResponse
            ),
        )

    @operation("toggle_api_key_status_admin_api_keys__api_key_id__status_patch")
    def toggle_status(
        self, api_key_id: str, body: AdminToggleApiKeyRequest
    ) -> AdminToggleApiKeyResponse:
        """Enable or disable an API key (Admin)."""
        return cast(
            AdminToggleApiKeyResponse,
            self._client.patch(
                f"/admin/api-keys/{api_key_id}/status",
                json_body=body,
                cast_to=AdminToggleApiKeyResponse,
            ),
        )

    @operation("delete_user_api_key_admin_api_keys__api_key_id__delete")
    def delete_admin(self, api_key_id: str) -> AdminDeleteApiKeyResponse:
        """Delete an API key (Admin)."""
        return cast(
            AdminDeleteApiKeyResponse,
            self._client.delete(f"/admin/api-keys/{api_key_id}", cast_to=AdminDeleteApiKeyResponse),
        )


class AsyncApiKeys(AsyncResource):
    """Async counterpart of `ApiKeys`."""

    namespace: ClassVar[str] = "api_keys"

    @operation("_get_api_keys_auth_config_api_key_get")
    async def list(self) -> GetApiKeysResponse:
        """List User API Keys."""
        return cast(
            GetApiKeysResponse,
            await self._client.get(
                "/auth/config/api-key", cast_to=GetApiKeysResponse, envelope=True
            ),
        )

    @operation("_create_api_key_auth_config_api_key_post")
    async def create(self) -> CreateApiKeyResponse:
        """Create New API Key."""
        return cast(
            CreateApiKeyResponse,
            await self._client.post(
                "/auth/config/api-key", cast_to=CreateApiKeyResponse, envelope=True
            ),
        )

    @operation("_delete_api_key_auth_config_api_key_delete")
    async def delete(self, body: DeleteApiKeyRequest) -> bool:
        """Delete API Key."""
        return cast(
            bool,
            await self._client.delete(
                "/auth/config/api-key", json_body=body, cast_to=bool, envelope=True
            ),
        )

    @operation("get_user_api_keys_admin_users__user_uuid__api_keys_get")
    async def get_user_keys(self, user_uuid: str) -> AdminUserApiKeysResponse:
        """Get user's API keys (Admin)."""
        return cast(
            AdminUserApiKeysResponse,
            await self._client.get(
                f"/admin/users/{user_uuid}/api-keys", cast_to=AdminUserApiKeysResponse
            ),
        )

    @operation("toggle_api_key_status_admin_api_keys__api_key_id__status_patch")
    async def toggle_status(
        self, api_key_id: str, body: AdminToggleApiKeyRequest
    ) -> AdminToggleApiKeyResponse:
        """Enable or disable an API key (Admin)."""
        return cast(
            AdminToggleApiKeyResponse,
            await self._client.patch(
                f"/admin/api-keys/{api_key_id}/status",
                json_body=body,
                cast_to=AdminToggleApiKeyResponse,
            ),
        )

    @operation("delete_user_api_key_admin_api_keys__api_key_id__delete")
    async def delete_admin(self, api_key_id: str) -> AdminDeleteApiKeyResponse:
        """Delete an API key (Admin)."""
        return cast(
            AdminDeleteApiKeyResponse,
            await self._client.delete(
                f"/admin/api-keys/{api_key_id}", cast_to=AdminDeleteApiKeyResponse
            ),
        )


Galene._NAMESPACES.append(ApiKeys)
AsyncGalene._NAMESPACES.append(AsyncApiKeys)
