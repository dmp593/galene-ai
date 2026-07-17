"""`users` resource: user profiles, search, and admin user management."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AdminChangeUserRoleRequest,
    AdminEditUserInfoRequest,
    AdminPasswordSetResponse,
    AdminSetUserActiveStatusRequest,
    AdminSetUserPasswordRequest,
    AdminUserActiveStatusChangedResponse,
    AdminUserAuthStatusResponse,
    AdminUserDeletedResponse,
    AdminUserInfoUpdatedResponse,
    AdminUserRoleChangedResponse,
    EditUserProfileRequest,
    RoleDetailResponse,
    UserDetailResponse,
    UserProfileResponse,
    UserSearchResponse,
)


class Users(SyncResource):
    """User profiles, search, and admin user management."""

    namespace: ClassVar[str] = "users"

    @operation("_user_disable_user__user_id__delete_delete")
    def disable(self, user_id: str) -> bool:
        """Disable User Account."""
        return cast(
            bool,
            self._client.delete(f"/user/{user_id}/delete", cast_to=bool, envelope=True),
        )

    @operation("_get_user_profile_user_profile_get")
    def get_profile(self) -> UserProfileResponse:
        """Get User Profile."""
        return cast(
            UserProfileResponse,
            self._client.get("/user/profile", cast_to=UserProfileResponse, envelope=True),
        )

    @operation("_edit_user_profile_user_profile_post")
    def update_profile(self, body: EditUserProfileRequest) -> dict[str, Any]:
        """Update User Profile."""
        return cast(
            "dict[str, Any]",
            self._client.post(
                "/user/profile", json_body=body, cast_to=dict
            ),  # spec: untyped response
        )

    @operation("_search_user_by_email_user_search_post")
    def search(self) -> list[UserSearchResponse]:
        """Search Users by Email."""
        return cast(
            "list[UserSearchResponse]",
            self._client.post("/user/search", cast_to=list[UserSearchResponse], envelope=True),
        )

    @operation("_get_user_by_uuid_user__user_uuid__get")
    def retrieve(self, user_uuid: str) -> UserDetailResponse:
        """Get User by UUID."""
        return cast(
            UserDetailResponse,
            self._client.get(f"/user/{user_uuid}", cast_to=UserDetailResponse, envelope=True),
        )

    @operation("admin_set_user_password_admin_users__user_uuid__set_password_post")
    def set_password(
        self, user_uuid: str, body: AdminSetUserPasswordRequest
    ) -> AdminPasswordSetResponse:
        """Admin Sets/Resets a User's Password."""
        return cast(
            AdminPasswordSetResponse,
            self._client.post(
                f"/admin/users/{user_uuid}/set-password",
                json_body=body,
                cast_to=AdminPasswordSetResponse,
            ),
        )

    @operation("admin_get_user_auth_status_admin_users__user_uuid__auth_status_get")
    def get_auth_status(self, user_uuid: str) -> AdminUserAuthStatusResponse:
        """Get User Authentication Status."""
        return cast(
            AdminUserAuthStatusResponse,
            self._client.get(
                f"/admin/users/{user_uuid}/auth-status", cast_to=AdminUserAuthStatusResponse
            ),
        )

    @operation("admin_change_user_role_admin_users__user_uuid__role_put")
    def change_role(
        self, user_uuid: str, body: AdminChangeUserRoleRequest
    ) -> AdminUserRoleChangedResponse:
        """Admin Changes a User's Role."""
        return cast(
            AdminUserRoleChangedResponse,
            self._client.put(
                f"/admin/users/{user_uuid}/role",
                json_body=body,
                cast_to=AdminUserRoleChangedResponse,
            ),
        )

    @operation("admin_remove_user_role_admin_users__user_uuid__roles__role_name__delete")
    def remove_role(self, user_uuid: str, role_name: str) -> None:
        """Admin Removes a Role from User."""
        self._client.delete(f"/admin/users/{user_uuid}/roles/{role_name}", cast_to=None)

    @operation("get_user_roles_admin_users__user_uuid__roles_get")
    def list_roles(self, user_uuid: str) -> list[RoleDetailResponse]:
        """Get User Roles."""
        return cast(
            "list[RoleDetailResponse]",
            self._client.get(f"/admin/users/{user_uuid}/roles", cast_to=list[RoleDetailResponse]),
        )

    @operation("admin_edit_user_info_admin_users__user_uuid__info_put")
    def update_info(
        self, user_uuid: str, body: AdminEditUserInfoRequest
    ) -> AdminUserInfoUpdatedResponse:
        """Admin Edits User Information."""
        return cast(
            AdminUserInfoUpdatedResponse,
            self._client.put(
                f"/admin/users/{user_uuid}/info",
                json_body=body,
                cast_to=AdminUserInfoUpdatedResponse,
            ),
        )

    @operation("admin_set_user_active_status_admin_users__user_uuid__status_put")
    def set_active_status(
        self, user_uuid: str, body: AdminSetUserActiveStatusRequest
    ) -> AdminUserActiveStatusChangedResponse:
        """Admin Disables or Enables a User Account."""
        return cast(
            AdminUserActiveStatusChangedResponse,
            self._client.put(
                f"/admin/users/{user_uuid}/status",
                json_body=body,
                cast_to=AdminUserActiveStatusChangedResponse,
            ),
        )

    @operation("admin_delete_user_admin_users__user_uuid__delete")
    def delete(
        self, user_uuid: str, *, reassign_agents_to: str | None = None
    ) -> AdminUserDeletedResponse:
        """Admin Deletes a User Account."""
        return cast(
            AdminUserDeletedResponse,
            self._client.delete(
                f"/admin/users/{user_uuid}",
                params={"reassign_agents_to": reassign_agents_to},
                cast_to=AdminUserDeletedResponse,
            ),
        )


class AsyncUsers(AsyncResource):
    """Async counterpart of `Users`."""

    namespace: ClassVar[str] = "users"

    @operation("_user_disable_user__user_id__delete_delete")
    async def disable(self, user_id: str) -> bool:
        """Disable User Account."""
        return cast(
            bool,
            await self._client.delete(f"/user/{user_id}/delete", cast_to=bool, envelope=True),
        )

    @operation("_get_user_profile_user_profile_get")
    async def get_profile(self) -> UserProfileResponse:
        """Get User Profile."""
        return cast(
            UserProfileResponse,
            await self._client.get("/user/profile", cast_to=UserProfileResponse, envelope=True),
        )

    @operation("_edit_user_profile_user_profile_post")
    async def update_profile(self, body: EditUserProfileRequest) -> dict[str, Any]:
        """Update User Profile."""
        return cast(
            "dict[str, Any]",
            await self._client.post(
                "/user/profile", json_body=body, cast_to=dict
            ),  # spec: untyped response
        )

    @operation("_search_user_by_email_user_search_post")
    async def search(self) -> list[UserSearchResponse]:
        """Search Users by Email."""
        return cast(
            "list[UserSearchResponse]",
            await self._client.post(
                "/user/search", cast_to=list[UserSearchResponse], envelope=True
            ),
        )

    @operation("_get_user_by_uuid_user__user_uuid__get")
    async def retrieve(self, user_uuid: str) -> UserDetailResponse:
        """Get User by UUID."""
        return cast(
            UserDetailResponse,
            await self._client.get(f"/user/{user_uuid}", cast_to=UserDetailResponse, envelope=True),
        )

    @operation("admin_set_user_password_admin_users__user_uuid__set_password_post")
    async def set_password(
        self, user_uuid: str, body: AdminSetUserPasswordRequest
    ) -> AdminPasswordSetResponse:
        """Admin Sets/Resets a User's Password."""
        return cast(
            AdminPasswordSetResponse,
            await self._client.post(
                f"/admin/users/{user_uuid}/set-password",
                json_body=body,
                cast_to=AdminPasswordSetResponse,
            ),
        )

    @operation("admin_get_user_auth_status_admin_users__user_uuid__auth_status_get")
    async def get_auth_status(self, user_uuid: str) -> AdminUserAuthStatusResponse:
        """Get User Authentication Status."""
        return cast(
            AdminUserAuthStatusResponse,
            await self._client.get(
                f"/admin/users/{user_uuid}/auth-status", cast_to=AdminUserAuthStatusResponse
            ),
        )

    @operation("admin_change_user_role_admin_users__user_uuid__role_put")
    async def change_role(
        self, user_uuid: str, body: AdminChangeUserRoleRequest
    ) -> AdminUserRoleChangedResponse:
        """Admin Changes a User's Role."""
        return cast(
            AdminUserRoleChangedResponse,
            await self._client.put(
                f"/admin/users/{user_uuid}/role",
                json_body=body,
                cast_to=AdminUserRoleChangedResponse,
            ),
        )

    @operation("admin_remove_user_role_admin_users__user_uuid__roles__role_name__delete")
    async def remove_role(self, user_uuid: str, role_name: str) -> None:
        """Admin Removes a Role from User."""
        await self._client.delete(f"/admin/users/{user_uuid}/roles/{role_name}", cast_to=None)

    @operation("get_user_roles_admin_users__user_uuid__roles_get")
    async def list_roles(self, user_uuid: str) -> list[RoleDetailResponse]:
        """Get User Roles."""
        return cast(
            "list[RoleDetailResponse]",
            await self._client.get(
                f"/admin/users/{user_uuid}/roles", cast_to=list[RoleDetailResponse]
            ),
        )

    @operation("admin_edit_user_info_admin_users__user_uuid__info_put")
    async def update_info(
        self, user_uuid: str, body: AdminEditUserInfoRequest
    ) -> AdminUserInfoUpdatedResponse:
        """Admin Edits User Information."""
        return cast(
            AdminUserInfoUpdatedResponse,
            await self._client.put(
                f"/admin/users/{user_uuid}/info",
                json_body=body,
                cast_to=AdminUserInfoUpdatedResponse,
            ),
        )

    @operation("admin_set_user_active_status_admin_users__user_uuid__status_put")
    async def set_active_status(
        self, user_uuid: str, body: AdminSetUserActiveStatusRequest
    ) -> AdminUserActiveStatusChangedResponse:
        """Admin Disables or Enables a User Account."""
        return cast(
            AdminUserActiveStatusChangedResponse,
            await self._client.put(
                f"/admin/users/{user_uuid}/status",
                json_body=body,
                cast_to=AdminUserActiveStatusChangedResponse,
            ),
        )

    @operation("admin_delete_user_admin_users__user_uuid__delete")
    async def delete(
        self, user_uuid: str, *, reassign_agents_to: str | None = None
    ) -> AdminUserDeletedResponse:
        """Admin Deletes a User Account."""
        return cast(
            AdminUserDeletedResponse,
            await self._client.delete(
                f"/admin/users/{user_uuid}",
                params={"reassign_agents_to": reassign_agents_to},
                cast_to=AdminUserDeletedResponse,
            ),
        )


Galene._NAMESPACES.append(Users)
AsyncGalene._NAMESPACES.append(AsyncUsers)
