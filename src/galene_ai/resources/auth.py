"""`auth` resource: signup, login/logout, token refresh, password reset, and SSO.

Covers the account-authentication endpoints (`/signup`, `/login`, `/logout`,
`/refresh-token`, `/reset-password`), the tenant SSO login/config endpoints
(`/auth/sso/{org_uuid}` and its `/config`), and the admin SSO-connector CRUD under
`/admin/organizations/{organization_uuid}/sso-connectors`.

The account and SSO-login operations return the backend's `WSResponse_*` envelope
(`{success, message, result}`), so they are decoded with `envelope=True` — the
`result` payload is returned on success and `GaleneError` is raised on `success:false`.
The admin SSO-connector operations return their models un-enveloped.
"""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    KeycloakSSORequest,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ResetPasswordResponse,
    SignupRequest,
    SignupResponse,
    SSOConfigResponse,
    SSOConnectorCreateRequest,
    SSOConnectorDetailResponse,
    SSOConnectorListResponse,
    SSOConnectorResponse,
    SSOConnectorUpdateRequest,
)


class Auth(SyncResource):
    """Signup, login/logout, token refresh, password reset, and SSO management."""

    namespace: ClassVar[str] = "auth"

    @operation("_signup_signup_post")
    def signup(self, body: SignupRequest) -> SignupResponse:
        """Create New User Account."""
        return cast(
            SignupResponse,
            self._client.post("/signup", json_body=body, cast_to=SignupResponse, envelope=True),
        )

    @operation("_login_login_post")
    def login(self, body: LoginRequest) -> LoginResponse:
        """User Authentication."""
        return cast(
            LoginResponse,
            self._client.post("/login", json_body=body, cast_to=LoginResponse, envelope=True),
        )

    @operation("_logout_logout_post")
    def logout(self, body: LogoutRequest) -> bool:
        """User Logout."""
        return cast(
            bool,
            self._client.post("/logout", json_body=body, cast_to=bool, envelope=True),
        )

    @operation("_refresh_token_refresh_token_post")
    def refresh_token(self, body: RefreshTokenRequest) -> LoginResponse:
        """Refresh Authentication Token."""
        return cast(
            LoginResponse,
            self._client.post(
                "/refresh-token", json_body=body, cast_to=LoginResponse, envelope=True
            ),
        )

    @operation("_reset_password_reset_password_post")
    def reset_password(self, body: ResetPasswordRequest) -> ResetPasswordResponse:
        """Reset User Password."""
        return cast(
            ResetPasswordResponse,
            self._client.post(
                "/reset-password",
                json_body=body,
                cast_to=ResetPasswordResponse,
                envelope=True,
            ),
        )

    @operation("_sso_auth_sso__org_uuid__post")
    def sso(
        self, org_uuid: str, body: KeycloakSSORequest, *, frontend_url: str | None = None
    ) -> LoginResponse:
        """Single Sign-On Authentication."""
        return cast(
            LoginResponse,
            self._client.post(
                f"/auth/sso/{org_uuid}",
                params={"frontend_url": frontend_url},
                json_body=body,
                cast_to=LoginResponse,
                envelope=True,
            ),
        )

    @operation("_get_sso_config_auth_sso__org_uuid__config_get")
    def get_sso_config(self, org_uuid: str) -> list[SSOConfigResponse]:
        """Get SSO configuration for organization."""
        return cast(
            list[SSOConfigResponse],
            self._client.get(f"/auth/sso/{org_uuid}/config", cast_to=list[SSOConfigResponse]),
        )

    @operation("create_sso_connector_admin_organizations__organization_uuid__sso_connectors_post")
    def create_sso_connector(
        self, organization_uuid: str, body: SSOConnectorCreateRequest
    ) -> SSOConnectorResponse:
        """Create an SSO Connector for an Organization."""
        return cast(
            SSOConnectorResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/sso-connectors",
                json_body=body,
                cast_to=SSOConnectorResponse,
            ),
        )

    @operation("list_sso_connectors_admin_organizations__organization_uuid__sso_connectors_get")
    def list_sso_connectors(self, organization_uuid: str) -> SSOConnectorListResponse:
        """List SSO Connectors for an Organization."""
        return cast(
            SSOConnectorListResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors",
                cast_to=SSOConnectorListResponse,
            ),
        )

    @operation(
        "get_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__get"
    )
    def get_sso_connector(
        self, organization_uuid: str, connector_uuid: str
    ) -> SSOConnectorDetailResponse:
        """Get a Specific SSO Connector for an Organization."""
        return cast(
            SSOConnectorDetailResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
                cast_to=SSOConnectorDetailResponse,
            ),
        )

    @operation(
        "update_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__put"
    )
    def update_sso_connector(
        self, organization_uuid: str, connector_uuid: str, body: SSOConnectorUpdateRequest
    ) -> SSOConnectorResponse:
        """Update an SSO Connector for an Organization."""
        return cast(
            SSOConnectorResponse,
            self._client.put(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
                json_body=body,
                cast_to=SSOConnectorResponse,
            ),
        )

    @operation(
        "delete_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__delete"
    )
    def delete_sso_connector(self, organization_uuid: str, connector_uuid: str) -> None:
        """Delete an SSO Connector for an Organization."""
        self._client.delete(
            f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
            cast_to=None,
        )


class AsyncAuth(AsyncResource):
    """Async counterpart of `Auth`."""

    namespace: ClassVar[str] = "auth"

    @operation("_signup_signup_post")
    async def signup(self, body: SignupRequest) -> SignupResponse:
        """Create New User Account."""
        return cast(
            SignupResponse,
            await self._client.post(
                "/signup", json_body=body, cast_to=SignupResponse, envelope=True
            ),
        )

    @operation("_login_login_post")
    async def login(self, body: LoginRequest) -> LoginResponse:
        """User Authentication."""
        return cast(
            LoginResponse,
            await self._client.post("/login", json_body=body, cast_to=LoginResponse, envelope=True),
        )

    @operation("_logout_logout_post")
    async def logout(self, body: LogoutRequest) -> bool:
        """User Logout."""
        return cast(
            bool,
            await self._client.post("/logout", json_body=body, cast_to=bool, envelope=True),
        )

    @operation("_refresh_token_refresh_token_post")
    async def refresh_token(self, body: RefreshTokenRequest) -> LoginResponse:
        """Refresh Authentication Token."""
        return cast(
            LoginResponse,
            await self._client.post(
                "/refresh-token", json_body=body, cast_to=LoginResponse, envelope=True
            ),
        )

    @operation("_reset_password_reset_password_post")
    async def reset_password(self, body: ResetPasswordRequest) -> ResetPasswordResponse:
        """Reset User Password."""
        return cast(
            ResetPasswordResponse,
            await self._client.post(
                "/reset-password",
                json_body=body,
                cast_to=ResetPasswordResponse,
                envelope=True,
            ),
        )

    @operation("_sso_auth_sso__org_uuid__post")
    async def sso(
        self, org_uuid: str, body: KeycloakSSORequest, *, frontend_url: str | None = None
    ) -> LoginResponse:
        """Single Sign-On Authentication."""
        return cast(
            LoginResponse,
            await self._client.post(
                f"/auth/sso/{org_uuid}",
                params={"frontend_url": frontend_url},
                json_body=body,
                cast_to=LoginResponse,
                envelope=True,
            ),
        )

    @operation("_get_sso_config_auth_sso__org_uuid__config_get")
    async def get_sso_config(self, org_uuid: str) -> list[SSOConfigResponse]:
        """Get SSO configuration for organization."""
        return cast(
            list[SSOConfigResponse],
            await self._client.get(f"/auth/sso/{org_uuid}/config", cast_to=list[SSOConfigResponse]),
        )

    @operation("create_sso_connector_admin_organizations__organization_uuid__sso_connectors_post")
    async def create_sso_connector(
        self, organization_uuid: str, body: SSOConnectorCreateRequest
    ) -> SSOConnectorResponse:
        """Create an SSO Connector for an Organization."""
        return cast(
            SSOConnectorResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/sso-connectors",
                json_body=body,
                cast_to=SSOConnectorResponse,
            ),
        )

    @operation("list_sso_connectors_admin_organizations__organization_uuid__sso_connectors_get")
    async def list_sso_connectors(self, organization_uuid: str) -> SSOConnectorListResponse:
        """List SSO Connectors for an Organization."""
        return cast(
            SSOConnectorListResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors",
                cast_to=SSOConnectorListResponse,
            ),
        )

    @operation(
        "get_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__get"
    )
    async def get_sso_connector(
        self, organization_uuid: str, connector_uuid: str
    ) -> SSOConnectorDetailResponse:
        """Get a Specific SSO Connector for an Organization."""
        return cast(
            SSOConnectorDetailResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
                cast_to=SSOConnectorDetailResponse,
            ),
        )

    @operation(
        "update_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__put"
    )
    async def update_sso_connector(
        self, organization_uuid: str, connector_uuid: str, body: SSOConnectorUpdateRequest
    ) -> SSOConnectorResponse:
        """Update an SSO Connector for an Organization."""
        return cast(
            SSOConnectorResponse,
            await self._client.put(
                f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
                json_body=body,
                cast_to=SSOConnectorResponse,
            ),
        )

    @operation(
        "delete_sso_connector_admin_organizations__organization_uuid__sso_connectors__connector_uuid__delete"
    )
    async def delete_sso_connector(self, organization_uuid: str, connector_uuid: str) -> None:
        """Delete an SSO Connector for an Organization."""
        await self._client.delete(
            f"/admin/organizations/{organization_uuid}/sso-connectors/{connector_uuid}",
            cast_to=None,
        )


Galene._NAMESPACES.append(Auth)
AsyncGalene._NAMESPACES.append(AsyncAuth)
