from aura.vision.vision_provider import VisionProvider


class VisionManager:
    """
    Vision Foundation for AURA.

    Current phase:
    - tracks vision capability status
    - exposes screen/camera placeholder providers
    - does not access screen or camera yet
    """

    def __init__(self):
        self.providers = [
            VisionProvider(
                name="screen_placeholder",
                provider_type="screen_analyzer",
                status="foundation",
                description="Placeholder provider for future screen analysis.",
                screen_supported=True,
                camera_supported=False,
            ),
            VisionProvider(
                name="camera_placeholder",
                provider_type="camera_analyzer",
                status="foundation",
                description="Placeholder provider for future camera/environment analysis.",
                screen_supported=False,
                camera_supported=True,
            ),
        ]

    def status(self) -> dict:
        return {
            "status": "foundation",
            "screen_access": False,
            "camera_access": False,
            "screen_ready": False,
            "camera_ready": False,
            "providers": len(self.providers),
            "note": "Vision foundation is online, but real screen/camera runtime is not connected yet.",
        }

    def list_providers(self) -> list[VisionProvider]:
        return self.providers
