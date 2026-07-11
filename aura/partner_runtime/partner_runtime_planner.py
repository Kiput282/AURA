"""Sprint 221 Unified Session Runtime contract.

Read-only integration over the existing partner planner and browser session
owner. No session, memory, permission, action, device, service, or release
runtime is activated here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.browser_chat_session_runtime import AuraBrowserChatSessionRuntimeManager
from aura.partner_runtime.partner_runtime_planning_manager import (
    PartnerRuntimePlanningManager,
)


class PartnerRuntimePlanner:
    """Contract planner for Sprint 221 Unified Session Runtime."""

    name = "partner_runtime"
    version = "0.1.0"
    block_start = 221
    block_end = 230
    current_sprint = 221
    next_sprint = 222
    next_boundary = "workspace_project_context_runtime"

    DEFERRED_BOUNDARIES = (
        (222, "workspace_project_context_runtime"),
        (223, "chat_to_memory_runtime_handoff"),
        (224, "voice_vision_chat_context_fusion"),
        (225, "personality_consistency_runtime"),
        (226, "multi_interface_state_synchronization"),
        (227, "service_persistence_launcher"),
        (228, "safe_auto_start_evaluation"),
        (229, "genesis_acceptance_rehearsal"),
        (230, "unified_partner_runtime_stabilization"),
    )
    SAFETY_BLOCKERS = (
        "unified_session_runtime_active",
        "workspace_project_context_runtime_active",
        "chat_to_memory_handoff_runtime_active",
        "context_fusion_runtime_active",
        "memory_write_active",
        "voice_listen_active",
        "microphone_capture_active",
        "vision_capture_active",
        "screen_capture_active",
        "permission_mutation_active",
        "audit_write_active",
        "action_execution_active",
        "tool_execution_active",
        "command_execution_active",
        "file_mutation_active",
        "desktop_control_active",
        "network_action_active",
        "git_action_active",
        "background_service_active",
        "browser_auto_launch_active",
        "public_listener_active",
        "lan_listener_active",
        "release_gate_open",
        "autonomous_action_active",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        session_manager: AuraBrowserChatSessionRuntimeManager | None = None,
        legacy_planner: PartnerRuntimePlanningManager | None = None,
    ) -> None:
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.session_manager = session_manager or AuraBrowserChatSessionRuntimeManager(
            project_root=self.project_root
        )
        self.legacy_planner = legacy_planner or PartnerRuntimePlanningManager(
            project_root=self.project_root
        )

    def _legacy_snapshot(self) -> dict[str, Any]:
        """Inspect the legacy planner without traversing its dependency graph."""
        try:
            boundary = self.legacy_planner.safety_boundary()
        except Exception as exc:  # pragma: no cover - defensive boundary
            return {
                "available": False,
                "planner_ready": False,
                "runtime_ready": False,
                "execution_ready": False,
                "snapshot_mode": "static_safety_boundary",
                "dependency_status_called": False,
                "integration_context_called": False,
                "journal_accessed": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

        planner_ready = (
            boundary.get("planner_only") is True
            and boundary.get("proposal_only") is True
            and boundary.get("metadata_only") is True
        )
        return {
            "available": True,
            "name": getattr(self.legacy_planner, "name", None),
            "version": getattr(self.legacy_planner, "version", None),
            "status": getattr(self.legacy_planner, "status_name", None),
            "planner_ready": planner_ready,
            "runtime_ready": boundary.get("runtime_ready") is True,
            "execution_ready": boundary.get("execution_ready") is True,
            "planner_only": boundary.get("planner_only") is True,
            "proposal_only": boundary.get("proposal_only") is True,
            "metadata_only": boundary.get("metadata_only") is True,
            "snapshot_mode": "static_safety_boundary",
            "dependency_status_called": False,
            "integration_context_called": False,
            "journal_accessed": False,
            "error": None,
        }

    def _session_snapshot(self) -> dict[str, Any]:
        """Inspect canonical session metadata without reading payloads."""

        try:
            snapshot = (
                self.session_manager
                .contract_snapshot()
            )
            boundary = snapshot.get(
                "safety_boundary",
                {},
            )

        except Exception as exc:  # pragma: no cover - defensive boundary
            return {
                "available": False,
                "degraded": True,
                "session_count": 0,
                "total_message_count": 0,
                "error_count": 1,
                "errors": [
                    f"{type(exc).__name__}: {exc}"
                ],
                "session_metrics_available": False,
                "session_metrics_inspected": False,
                "session_payloads_read": 0,
                "inspection_read_only": True,
                "metadata_only": True,
                "safety_boundary": {},
            }

        return {
            "available": True,
            "name": snapshot.get("name"),
            "component_version":
                snapshot.get(
                    "component_version"
                ),
            "source_sprint":
                snapshot.get("sprint"),
            "schema_version":
                snapshot.get(
                    "schema_version"
                ),
            "status": snapshot.get("status"),
            "degraded":
                snapshot.get("degraded")
                is True,
            "storage_path":
                snapshot.get(
                    "storage_path"
                ),
            "storage_exists":
                snapshot.get(
                    "storage_exists"
                )
                is True,
            "session_count":
                int(
                    snapshot.get(
                        "session_count",
                        0,
                    )
                ),
            "total_message_count":
                int(
                    snapshot.get(
                        "total_message_count",
                        0,
                    )
                ),
            "error_count":
                int(
                    snapshot.get(
                        "error_count",
                        0,
                    )
                ),
            "errors":
                list(
                    snapshot.get(
                        "errors",
                        [],
                    )
                ),
            "session_metrics_available":
                snapshot.get(
                    "session_metrics_available"
                )
                is True,
            "session_metrics_inspected":
                snapshot.get(
                    "session_metrics_inspected"
                )
                is True,
            "session_payloads_read":
                int(
                    snapshot.get(
                        "session_payloads_read",
                        0,
                    )
                ),
            "inspection_read_only": True,
            "metadata_only":
                snapshot.get(
                    "metadata_only"
                )
                is True,
            "session_id_pattern":
                self.session_manager
                ._SESSION_ID_RE.pattern,
            "message_id_pattern":
                self.session_manager
                ._MESSAGE_ID_RE.pattern,
            "client_message_id_pattern": (
                self.session_manager
                ._CLIENT_MESSAGE_ID_RE.pattern
            ),
            "safety_boundary": boundary,
        }


    def unified_session_runtime_contract(self) -> dict[str, Any]:
        legacy = self._legacy_snapshot()
        session = self._session_snapshot()
        boundary = session.get("safety_boundary", {})
        session_checks = {
            "owner": session.get("name") == "aura_browser_chat_session_runtime",
            "source_sprint": session.get("source_sprint") == 186,
            "schema": session.get("schema_version") == "1.0",
            "session_id": session.get("session_id_pattern")
            == r"^chat_[0-9a-f]{32}$",
            "message_id": session.get("message_id_pattern")
            == r"^msg_[0-9a-f]{32}$",
            "client_message_id": session.get("client_message_id_pattern")
            == r"^client_[A-Za-z0-9_-]{1,64}$",
            "revision": boundary.get("optimistic_revision_control") is True,
            "atomic_write": boundary.get("atomic_session_writes") is True,
            "integrity": boundary.get("session_integrity_hash") is True,
            "safe_idle": boundary.get("safe_idle") is True,
        }
        session_ready = session.get("available") is True and all(
            session_checks.values()
        )
        legacy_ready = (
            legacy.get("available") is True
            and legacy.get("planner_ready") is True
            and legacy.get("runtime_ready") is False
            and legacy.get("execution_ready") is False
        )
        ready = session_ready and legacy_ready

        contract: dict[str, Any] = {
            "sprint": self.current_sprint,
            "name": self.name,
            "unified_session_runtime_contract_ready": ready,
            "unified_session_runtime_ready": False,
            "unified_session_runtime_status": (
                "unified_session_runtime_contract_ready"
                if ready
                else "unified_session_runtime_contract_degraded"
            ),
            "partner_runtime_block_start": self.block_start,
            "partner_runtime_block_end": self.block_end,
            "partner_runtime_current_sprint": self.current_sprint,
            "partner_runtime_next_sprint": self.next_sprint,
            "partner_runtime_next_boundary": self.next_boundary,
            "contract_only": True,
            "planning_ready": ready,
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "canonical_session_owner": "aura_browser_chat_session_runtime",
            "canonical_session_contract_ready": session_ready,
            "canonical_session_contract_checks": session_checks,
            "canonical_session_storage_reused": True,
            "duplicate_session_storage_created": False,
            "duplicate_session_id_schema_created": False,
            "session_created": False,
            "message_submitted": False,
            "session_cleared": False,
            "legacy_partner_planner_contract_ready": legacy_ready,
            "legacy_partner_planner_preserved": True,
            "legacy_partner_planner_promoted_to_executor": False,
            "session_status_snapshot_read_only": True,
            "session_snapshot": session,
            "legacy_partner_snapshot": legacy,
            "deferred_boundaries": [
                {"sprint": sprint, "boundary": name}
                for sprint, name in self.DEFERRED_BOUNDARIES
            ],
            "workspace_project_context_deferred_to_sprint_222": True,
            "chat_to_memory_handoff_deferred_to_sprint_223": True,
            "context_fusion_deferred_to_sprint_224": True,
            "permission_before_action_preserved": True,
            "permission_before_memory_write_preserved": True,
            "localhost_only_boundary_preserved": True,
            "safe_idle_preserved": True,
            "runtime_scope": "unified_session_runtime_contract_only",
            "safety_blockers": list(self.SAFETY_BLOCKERS),
            "safety_blocker_count": len(self.SAFETY_BLOCKERS),
        }
        contract.update({name: False for name in self.SAFETY_BLOCKERS})
        contract["all_safety_blockers_inactive"] = all(
            contract[name] is False for name in self.SAFETY_BLOCKERS
        )
        return contract

    def status(self) -> dict[str, Any]:
        contract = self.unified_session_runtime_contract()
        session = contract["session_snapshot"]
        return {
            "name": self.name,
            "version": self.version,
            "status": "planning",
            "planning_ready": contract["planning_ready"],
            "runtime_ready": False,
            "unified_session_runtime_contract_ready": contract[
                "unified_session_runtime_contract_ready"
            ],
            "unified_session_runtime_status": contract[
                "unified_session_runtime_status"
            ],
            "partner_runtime_current_sprint": self.current_sprint,
            "partner_runtime_next_sprint": self.next_sprint,
            "partner_runtime_next_boundary": self.next_boundary,
            "canonical_session_owner": contract["canonical_session_owner"],
            "session_count": session["session_count"],
            "total_message_count": session["total_message_count"],
            "session_source_degraded": session["degraded"],
            "all_safety_blockers_inactive": contract[
                "all_safety_blockers_inactive"
            ],
            "runtime_scope": contract["runtime_scope"],
            "contract": contract,
        }

    def context(self) -> dict[str, Any]:
        contract = self.unified_session_runtime_contract()
        return {
            "name": self.name,
            "version": self.version,
            "status": contract["unified_session_runtime_status"],
            "current_sprint": self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "canonical_session_owner": contract["canonical_session_owner"],
            "session_snapshot": contract["session_snapshot"],
            "legacy_partner_snapshot": contract["legacy_partner_snapshot"],
            "contract_only": True,
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        contract = self.unified_session_runtime_contract()
        assertions = {
            "contract_ready": contract[
                "unified_session_runtime_contract_ready"
            ] is True,
            "runtime_disabled": contract["runtime_ready"] is False,
            "activation_blocked": contract["runtime_activation_allowed"] is False,
            "release_gate_closed": contract["release_gate_open"] is False,
            "current_sprint_221": contract[
                "partner_runtime_current_sprint"
            ] == 221,
            "next_sprint_222": contract["partner_runtime_next_sprint"] == 222,
            "next_boundary_correct": contract[
                "partner_runtime_next_boundary"
            ] == "workspace_project_context_runtime",
            "canonical_owner_preserved": contract[
                "canonical_session_owner"
            ] == "aura_browser_chat_session_runtime",
            "canonical_contract_ready": contract[
                "canonical_session_contract_ready"
            ] is True,
            "canonical_storage_reused": contract[
                "canonical_session_storage_reused"
            ] is True,
            "no_duplicate_storage": contract[
                "duplicate_session_storage_created"
            ] is False,
            "no_duplicate_id_schema": contract[
                "duplicate_session_id_schema_created"
            ] is False,
            "legacy_planner_preserved": contract[
                "legacy_partner_planner_preserved"
            ] is True,
            "legacy_planner_not_executor": contract[
                "legacy_partner_planner_promoted_to_executor"
            ] is False,
            "snapshot_read_only": contract[
                "session_status_snapshot_read_only"
            ] is True,
            "no_session_created": contract["session_created"] is False,
            "no_message_submitted": contract["message_submitted"] is False,
            "no_session_cleared": contract["session_cleared"] is False,
            "workspace_deferred": contract[
                "workspace_project_context_deferred_to_sprint_222"
            ] is True,
            "memory_handoff_deferred": contract[
                "chat_to_memory_handoff_deferred_to_sprint_223"
            ] is True,
            "fusion_deferred": contract[
                "context_fusion_deferred_to_sprint_224"
            ] is True,
            "permission_before_action_preserved": contract[
                "permission_before_action_preserved"
            ] is True,
            "permission_before_memory_write_preserved": contract[
                "permission_before_memory_write_preserved"
            ] is True,
            "localhost_boundary_preserved": contract[
                "localhost_only_boundary_preserved"
            ] is True,
            "safe_idle_preserved": contract["safe_idle_preserved"] is True,
            "all_safety_blockers_inactive": contract[
                "all_safety_blockers_inactive"
            ] is True,
            "runtime_scope_contract_only": contract[
                "runtime_scope"
            ] == "unified_session_runtime_contract_only",
        }
        assertions.update(
            {
                f"{name}_inactive": contract[name] is False
                for name in self.SAFETY_BLOCKERS
            }
        )
        failed = [name for name, passed in assertions.items() if not passed]
        return {
            "status": "checked",
            "planning_ready": contract["planning_ready"],
            "runtime_ready": False,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "partner_runtime_current_sprint": self.current_sprint,
            "partner_runtime_next_sprint": self.next_sprint,
            "partner_runtime_next_boundary": self.next_boundary,
            "unified_session_runtime_contract": contract,
        }

    def plan(self) -> dict[str, Any]:
        contract = self.unified_session_runtime_contract()
        return {
            "name": self.name,
            "sprint": self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "contract_ready": contract[
                "unified_session_runtime_contract_ready"
            ],
            "runtime_ready": False,
            "runtime_scope": contract["runtime_scope"],
            "canonical_session_owner": contract["canonical_session_owner"],
            "deferred_boundaries": contract["deferred_boundaries"],
        }
