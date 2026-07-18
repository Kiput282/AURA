from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


class DailyUseAcceptanceRehearsalReleaseHarnessError(
    RuntimeError
):
    pass


class DailyUseAcceptanceRehearsalReleaseHarnessRuntimeManager:
    VERSION = "1.2.9"
    ANCHOR_VERSION = "1.2.8"
    CURRENT_SPRINT = 269
    NEXT_SPRINT = 270
    BOUNDARY = (
        "daily_use_acceptance_rehearsal_and_release_harness"
    )
    NEXT_BOUNDARY = (
        "daily_local_assistant_live_acceptance_stabilization"
    )
    STEP_IDS = (
        "baseline",
        "service_visibility",
        "browser_chat_readiness",
        "model_handoff_readiness",
        "memory_review_readiness",
        "permission_action_visibility",
        "resource_readiness",
        "release_decision",
        "safe_idle_return",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    @staticmethod
    def _mapping(
        value: Any,
    ) -> dict[str, Any]:
        return (
            dict(value)
            if isinstance(value, Mapping)
            else {}
        )

    @staticmethod
    def _integer(
        value: Any,
    ) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

    @classmethod
    def _json_safe(
        cls,
        value: Any,
    ) -> Any:
        if isinstance(value, Mapping):
            return {
                str(key): cls._json_safe(item)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [
                cls._json_safe(item)
                for item in value
            ]
        if value is None or isinstance(
            value,
            (str, int, float, bool),
        ):
            return value
        return repr(value)

    @staticmethod
    def _step(
        step_id: str,
        title: str,
        passed: bool,
        detail: str,
        *,
        owner: str,
        evidence: Mapping[str, Any] | None = None,
        failure_policy: str,
    ) -> dict[str, Any]:
        return {
            "step_id": step_id,
            "title": title,
            "state": (
                "ready"
                if passed
                else "blocked"
            ),
            "passed": passed,
            "detail": detail,
            "owner": owner,
            "evidence": dict(evidence or {}),
            "failure_policy": failure_policy,
            "actions_allowed": False,
            "mutation_allowed": False,
            "persisted": False,
            "read_only": True,
            "safe_idle": True,
        }

    def snapshot(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self._mapping(root_payload)
        panels = self._mapping(payload.get("panels"))
        service = self._mapping(panels.get("service"))
        memory = self._mapping(panels.get("memory"))

        operations = self._mapping(
            payload.get("runtime_ux_consolidation")
        )
        operation_owners = self._mapping(
            operations.get("owners")
        )
        chat = self._mapping(operations.get("chat"))
        model = self._mapping(
            operations.get("model_runtime")
        )
        memory_review = self._mapping(
            operations.get("memory_review")
        )

        visibility = self._mapping(
            payload.get(
                "permission_audit_action_visibility_ux"
            )
        )
        visibility_sections = self._mapping(
            visibility.get("sections")
        )

        resources = self._mapping(
            payload.get(
                "atlas_resource_monitoring_dashboard"
            )
        )
        resource_current = self._mapping(
            resources.get("current")
        )
        resource_history = self._mapping(
            resources.get("history")
        )

        root_read_only = payload.get("read_only") is True
        root_no_mutation = (
            payload.get("mutation_allowed") is False
        )
        baseline_passed = (
            root_read_only
            and root_no_mutation
            and self._integer(
                payload.get("route_count")
            )
            == 9
            and self._integer(
                payload.get("panel_count")
            )
            == 8
            and bool(panels)
        )

        service_passed = (
            bool(service)
            and root_read_only
            and root_no_mutation
        )

        chat_passed = (
            bool(chat)
            and (
                chat.get("available") is True
                or bool(chat.get("workspace_route"))
            )
            and root_read_only
        )

        model_passed = (
            bool(model)
            and bool(
                operation_owners.get("model_runtime")
                or model.get(
                    "queue_and_budget_visibility"
                )
                is True
            )
            and operations.get(
                "model_activation_route"
            )
            is False
        )

        memory_passed = (
            bool(memory)
            and bool(memory_review)
            and operations.get("memory_write_route")
            is False
        )

        visibility_passed = (
            visibility.get("section_count") == 6
            and set(visibility_sections)
            == {
                "permission",
                "audit",
                "proposal",
                "approval",
                "action",
                "recovery",
            }
            and visibility.get("read_only") is True
            and visibility.get("safe_idle") is True
            and visibility.get(
                "automatic_permission_grant"
            )
            is False
            and visibility.get(
                "automatic_recovery"
            )
            is False
            and visibility.get(
                "new_execution_authority"
            )
            is False
        )

        resource_passed = (
            bool(resources)
            and bool(resource_current)
            and bool(resource_history)
            and resources.get("read_only") is True
            and resources.get("safe_idle") is True
        )

        steps: dict[str, dict[str, Any]] = {}

        steps["baseline"] = self._step(
            "baseline",
            "Baseline",
            baseline_passed,
            (
                "Boot-facing Control Center schema is "
                "available and read-only."
            ),
            owner="control_center_backend_snapshot",
            evidence={
                "route_count": self._integer(
                    payload.get("route_count")
                ),
                "panel_count": self._integer(
                    payload.get("panel_count")
                ),
                "read_only": root_read_only,
                "mutation_allowed":
                payload.get("mutation_allowed"),
            },
            failure_policy=(
                "Stop before runtime use and record "
                "the failed baseline dimension."
            ),
        )

        steps["service_visibility"] = self._step(
            "service_visibility",
            "Service visibility",
            service_passed,
            (
                "Service status is visible without "
                "start, stop, or restart execution."
            ),
            owner="control_center_service_panel",
            evidence={
                "status": service.get("status"),
                "read_only": service.get("read_only"),
                "actions_allowed":
                service.get("actions_allowed"),
            },
            failure_policy=(
                "Expose bounded failure metadata only; "
                "do not change service lifecycle."
            ),
        )

        steps["browser_chat_readiness"] = self._step(
            "browser_chat_readiness",
            "Browser chat readiness",
            chat_passed,
            (
                "Browser chat workspace metadata is "
                "available without creating a session."
            ),
            owner="runtime_ux_chat_workspace",
            evidence={
                "available": chat.get("available"),
                "workspace_route":
                chat.get("workspace_route"),
                "embedded": chat.get("embedded"),
            },
            failure_policy=(
                "Do not create, rename, archive, restore, "
                "or mutate a chat session."
            ),
        )

        steps["model_handoff_readiness"] = self._step(
            "model_handoff_readiness",
            "Model handoff readiness",
            model_passed,
            (
                "Model queue and resource-budget status "
                "is visible without model activation."
            ),
            owner="runtime_ux_model_runtime",
            evidence={
                "owner_present": bool(
                    operation_owners.get(
                        "model_runtime"
                    )
                ),
                "queue_and_budget_visibility":
                model.get(
                    "queue_and_budget_visibility"
                ),
                "model_activation_route":
                operations.get(
                    "model_activation_route"
                ),
            },
            failure_policy=(
                "Keep the model stopped and block the "
                "release decision."
            ),
        )

        steps["memory_review_readiness"] = self._step(
            "memory_review_readiness",
            "Memory review readiness",
            memory_passed,
            (
                "Memory and review summaries are visible "
                "without durable writes."
            ),
            owner="memory_panel_and_review_summary",
            evidence={
                "memory_status": memory.get("status"),
                "summary_visible":
                memory_review.get("summary_visible"),
                "memory_write_route":
                operations.get("memory_write_route"),
            },
            failure_policy=(
                "Do not approve, save, correct, delete, "
                "or persist memory."
            ),
        )

        steps["permission_action_visibility"] = self._step(
            "permission_action_visibility",
            "Permission and action visibility",
            visibility_passed,
            (
                "All six permission, audit, proposal, "
                "approval, action, and recovery sections "
                "are visible."
            ),
            owner=(
                "permission_audit_action_visibility_ux"
            ),
            evidence={
                "section_count":
                visibility.get("section_count"),
                "section_ids":
                sorted(visibility_sections),
                "automatic_permission_grant":
                visibility.get(
                    "automatic_permission_grant"
                ),
                "automatic_recovery":
                visibility.get(
                    "automatic_recovery"
                ),
            },
            failure_policy=(
                "Do not grant permission or execute "
                "recovery."
            ),
        )

        steps["resource_readiness"] = self._step(
            "resource_readiness",
            "ATLAS resource readiness",
            resource_passed,
            (
                "Current and rolling resource snapshots "
                "are available without starting a worker."
            ),
            owner="atlas_resource_monitoring_dashboard",
            evidence={
                "current_keys":
                sorted(resource_current),
                "history_keys":
                sorted(resource_history),
                "read_only":
                resources.get("read_only"),
                "safe_idle":
                resources.get("safe_idle"),
            },
            failure_policy=(
                "Do not start a background sampler or "
                "persist resource history."
            ),
        )

        pre_release_ids = self.STEP_IDS[:7]
        pre_release_ready = all(
            steps[step_id]["passed"]
            for step_id in pre_release_ids
        )

        steps["release_decision"] = self._step(
            "release_decision",
            "Release decision",
            pre_release_ready,
            (
                "Contract-only rehearsal is ready for "
                "Sprint 270 live acceptance."
                if pre_release_ready
                else
                "Contract-only rehearsal is blocked by "
                "one or more readiness findings."
            ),
            owner="sprint_269_release_harness",
            evidence={
                "ready_pre_release_steps": sum(
                    1
                    for step_id in pre_release_ids
                    if steps[step_id]["passed"]
                ),
                "pre_release_step_count":
                len(pre_release_ids),
                "live_e2e_required": False,
                "sprint_270_live_e2e_required": True,
            },
            failure_policy=(
                "Block release; do not commit, push, or "
                "perform a live acceptance run."
            ),
        )

        safe_idle_passed = all(
            (
                root_read_only,
                root_no_mutation,
                operations.get(
                    "service_action_routes"
                )
                is False,
                operations.get(
                    "restart_action_routes"
                )
                is False,
                operations.get(
                    "permission_grant_route"
                )
                is False,
                operations.get(
                    "recovery_execution_route"
                )
                is False,
                operations.get(
                    "model_activation_route"
                )
                is False,
                operations.get(
                    "memory_write_route"
                )
                is False,
                visibility.get(
                    "runtime_mutated"
                )
                is False,
                visibility.get(
                    "new_execution_authority"
                )
                is False,
            )
        )

        steps["safe_idle_return"] = self._step(
            "safe_idle_return",
            "Safe-idle return",
            safe_idle_passed,
            (
                "All inspected surfaces remain read-only "
                "with no execution route enabled."
            ),
            owner="cross_surface_safety_boundary",
            evidence={
                "root_read_only": root_read_only,
                "root_mutation_allowed":
                payload.get("mutation_allowed"),
                "service_action_routes":
                operations.get(
                    "service_action_routes"
                ),
                "restart_action_routes":
                operations.get(
                    "restart_action_routes"
                ),
                "permission_grant_route":
                operations.get(
                    "permission_grant_route"
                ),
                "recovery_execution_route":
                operations.get(
                    "recovery_execution_route"
                ),
                "model_activation_route":
                operations.get(
                    "model_activation_route"
                ),
                "memory_write_route":
                operations.get(
                    "memory_write_route"
                ),
            },
            failure_policy=(
                "Block release until safe-idle is "
                "restored and verified."
            ),
        )

        ready_step_count = sum(
            1
            for step in steps.values()
            if step["passed"]
        )
        rehearsal_ready = (
            ready_step_count == len(self.STEP_IDS)
        )

        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "status": (
                "ready"
                if rehearsal_ready
                else "blocked"
            ),
            "runtime_mode": "contract_only_rehearsal",
            "step_count": len(self.STEP_IDS),
            "ready_step_count": ready_step_count,
            "blocked_step_count":
            len(self.STEP_IDS) - ready_step_count,
            "step_ids": list(self.STEP_IDS),
            "steps": self._json_safe(steps),
            "rehearsal_ready": rehearsal_ready,
            "release_harness_ready": rehearsal_ready,
            "block_release_ready": False,
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "sprint_270_failure_recovery_required": True,
            "sprint_270_safe_idle_return_required": True,
            "result_persistence_enabled": False,
            "chat_session_created": False,
            "model_invoked": False,
            "memory_written": False,
            "service_lifecycle_changed": False,
            "permission_granted": False,
            "recovery_executed": False,
            "new_http_route": False,
            "background_worker_enabled": False,
            "external_dependency_added": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.snapshot(
            root_payload=root_payload
        )

    def context(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        snapshot = self.snapshot(
            root_payload=root_payload
        )
        return {
            "version": snapshot["version"],
            "current_sprint":
            snapshot["current_sprint"],
            "next_sprint": snapshot["next_sprint"],
            "boundary": snapshot["boundary"],
            "next_boundary":
            snapshot["next_boundary"],
            "runtime_mode":
            snapshot["runtime_mode"],
            "step_ids": snapshot["step_ids"],
            "rehearsal_ready":
            snapshot["rehearsal_ready"],
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "read_only": True,
            "safe_idle": True,
        }

    def check(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        snapshot = self.snapshot(
            root_payload=root_payload
        )
        return {
            **snapshot,
            "status_valid":
            snapshot["rehearsal_ready"],
            "finding_count":
            snapshot["blocked_step_count"],
            "findings": [
                step_id
                for step_id, step
                in snapshot["steps"].items()
                if not step["passed"]
            ],
        }

    def preview(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            **self.check(
                root_payload=root_payload
            ),
            "preview_only": True,
            "commit_performed": False,
            "push_performed": False,
        }

    def review(
        self,
        *,
        root_payload: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            **self.check(
                root_payload=root_payload
            ),
            "review_mode":
            "daily_use_acceptance_rehearsal",
            "commit_performed": False,
            "push_performed": False,
        }

    def _synthetic_root_payload(
        self,
    ) -> dict[str, Any]:
        return {
            "route_count": 9,
            "panel_count": 8,
            "read_only": True,
            "mutation_allowed": False,
            "panels": {
                "service": {
                    "status": "ready",
                    "read_only": True,
                    "actions_allowed": False,
                },
                "memory": {
                    "status": "ready",
                    "read_only": True,
                },
            },
            "runtime_ux_consolidation": {
                "owners": {
                    "model_runtime": {
                        "status": "ready",
                    },
                },
                "chat": {
                    "available": True,
                    "workspace_route": "/chat",
                    "embedded": False,
                },
                "model_runtime": {
                    "queue_and_budget_visibility": True,
                },
                "memory_review": {
                    "summary_visible": True,
                },
                "service_action_routes": False,
                "restart_action_routes": False,
                "permission_grant_route": False,
                "recovery_execution_route": False,
                "model_activation_route": False,
                "memory_write_route": False,
            },
            "permission_audit_action_visibility_ux": {
                "section_count": 6,
                "sections": {
                    section_id: {
                        "read_only": True,
                        "safe_idle": True,
                    }
                    for section_id in (
                        "permission",
                        "audit",
                        "proposal",
                        "approval",
                        "action",
                        "recovery",
                    )
                },
                "automatic_permission_grant": False,
                "automatic_recovery": False,
                "new_http_route": False,
                "mutation_routes": False,
                "new_execution_authority": False,
                "runtime_mutated": False,
                "read_only": True,
                "safe_idle": True,
            },
            "atlas_resource_monitoring_dashboard": {
                "current": {
                    "cpu": {},
                    "memory": {},
                },
                "history": {
                    "5": {},
                    "15": {},
                    "60": {},
                },
                "read_only": True,
                "safe_idle": True,
            },
        }

    def self_test(
        self,
    ) -> dict[str, Any]:
        snapshot = self.snapshot(
            root_payload=self._synthetic_root_payload()
        )
        assertions: dict[str, bool] = {}

        for step_id in self.STEP_IDS:
            step = snapshot["steps"][step_id]
            prefix = f"step:{step_id}"
            assertions[
                f"{prefix}:id"
            ] = step["step_id"] == step_id
            assertions[
                f"{prefix}:state"
            ] = step["state"] == "ready"
            assertions[
                f"{prefix}:passed"
            ] = step["passed"] is True
            assertions[
                f"{prefix}:read_only"
            ] = step["read_only"] is True
            assertions[
                f"{prefix}:actions"
            ] = step["actions_allowed"] is False
            assertions[
                f"{prefix}:mutation"
            ] = step["mutation_allowed"] is False
            assertions[
                f"{prefix}:persisted"
            ] = step["persisted"] is False
            assertions[
                f"{prefix}:safe_idle"
            ] = step["safe_idle"] is True

        failed = [
            name
            for name, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise DailyUseAcceptanceRehearsalReleaseHarnessError(
                "Sprint 269 runtime self-test failed: "
                + ", ".join(failed)
            )

        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "step_count": len(self.STEP_IDS),
            "ready_step_count":
            snapshot["ready_step_count"],
            "runtime_mode":
            snapshot["runtime_mode"],
            "rehearsal_ready":
            snapshot["rehearsal_ready"],
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "result_persistence_enabled": False,
            "new_http_route": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }
