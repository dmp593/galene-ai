import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import (
    AudioSampleRefTextUpdateRequest,
    AudioSampleTranscriptionRequest,
    OrganizationLanguageRefTextUpdateRequest,
    OrganizationLanguageTranscriptionRequest,
)


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def _lang_settings(result=None):
    return {"success": True, "message": "ok", "result": result or {"languages": {}}}


def _sample(sample_id="s1"):
    return {
        "id": sample_id,
        "name": "myvoice",
        "filename": "v.wav",
        "size": 100,
        "mime_type": "audio/wav",
        "created_at": 1699564800,
        "ref_text": "hello",
        "has_ref_text": True,
    }


def test_list_language_samples_hits_endpoint_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/admin/organizations/org1/tts-language-samples"
        return httpx.Response(200, json=_lang_settings({"languages": {"en": {}}}))

    resp = _client(handler).tts.list_language_samples("org1")
    assert resp.success is True
    assert resp.result == {"languages": {"en": {}}}


def test_upload_language_sample_sends_multipart_and_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org1/tts-language-samples/en"
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b'name="file"; filename="s.wav"' in req.content
        return httpx.Response(200, json=_lang_settings())

    resp = _client(handler).tts.upload_language_sample("org1", "en", b"abc", filename="s.wav")
    assert resp.message == "ok"


def test_delete_language_sample_hits_endpoint():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/admin/organizations/org1/tts-language-samples/en"
        return httpx.Response(200, json=_lang_settings())

    resp = _client(handler).tts.delete_language_sample("org1", "en")
    assert resp.success is True


def test_transcribe_language_sample_sends_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/admin/organizations/org1/tts-language-samples/en/transcribe"
        assert b'"language":"it"' in req.content
        return httpx.Response(200, json=_lang_settings())

    resp = _client(handler).tts.transcribe_language_sample(
        "org1", "en", body=OrganizationLanguageTranscriptionRequest(language="it")
    )
    assert resp.success is True


def test_update_language_sample_ref_text_patches():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PATCH"
        assert req.url.path == "/admin/organizations/org1/tts-language-samples/en/ref-text"
        assert b'"ref_text":"hola"' in req.content
        return httpx.Response(200, json=_lang_settings())

    resp = _client(handler).tts.update_language_sample_ref_text(
        "org1", "en", body=OrganizationLanguageRefTextUpdateRequest(ref_text="hola")
    )
    assert resp.success is True


def test_get_voices_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/tts-audio-samples/voices"
        return httpx.Response(
            200,
            json={"predefined_voices": ["alloy", "echo"], "custom_voices": ["myvoice"]},
        )

    resp = _client(handler).tts.get_voices()
    assert resp.predefined_voices == ["alloy", "echo"]
    assert resp.custom_voices == ["myvoice"]


def test_list_samples_decodes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/tts-audio-samples"
        return httpx.Response(200, json={"total": 1, "samples": [_sample()]})

    resp = _client(handler).tts.list_samples()
    assert resp.total == 1
    assert resp.samples[0].name == "myvoice"


def test_upload_sample_sends_multipart_form_fields():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/tts-audio-samples"
        body = req.content
        assert b'name="name"\r\n\r\nmyvoice' in body
        assert b'name="description"\r\n\r\ndesc' in body
        assert b'name="ref_text"\r\n\r\nhello' in body
        assert b'name="file"; filename="v.wav"' in body
        return httpx.Response(200, json=_sample())

    resp = _client(handler).tts.upload_sample(
        b"abc", name="myvoice", description="desc", ref_text="hello", filename="v.wav"
    )
    assert resp.id == "s1"
    assert resp.name == "myvoice"


def test_upload_sample_omits_optional_fields():
    def handler(req: httpx.Request) -> httpx.Response:
        body = req.content
        assert b'name="name"\r\n\r\nmyvoice' in body
        assert b"description" not in body
        assert b"ref_text" not in body
        return httpx.Response(200, json=_sample())

    resp = _client(handler).tts.upload_sample(b"abc", name="myvoice")
    assert resp.id == "s1"


def test_transcribe_sample_sends_body():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/tts-audio-samples/s1/transcribe"
        assert b'"language":"en"' in req.content
        return httpx.Response(200, json=_sample())

    resp = _client(handler).tts.transcribe_sample(
        "s1", body=AudioSampleTranscriptionRequest(language="en")
    )
    assert resp.id == "s1"


def test_update_sample_ref_text_patches():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "PATCH"
        assert req.url.path == "/tts-audio-samples/s1/ref-text"
        assert b'"ref_text":"new text"' in req.content
        return httpx.Response(200, json=_sample())

    resp = _client(handler).tts.update_sample_ref_text(
        "s1", body=AudioSampleRefTextUpdateRequest(ref_text="new text")
    )
    assert resp.id == "s1"


def test_download_sample_returns_bytes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/tts-audio-samples/s1"
        return httpx.Response(200, content=b"\x00\x01wav")

    assert _client(handler).tts.download_sample("s1") == b"\x00\x01wav"


def test_delete_sample_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "DELETE"
        assert req.url.path == "/tts-audio-samples/s1"
        return httpx.Response(200, json={"deleted": True, "id": "s1"})

    result = _client(handler).tts.delete_sample("s1")
    assert result["deleted"] is True


async def test_async_tts_get_voices_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/tts-audio-samples/voices"
        return httpx.Response(200, json={"predefined_voices": ["alloy"], "custom_voices": []})

    client = _aclient(handler)
    try:
        resp = await client.tts.get_voices()
        assert resp.predefined_voices == ["alloy"]
    finally:
        await client.aclose()
