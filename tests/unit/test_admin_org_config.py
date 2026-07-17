import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    BrandGeneralCreateRequest,
    BrandPaletteCreateRequest,
    ColorSetting,
    DomainSettingsUpdateRequest,
    OrganizationGeneralCreateRequest,
    PlatformCapabilitiesCreateRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


ORG = "org-1"


def test_set_general():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/organization_general"
        assert b"new@x.com" in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "organization_general",
                "value": {"support_email": "help@x.com"},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_general(
        ORG, body=OrganizationGeneralCreateRequest(support_email="new@x.com")
    )
    assert result.id == 7
    assert result.name == "organization_general"


def test_retrieve_general():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/organization_general"
        return httpx.Response(200, json={"support_email": "help@x.com"})

    result = _client(handler).admin.org_config.retrieve_general(ORG)
    assert result.support_email == "help@x.com"


def test_update_domain_settings():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PUT"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/domain_settings"
        assert b"app.company.com" in req.content
        return httpx.Response(
            200, json={"domain_name": "app.company.com", "certificate": None, "private_key": None}
        )

    result = _client(handler).admin.org_config.update_domain_settings(
        ORG, body=DomainSettingsUpdateRequest(domain_name="app.company.com")
    )
    assert result.domain_name == "app.company.com"


def test_retrieve_domain_settings():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/domain_settings"
        return httpx.Response(
            200, json={"domain_name": "app.company.com", "certificate": None, "private_key": None}
        )

    result = _client(handler).admin.org_config.retrieve_domain_settings(ORG)
    assert result.domain_name == "app.company.com"


def test_set_brand_palette():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_palette"
        assert b"#a21caf" in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_palette",
                "value": {
                    "primary": {"color": "#a21caf", "hover_color": "#c026d3"},
                    "secondary": {"color": "#3b82f6", "hover_color": "#2563eb"},
                    "tertiary": {"color": "#6b7280", "hover_color": "#4b5563"},
                },
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_brand_palette(
        ORG,
        body=BrandPaletteCreateRequest(
            primary=ColorSetting(color="#a21caf", hover_color="#c026d3"),
            secondary=ColorSetting(color="#3b82f6", hover_color="#2563eb"),
            tertiary=ColorSetting(color="#6b7280", hover_color="#4b5563"),
        ),
    )
    assert result.id == 7
    assert result.name == "brand_palette"


def test_retrieve_brand_palette():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_palette"
        return httpx.Response(
            200,
            json={
                "primary": {"color": "#a21caf", "hover_color": "#c026d3"},
                "secondary": {"color": "#3b82f6", "hover_color": "#2563eb"},
                "tertiary": {"color": "#6b7280", "hover_color": "#4b5563"},
            },
        )

    result = _client(handler).admin.org_config.retrieve_brand_palette(ORG)
    assert result.primary.color == "#a21caf"


def test_retrieve_brand_assets():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets"
        return httpx.Response(200, json={"favicon": None})

    result = _client(handler).admin.org_config.retrieve_brand_assets(ORG)
    assert result.favicon is None


def test_set_square_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/square_logo"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_square_logo(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_square_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/square_logo"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_square_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_white_square_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/white_square_logo"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_white_square_logo(
        ORG, b"img", filename="logo.png"
    )
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_white_square_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/white_square_logo"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_white_square_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_extended_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/extended_logo"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_extended_logo(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_extended_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/extended_logo"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_extended_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_white_extended_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert (
            req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/white_extended_logo"
        )
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_white_extended_logo(
        ORG, b"img", filename="logo.png"
    )
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_white_extended_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert (
            req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/white_extended_logo"
        )
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_white_extended_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_login_page_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/login_page_logo"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_login_page_logo(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_login_page_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/login_page_logo"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_login_page_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_white_login_page_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert (
            req.url.path
            == f"/admin/organizations/{ORG}/settings/brand_assets/white_login_page_logo"
        )
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_white_login_page_logo(
        ORG, b"img", filename="logo.png"
    )
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_white_login_page_logo():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert (
            req.url.path
            == f"/admin/organizations/{ORG}/settings/brand_assets/white_login_page_logo"
        )
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_white_login_page_logo(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_login_background_image():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert (
            req.url.path
            == f"/admin/organizations/{ORG}/settings/brand_assets/login_background_image"
        )
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_login_background_image(
        ORG, b"img", filename="logo.png"
    )
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_login_background_image():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert (
            req.url.path
            == f"/admin/organizations/{ORG}/settings/brand_assets/login_background_image"
        )
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_login_background_image(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_favicon():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_favicon(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_favicon():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_favicon(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_favicon_16():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon_16"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_favicon_16(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_favicon_16():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon_16"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_favicon_16(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_favicon_32():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon_32"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_favicon_32(ORG, b"img", filename="logo.png")
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_favicon_32():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/favicon_32"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_favicon_32(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_apple_touch_icon():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/apple_touch_icon"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="logo.png"' in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_apple_touch_icon(
        ORG, b"img", filename="logo.png"
    )
    assert result.id == 7
    assert result.name == "brand_assets"


def test_delete_apple_touch_icon():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_assets/apple_touch_icon"
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_assets",
                "value": {},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.delete_apple_touch_icon(ORG)
    assert result.id == 7
    assert result.name == "brand_assets"


def test_set_brand_general():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_general"
        assert b"Zeus" in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "brand_general",
                "value": {"agent_name": "Zeus"},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_brand_general(
        ORG, body=BrandGeneralCreateRequest(agent_name="Zeus")
    )
    assert result.id == 7
    assert result.name == "brand_general"


def test_retrieve_brand_general():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/brand_general"
        return httpx.Response(200, json={"agent_name": "Zeus"})

    result = _client(handler).admin.org_config.retrieve_brand_general(ORG)
    assert result.agent_name == "Zeus"


def test_set_platform_capabilities():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/platform_capabilities"
        assert b"voice" in req.content
        return httpx.Response(
            200,
            json={
                "id": 7,
                "created_at": 1699,
                "updated_at": 1700,
                "name": "platform_capabilities",
                "value": {"voice": False},
                "org_uuid": "org-1",
            },
        )

    result = _client(handler).admin.org_config.set_platform_capabilities(
        ORG, body=PlatformCapabilitiesCreateRequest(voice=False)
    )
    assert result.id == 7
    assert result.name == "platform_capabilities"


def test_retrieve_platform_capabilities():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/platform_capabilities"
        return httpx.Response(200, json={"voice": False})

    result = _client(handler).admin.org_config.retrieve_platform_capabilities(ORG)
    assert result.voice is False


async def test_async_org_config_retrieve_general_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == f"/admin/organizations/{ORG}/settings/organization_general"
        return httpx.Response(200, json={"support_email": "help@x.com"})

    client = _aclient(handler)
    try:
        result = await client.admin.org_config.retrieve_general(ORG)
        assert result.support_email == "help@x.com"
    finally:
        await client.aclose()
