from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Event:
    """
    Represents a single event inside AURA.

    Example:
    - aura.boot.started
    - aura.boot.ready
    - user.spoke
    - response.ready
    """

    name: str
    source: str = "aura"
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        return f"Event(name={self.name}, source={self.source}, payload={self.payload})"
