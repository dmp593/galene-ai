"""`audio` resource: OpenAI-compatible text-to-speech, transcription, and translation.

`/v1/audio/*` mirrors OpenAI's Audio API. `speech` returns raw audio bytes;
`transcriptions`/`translations` upload an audio file via multipart and decode a
`Transcription` (`{text}`); `voices` lists available TTS voices (untyped response).
"""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models import Transcription
from galene_ai.models._generated import AudioSpeechRequest


class Audio(SyncResource):
    """List voices, synthesize speech, and transcribe or translate audio."""

    namespace: ClassVar[str] = "audio"

    @operation("_audio_voices_v1_audio_voices_get")
    def voices(self) -> dict[str, Any]:
        """List available TTS voices."""
        # spec: untyped response
        return cast(dict[str, Any], self._client.get("/v1/audio/voices", cast_to=dict))

    @operation("_create_speech_v1_audio_speech_post")
    def speech(self, body: AudioSpeechRequest, *, store: bool | None = None) -> bytes:
        """Generate speech from text."""
        return cast(
            bytes,
            self._client.post(
                "/v1/audio/speech",
                params={"store": store},
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("_create_transcription_v1_audio_transcriptions_post")
    def transcribe(self, file: bytes, *, model: str, filename: str | None = None) -> Transcription:
        """Transcribe audio to text."""
        return cast(
            Transcription,
            self._client.post(
                "/v1/audio/transcriptions",
                data={"model": model},
                files={"file": (filename or "audio", file)},
                cast_to=Transcription,
            ),
        )

    @operation("_create_translation_v1_audio_translations_post")
    def translate(self, file: bytes, *, model: str, filename: str | None = None) -> Transcription:
        """Translate audio to English text."""
        return cast(
            Transcription,
            self._client.post(
                "/v1/audio/translations",
                data={"model": model},
                files={"file": (filename or "audio", file)},
                cast_to=Transcription,
            ),
        )


class AsyncAudio(AsyncResource):
    """Async counterpart of `Audio`."""

    namespace: ClassVar[str] = "audio"

    @operation("_audio_voices_v1_audio_voices_get")
    async def voices(self) -> dict[str, Any]:
        """List available TTS voices."""
        # spec: untyped response
        return cast(dict[str, Any], await self._client.get("/v1/audio/voices", cast_to=dict))

    @operation("_create_speech_v1_audio_speech_post")
    async def speech(self, body: AudioSpeechRequest, *, store: bool | None = None) -> bytes:
        """Generate speech from text."""
        return cast(
            bytes,
            await self._client.post(
                "/v1/audio/speech",
                params={"store": store},
                json_body=body,
                cast_to=bytes,
            ),
        )

    @operation("_create_transcription_v1_audio_transcriptions_post")
    async def transcribe(
        self, file: bytes, *, model: str, filename: str | None = None
    ) -> Transcription:
        """Transcribe audio to text."""
        return cast(
            Transcription,
            await self._client.post(
                "/v1/audio/transcriptions",
                data={"model": model},
                files={"file": (filename or "audio", file)},
                cast_to=Transcription,
            ),
        )

    @operation("_create_translation_v1_audio_translations_post")
    async def translate(
        self, file: bytes, *, model: str, filename: str | None = None
    ) -> Transcription:
        """Translate audio to English text."""
        return cast(
            Transcription,
            await self._client.post(
                "/v1/audio/translations",
                data={"model": model},
                files={"file": (filename or "audio", file)},
                cast_to=Transcription,
            ),
        )


Galene._NAMESPACES.append(Audio)
AsyncGalene._NAMESPACES.append(AsyncAudio)
