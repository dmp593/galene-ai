"""`tts` resource: text-to-speech voice samples and organization language samples."""

from __future__ import annotations

from typing import Any, ClassVar, cast

from galene_ai._client import AsyncGalene, Galene
from galene_ai._core.resource import AsyncResource, SyncResource, operation
from galene_ai.models._generated import (
    AudioSampleListResponse,
    AudioSampleRefTextUpdateRequest,
    AudioSampleResponse,
    AudioSampleTranscriptionRequest,
    AvailableVoicesResponse,
    OrganizationLanguageAudioSettingsResponse,
    OrganizationLanguageRefTextUpdateRequest,
    OrganizationLanguageTranscriptionRequest,
)


class Tts(SyncResource):
    """TTS voice samples and organization language reference samples."""

    namespace: ClassVar[str] = "tts"

    @operation(
        "list_tts_language_samples_admin_organizations__organization_uuid__tts_language_samples_get"
    )
    def list_language_samples(
        self, organization_uuid: str
    ) -> OrganizationLanguageAudioSettingsResponse:
        """List TTS language reference samples for an organization."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            self._client.get(
                f"/admin/organizations/{organization_uuid}/tts-language-samples",
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "upload_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__post"
    )
    def upload_language_sample(
        self,
        organization_uuid: str,
        language_code: str,
        file: bytes,
        *,
        filename: str | None = None,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Upload or replace organization TTS language sample."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}",
                files=files,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "delete_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__delete"
    )
    def delete_language_sample(
        self, organization_uuid: str, language_code: str
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Delete organization TTS language sample."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            self._client.delete(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}",
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "transcribe_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__transcribe_post"
    )
    def transcribe_language_sample(
        self,
        organization_uuid: str,
        language_code: str,
        *,
        body: OrganizationLanguageTranscriptionRequest,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Transcribe organization language sample."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            self._client.post(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}/transcribe",
                json_body=body,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "update_tts_language_sample_ref_text_admin_organizations__organization_uuid__tts_language_samples__language_code__ref_text_patch"
    )
    def update_language_sample_ref_text(
        self,
        organization_uuid: str,
        language_code: str,
        *,
        body: OrganizationLanguageRefTextUpdateRequest,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Update organization language sample ref_text."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            self._client.patch(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}/ref-text",
                json_body=body,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation("get_voices_tts_audio_samples_voices_get")
    def get_voices(self) -> AvailableVoicesResponse:
        """Get Available Voices."""
        return cast(
            AvailableVoicesResponse,
            self._client.get("/tts-audio-samples/voices", cast_to=AvailableVoicesResponse),
        )

    @operation("list_samples_tts_audio_samples_get")
    def list_samples(self) -> AudioSampleListResponse:
        """List Audio Samples."""
        return cast(
            AudioSampleListResponse,
            self._client.get("/tts-audio-samples", cast_to=AudioSampleListResponse),
        )

    @operation("upload_sample_tts_audio_samples_post")
    def upload_sample(
        self,
        file: bytes,
        *,
        name: str,
        description: str | None = None,
        ref_text: str | None = None,
        filename: str | None = None,
    ) -> AudioSampleResponse:
        """Upload Audio Sample."""
        files = {"file": (filename or "upload", file)}
        data: dict[str, str] = {"name": name}
        if description is not None:
            data["description"] = description
        if ref_text is not None:
            data["ref_text"] = ref_text
        return cast(
            AudioSampleResponse,
            self._client.post(
                "/tts-audio-samples",
                data=data,
                files=files,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("transcribe_sample_ref_text_tts_audio_samples__sample_id__transcribe_post")
    def transcribe_sample(
        self, sample_id: str, *, body: AudioSampleTranscriptionRequest
    ) -> AudioSampleResponse:
        """Transcribe Audio Sample To Ref Text."""
        return cast(
            AudioSampleResponse,
            self._client.post(
                f"/tts-audio-samples/{sample_id}/transcribe",
                json_body=body,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("patch_sample_ref_text_tts_audio_samples__sample_id__ref_text_patch")
    def update_sample_ref_text(
        self, sample_id: str, *, body: AudioSampleRefTextUpdateRequest
    ) -> AudioSampleResponse:
        """Update Audio Sample Ref Text."""
        return cast(
            AudioSampleResponse,
            self._client.patch(
                f"/tts-audio-samples/{sample_id}/ref-text",
                json_body=body,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("get_sample_file_tts_audio_samples__sample_id__get")
    def download_sample(self, sample_id: str) -> bytes:
        """Download Audio Sample."""
        return cast(bytes, self._client.get(f"/tts-audio-samples/{sample_id}", cast_to=bytes))

    @operation("delete_sample_tts_audio_samples__sample_id__delete")
    def delete_sample(self, sample_id: str) -> dict[str, Any]:
        """Delete Audio Sample."""
        # spec: untyped response
        return cast(
            "dict[str, Any]",
            self._client.delete(f"/tts-audio-samples/{sample_id}", cast_to=dict),
        )


class AsyncTts(AsyncResource):
    """Async counterpart of `Tts`."""

    namespace: ClassVar[str] = "tts"

    @operation(
        "list_tts_language_samples_admin_organizations__organization_uuid__tts_language_samples_get"
    )
    async def list_language_samples(
        self, organization_uuid: str
    ) -> OrganizationLanguageAudioSettingsResponse:
        """List TTS language reference samples for an organization."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            await self._client.get(
                f"/admin/organizations/{organization_uuid}/tts-language-samples",
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "upload_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__post"
    )
    async def upload_language_sample(
        self,
        organization_uuid: str,
        language_code: str,
        file: bytes,
        *,
        filename: str | None = None,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Upload or replace organization TTS language sample."""
        files = {"file": (filename or "upload", file)}
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}",
                files=files,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "delete_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__delete"
    )
    async def delete_language_sample(
        self, organization_uuid: str, language_code: str
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Delete organization TTS language sample."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            await self._client.delete(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}",
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "transcribe_tts_language_sample_admin_organizations__organization_uuid__tts_language_samples__language_code__transcribe_post"
    )
    async def transcribe_language_sample(
        self,
        organization_uuid: str,
        language_code: str,
        *,
        body: OrganizationLanguageTranscriptionRequest,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Transcribe organization language sample."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            await self._client.post(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}/transcribe",
                json_body=body,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation(
        "update_tts_language_sample_ref_text_admin_organizations__organization_uuid__tts_language_samples__language_code__ref_text_patch"
    )
    async def update_language_sample_ref_text(
        self,
        organization_uuid: str,
        language_code: str,
        *,
        body: OrganizationLanguageRefTextUpdateRequest,
    ) -> OrganizationLanguageAudioSettingsResponse:
        """Update organization language sample ref_text."""
        return cast(
            OrganizationLanguageAudioSettingsResponse,
            await self._client.patch(
                f"/admin/organizations/{organization_uuid}/tts-language-samples/{language_code}/ref-text",
                json_body=body,
                cast_to=OrganizationLanguageAudioSettingsResponse,
            ),
        )

    @operation("get_voices_tts_audio_samples_voices_get")
    async def get_voices(self) -> AvailableVoicesResponse:
        """Get Available Voices."""
        return cast(
            AvailableVoicesResponse,
            await self._client.get("/tts-audio-samples/voices", cast_to=AvailableVoicesResponse),
        )

    @operation("list_samples_tts_audio_samples_get")
    async def list_samples(self) -> AudioSampleListResponse:
        """List Audio Samples."""
        return cast(
            AudioSampleListResponse,
            await self._client.get("/tts-audio-samples", cast_to=AudioSampleListResponse),
        )

    @operation("upload_sample_tts_audio_samples_post")
    async def upload_sample(
        self,
        file: bytes,
        *,
        name: str,
        description: str | None = None,
        ref_text: str | None = None,
        filename: str | None = None,
    ) -> AudioSampleResponse:
        """Upload Audio Sample."""
        files = {"file": (filename or "upload", file)}
        data: dict[str, str] = {"name": name}
        if description is not None:
            data["description"] = description
        if ref_text is not None:
            data["ref_text"] = ref_text
        return cast(
            AudioSampleResponse,
            await self._client.post(
                "/tts-audio-samples",
                data=data,
                files=files,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("transcribe_sample_ref_text_tts_audio_samples__sample_id__transcribe_post")
    async def transcribe_sample(
        self, sample_id: str, *, body: AudioSampleTranscriptionRequest
    ) -> AudioSampleResponse:
        """Transcribe Audio Sample To Ref Text."""
        return cast(
            AudioSampleResponse,
            await self._client.post(
                f"/tts-audio-samples/{sample_id}/transcribe",
                json_body=body,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("patch_sample_ref_text_tts_audio_samples__sample_id__ref_text_patch")
    async def update_sample_ref_text(
        self, sample_id: str, *, body: AudioSampleRefTextUpdateRequest
    ) -> AudioSampleResponse:
        """Update Audio Sample Ref Text."""
        return cast(
            AudioSampleResponse,
            await self._client.patch(
                f"/tts-audio-samples/{sample_id}/ref-text",
                json_body=body,
                cast_to=AudioSampleResponse,
            ),
        )

    @operation("get_sample_file_tts_audio_samples__sample_id__get")
    async def download_sample(self, sample_id: str) -> bytes:
        """Download Audio Sample."""
        return cast(bytes, await self._client.get(f"/tts-audio-samples/{sample_id}", cast_to=bytes))

    @operation("delete_sample_tts_audio_samples__sample_id__delete")
    async def delete_sample(self, sample_id: str) -> dict[str, Any]:
        """Delete Audio Sample."""
        # spec: untyped response
        return cast(
            "dict[str, Any]",
            await self._client.delete(f"/tts-audio-samples/{sample_id}", cast_to=dict),
        )


Galene._NAMESPACES.append(Tts)
AsyncGalene._NAMESPACES.append(AsyncTts)
