from aura.voice.voice_provider import VoiceProvider


class VoiceManager:
    """
    Voice Foundation for AURA.

    Current phase:
    - tracks voice capability status
    - exposes STT/TTS placeholder providers
    - does not access microphone or speaker yet
    """

    def __init__(self):
        self.providers = [
            VoiceProvider(
                name="stt_placeholder",
                provider_type="speech_to_text",
                status="foundation",
                description="Placeholder provider for future speech-to-text input.",
                input_supported=True,
                output_supported=False,
            ),
            VoiceProvider(
                name="tts_placeholder",
                provider_type="text_to_speech",
                status="foundation",
                description="Placeholder provider for future text-to-speech output.",
                input_supported=False,
                output_supported=True,
            ),
        ]

    def status(self) -> dict:
        return {
            "status": "foundation",
            "microphone_access": False,
            "speaker_output": False,
            "stt_ready": False,
            "tts_ready": False,
            "providers": len(self.providers),
            "note": "Voice foundation is online, but real STT/TTS runtime is not connected yet.",
        }

    def list_providers(self) -> list[VoiceProvider]:
        return self.providers
