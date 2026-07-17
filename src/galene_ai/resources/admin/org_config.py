"""Admin ``org_config`` resource namespace."""

from __future__ import annotations

from typing import ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    BrandAssetsValue,
    BrandGeneralCreateRequest,
    BrandGeneralValue,
    BrandPaletteCreateRequest,
    BrandPaletteValue,
    DomainSettingsResponse,
    DomainSettingsUpdateRequest,
    OrganizationGeneralCreateRequest,
    OrganizationGeneralValue,
    OrgBrandAssetsConfigResponse,
    OrgBrandGeneralConfigResponse,
    OrgBrandPaletteConfigResponse,
    OrgGeneralConfigResponse,
    OrgPlatformCapabilitiesConfigResponse,
    PlatformCapabilitiesCreateRequest,
    PlatformCapabilitiesValue,
)


class OrgConfig(SyncResource):
    """Organization-level configuration (general, domain, brand, capabilities)."""

    namespace: ClassVar[str] = "org_config"

    @operation(
        "set_organization_general_settings_admin_organizations__org_uuid__settings_organization_general_post"
    )
    def set_general(
        self, org_uuid: str, *, body: OrganizationGeneralCreateRequest
    ) -> OrgGeneralConfigResponse:
        """Set Organization General Settings (Superadmin)."""
        return cast(
            OrgGeneralConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/organization_general",
                json_body=body,
                cast_to=OrgGeneralConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_general_settings_admin_organizations__org_uuid__settings_organization_general_get"
    )
    def retrieve_general(self, org_uuid: str) -> OrganizationGeneralValue:
        """Get Organization General Settings."""
        return cast(
            OrganizationGeneralValue,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/organization_general",
                cast_to=OrganizationGeneralValue,
            ),
        )

    @operation(
        "update_organization_domain_settings_admin_organizations__org_uuid__settings_domain_settings_put"
    )
    def update_domain_settings(
        self, org_uuid: str, *, body: DomainSettingsUpdateRequest
    ) -> DomainSettingsResponse:
        """Update Organization Domain Settings."""
        return cast(
            DomainSettingsResponse,
            self._client.put(
                f"/admin/organizations/{org_uuid}/settings/domain_settings",
                json_body=body,
                cast_to=DomainSettingsResponse,
            ),
        )

    @operation(
        "retrieve_organization_domain_settings_admin_organizations__org_uuid__settings_domain_settings_get"
    )
    def retrieve_domain_settings(self, org_uuid: str) -> DomainSettingsResponse:
        """Get Organization Domain Settings."""
        return cast(
            DomainSettingsResponse,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/domain_settings",
                cast_to=DomainSettingsResponse,
            ),
        )

    @operation(
        "set_organization_brand_palette_admin_organizations__org_uuid__settings_brand_palette_post"
    )
    def set_brand_palette(
        self, org_uuid: str, *, body: BrandPaletteCreateRequest
    ) -> OrgBrandPaletteConfigResponse:
        """Set Organization Brand Palette."""
        return cast(
            OrgBrandPaletteConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_palette",
                json_body=body,
                cast_to=OrgBrandPaletteConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_brand_palette_admin_organizations__org_uuid__settings_brand_palette_get"
    )
    def retrieve_brand_palette(self, org_uuid: str) -> BrandPaletteValue:
        """Get Organization Brand Palette."""
        return cast(
            BrandPaletteValue,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_palette", cast_to=BrandPaletteValue
            ),
        )

    @operation(
        "retrieve_organization_brand_assets_admin_organizations__org_uuid__settings_brand_assets_get"
    )
    def retrieve_brand_assets(self, org_uuid: str) -> BrandAssetsValue:
        """Get Organization Brand Assets."""
        return cast(
            BrandAssetsValue,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_assets", cast_to=BrandAssetsValue
            ),
        )

    @operation(
        "set_org_square_logo_admin_organizations__org_uuid__settings_brand_assets_square_logo_post"
    )
    def set_square_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Square Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/square_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_square_logo_admin_organizations__org_uuid__settings_brand_assets_square_logo_delete"
    )
    def delete_square_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Square Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/square_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_square_logo_admin_organizations__org_uuid__settings_brand_assets_white_square_logo_post"
    )
    def set_white_square_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Square Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_square_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_square_logo_admin_organizations__org_uuid__settings_brand_assets_white_square_logo_delete"
    )
    def delete_white_square_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Square Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_square_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_extended_logo_admin_organizations__org_uuid__settings_brand_assets_extended_logo_post"
    )
    def set_extended_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Extended Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/extended_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_extended_logo_admin_organizations__org_uuid__settings_brand_assets_extended_logo_delete"
    )
    def delete_extended_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Extended Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/extended_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_extended_logo_admin_organizations__org_uuid__settings_brand_assets_white_extended_logo_post"
    )
    def set_white_extended_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Extended Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_extended_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_extended_logo_admin_organizations__org_uuid__settings_brand_assets_white_extended_logo_delete"
    )
    def delete_white_extended_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Extended Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_extended_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_login_page_logo_post"
    )
    def set_login_page_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Login Page Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_page_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_login_page_logo_delete"
    )
    def delete_login_page_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Login Page Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_page_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_white_login_page_logo_post"
    )
    def set_white_login_page_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Login Page Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_login_page_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_white_login_page_logo_delete"
    )
    def delete_white_login_page_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Login Page Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_login_page_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_login_background_image_admin_organizations__org_uuid__settings_brand_assets_login_background_image_post"
    )
    def set_login_background_image(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Login Background Image."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_background_image",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_login_background_image_admin_organizations__org_uuid__settings_brand_assets_login_background_image_delete"
    )
    def delete_login_background_image(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Login Background Image."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_background_image",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation("set_org_favicon_admin_organizations__org_uuid__settings_brand_assets_favicon_post")
    def set_favicon(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_admin_organizations__org_uuid__settings_brand_assets_favicon_delete"
    )
    def delete_favicon(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_favicon_16_admin_organizations__org_uuid__settings_brand_assets_favicon_16_post"
    )
    def set_favicon_16(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon 16x16."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_16",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_16_admin_organizations__org_uuid__settings_brand_assets_favicon_16_delete"
    )
    def delete_favicon_16(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon 16x16."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_16",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_favicon_32_admin_organizations__org_uuid__settings_brand_assets_favicon_32_post"
    )
    def set_favicon_32(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon 32x32."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_32",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_32_admin_organizations__org_uuid__settings_brand_assets_favicon_32_delete"
    )
    def delete_favicon_32(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon 32x32."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_32",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_apple_touch_icon_admin_organizations__org_uuid__settings_brand_assets_apple_touch_icon_post"
    )
    def set_apple_touch_icon(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Apple Touch Icon."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/apple_touch_icon",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_apple_touch_icon_admin_organizations__org_uuid__settings_brand_assets_apple_touch_icon_delete"
    )
    def delete_apple_touch_icon(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Apple Touch Icon."""
        return cast(
            OrgBrandAssetsConfigResponse,
            self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/apple_touch_icon",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_organization_brand_general_admin_organizations__org_uuid__settings_brand_general_post"
    )
    def set_brand_general(
        self, org_uuid: str, *, body: BrandGeneralCreateRequest
    ) -> OrgBrandGeneralConfigResponse:
        """Set Organization Brand General Settings (Superadmin)."""
        return cast(
            OrgBrandGeneralConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_general",
                json_body=body,
                cast_to=OrgBrandGeneralConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_brand_general_admin_organizations__org_uuid__settings_brand_general_get"
    )
    def retrieve_brand_general(self, org_uuid: str) -> BrandGeneralValue:
        """Get Organization Brand General Settings."""
        return cast(
            BrandGeneralValue,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_general", cast_to=BrandGeneralValue
            ),
        )

    @operation(
        "set_organization_platform_capabilities_admin_organizations__org_uuid__settings_platform_capabilities_post"
    )
    def set_platform_capabilities(
        self, org_uuid: str, *, body: PlatformCapabilitiesCreateRequest
    ) -> OrgPlatformCapabilitiesConfigResponse:
        """Set Organization Platform Capabilities."""
        return cast(
            OrgPlatformCapabilitiesConfigResponse,
            self._client.post(
                f"/admin/organizations/{org_uuid}/settings/platform_capabilities",
                json_body=body,
                cast_to=OrgPlatformCapabilitiesConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_platform_capabilities_admin_organizations__org_uuid__settings_platform_capabilities_get"
    )
    def retrieve_platform_capabilities(self, org_uuid: str) -> PlatformCapabilitiesValue:
        """Get Organization Platform Capabilities (Superadmin)."""
        return cast(
            PlatformCapabilitiesValue,
            self._client.get(
                f"/admin/organizations/{org_uuid}/settings/platform_capabilities",
                cast_to=PlatformCapabilitiesValue,
            ),
        )


class AsyncOrgConfig(AsyncResource):
    """Async counterpart of :class:`OrgConfig`."""

    namespace: ClassVar[str] = "org_config"

    @operation(
        "set_organization_general_settings_admin_organizations__org_uuid__settings_organization_general_post"
    )
    async def set_general(
        self, org_uuid: str, *, body: OrganizationGeneralCreateRequest
    ) -> OrgGeneralConfigResponse:
        """Set Organization General Settings (Superadmin)."""
        return cast(
            OrgGeneralConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/organization_general",
                json_body=body,
                cast_to=OrgGeneralConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_general_settings_admin_organizations__org_uuid__settings_organization_general_get"
    )
    async def retrieve_general(self, org_uuid: str) -> OrganizationGeneralValue:
        """Get Organization General Settings."""
        return cast(
            OrganizationGeneralValue,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/organization_general",
                cast_to=OrganizationGeneralValue,
            ),
        )

    @operation(
        "update_organization_domain_settings_admin_organizations__org_uuid__settings_domain_settings_put"
    )
    async def update_domain_settings(
        self, org_uuid: str, *, body: DomainSettingsUpdateRequest
    ) -> DomainSettingsResponse:
        """Update Organization Domain Settings."""
        return cast(
            DomainSettingsResponse,
            await self._client.put(
                f"/admin/organizations/{org_uuid}/settings/domain_settings",
                json_body=body,
                cast_to=DomainSettingsResponse,
            ),
        )

    @operation(
        "retrieve_organization_domain_settings_admin_organizations__org_uuid__settings_domain_settings_get"
    )
    async def retrieve_domain_settings(self, org_uuid: str) -> DomainSettingsResponse:
        """Get Organization Domain Settings."""
        return cast(
            DomainSettingsResponse,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/domain_settings",
                cast_to=DomainSettingsResponse,
            ),
        )

    @operation(
        "set_organization_brand_palette_admin_organizations__org_uuid__settings_brand_palette_post"
    )
    async def set_brand_palette(
        self, org_uuid: str, *, body: BrandPaletteCreateRequest
    ) -> OrgBrandPaletteConfigResponse:
        """Set Organization Brand Palette."""
        return cast(
            OrgBrandPaletteConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_palette",
                json_body=body,
                cast_to=OrgBrandPaletteConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_brand_palette_admin_organizations__org_uuid__settings_brand_palette_get"
    )
    async def retrieve_brand_palette(self, org_uuid: str) -> BrandPaletteValue:
        """Get Organization Brand Palette."""
        return cast(
            BrandPaletteValue,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_palette", cast_to=BrandPaletteValue
            ),
        )

    @operation(
        "retrieve_organization_brand_assets_admin_organizations__org_uuid__settings_brand_assets_get"
    )
    async def retrieve_brand_assets(self, org_uuid: str) -> BrandAssetsValue:
        """Get Organization Brand Assets."""
        return cast(
            BrandAssetsValue,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_assets", cast_to=BrandAssetsValue
            ),
        )

    @operation(
        "set_org_square_logo_admin_organizations__org_uuid__settings_brand_assets_square_logo_post"
    )
    async def set_square_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Square Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/square_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_square_logo_admin_organizations__org_uuid__settings_brand_assets_square_logo_delete"
    )
    async def delete_square_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Square Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/square_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_square_logo_admin_organizations__org_uuid__settings_brand_assets_white_square_logo_post"
    )
    async def set_white_square_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Square Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_square_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_square_logo_admin_organizations__org_uuid__settings_brand_assets_white_square_logo_delete"
    )
    async def delete_white_square_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Square Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_square_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_extended_logo_admin_organizations__org_uuid__settings_brand_assets_extended_logo_post"
    )
    async def set_extended_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Extended Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/extended_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_extended_logo_admin_organizations__org_uuid__settings_brand_assets_extended_logo_delete"
    )
    async def delete_extended_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Extended Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/extended_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_extended_logo_admin_organizations__org_uuid__settings_brand_assets_white_extended_logo_post"
    )
    async def set_white_extended_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Extended Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_extended_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_extended_logo_admin_organizations__org_uuid__settings_brand_assets_white_extended_logo_delete"
    )
    async def delete_white_extended_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Extended Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_extended_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_login_page_logo_post"
    )
    async def set_login_page_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Login Page Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_page_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_login_page_logo_delete"
    )
    async def delete_login_page_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Login Page Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_page_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_white_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_white_login_page_logo_post"
    )
    async def set_white_login_page_logo(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization White Login Page Logo."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_login_page_logo",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_white_login_page_logo_admin_organizations__org_uuid__settings_brand_assets_white_login_page_logo_delete"
    )
    async def delete_white_login_page_logo(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization White Login Page Logo."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/white_login_page_logo",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_login_background_image_admin_organizations__org_uuid__settings_brand_assets_login_background_image_post"
    )
    async def set_login_background_image(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Login Background Image."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_background_image",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_login_background_image_admin_organizations__org_uuid__settings_brand_assets_login_background_image_delete"
    )
    async def delete_login_background_image(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Login Background Image."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/login_background_image",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation("set_org_favicon_admin_organizations__org_uuid__settings_brand_assets_favicon_post")
    async def set_favicon(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_admin_organizations__org_uuid__settings_brand_assets_favicon_delete"
    )
    async def delete_favicon(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_favicon_16_admin_organizations__org_uuid__settings_brand_assets_favicon_16_post"
    )
    async def set_favicon_16(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon 16x16."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_16",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_16_admin_organizations__org_uuid__settings_brand_assets_favicon_16_delete"
    )
    async def delete_favicon_16(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon 16x16."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_16",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_favicon_32_admin_organizations__org_uuid__settings_brand_assets_favicon_32_post"
    )
    async def set_favicon_32(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Favicon 32x32."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_32",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_favicon_32_admin_organizations__org_uuid__settings_brand_assets_favicon_32_delete"
    )
    async def delete_favicon_32(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Favicon 32x32."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/favicon_32",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_org_apple_touch_icon_admin_organizations__org_uuid__settings_brand_assets_apple_touch_icon_post"
    )
    async def set_apple_touch_icon(
        self, org_uuid: str, file: bytes, *, filename: str | None = None
    ) -> OrgBrandAssetsConfigResponse:
        """Set Organization Apple Touch Icon."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/apple_touch_icon",
                files=files,
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "delete_org_apple_touch_icon_admin_organizations__org_uuid__settings_brand_assets_apple_touch_icon_delete"
    )
    async def delete_apple_touch_icon(self, org_uuid: str) -> OrgBrandAssetsConfigResponse:
        """Delete Organization Apple Touch Icon."""
        return cast(
            OrgBrandAssetsConfigResponse,
            await self._client.delete(
                f"/admin/organizations/{org_uuid}/settings/brand_assets/apple_touch_icon",
                cast_to=OrgBrandAssetsConfigResponse,
            ),
        )

    @operation(
        "set_organization_brand_general_admin_organizations__org_uuid__settings_brand_general_post"
    )
    async def set_brand_general(
        self, org_uuid: str, *, body: BrandGeneralCreateRequest
    ) -> OrgBrandGeneralConfigResponse:
        """Set Organization Brand General Settings (Superadmin)."""
        return cast(
            OrgBrandGeneralConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/brand_general",
                json_body=body,
                cast_to=OrgBrandGeneralConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_brand_general_admin_organizations__org_uuid__settings_brand_general_get"
    )
    async def retrieve_brand_general(self, org_uuid: str) -> BrandGeneralValue:
        """Get Organization Brand General Settings."""
        return cast(
            BrandGeneralValue,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/brand_general", cast_to=BrandGeneralValue
            ),
        )

    @operation(
        "set_organization_platform_capabilities_admin_organizations__org_uuid__settings_platform_capabilities_post"
    )
    async def set_platform_capabilities(
        self, org_uuid: str, *, body: PlatformCapabilitiesCreateRequest
    ) -> OrgPlatformCapabilitiesConfigResponse:
        """Set Organization Platform Capabilities."""
        return cast(
            OrgPlatformCapabilitiesConfigResponse,
            await self._client.post(
                f"/admin/organizations/{org_uuid}/settings/platform_capabilities",
                json_body=body,
                cast_to=OrgPlatformCapabilitiesConfigResponse,
            ),
        )

    @operation(
        "retrieve_organization_platform_capabilities_admin_organizations__org_uuid__settings_platform_capabilities_get"
    )
    async def retrieve_platform_capabilities(self, org_uuid: str) -> PlatformCapabilitiesValue:
        """Get Organization Platform Capabilities (Superadmin)."""
        return cast(
            PlatformCapabilitiesValue,
            await self._client.get(
                f"/admin/organizations/{org_uuid}/settings/platform_capabilities",
                cast_to=PlatformCapabilitiesValue,
            ),
        )


Galene._ADMIN_NAMESPACES.append(OrgConfig)
AsyncGalene._ADMIN_NAMESPACES.append(AsyncOrgConfig)
