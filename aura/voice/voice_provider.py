from dataclasses import dataclass, field
from typing import Any


@dataclass
class VoiceProvider:
    """
    Represents a voice-related provider.

    Current phase:
    - metadata only
    - no real microphone or speaker access yet
    """

    name: str
    provider_type: str
    status: str
    description: str
    input_supported: bool = False
    output_supported: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "provider_type": self.provider_type,
            "status": self.status,
            "description": self.description,
            "input_supported": self.input_supported,
            "output_supported": self.output_supported,
            "metadata": self.metadata,
        }
