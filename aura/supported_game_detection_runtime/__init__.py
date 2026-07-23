"""Sprint 282 supported-game detection runtime."""

from .aura_supported_game_detection_orion_adapter import (
    AuraWindowsSupportedGameDetectionAdapter,
)
from .aura_supported_game_detection_runtime_manager import (
    AuraSupportedGameDetectionRuntimeManager,
    SupportedGameDetectionRuntimeError,
)

__all__ = [
    "AuraSupportedGameDetectionRuntimeManager",
    "AuraWindowsSupportedGameDetectionAdapter",
    "SupportedGameDetectionRuntimeError",
]
