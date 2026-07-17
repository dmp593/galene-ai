import httpx

from galene_ai import AsyncGalene, Galene
from galene_ai.models import AudioSpeechRequest


def _client(handler) -> Galene:
    http = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://x")
    return Galene(api_key="k", base_url="https://x", http_client=http)


def _aclient(handler) -> AsyncGalene:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://x")
    return AsyncGalene(api_key="k", base_url="https://x", http_client=http)


def test_voices_hits_endpoint_and_returns_dict():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "GET"
        assert req.url.path == "/v1/audio/voices"
        return httpx.Response(200, json={"voices": ["alloy", "echo"]})

    result = _client(handler).audio.voices()
    assert result["voices"] == ["alloy", "echo"]


def test_speech_posts_json_body_and_returns_bytes():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/audio/speech"
        assert req.url.params["store"] == "true"
        assert b"Hello world" in req.content
        return httpx.Response(200, content=b"\x00\x01audio")

    body = AudioSpeechRequest(model="galene-tts", input="Hello world", voice="alloy")
    result = _client(handler).audio.speech(body, store=True)
    assert result == b"\x00\x01audio"


def test_speech_omits_store_param_when_absent():
    def handler(req: httpx.Request) -> httpx.Response:
        assert "store" not in req.url.params
        return httpx.Response(200, content=b"raw")

    body = AudioSpeechRequest(model="galene-tts", input="Hi")
    assert _client(handler).audio.speech(body) == b"raw"


def test_transcribe_sends_multipart_and_decodes_text():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/audio/transcriptions"
        assert req.headers["content-type"].startswith("multipart/form-data")
        body = req.content
        assert b'name="model"\r\n\r\ngalene-stt' in body
        assert b'name="file"; filename="clip.wav"' in body
        return httpx.Response(200, json={"text": "hello there"})

    result = _client(handler).audio.transcribe(b"riff", model="galene-stt", filename="clip.wav")
    assert result.text == "hello there"


def test_translate_sends_multipart_and_decodes_text():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/audio/translations"
        body = req.content
        assert b'name="model"\r\n\r\ngalene-stt' in body
        assert b'name="file"; filename="audio"' in body
        return httpx.Response(200, json={"text": "buongiorno -> good morning"})

    result = _client(handler).audio.translate(b"riff", model="galene-stt")
    assert result.text == "buongiorno -> good morning"


async def test_async_audio_transcribe_smoke():
    def handler(req: httpx.Request) -> httpx.Response:
        assert req.method == "POST"
        assert req.url.path == "/v1/audio/transcriptions"
        return httpx.Response(200, json={"text": "async ok"})

    client = _aclient(handler)
    try:
        result = await client.audio.transcribe(b"riff", model="galene-stt")
        assert result.text == "async ok"
    finally:
        await client.aclose()
