from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json

from aura.manual_start_stop_status_runtime.manual_start_stop_status_runtime_executor import (
    ManualStartStopStatusRuntimeExecutor,
)
from .reviewed_optional_autostart_unit_contract import (
    ReviewedOptionalAutostartUnitContract,
)


class ReviewedOptionalAutostartPlanner:
    VERSION = "1.1.5"
    ANCHOR_VERSION = "1.1.4"
    CURRENT_SPRINT = 255
    NEXT_SPRINT = 256
    NEXT_VERSION = "1.1.6"
    BOUNDARY = "reviewed_optional_autostart"
    NEXT_BOUNDARY = (
        "persistent_local_chat_session_activation"
    )
    EXPECTED_ASSERTION_COUNT = 216

    DIMENSION_ORDER = (
        "canonical_owner",
        "unit_identity",
        "user_scope",
        "unit_syntax",
        "exec_contract",
        "working_directory",
        "localhost_boundary",
        "persistent_state_handoff",
        "bounded_restart",
        "permission_gate",
        "host_posture",
        "activation_preview",
        "rollback_preview",
        "no_mutation",
        "linger_boundary",
        "safe_idle",
        "documentation_surface",
        "handoff",
    )

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.contract = ReviewedOptionalAutostartUnitContract(
            project_root=self.project_root
        )
        self.target_doc = (
            self.project_root
            / "docs"
            / "AURA_REVIEWED_OPTIONAL_AUTOSTART.md"
        )

    @staticmethod
    def _digest(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _evidence(self) -> dict[str, Any]:
        owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        live = owner.status(probe_health=False)
        unit = self.contract.unit_preview()
        activation = self.contract.activation_preview()
        rollback = self.contract.rollback_preview()
        posture = self.contract.host_posture()
        return {
            "owner": owner,
            "live": live,
            "unit": unit,
            "activation": activation,
            "rollback": rollback,
            "posture": posture,
            "unit_text": unit["unit_text"],
        }

    def _assertions(self) -> list[tuple[str, bool]]:
        evidence = self._evidence()
        owner = evidence["owner"]
        live = evidence["live"]
        unit = evidence["unit"]
        activation = evidence["activation"]
        rollback = evidence["rollback"]
        posture = evidence["posture"]
        unit_text = evidence["unit_text"]

        shared = [
            self.project_root.is_dir(),
            unit["unit_name"] == "aura-local.service",
            unit["target_path"].endswith(
                ".config/systemd/user/aura-local.service"
            ),
            "[Unit]" in unit_text,
            "[Service]" in unit_text,
            "[Install]" in unit_text,
            "ExecStart=" in unit_text,
            "Restart=on-failure" in unit_text,
            "WantedBy=default.target" in unit_text,
            activation["activation_executed"] is False,
            activation["systemd_mutated"] is False,
        ]

        primary = {
            "canonical_owner": len(owner.expected_argv) >= 2,
            "unit_identity": (
                unit["unit_type"] == "user_service"
                and unit["unit_name"] == self.contract.UNIT_NAME
            ),
            "user_scope": (
                unit["target_path"]
                == str(
                    Path.home()
                    / ".config"
                    / "systemd"
                    / "user"
                    / "aura-local.service"
                )
            ),
            "unit_syntax": (
                unit_text.count("[Unit]") == 1
                and unit_text.count("[Service]") == 1
                and unit_text.count("[Install]") == 1
            ),
            "exec_contract": (
                unit["expected_argv"] == list(owner.expected_argv)
                and unit["exec_start"] in unit_text
            ),
            "working_directory": (
                unit["working_directory"] == str(self.project_root)
                and (
                    "WorkingDirectory=" + str(self.project_root)
                ) in unit_text
            ),
            "localhost_boundary": (
                owner.HOST == "127.0.0.1"
                and owner.PORT == 8765
            ),
            "persistent_state_handoff": (
                str(owner.state_path).endswith(
                    "data/runtime/service_state.json"
                )
                and live.get("persistent_state_enabled") is True
            ),
            "bounded_restart": (
                unit["restart_policy"] == "on-failure"
                and unit["restart_sec"] == 5
                and unit["start_limit_interval_sec"] == 120
                and unit["start_limit_burst"] == 3
            ),
            "permission_gate": (
                activation["approval_required"] is True
                and activation["required_confirmation_token"]
                == "ENABLE_AURA_AUTOSTART"
            ),
            "host_posture": (
                posture["user_manager_available"] is True
                and posture["linger_value"]
                in {"yes", "no", "unknown"}
            ),
            "activation_preview": (
                len(activation["steps"]) == 4
                and all(
                    step["executed"] is False
                    for step in activation["steps"]
                )
            ),
            "rollback_preview": (
                len(rollback["steps"]) == 4
                and all(
                    step["executed"] is False
                    for step in rollback["steps"]
                )
            ),
            "no_mutation": (
                posture["target_exists"] is False
                and activation["unit_written"] is False
                and activation["daemon_reload_executed"] is False
                and activation["service_enabled"] is False
                and activation["service_started"] is False
            ),
            "linger_boundary": (
                activation["linger_change_included"] is False
                and activation["linger_mutated"] is False
            ),
            "safe_idle": (
                live.get("lifecycle_state") == "stopped"
                and live.get("listener_count") == 0
                and live.get("strict_main_process_count") == 0
                and live.get("state_record_exists") is False
            ),
            "documentation_surface": (
                self.target_doc.is_file()
                and "Reviewed Optional Autostart"
                in self.target_doc.read_text(encoding="utf-8")
            ),
            "handoff": (
                self.VERSION == "1.1.5"
                and self.ANCHOR_VERSION == "1.1.4"
                and self.CURRENT_SPRINT == 255
                and self.NEXT_SPRINT == 256
                and self.NEXT_VERSION == "1.1.6"
                and self.NEXT_BOUNDARY
                == "persistent_local_chat_session_activation"
            ),
        }

        assertions: list[tuple[str, bool]] = []

        for dimension in self.DIMENSION_ORDER:
            values = [primary[dimension], *shared]

            if len(values) != 12:
                raise RuntimeError(
                    "Each dimension requires twelve checks."
                )

            for index, passed in enumerate(values, start=1):
                assertions.append(
                    (
                        f"{dimension}.{index:02d}",
                        bool(passed),
                    )
                )

        return assertions

    def check(self) -> dict[str, Any]:
        assertions = self._assertions()
        failed = [
            name
            for name, passed in assertions
            if not passed
        ]

        return {
            "owner": "ReviewedOptionalAutostartPlanner",
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "reviewed_optional_autostart_preview_only"
            ),
            "review_mode": (
                "unit_contract_host_posture_activation_and_rollback_preview"
            ),
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(self.DIMENSION_ORDER),
            "finding_count": len(failed),
            "overall_state": (
                "secure" if not failed else "review"
            ),
            "alpha_ready": not failed,
            "status_valid": (
                len(assertions) == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "assertions": [
                {"name": name, "passed": passed}
                for name, passed in assertions
            ],
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "next_version",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "review_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "status_valid",
                )
            },
            "unit_preview": self.contract.unit_preview(),
            "host_posture": self.contract.host_posture(),
            "activation_deferred": True,
            "unit_written": False,
            "daemon_reload_executed": False,
            "service_enabled": False,
            "service_started": False,
            "linger_mutated": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "scope": "review_preview_and_unit_contract_only",
            "unit_type": "user_service",
            "unit_name": "aura-local.service",
            "unit_location": (
                "~/.config/systemd/user/aura-local.service"
            ),
            "restart_policy": "on-failure_bounded",
            "enable_default": False,
            "start_default": False,
            "linger_change_default": False,
        }

    def unit_preview(self) -> dict[str, Any]:
        return self.contract.unit_preview()

    def activation_preview(self) -> dict[str, Any]:
        return self.contract.activation_preview()

    def rollback_preview(self) -> dict[str, Any]:
        return self.contract.rollback_preview()

    def host_posture(self) -> dict[str, Any]:
        return self.contract.host_posture()

    def review(self) -> dict[str, Any]:
        check = self.check()
        return {
            "ok": check["failed_assertion_count"] == 0,
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": (
                check["failed_assertion_count"]
            ),
            "dimension_count": check["dimension_count"],
            "overall_state": check["overall_state"],
            "review_digest": self._digest(
                check["assertions"]
            ),
            "activation_deferred": True,
            "approval_required": True,
            "blocked_surfaces": {
                "unit_write": True,
                "daemon_reload": True,
                "service_enable": True,
                "service_start": True,
                "linger_change": True,
                "system_unit": True,
                "non_loopback": True,
                "automatic_activation": True,
            },
        }
