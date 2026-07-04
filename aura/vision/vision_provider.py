from dataclasses import dataclass, field
from typing import Any


@dataclass
class VisionProvider:
    """
    Represents a vision-related provider.

    Current phase:
    - metadata only
    - no real screen or camera access yet
    """

    name: str
    provider_type: str
    status: str
    description: str
    screen_supported: bool = False
    camera_supported: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "provider_type": self.provider_type,
            "status": self.status,
            "description": self.description,
            "screen_supported": self.screen_supported,
            "camera_supported": self.camera_supported,
            "metadata": self.metadata,
        }
