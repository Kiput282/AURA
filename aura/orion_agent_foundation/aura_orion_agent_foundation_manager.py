"""AURA ORION Agent Foundation.

Sprint 273 establishes a deterministic, side-effect-free ATLAS-side
foundation for a future ORION agent. It does not start a listener, open
a connection, authenticate, pair a device, exchange heartbeats,
negotiate capabilities, preview or approve actions, change permission,
write audit records, execute actions, persist runtime state, or mutate
ATLAS/ORION.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class OrionAgentFoundationError(RuntimeError):
    """Raised when the ORION agent foundation violates its own contract."""


@dataclass(frozen=True, slots=True)
class OrionAgentFoundationIdentity:
    """Stable metadata for the Sprint 273 foundation."""

    component_name: str
    component_version: str
    sprint: int
    boundary: str
    host_role: str
    remote_role: str


class AuraOrionAgentFoundationManager:
    """Expose the ORION agent foundation without runtime activation."""

    COMPONENT_NAME = "aura_orion_agent_foundation"
    COMPONENT_VERSION = "0.1.0"
    SPRINT = 273
    BOUNDARY = "orion_agent_foundation"
    HOST_ROLE = "ATLAS_CONTROL_PLANE"
    REMOTE_ROLE = "ORION_AGENT_DEFERRED"

    FALSE_RUNTIME_FIELDS = (
        "network_listener_active",
        "network_connection_active",
        "pairing_active",
        "authenticated",
        "device_identity_bound",
        "heartbeat_active",
        "capability_negotiation_active",
        "live_grounding_active",
        "action_preview_active",
        "approval_active",
        "permission_active",
        "audit_write_active",
        "real_action_execution_active",
        "watchdog_active",
        "emergency_stop_active",
        "recovery_active",
    )

    DEFERRED_BOUNDARIES = {
        "sprint_274": (
            "authenticated_pairing",
            "device_identity",
            "credentials_or_shared_secret",
        ),
        "sprint_275": (
            "heartbeat",
            "capability_negotiation",
            "live_grounding",
        ),
        "sprint_276": (
            "action_preview",
            "explicit_approval",
        ),
        "sprint_277": (
            "scoped_permission",
            "permission_expiry",
            "audit_write",
            "reviewed_memory",
        ),
        "sprint_278": (
            "orion_capture_actions",
            "orion_app_actions",
            "orion_file_actions",
            "orion_obs_actions",
        ),
        "sprint_279": (
            "watchdog",
            "emergency_stop_runtime",
            "recovery_execution",
            "dialogue_evaluation",
        ),
    }

    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root)

    def identity(self) -> dict[str, Any]:
        """Return deterministic component identity metadata."""

        identity = OrionAgentFoundationIdentity(
            component_name=self.COMPONENT_NAME,
            component_version=self.COMPONENT_VERSION,
            sprint=self.SPRINT,
            boundary=self.BOUNDARY,
            host_role=self.HOST_ROLE,
            remote_role=self.REMOTE_ROLE,
        )
        return asdict(identity)

    def status(self) -> dict[str, Any]:
        """Return the closed, foundation-only runtime state."""

        false_runtime = {
            field: False for field in self.FALSE_RUNTIME_FIELDS
        }
        return {
            "status": "ready",
            "reason": "orion_agent_foundation_ready_runtime_closed",
            "safe_idle": True,
            "foundation_only": True,
            **false_runtime,
        }

    def inspect_foundation(self) -> dict[str, Any]:
        """Describe the foundation schema and explicitly deferred work."""

        return {
            "identity": self.identity(),
            "runtime": self.status(),
            "manager_methods": [
                "__init__",
                "identity",
                "status",
                "inspect_foundation",
                "self_test",
            ],
            "deferred_boundaries": {
                sprint: list(items)
                for sprint, items in self.DEFERRED_BOUNDARIES.items()
            },
            "hard_guards": {
                "bind_network_listener": False,
                "open_network_connection": False,
                "read_or_write_credentials": False,
                "generate_device_identity": False,
                "pair_device": False,
                "send_heartbeat": False,
                "negotiate_capabilities": False,
                "execute_action": False,
                "write_audit_record": False,
                "persist_runtime_state": False,
                "mutate_orion": False,
                "mutate_atlas": False,
            },
        }

    def self_test(self) -> dict[str, Any]:
        """Validate the foundation contract without external side effects."""

        identity = self.identity()
        status = self.status()
        inspection = self.inspect_foundation()

        assertions: list[tuple[str, bool]] = []

        expected_identity = {
            "component_name": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "sprint": self.SPRINT,
            "boundary": self.BOUNDARY,
            "host_role": self.HOST_ROLE,
            "remote_role": self.REMOTE_ROLE,
        }
        for field, expected in expected_identity.items():
            assertions.append(
                (
                    f"identity_{field}",
                    identity.get(field) == expected,
                )
            )

        required_status_fields = (
            "status",
            "reason",
            "safe_idle",
            "foundation_only",
            *self.FALSE_RUNTIME_FIELDS,
        )
        for field in required_status_fields:
            assertions.append(
                (
                    f"status_field_{field}",
                    field in status,
                )
            )

        assertions.extend(
            [
                ("status_ready", status["status"] == "ready"),
                (
                    "status_reason",
                    status["reason"]
                    == "orion_agent_foundation_ready_runtime_closed",
                ),
                ("safe_idle_true", status["safe_idle"] is True),
                (
                    "foundation_only_true",
                    status["foundation_only"] is True,
                ),
            ]
        )

        for field in self.FALSE_RUNTIME_FIELDS:
            assertions.append(
                (
                    f"runtime_false_{field}",
                    status[field] is False,
                )
            )

        hard_guards = inspection["hard_guards"]
        for guard, value in hard_guards.items():
            assertions.append(
                (
                    f"hard_guard_{guard}",
                    value is False,
                )
            )

        deferred = inspection["deferred_boundaries"]
        assertions.extend(
            [
                (
                    "deferred_sprint_count",
                    sorted(deferred)
                    == [
                        "sprint_274",
                        "sprint_275",
                        "sprint_276",
                        "sprint_277",
                        "sprint_278",
                        "sprint_279",
                    ],
                ),
                (
                    "constructor_side_effects_zero",
                    self.project_root == Path(self.project_root),
                ),
                (
                    "network_side_effects_zero",
                    not status["network_listener_active"]
                    and not status["network_connection_active"],
                ),
                (
                    "action_side_effects_zero",
                    not status["real_action_execution_active"],
                ),
            ]
        )

        failed = [
            name for name, passed in assertions if not passed
        ]
        payload = {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "identity": identity,
            "runtime": status,
            "foundation": inspection,
        }

        if failed:
            raise OrionAgentFoundationError(
                "ORION agent foundation self-test failed: "
                + ", ".join(failed)
            )

        return payload
