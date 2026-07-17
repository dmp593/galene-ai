import httpx

from galene_ai import AsyncGalene, Galene


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_deploy_updates_posts_to_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org-123/deploy-updates"
        return httpx.Response(
            200,
            json={
                "message": "Frontend deployment started successfully",
                "organization_uuid": "org-123",
                "workflow_id": "AdminOrgFrontendDeploymentWorkflow_1699564800",
                "workflow_run_id": "workflow-run-uuid-123",
            },
        )

    result = _client(handler).admin.deployment.deploy_updates("org-123")
    assert result["organization_uuid"] == "org-123"
    assert result["message"] == "Frontend deployment started successfully"


async def test_async_deploy_updates_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org-9/deploy-updates"
        return httpx.Response(
            200,
            json={
                "message": "Frontend deployment started successfully",
                "organization_uuid": "org-9",
                "workflow_id": "wf-9",
                "workflow_run_id": "run-9",
            },
        )

    client = _aclient(handler)
    try:
        result = await client.admin.deployment.deploy_updates("org-9")
        assert result["organization_uuid"] == "org-9"
        assert result["workflow_id"] == "wf-9"
    finally:
        await client.aclose()
