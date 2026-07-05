from dataclasses import dataclass, field
from typing import Any


@dataclass
class SandboxPolicy:
    """
    Metadata policy for tool execution sandbox.

    Current phase:
    - classify commands
    - allow dry-run proposals
    - block dangerous patterns
    - no real execution by default
    """

    name: str
    status: str
    description: str
    allowed_commands: list[str] = field(default_factory=list)
    blocked_commands: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)
    dry_run_supported: bool = True
    real_execution_supported: bool = False
    requires_confirmation_for_execution: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "description": self.description,
            "allowed_commands": self.allowed_commands,
            "blocked_commands": self.blocked_commands,
            "blocked_patterns": self.blocked_patterns,
            "dry_run_supported": self.dry_run_supported,
            "real_execution_supported": self.real_execution_supported,
            "requires_confirmation_for_execution": self.requires_confirmation_for_execution,
            "metadata": self.metadata,
        }
