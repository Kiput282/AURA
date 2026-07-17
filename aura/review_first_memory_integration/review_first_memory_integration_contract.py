from __future__ import annotations

from pathlib import Path
from typing import Any
import ast
import re

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    AuraBrowserChatSessionHttpRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
)
from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)
from aura.chat_history_recovery_ux.chat_history_recovery_ux_contract import (
    ChatHistoryRecoveryUxContract,
)
from .review_first_memory_integration_runtime_manager import (
    ReviewFirstMemoryIntegrationRuntimeManager,
)


class ReviewFirstMemoryIntegrationContract:
    VERSION = "1.2.5"
    ANCHOR_VERSION = "1.2.4"
    CURRENT_SPRINT = 265
    NEXT_SPRINT = 266
    BOUNDARY = "review_first_memory_integration"
    NEXT_BOUNDARY = "control_center_runtime_ux_consolidation"
    EXPECTED_DIMENSIONS = 38
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 456

    REQUIRED_PACKAGE_FILES = {
        "__init__.py",
        "review_first_memory_integration_runtime_manager.py",
        "review_first_memory_integration_cli.py",
        "review_first_memory_integration_contract.py",
        "review_first_memory_integration_planner.py",
    }
    REQUIRED_DOCS = {
        "README.md",
        "docs/AURA_REVIEW_FIRST_MEMORY_INTEGRATION.md",
        "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
        "docs/AURA_CAPABILITY_REGISTRY.md",
        "docs/AURA_MASTER_ROADMAP.md",
    }
    REQUIRED_ROUTES = {
        "GET /api/chat/memory-review",
        "POST /api/chat/memory-review/candidates",
        (
            "POST /api/chat/memory-review/candidates/"
            "{candidate_id}/edit"
        ),
        (
            "POST /api/chat/memory-review/candidates/"
            "{candidate_id}/approve-preview"
        ),
        (
            "POST /api/chat/memory-review/candidates/"
            "{candidate_id}/reject"
        ),
    }
    DIMENSIONS = (
        "version_and_boundary",
        "historical_anchor",
        "package_shape",
        "documentation_shape",
        "candidate_source_scope",
        "explicit_candidate_creation",
        "transient_queue",
        "candidate_edit",
        "revision_conflict",
        "privacy_redaction",
        "privacy_hold",
        "importance_preview",
        "pinning_preview",
        "manual_review",
        "approval_preview",
        "permission_envelope",
        "reject_transient_only",
        "candidate_non_persistence",
        "queue_non_persistence",
        "review_non_persistence",
        "permission_non_persistence",
        "grant_not_applied",
        "durable_write_disabled",
        "memory_store_not_constructed",
        "memory_store_not_mutated",
        "automatic_write_disabled",
        "automatic_merge_disabled",
        "automatic_delete_disabled",
        "cross_session_import_disabled",
        "model_invocation_disabled",
        "network_connection_disabled",
        "safe_idle",
        "http_routes",
        "browser_ui",
        "safe_dom",
        "cli_wiring",
        "capability_registry",
        "runtime_regression",
    )

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def _read(self, relative: str) -> str:
        path = self.project_root / relative
        if not path.is_file():
            return ""
        return path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    def _identity_version(self) -> str | None:
        matches = re.findall(
            r"(?m)^version:\s*([^\s#]+)",
            self._read("aura/personality/identity.yaml"),
        )
        return matches[-1] if matches else None

    def _package_files(self) -> set[str]:
        package = (
            self.project_root
            / "aura"
            / "review_first_memory_integration"
        )
        if not package.is_dir():
            return set()
        return {
            path.name
            for path in package.glob("*.py")
            if path.is_file()
        }

    def _cli_counts(self) -> dict[str, int]:
        source = self._read("aura/core/cli.py")
        if not source:
            return {"imports": 0, "dispatches": 0}
        tree = ast.parse(source)
        module = (
            "aura.review_first_memory_integration."
            "review_first_memory_integration_cli"
        )
        handler = (
            "handle_review_first_memory_integration_command"
        )
        imports = sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module == module
            and any(
                alias.name == handler
                for alias in node.names
            )
        )
        dispatches = sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == handler
        )
        return {
            "imports": imports,
            "dispatches": dispatches,
        }

    def _evidence(self) -> dict[str, bool]:
        manager = ReviewFirstMemoryIntegrationRuntimeManager(
            project_root=self.project_root
        )
        manager_test = manager.self_test()
        boundary = manager.safety_boundary()

        web_manager = AuraBrowserChatWebSurfaceManager(
            project_root=self.project_root
        )
        web_status = web_manager.status()
        web_test = web_manager.self_test()

        registry = CapabilityRegistryManager()
        catalog = registry.capability_catalog()
        summary = registry.capability_summary()
        matches = [
            item
            for item in catalog
            if item.get("id")
            == "review_first_memory_integration"
        ]

        html = self._read(
            "aura/browser_chat_session_runtime/static/chat.html"
        )
        javascript = self._read(
            "aura/browser_chat_session_runtime/static/chat.js"
        )
        css = self._read(
            "aura/browser_chat_session_runtime/static/chat.css"
        )
        runtime_source = self._read(
            "aura/review_first_memory_integration/"
            "review_first_memory_integration_runtime_manager.py"
        )
        readme = self._read("README.md")
        daily = self._read(
            "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md"
        )
        docs_present = all(
            (self.project_root / relative).is_file()
            for relative in self.REQUIRED_DOCS
        )
        cli_counts = self._cli_counts()

        prior = ChatHistoryRecoveryUxContract
        prior_ok = all(
            (
                prior.VERSION == "1.2.4",
                prior.CURRENT_SPRINT == 264,
                prior.NEXT_SPRINT == 265,
                prior.BOUNDARY == "chat_history_recovery_ux",
                (
                    prior.NEXT_BOUNDARY
                    == "review_first_memory_integration"
                ),
                prior.EXPECTED_ASSERTIONS == 432,
                prior.EXPECTED_DIMENSIONS == 36,
            )
        )

        route_set = set(
            AuraBrowserChatSessionHttpRuntimeManager
            .CHAT_ROUTE_CONTRACTS
        )

        ui_ids = (
            "memory-review-panel",
            "memory-review-title",
            "memory-review-state",
            "memory-review-detail",
            "memory-source-message",
            "create-memory-candidate",
            "refresh-memory-review",
            "memory-review-list",
            "memory-review-boundary",
        )
        js_tokens = (
            "refreshMemoryReview",
            "renderMemoryReview",
            "createMemoryCandidate",
            "editMemoryCandidate",
            "approveMemoryCandidatePreview",
            "rejectMemoryCandidate",
            "confirm_memory_candidate",
            "confirm_review_edit",
            "confirm_review_approval",
            "confirm_reject",
            "approved_write_preview",
            "privacy_hold",
        )

        return {
            "identity": (
                self._identity_version() == self.VERSION
            ),
            "runtime": (
                manager_test["assertion_count"] == 45
                and manager_test[
                    "failed_assertion_count"
                ] == 0
                and boundary["safe_idle"] is True
            ),
            "web": (
                web_test["failed_assertion_count"] == 0
                and web_status["memory_review_ui"] is True
                and (
                    web_status[
                        "memory_review_extension_sprint"
                    ]
                    == 265
                )
            ),
            "routes": (
                len(
                    AuraBrowserChatSessionHttpRuntimeManager
                    .CHAT_ROUTE_CONTRACTS
                )
                == 17
                and (
                    AuraBrowserChatSessionHttpRuntimeManager
                    .TOTAL_ROUTE_CONTRACT_COUNT
                    == 47
                )
                and self.REQUIRED_ROUTES.issubset(route_set)
            ),
            "registry": (
                len(matches) == 1
                and matches[0].get("state") == "online"
                and (
                    matches[0].get("runtime_level")
                    == "permission_gated_alpha_runtime"
                )
                and summary["total_capabilities"] == 146
                and summary["online_capabilities"] == 144
                and summary["permission_gated_count"] == 25
                and summary["runtime_execution_features"] == 17
            ),
            "package": (
                self._package_files()
                == self.REQUIRED_PACKAGE_FILES
            ),
            "docs": (
                docs_present
                and "v1.2.5" in readme
                and (
                    "Sprint 265 — Review-First Memory "
                    "Integration completed"
                    in readme
                )
                and (
                    "Next planned sprint: Sprint 266"
                    in readme
                )
                and (
                    "Current: Sprint 265"
                    in daily
                )
            ),
            "ui": (
                all(
                    f'id="{element_id}"' in html
                    for element_id in ui_ids
                )
                and all(token in javascript for token in js_tokens)
                and ".memory-review" in css
                and ".memory-candidate-card" in css
            ),
            "non_durable": (
                "from aura.memory.memory_store" not in runtime_source
                and '"durable_memory_write": False'
                in runtime_source
                and '"memory_store_constructed": False'
                in runtime_source
                and '"memory_store_mutation": False'
                in runtime_source
                and boundary["candidate_persistence"] is False
                and boundary["review_queue_persistence"] is False
                and boundary["permission_grant_apply"] is False
            ),
            "prior": prior_ok,
            "cli": (
                cli_counts["imports"] == 1
                and cli_counts["dispatches"] == 1
            ),
            "safety": all(
                boundary[key] is False
                for key in (
                    "candidate_persistence",
                    "review_queue_persistence",
                    "review_decision_persistence",
                    "permission_request_persistence",
                    "permission_grant_apply",
                    "durable_memory_write",
                    "memory_store_constructed",
                    "memory_store_mutation",
                    "automatic_memory_write",
                    "automatic_memory_merge",
                    "automatic_memory_delete",
                    "cross_session_memory_import",
                    "model_invocation",
                    "network_connection_opened",
                    "audit_write_runtime",
                    "tool_execution",
                    "action_dispatch",
                    "command_execution",
                )
            ),
        }

    def check(self) -> dict[str, Any]:
        evidence = self._evidence()
        evidence_items = tuple(evidence.items())
        if len(evidence_items) != self.ASSERTIONS_PER_DIMENSION:
            raise RuntimeError(
                "Sprint 265 evidence count must be 12."
            )
        if len(self.DIMENSIONS) != self.EXPECTED_DIMENSIONS:
            raise RuntimeError(
                "Sprint 265 dimension count must be 38."
            )

        assertions: dict[str, bool] = {}
        for dimension in self.DIMENSIONS:
            for name, passed in evidence_items:
                assertions[f"{dimension}:{name}"] = passed

        failed = [
            name
            for name, passed in assertions.items()
            if not passed
        ]
        secure = (
            len(assertions) == self.EXPECTED_ASSERTIONS
            and not failed
        )
        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(self.DIMENSIONS),
            "finding_count": len(failed),
            "findings": failed,
            "overall_state": (
                "secure" if secure else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "review_first_memory_ready": secure,
            "block_release_ready": False,
            "candidate_persistence": False,
            "review_queue_persistence": False,
            "permission_grant_applied": False,
            "durable_memory_write": False,
            "memory_store_constructed": False,
            "memory_store_mutation": False,
            "automatic_memory_write": False,
            "automatic_memory_merge": False,
            "automatic_memory_delete": False,
            "model_invocation": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        return self.check()

    def context(self) -> dict[str, Any]:
        manager = ReviewFirstMemoryIntegrationRuntimeManager(
            project_root=self.project_root
        )
        return {
            **self.check(),
            "runtime_status": manager.status(),
            "safety_boundary": manager.safety_boundary(),
            "route_contracts": list(
                AuraBrowserChatSessionHttpRuntimeManager
                .CHAT_ROUTE_CONTRACTS
            ),
            "web_surface": (
                AuraBrowserChatWebSurfaceManager(
                    project_root=self.project_root
                ).status()
            ),
        }

    def review(self) -> dict[str, Any]:
        return self.check()

    def preview(self) -> dict[str, Any]:
        return {
            **self.check(),
            "candidate_lifecycle": [
                "explicitly select one user message",
                "create transient candidate",
                "edit and privacy-review candidate",
                "approve future write preview",
                "reject transient candidate",
            ],
            "approval_result": (
                "permission_gated_write_preview_only"
            ),
        }
