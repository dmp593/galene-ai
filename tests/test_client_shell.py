from galene_ai import AsyncGalene, Galene


def test_client_constructs_with_api_key():
    client = Galene(api_key="sk-test", base_url="https://x")
    assert client is not None
    client.close()


async def test_async_client_context_manager():
    async with AsyncGalene(api_key="sk-test", base_url="https://x") as client:
        assert client is not None
