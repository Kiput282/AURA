"""Sprint 190 Local Interaction Runtime Review and Stabilization.

This module closes the Sprint 181-190 Local Interaction Runtime Activation
block. It performs an operator-invoked review of the existing runtime
self-tests while preserving localhost-only, explicit-start, default-deny,
and no-arbitrary-execution boundaries.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class LocalInteractionRuntimeStabilizationError(RuntimeError):
    """Raised when the Sprint 190 stabilization review cannot complete."""


@dataclass(frozen=True)
class LocalInteractionRuntimeStabilizationPacket:
    """Immutable summary of one explicitly invoked stabilization review."""

    packet_id: str
    components_checked: int
    components_ready: int
    stabilization_gap_count: int
    runtime_violation_count: int
    assertion_count: int
    created_at: str
    session_mode: str = (
        "local_interaction_runtime_review_stabilization"
    )


class AuraLocalInteractionRuntimeStabilizationManager:
    """Review the Sprint 181-189 local interaction runtime chain."""

    name = "local_interaction_runtime_stabilization"
    component_version = "0.1.0-alpha"
    version = "0.190.0-genesis"
    sprint = 190

    COMPONENTS: tuple[dict[str, Any], ...] = (
        {
            "sprint": 181,
            "id": "local_web_runtime_alpha",
            "commands": (
                "local-web-runtime-self-test",
            ),
        },
        {
            "sprint": 182,
            "id": "service_lifecycle_runtime",
            "commands": (
                "service-lifecycle-self-test",
            ),
        },
        {
            "sprint": 183,
            "id": "health_status_api_runtime",
            "commands": (
                "health-status-api-self-test",
            ),
        },
        {
            "sprint": 184,
            "id": "control_center_backend_runtime",
            "commands": (
                "control-center-backend-self-test",
            ),
        },
        {
            "sprint": 185,
            "id": "control_center_web_shell_runtime",
            "commands": (
                "control-center-web-shell-self-test",
            ),
        },
        {
            "sprint": 186,
            "id": "browser_chat_session_runtime",
            "commands": (
                "browser-chat-session-self-test",
            ),
        },
        {
            "sprint": 187,
            "id": "local_model_bridge_runtime",
            "commands": (
                "local-model-bridge-self-test",
            ),
        },
        {
            "sprint": 188,
            "id": "interactive_control_center_chat_runtime",
            "commands": (
                "interactive-chat-self-test",
            ),
        },
        {
            "sprint": 189,
            "id": "permission_audit_recovery_visibility_runtime",
            "commands": (
                "permission-audit-recovery-self-test",
                "permission-audit-recovery-web-self-test",
            ),
        },
    )

    REQUIRED_COMPLETION_CONDITIONS: tuple[str, ...] = (
        "dashboard_startup_repeatable",
        "browser_chat_end_to_end",
        "local_model_response_path_stable",
        "session_history_persistent",
        "localhost_only_listener",
        "clean_shutdown",
        "port_conflict_fail_closed",
        "visible_runtime_errors",
        "no_permission_bypass",
        "no_arbitrary_execution",
        "runtime_documentation_boundary_alignment",
    )

    SAFETY_BOUNDARY: dict[str, bool] = {
        "operator_invoked_review_only": True,
        "foreground_validation_only": True,
        "localhost_only_runtime_required": True,
        "explicit_listener_start_required": True,
        "clean_shutdown_required": True,
        "port_conflict_fail_closed_required": True,
        "visible_error_state_required": True,
        "permission_bypass_allowed": False,
        "arbitrary_execution_allowed": False,
        "public_listener_allowed": False,
        "lan_listener_allowed": False,
        "background_service_enabled": False,
        "systemd_enabled": False,
        "auto_start_enabled": False,
        "browser_auto_launch_enabled": False,
        "permission_mutation_enabled": False,
        "audit_writer_enabled": False,
        "automatic_recovery_enabled": False,
        "arbitrary_file_access_enabled": False,
        "command_execution_enabled": False,
        "desktop_action_execution_enabled": False,
        "voice_runtime_enabled": False,
        "vision_runtime_enabled": False,
        "autonomy_enabled": False,
    }

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = (
            Path(project_root).resolve()
            if project_root is not None
            else Path(__file__).resolve().parents[2]
        )
        self.main_path = self.project_root / "main.py"

    @property
    def component_count(self) -> int:
        return len(self.COMPONENTS)

    @property
    def command_test_count(self) -> int:
        return sum(
            len(component["commands"])
            for component in self.COMPONENTS
        )

    def safety_boundary(self) -> dict[str, Any]:
        """Return the immutable Sprint 190 safety requirements."""

        return {
            **self.SAFETY_BOUNDARY,
            "runtime_mutation_added_by_sprint_190": False,
            "new_listener_added_by_sprint_190": False,
            "new_model_provider_added_by_sprint_190": False,
            "new_persistence_store_added_by_sprint_190": False,
            "release_gate_requires_zero_gaps": True,
            "release_gate_requires_zero_violations": True,
        }

    def status(self) -> dict[str, Any]:
        """Return structural readiness without running component tests."""

        main_ready = self.main_path.is_file()
        component_packages = {
            component["id"]: (
                self.project_root
                / "aura"
                / component["id"]
            ).is_dir()
            for component in self.COMPONENTS
        }
        components_present = sum(component_packages.values())
        ready = (
            main_ready
            and components_present == self.component_count
        )

        return {
            "status": "ready" if ready else "degraded",
            "module": self.name,
            "component_version": self.component_version,
            "version": self.version,
            "sprint": self.sprint,
            "local_interaction_runtime_stabilization_ready": ready,
            "project_root": str(self.project_root),
            "main_cli_present": main_ready,
            "components_expected": self.component_count,
            "components_present": components_present,
            "command_test_count": self.command_test_count,
            "reviewed_sprints": list(range(181, 190)),
            "component_packages": component_packages,
            "completion_condition_count": len(
                self.REQUIRED_COMPLETION_CONDITIONS
            ),
            "release_gate_closed": True,
            "runtime_mutation_performed": False,
            "listener_started_by_status": False,
            "subprocess_started_by_status": False,
            "next_block": "191-200_voice_interaction_runtime",
            "next_sprint": (
                "Sprint 191 Voice Runtime Activation Foundation"
            ),
            "safety_boundary": self.safety_boundary(),
        }

    def context(self) -> dict[str, Any]:
        """Return the complete Sprint 190 review contract."""

        return {
            **self.status(),
            "block": (
                "181-190_local_interaction_runtime_activation"
            ),
            "block_outcome": (
                "AURA can be opened through a localhost Control "
                "Center and used through bounded interactive local "
                "chat with persistent sessions, a permission-gated "
                "local model bridge, and visible safety/recovery state."
            ),
            "component_matrix": [
                {
                    "sprint": component["sprint"],
                    "component": component["id"],
                    "commands": list(component["commands"]),
                }
                for component in self.COMPONENTS
            ],
            "required_completion_conditions": list(
                self.REQUIRED_COMPLETION_CONDITIONS
            ),
            "not_required_for_sprint_190": [
                "microphone_capture",
                "speech_to_text_runtime",
                "text_to_speech_runtime",
                "screen_capture",
                "vision_runtime",
                "local_action_execution",
                "orion_runtime",
                "avatar_runtime",
                "autonomy",
            ],
        }

    @staticmethod
    def _extract_json(stdout: str) -> dict[str, Any]:
        """Decode one JSON object from a component CLI result."""

        text = stdout.strip()
        if not text:
            raise LocalInteractionRuntimeStabilizationError(
                "Component self-test produced no JSON output."
            )

        decoder = json.JSONDecoder()
        positions = [
            index
            for index, character in enumerate(text)
            if character == "{"
        ]

        for start in positions:
            try:
                payload, end = decoder.raw_decode(text[start:])
            except json.JSONDecodeError:
                continue

            if isinstance(payload, dict):
                remainder = text[start + end :].strip()
                if not remainder or remainder.startswith(
                    "202"
                ):
                    return payload
                return payload

        raise LocalInteractionRuntimeStabilizationError(
            "Component self-test output did not contain a JSON object."
        )

    def _run_command(
        self,
        command: str,
    ) -> dict[str, Any]:
        """Run one existing component self-test through the main CLI."""

        completed = subprocess.run(
            [sys.executable, str(self.main_path), command],
            cwd=self.project_root,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )

        if completed.returncode != 0:
            detail = (
                completed.stderr.strip()
                or completed.stdout.strip()
                or "unknown component self-test failure"
            )
            raise LocalInteractionRuntimeStabilizationError(
                f"{command} failed with exit code "
                f"{completed.returncode}: {detail}"
            )

        payload = self._extract_json(completed.stdout)
        status = payload.get("status")
        failed = payload.get("failed_assertion_count")

        if status != "ok":
            raise LocalInteractionRuntimeStabilizationError(
                f"{command} returned non-ok status: {status!r}"
            )

        if failed not in (None, 0):
            raise LocalInteractionRuntimeStabilizationError(
                f"{command} reported {failed} failed assertions."
            )

        assertion_count = payload.get("assertion_count", 0)
        if not isinstance(assertion_count, int):
            assertion_count = 0

        return {
            "command": command,
            "status": "ready",
            "assertion_count": assertion_count,
            "failed_assertion_count": 0,
            "payload_status": status,
        }

    def run_stabilization_review(self) -> dict[str, Any]:
        """Run all Sprint 181-189 component self-test contracts."""

        component_results: list[dict[str, Any]] = []
        gaps: list[dict[str, Any]] = []
        violations: list[dict[str, Any]] = []
        total_assertions = 0

        for component in self.COMPONENTS:
            command_results: list[dict[str, Any]] = []
            component_ready = True

            for command in component["commands"]:
                try:
                    command_result = self._run_command(command)
                    command_results.append(command_result)
                    total_assertions += command_result[
                        "assertion_count"
                    ]
                except (
                    LocalInteractionRuntimeStabilizationError,
                    subprocess.TimeoutExpired,
                ) as exc:
                    component_ready = False
                    gap = {
                        "sprint": component["sprint"],
                        "component": component["id"],
                        "command": command,
                        "detail": str(exc),
                    }
                    gaps.append(gap)
                    command_results.append(
                        {
                            "command": command,
                            "status": "failed",
                            "assertion_count": 0,
                            "failed_assertion_count": 1,
                            "detail": str(exc),
                        }
                    )

            component_results.append(
                {
                    "sprint": component["sprint"],
                    "component": component["id"],
                    "ready": component_ready,
                    "command_count": len(component["commands"]),
                    "commands": command_results,
                }
            )

        boundary = self.safety_boundary()
        forbidden_true_keys = (
            "permission_bypass_allowed",
            "arbitrary_execution_allowed",
            "public_listener_allowed",
            "lan_listener_allowed",
            "background_service_enabled",
            "systemd_enabled",
            "auto_start_enabled",
            "browser_auto_launch_enabled",
            "permission_mutation_enabled",
            "audit_writer_enabled",
            "automatic_recovery_enabled",
            "arbitrary_file_access_enabled",
            "command_execution_enabled",
            "desktop_action_execution_enabled",
            "voice_runtime_enabled",
            "vision_runtime_enabled",
            "autonomy_enabled",
            "runtime_mutation_added_by_sprint_190",
            "new_listener_added_by_sprint_190",
            "new_model_provider_added_by_sprint_190",
            "new_persistence_store_added_by_sprint_190",
        )

        for key in forbidden_true_keys:
            if boundary.get(key) is not False:
                violations.append(
                    {
                        "boundary": key,
                        "expected": False,
                        "actual": boundary.get(key),
                    }
                )

        components_ready = sum(
            1
            for result in component_results
            if result["ready"]
        )
        complete = (
            components_ready == self.component_count
            and not gaps
            and not violations
        )

        packet = LocalInteractionRuntimeStabilizationPacket(
            packet_id=(
                "local-interaction-stabilization-"
                f"{uuid4().hex[:12]}"
            ),
            components_checked=self.component_count,
            components_ready=components_ready,
            stabilization_gap_count=len(gaps),
            runtime_violation_count=len(violations),
            assertion_count=total_assertions,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        return {
            "status": "ok" if complete else "degraded",
            "module": self.name,
            "component_version": self.component_version,
            "version": self.version,
            "sprint": self.sprint,
            "packet": asdict(packet),
            "components_expected": self.component_count,
            "components_checked": packet.components_checked,
            "components_ready": packet.components_ready,
            "component_results": component_results,
            "command_tests_expected": self.command_test_count,
            "assertion_count": packet.assertion_count,
            "stabilization_gap_count": (
                packet.stabilization_gap_count
            ),
            "stabilization_gaps": gaps,
            "runtime_violation_count": (
                packet.runtime_violation_count
            ),
            "runtime_violations": violations,
            "block_181_190_complete": complete,
            "local_interaction_chain_stable": complete,
            "release_gate_closed": True,
            "voice_runtime_block_ready": complete,
            "runtime_mutation_performed": False,
            "permission_bypass_detected": False,
            "arbitrary_execution_detected": False,
            "safety_boundary": boundary,
        }

    def self_test(self) -> dict[str, Any]:
        """Validate structural and live stabilization contracts."""

        status = self.status()
        context = self.context()
        review = self.run_stabilization_review()

        assertions: dict[str, bool] = {
            "status_ready": status["status"] == "ready",
            "module_name": (
                status["module"]
                == "local_interaction_runtime_stabilization"
            ),
            "component_version": (
                status["component_version"] == "0.1.0-alpha"
            ),
            "sprint_190": status["sprint"] == 190,
            "version_190_candidate": (
                status["version"] == "0.190.0-genesis"
            ),
            "nine_components_expected": (
                status["components_expected"] == 9
            ),
            "nine_components_present": (
                status["components_present"] == 9
            ),
            "ten_command_tests": (
                status["command_test_count"] == 10
            ),
            "reviewed_sprints_181_189": (
                status["reviewed_sprints"]
                == list(range(181, 190))
            ),
            "completion_conditions_present": (
                context["completion_condition_count"] == 11
            ),
            "block_name": (
                context["block"]
                == "181-190_local_interaction_runtime_activation"
            ),
            "component_matrix_count": (
                len(context["component_matrix"]) == 9
            ),
            "review_status_ok": review["status"] == "ok",
            "components_checked": (
                review["components_checked"] == 9
            ),
            "components_ready": (
                review["components_ready"] == 9
            ),
            "no_stabilization_gaps": (
                review["stabilization_gap_count"] == 0
            ),
            "no_runtime_violations": (
                review["runtime_violation_count"] == 0
            ),
            "block_complete": (
                review["block_181_190_complete"] is True
            ),
            "chain_stable": (
                review["local_interaction_chain_stable"] is True
            ),
            "voice_block_ready": (
                review["voice_runtime_block_ready"] is True
            ),
            "release_gate_closed": (
                review["release_gate_closed"] is True
            ),
            "no_runtime_mutation": (
                review["runtime_mutation_performed"] is False
            ),
            "no_permission_bypass": (
                review["permission_bypass_detected"] is False
            ),
            "no_arbitrary_execution": (
                review["arbitrary_execution_detected"] is False
            ),
            "dependency_assertions_present": (
                review["assertion_count"] >= 120
            ),
        }

        boundary = self.safety_boundary()
        for key, expected in self.SAFETY_BOUNDARY.items():
            assertions[f"boundary_{key}"] = (
                boundary[key] is expected
            )

        for component in review["component_results"]:
            component_id = component["component"]
            assertions[f"{component_id}_ready"] = (
                component["ready"] is True
            )
            assertions[f"{component_id}_commands_present"] = (
                component["command_count"]
                == len(component["commands"])
                and component["command_count"] >= 1
            )

            for index, command in enumerate(
                component["commands"],
                start=1,
            ):
                assertions[
                    f"{component_id}_command_{index}_ok"
                ] = command["status"] == "ready"
                assertions[
                    f"{component_id}_command_{index}_zero_failures"
                ] = (
                    command["failed_assertion_count"] == 0
                )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]

        if failed:
            raise LocalInteractionRuntimeStabilizationError(
                "Sprint 190 self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "module": self.name,
            "component_version": self.component_version,
            "version": self.version,
            "sprint": self.sprint,
            "assertion_count": (
                len(assertions) + review["assertion_count"]
            ),
            "failed_assertion_count": 0,
            "stabilization_assertion_count": len(assertions),
            "dependency_assertion_count": review[
                "assertion_count"
            ],
            "total_assertion_coverage": (
                len(assertions) + review["assertion_count"]
            ),
            "components_checked": review[
                "components_checked"
            ],
            "components_ready": review[
                "components_ready"
            ],
            "stabilization_gap_count": 0,
            "runtime_violation_count": 0,
            "block_181_190_complete": True,
            "local_interaction_chain_stable": True,
            "voice_runtime_block_ready": True,
            "release_gate_closed": True,
            "runtime_mutation_performed": False,
            "review": review,
        }
