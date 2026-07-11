"""Sprint 223 Chat-to-Memory Runtime Handoff contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.chat_to_memory_handoff_contract.aura_chat_to_memory_handoff_contract_manager import (
    AuraChatToMemoryHandoffContractManager,
)
from aura.memory_privacy_redaction_layer.aura_memory_privacy_redaction_layer_manager import (
    AuraMemoryPrivacyRedactionLayerManager,
)
from aura.memory_review_queue.aura_memory_review_queue_manager import (
    AuraMemoryReviewQueueManager,
)
from aura.memory_write_permission_gate.aura_memory_write_permission_gate_manager import (
    AuraMemoryWritePermissionGateManager,
)
from aura.partner_runtime.workspace_project_context_planner import (
    WorkspaceProjectContextPlanner,
)


class ChatToMemoryRuntimeHandoffPlanner:
    """Compose existing preview-only memory contracts without persistence."""

    name = "chat_to_memory_runtime_handoff"
    version = "0.1.0"
    current_sprint = 223
    next_sprint = 224
    next_boundary = "voice_vision_chat_context_fusion"

    canonical_session_owner = "aura_browser_chat_session_runtime"
    canonical_handoff_owner = (
        "aura.chat_to_memory_handoff_contract."
        "AuraChatToMemoryHandoffContractManager"
    )
    canonical_memory_store_owner = "aura.memory.memory_store.MemoryStore"
    permission_scope = "memory.write.single_candidate"

    safety_blockers = (
        "chat_to_memory_runtime_handoff_active",
        "chat_store_read_active",
        "chat_history_scan_active",
        "chat_turn_lookup_active",
        "chat_event_consumption_active",
        "memory_candidate_persist_active",
        "review_queue_persist_active",
        "review_decision_apply_active",
        "permission_request_persist_active",
        "permission_grant_apply_active",
        "permission_scope_activation_active",
        "permission_grant_consume_active",
        "memory_write_active",
        "memory_store_mutation_active",
        "memory_delete_active",
        "audit_write_active",
        "model_request_active",
        "network_action_active",
        "command_execution_active",
        "tool_execution_active",
        "file_mutation_active",
        "background_service_active",
        "release_gate_open",
        "autonomous_action_active",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        workspace_planner: WorkspaceProjectContextPlanner | None = None,
        handoff_manager: AuraChatToMemoryHandoffContractManager | None = None,
        permission_manager: AuraMemoryWritePermissionGateManager | None = None,
        review_manager: AuraMemoryReviewQueueManager | None = None,
        privacy_manager: AuraMemoryPrivacyRedactionLayerManager | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

        self.workspace_planner = (
            workspace_planner
            or WorkspaceProjectContextPlanner(
                self.project_root
            )
        )

        self.handoff_manager = (
            handoff_manager
            or AuraChatToMemoryHandoffContractManager(
                self.project_root
            )
        )

        self.permission_manager = (
            permission_manager
            or AuraMemoryWritePermissionGateManager(
                self.project_root
            )
        )

        self.review_manager = (
            review_manager
            or AuraMemoryReviewQueueManager(
                self.project_root
            )
        )

        self.privacy_manager = (
            privacy_manager
            or AuraMemoryPrivacyRedactionLayerManager(
                self.project_root
            )
        )

    @staticmethod
    def _manager_status(
        manager: object,
        *,
        owner: str,
        ready_key: str,
    ) -> dict[str, Any]:
        try:
            payload = manager.status()
        except Exception as exc:
            return {
                "owner": owner,
                "available": False,
                "ready": False,
                "ready_key": ready_key,
                "status": "error",
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
                "payload": {},
                "status_called": True,
                "context_called": False,
                "preview_method_called": False,
            }

        return {
            "owner": owner,
            "available": True,
            "ready": payload.get(ready_key) is True,
            "ready_key": ready_key,
            "status": payload.get(
                "status",
                "unknown",
            ),
            "error": None,
            "payload": payload,
            "status_called": True,
            "context_called": False,
            "preview_method_called": False,
        }

    def _workspace_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            check = self.workspace_planner.check()
        except Exception as exc:
            return {
                "contract_ready": False,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "canonical_session_owner": None,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        contract = check[
            "workspace_project_context_contract"
        ]

        return {
            "contract_ready": (
                contract[
                    "workspace_project_context_"
                    "contract_ready"
                ]
                is True
            ),
            "assertion_count":
                check["assertion_count"],
            "failed_assertion_count":
                check[
                    "failed_assertion_count"
                ],
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "error": None,
        }

    @staticmethod
    def _all_zero(
        payload: dict[str, Any],
        keys: tuple[str, ...],
    ) -> bool:
        return all(
            payload.get(key) == 0
            for key in keys
        )

    def chat_to_memory_runtime_handoff_contract(
        self,
    ) -> dict[str, Any]:
        workspace = self._workspace_snapshot()

        handoff = self._manager_status(
            self.handoff_manager,
            owner=self.canonical_handoff_owner,
            ready_key=(
                "chat_to_memory_handoff_"
                "contract_ready"
            ),
        )

        permission = self._manager_status(
            self.permission_manager,
            owner=(
                "aura.memory_write_permission_gate."
                "AuraMemoryWritePermissionGateManager"
            ),
            ready_key=(
                "memory_write_permission_gate_ready"
            ),
        )

        review = self._manager_status(
            self.review_manager,
            owner=(
                "aura.memory_review_queue."
                "AuraMemoryReviewQueueManager"
            ),
            ready_key="memory_review_queue_ready",
        )

        privacy = self._manager_status(
            self.privacy_manager,
            owner=(
                "aura.memory_privacy_redaction_layer."
                "AuraMemoryPrivacyRedactionLayerManager"
            ),
            ready_key=(
                "memory_privacy_redaction_layer_ready"
            ),
        )

        handoff_payload = handoff["payload"]
        permission_payload = permission["payload"]
        review_payload = review["payload"]
        privacy_payload = privacy["payload"]

        handoff_zero = self._all_zero(
            handoff_payload,
            (
                "runtime_chat_store_reads",
                "runtime_chat_history_scans",
                "runtime_chat_turn_lookups",
                "runtime_chat_events_consumed",
                (
                    "runtime_chat_memory_"
                    "handoffs_persisted"
                ),
                (
                    "runtime_memory_candidates_"
                    "persisted"
                ),
                (
                    "runtime_review_items_"
                    "persisted"
                ),
                (
                    "runtime_permission_requests_"
                    "persisted"
                ),
                (
                    "runtime_permission_grants_"
                    "applied"
                ),
                "runtime_memory_writes",
                "runtime_memory_store_mutations",
                "runtime_audit_events_written",
                "runtime_commands_executed",
                "runtime_tools_executed",
                "runtime_network_requests",
                "runtime_execution_features",
            ),
        )

        permission_zero = self._all_zero(
            permission_payload,
            (
                (
                    "runtime_permission_requests_"
                    "persisted"
                ),
                (
                    "runtime_permission_grants_"
                    "applied"
                ),
                "runtime_memory_writes",
                "runtime_memory_store_mutations",
                "runtime_audit_events_written",
                "runtime_commands_executed",
                "runtime_tools_executed",
                "runtime_network_requests",
                "runtime_execution_features",
            ),
        )

        privacy_zero = self._all_zero(
            privacy_payload,
            (
                (
                    "runtime_privacy_evaluations_"
                    "persisted"
                ),
                (
                    "runtime_review_items_"
                    "persisted"
                ),
                (
                    "runtime_permission_requests_"
                    "persisted"
                ),
                (
                    "runtime_permission_grants_"
                    "applied"
                ),
                "runtime_memory_writes",
                "runtime_memory_store_mutations",
                "runtime_audit_events_written",
                "runtime_commands_executed",
                "runtime_tools_executed",
                "runtime_network_requests",
                "runtime_execution_features",
            ),
        )

        ready = all(
            (
                workspace["contract_ready"],
                workspace["assertion_count"] == 52,
                (
                    workspace[
                        "failed_assertion_count"
                    ]
                    == 0
                ),
                (
                    workspace[
                        "canonical_session_owner"
                    ]
                    == self.canonical_session_owner
                ),
                handoff["ready"],
                permission["ready"],
                review["ready"],
                privacy["ready"],
                handoff_payload.get(
                    "explicit_user_memory_request_required"
                )
                is True,
                handoff_payload.get(
                    "single_user_turn_handoff_enabled"
                )
                is True,
                handoff_payload.get(
                    "manual_review_required"
                )
                is True,
                handoff_payload.get(
                    "privacy_review_required"
                )
                is True,
                handoff_payload.get(
                    "chat_store_read_disabled"
                )
                is True,
                handoff_payload.get(
                    "chat_history_scan_disabled"
                )
                is True,
                handoff_payload.get(
                    "review_queue_persist_disabled"
                )
                is True,
                handoff_payload.get(
                    "permission_grant_apply_disabled"
                )
                is True,
                handoff_payload.get(
                    "memory_write_runtime_disabled"
                )
                is True,
                handoff_payload.get(
                    "memory_store_mutation_disabled"
                )
                is True,
                permission_payload.get(
                    "explicit_user_decision_required"
                )
                is True,
                permission_payload.get(
                    "default_deny_without_grant"
                )
                is True,
                permission_payload.get(
                    "one_shot_grant_required"
                )
                is True,
                permission_payload.get(
                    "permission_expiry_required"
                )
                is True,
                review_payload.get(
                    "manual_review_required"
                )
                is True,
                review_payload.get(
                    "privacy_review_required"
                )
                is True,
                review_payload.get(
                    "review_queue_persist_disabled"
                )
                is True,
                review_payload.get(
                    "review_decision_apply_disabled"
                )
                is True,
                privacy_payload.get(
                    "privacy_review_required"
                )
                is True,
                privacy_payload.get(
                    "manual_review_required"
                )
                is True,
                privacy_payload.get(
                    "permission_required_after_"
                    "privacy_review"
                )
                is True,
                handoff_zero,
                permission_zero,
                privacy_zero,
            )
        )

        contract: dict[str, Any] = {
            (
                "chat_to_memory_runtime_handoff_"
                "contract_ready"
            ):
                ready,
            (
                "chat_to_memory_runtime_handoff_"
                "runtime_ready"
            ):
                False,
            "status": (
                "chat_to_memory_runtime_handoff_"
                "contract_ready"
                if ready
                else
                "chat_to_memory_runtime_handoff_"
                "contract_degraded"
            ),
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "planning_ready": ready,
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "contract_only": True,
            "preview_only": True,
            "canonical_session_owner":
                self.canonical_session_owner,
            "canonical_handoff_owner":
                self.canonical_handoff_owner,
            "canonical_memory_store_owner":
                self.canonical_memory_store_owner,
            "permission_scope":
                self.permission_scope,
            "workspace_project_context_snapshot":
                workspace,
            "handoff_contract_snapshot":
                handoff,
            "memory_write_permission_snapshot":
                permission,
            "memory_review_queue_snapshot":
                review,
            "memory_privacy_snapshot":
                privacy,
            "explicit_user_memory_request_required":
                True,
            "single_direct_user_turn_required":
                True,
            "assistant_message_handoff_allowed":
                False,
            "system_message_handoff_allowed":
                False,
            "tool_message_handoff_allowed":
                False,
            "manual_review_required": True,
            "privacy_review_required": True,
            "permission_required_after_privacy_review":
                True,
            "default_deny_without_grant": True,
            "one_shot_grant_required": True,
            "permission_expiry_required": True,
            "chat_store_read_performed": False,
            "chat_history_scan_performed": False,
            "chat_turn_lookup_performed": False,
            "chat_event_consumed": False,
            "handoff_persisted": False,
            "memory_candidate_persisted": False,
            "review_queue_item_persisted": False,
            "review_decision_applied": False,
            "permission_request_persisted": False,
            "permission_grant_applied": False,
            "memory_write_performed": False,
            "memory_store_mutated": False,
            "audit_event_written": False,
            "model_request_dispatched": False,
            "network_request_performed": False,
            "command_executed": False,
            "tool_executed": False,
            "file_mutated": False,
            "runtime_execution_features": 0,
            "dependency_runtime_zero": (
                handoff_zero
                and permission_zero
                and privacy_zero
            ),
            "safe_idle_preserved": True,
            "runtime_scope": (
                "chat_to_memory_runtime_handoff_"
                "contract_only"
            ),
            "safety_blockers": list(
                self.safety_blockers
            ),
        }

        contract.update(
            {
                name: False
                for name in self.safety_blockers
            }
        )

        contract[
            "all_safety_blockers_inactive"
        ] = all(
            contract[name] is False
            for name in self.safety_blockers
        )

        return contract

    def status(self) -> dict[str, Any]:
        contract = (
            self.chat_to_memory_runtime_handoff_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "planning_ready":
                contract["planning_ready"],
            "runtime_ready": False,
            (
                "chat_to_memory_runtime_handoff_"
                "contract_ready"
            ):
                contract[
                    "chat_to_memory_runtime_handoff_"
                    "contract_ready"
                ],
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "canonical_handoff_owner":
                contract[
                    "canonical_handoff_owner"
                ],
            "runtime_scope":
                contract["runtime_scope"],
            "contract": contract,
        }

    def context(self) -> dict[str, Any]:
        contract = (
            self.chat_to_memory_runtime_handoff_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "current_sprint":
                self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "canonical_handoff_owner":
                contract[
                    "canonical_handoff_owner"
                ],
            "permission_scope":
                contract["permission_scope"],
            "workspace_project_context_snapshot":
                contract[
                    "workspace_project_context_snapshot"
                ],
            "handoff_contract_snapshot":
                contract[
                    "handoff_contract_snapshot"
                ],
            "memory_write_permission_snapshot":
                contract[
                    "memory_write_permission_snapshot"
                ],
            "memory_review_queue_snapshot":
                contract[
                    "memory_review_queue_snapshot"
                ],
            "memory_privacy_snapshot":
                contract[
                    "memory_privacy_snapshot"
                ],
            "contract_only": True,
            "preview_only": True,
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        contract = (
            self.chat_to_memory_runtime_handoff_contract()
        )

        workspace = contract[
            "workspace_project_context_snapshot"
        ]
        handoff = contract[
            "handoff_contract_snapshot"
        ]
        permission = contract[
            "memory_write_permission_snapshot"
        ]
        review = contract[
            "memory_review_queue_snapshot"
        ]
        privacy = contract[
            "memory_privacy_snapshot"
        ]

        assertions = {
            "contract_ready": (
                contract[
                    "chat_to_memory_runtime_handoff_"
                    "contract_ready"
                ]
                is True
            ),
            "runtime_disabled":
                contract["runtime_ready"] is False,
            "activation_blocked": (
                contract[
                    "runtime_activation_allowed"
                ]
                is False
            ),
            "release_gate_closed": (
                contract["release_gate_open"]
                is False
            ),
            "current_sprint_223": (
                contract[
                    "partner_runtime_current_sprint"
                ]
                == 223
            ),
            "next_sprint_224": (
                contract[
                    "partner_runtime_next_sprint"
                ]
                == 224
            ),
            "next_boundary_correct": (
                contract[
                    "partner_runtime_next_boundary"
                ]
                == (
                    "voice_vision_chat_context_fusion"
                )
            ),
            "workspace_contract_ready": (
                workspace["contract_ready"]
                is True
            ),
            "workspace_assertion_count_52": (
                workspace["assertion_count"]
                == 52
            ),
            "workspace_failed_zero": (
                workspace[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "canonical_session_owner_preserved": (
                contract[
                    "canonical_session_owner"
                ]
                == (
                    "aura_browser_chat_"
                    "session_runtime"
                )
            ),
            "handoff_contract_ready":
                handoff["ready"] is True,
            "permission_gate_ready":
                permission["ready"] is True,
            "review_queue_ready":
                review["ready"] is True,
            "privacy_layer_ready":
                privacy["ready"] is True,
            "explicit_memory_request_required": (
                contract[
                    "explicit_user_memory_"
                    "request_required"
                ]
                is True
            ),
            "direct_user_turn_only": (
                contract[
                    "single_direct_user_turn_required"
                ]
                is True
            ),
            "manual_review_required": (
                contract[
                    "manual_review_required"
                ]
                is True
            ),
            "privacy_review_required": (
                contract[
                    "privacy_review_required"
                ]
                is True
            ),
            "permission_after_privacy": (
                contract[
                    "permission_required_after_"
                    "privacy_review"
                ]
                is True
            ),
            "default_deny": (
                contract[
                    "default_deny_without_grant"
                ]
                is True
            ),
            "one_shot_grant_required": (
                contract[
                    "one_shot_grant_required"
                ]
                is True
            ),
            "permission_expiry_required": (
                contract[
                    "permission_expiry_required"
                ]
                is True
            ),
            "chat_store_not_read": (
                contract[
                    "chat_store_read_performed"
                ]
                is False
            ),
            "chat_history_not_scanned": (
                contract[
                    "chat_history_scan_performed"
                ]
                is False
            ),
            "handoff_not_persisted": (
                contract[
                    "handoff_persisted"
                ]
                is False
            ),
            "candidate_not_persisted": (
                contract[
                    "memory_candidate_persisted"
                ]
                is False
            ),
            "review_queue_not_persisted": (
                contract[
                    "review_queue_item_persisted"
                ]
                is False
            ),
            "review_decision_not_applied": (
                contract[
                    "review_decision_applied"
                ]
                is False
            ),
            "permission_request_not_persisted": (
                contract[
                    "permission_request_persisted"
                ]
                is False
            ),
            "permission_grant_not_applied": (
                contract[
                    "permission_grant_applied"
                ]
                is False
            ),
            "memory_not_written": (
                contract[
                    "memory_write_performed"
                ]
                is False
            ),
            "memory_store_not_mutated": (
                contract[
                    "memory_store_mutated"
                ]
                is False
            ),
            "audit_not_written": (
                contract[
                    "audit_event_written"
                ]
                is False
            ),
            "command_not_executed": (
                contract[
                    "command_executed"
                ]
                is False
            ),
            "tool_not_executed": (
                contract["tool_executed"]
                is False
            ),
            "network_not_used": (
                contract[
                    "network_request_performed"
                ]
                is False
            ),
            "file_not_mutated": (
                contract["file_mutated"]
                is False
            ),
            "runtime_execution_zero": (
                contract[
                    "runtime_execution_features"
                ]
                == 0
            ),
            "all_blockers_inactive": (
                contract[
                    "all_safety_blockers_inactive"
                ]
                is True
            ),
            "runtime_scope_correct": (
                contract["runtime_scope"]
                == (
                    "chat_to_memory_runtime_handoff_"
                    "contract_only"
                )
            ),
        }

        assertions.update(
            {
                f"{name}_inactive":
                    contract[name] is False
                for name
                in self.safety_blockers
            }
        )

        failed = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "status": "checked",
            "planning_ready":
                contract["planning_ready"],
            "runtime_ready": False,
            "assertion_count":
                len(assertions),
            "failed_assertion_count":
                len(failed),
            "failed_assertions": failed,
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "chat_to_memory_runtime_handoff_contract":
                contract,
        }

    def plan(self) -> dict[str, Any]:
        contract = (
            self.chat_to_memory_runtime_handoff_contract()
        )

        return {
            "name": self.name,
            "sprint": self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "contract_ready": contract[
                "chat_to_memory_runtime_handoff_"
                "contract_ready"
            ],
            "runtime_ready": False,
            "runtime_scope":
                contract["runtime_scope"],
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
            "canonical_handoff_owner":
                contract[
                    "canonical_handoff_owner"
                ],
            "permission_scope":
                contract["permission_scope"],
        }
