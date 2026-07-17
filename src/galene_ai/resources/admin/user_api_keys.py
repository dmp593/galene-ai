"""`admin.user_api_keys` resource: administer per-user API keys."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import AdminCreateApiKeyResponse


class UserApiKeys(SyncResource):
    """Administer per-user API keys."""

    namespace: ClassVar[str] = "user_api_keys"

    @operation("create_user_api_key_admin_users__user_uuid__api_keys_post")
    def create(self, user_uuid: str) -> AdminCreateApiKeyResponse:
        """Create API Key for User."""
        return cast(
            AdminCreateApiKeyResponse,
            self._client.post(
                f"/admin/users/{user_uuid}/api-keys",
                cast_to=AdminCreateApiKeyResponse,
            ),
        )


class AsyncUserApiKeys(AsyncResource):
    """Async counterpart of `UserApiKeys`."""

    namespace: ClassVar[str] = "user_api_keys"

    @operation("create_user_api_key_admin_users__user_uuid__api_keys_post")
    async def create(self, user_uuid: str) -> AdminCreateApiKeyResponse:
        """Create API Key for User."""
        return cast(
            AdminCreateApiKeyResponse,
            await self._client.post(
                f"/admin/users/{user_uuid}/api-keys",
                cast_to=AdminCreateApiKeyResponse,
            ),
        )


Galene._ADMIN_NAMESPACES.append(UserApiKeys)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncUserApiKeys)
