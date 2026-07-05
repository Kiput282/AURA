from dataclasses import dataclass, field
from typing import Any


@dataclass
class AvatarProvider:
    """
    Represents an avatar-related provider.

    Current phase:
    - metadata only
    - no real 3D avatar runtime yet
    """

    name: str
    provider_type: str
    status: str
    description: str
    expression_supported: bool = False
    gesture_supported: bool = False
    state_supported: bool = False
    runtime_supported: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "provider_type": self.provider_type,
            "status": self.status,
            "description": self.description,
            "expression_supported": self.expression_supported,
            "gesture_supported": self.gesture_supported,
            "state_supported": self.state_supported,
            "runtime_supported": self.runtime_supported,
            "metadata": self.metadata,
        }
