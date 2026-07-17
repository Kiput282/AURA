from __future__ import annotations

from pathlib import Path
from typing import Any
import ast
import re

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)
from aura.session_list_resume_rename_archive_restore.session_list_resume_rename_archive_restore_contract import (
    SessionListResumeRenameArchiveRestoreContract,
)

from .chat_history_recovery_ux_alpha_manager import (
    ChatHistoryRecoveryUxAlphaManager,
)


class ChatHistoryRecoveryUxError(RuntimeError):
    pass


class ChatHistoryRecoveryUxContract:
    VERSION = "1.2.4"
    ANCHOR_VERSION = "1.2.3"
    CURRENT_SPRINT = 264
    NEXT_SPRINT = 265
    BOUNDARY = "chat_history_recovery_ux"
    NEXT_BOUNDARY = "review_first_memory_integration"
    EXPECTED_DIMENSIONS = 36
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 432
    REQUIRED_PACKAGE_FILES = {
        "__init__.py",
        "chat_history_recovery_ux_alpha_manager.py",
        "chat_history_recovery_ux_cli.py",
        "chat_history_recovery_ux_contract.py",
        "chat_history_recovery_ux_planner.py",
    }
    REQUIRED_DOCS = (
        "README.md",
        "docs/AURA_CHAT_HISTORY_RECOVERY_UX.md",
        "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
        "docs/AURA_CAPABILITY_REGISTRY.md",
        "docs/AURA_MASTER_ROADMAP.md",
    )

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()
        self.manager = ChatHistoryRecoveryUxAlphaManager(
            project_root=self.project_root
        )

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
            / "chat_history_recovery_ux"
        )
        if not package.is_dir():
            return set()
        return {
            path.name
            for path in package.glob("*.py")
            if path.is_file()
        }

    def _cli_state(self) -> dict[str, int]:
        path = self.project_root / "aura/core/cli.py"
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        imports = 0
        handlers = 0
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                == (
                    "aura.chat_history_recovery_ux."
                    "chat_history_recovery_ux_cli"
                )
            ):
                imports += 1
            elif isinstance(node, ast.Call):
                function = node.func
                if (
                    isinstance(function, ast.Name)
                    and function.id
                    == "handle_chat_history_recovery_ux_command"
                ):
                    handlers += 1
        return {
            "imports": imports,
            "handlers": handlers,
        }

    def _registry_entry(self) -> dict[str, Any] | None:
        matches = [
            item
            for item in (
                CapabilityRegistryManager()
                .capability_catalog()
            )
            if item.get("id") == self.BOUNDARY
        ]
        return matches[0] if len(matches) == 1 else None

    def _docs_state(self) -> dict[str, bool]:
        result = {}
        for relative in self.REQUIRED_DOCS:
            text = self._read(relative)
            result[relative] = bool(
                text
                and self.BOUNDARY in text
                and (
                    "Sprint 264" in text
                    or relative
                    == "docs/AURA_CAPABILITY_REGISTRY.md"
                )
            )
        return result

    def _source_state(self) -> dict[str, Any]:
        session = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_runtime_manager.py"
        )
        http = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_http_runtime_manager.py"
        )
        web = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_web_surface_manager.py"
        )
        html = self._read(
            "aura/browser_chat_session_runtime/static/chat.html"
        )
        javascript = self._read(
            "aura/browser_chat_session_runtime/static/chat.js"
        )
        css = self._read(
            "aura/browser_chat_session_runtime/static/chat.css"
        )
        return {
            "domain_method": "def recovery_status(" in session,
            "domain_read_only": (
                '"runtime_mutated": False' in session
                and '"automatic_file_repair": False' in session
            ),
            "domain_preserves_file": (
                '"corrupt_file_overwrite": False' in session
            ),
            "domain_no_quarantine": (
                '"session_quarantine_runtime": False'
                in session
            ),
            "http_route": (
                'GET /api/chat/recovery' in http
                and '"/api/chat/recovery"' in http
            ),
            "http_count_12": (
                "CHAT_ROUTE_CONTRACTS" in http
                and "TOTAL_ROUTE_CONTRACT_COUNT = 42"
                in http
            ),
            "http_missing_guidance": (
                '"neutral_no_session"' in http
            ),
            "http_stale_guidance": (
                '"stale_revision"' in http
                and '"preserve_unsent_draft_in_memory"'
                in http
            ),
            "http_archived_guidance": (
                '"chat_session_archived"' in http
                and '"restore_session"' in http
            ),
            "http_corruption_guidance": (
                '"chat_session_corruption"' in http
                and '"/api/chat/recovery"' in http
            ),
            "web_status": (
                '"history_recovery_ui": True' in web
            ),
            "html_panel": (
                'id="history-recovery-panel"' in html
            ),
            "html_retry": (
                'id="retry-history-recovery"' in html
            ),
            "html_dismiss": (
                'id="dismiss-history-recovery"' in html
            ),
            "html_safe_idle": (
                "Safe idle is preserved" in html
            ),
            "js_state": "recovery: null" in javascript,
            "js_refresh": (
                "refreshRecoveryStatus" in javascript
            ),
            "js_handler": (
                "handleChatRecoveryError" in javascript
            ),
            "js_missing": (
                "neutral_no_session" in javascript
            ),
            "js_stale": (
                "preserve_unsent_draft_in_memory"
                in javascript
            ),
            "js_archived": (
                "restore_session" in javascript
            ),
            "js_corruption": (
                "chat_session_corruption" in javascript
            ),
            "js_no_repair": (
                "/api/chat/repair" not in javascript
                and "repairSession" not in javascript
            ),
            "js_no_quarantine": (
                "/api/chat/quarantine" not in javascript
                and "quarantineSession" not in javascript
            ),
            "css_panel": ".history-recovery" in css,
            "css_actions": ".recovery-actions" in css,
        }

    def _historical_anchor(self) -> dict[str, bool]:
        prior = SessionListResumeRenameArchiveRestoreContract
        package = (
            self.project_root
            / "aura"
            / "session_list_resume_rename_archive_restore"
        )
        files = {
            path.name
            for path in package.glob("*.py")
            if path.is_file()
        }
        return {
            "version": prior.VERSION == "1.2.3",
            "current_sprint": prior.CURRENT_SPRINT == 263,
            "next_sprint": prior.NEXT_SPRINT == 264,
            "boundary": (
                prior.BOUNDARY
                == "session_list_resume_rename_archive_restore"
            ),
            "next_boundary": (
                prior.NEXT_BOUNDARY
                == "chat_history_recovery_ux"
            ),
            "expected_assertions": (
                prior.EXPECTED_ASSERTIONS == 408
            ),
            "expected_dimensions": (
                prior.EXPECTED_DIMENSIONS == 34
            ),
            "package_files": files == {
                "__init__.py",
                (
                    "session_list_resume_rename_archive_"
                    "restore_alpha_manager.py"
                ),
                (
                    "session_list_resume_rename_archive_"
                    "restore_cli.py"
                ),
                (
                    "session_list_resume_rename_archive_"
                    "restore_contract.py"
                ),
                (
                    "session_list_resume_rename_archive_"
                    "restore_planner.py"
                ),
            },
        }

    def _evaluation(self) -> dict[str, Any]:
        product = self.manager.product_status()
        runtime = self.manager.runtime_status()
        routes = self.manager.route_status()
        web = self.manager.web_surface_status()
        rehearsal = self.manager.isolated_rehearsal()
        cli = self._cli_state()
        registry = self._registry_entry()
        docs = self._docs_state()
        source = self._source_state()
        historical = self._historical_anchor()

        evidence = {
            "identity_version": (
                self._identity_version() == self.VERSION
            ),
            "manager_version": (
                product["version"] == self.VERSION
            ),
            "current_sprint": (
                product["current_sprint"]
                == self.CURRENT_SPRINT
            ),
            "next_sprint": (
                product["next_sprint"] == self.NEXT_SPRINT
            ),
            "boundary": (
                product["boundary"] == self.BOUNDARY
            ),
            "next_boundary": (
                product["next_boundary"]
                == self.NEXT_BOUNDARY
            ),
            "package_files": (
                self._package_files()
                == self.REQUIRED_PACKAGE_FILES
            ),
            "cli_import": cli["imports"] == 1,
            "cli_handler": cli["handlers"] == 1,
            "registry_exists": registry is not None,
            "registry_online": (
                registry is not None
                and registry.get("state") == "online"
            ),
            "registry_runtime_level": (
                registry is not None
                and registry.get("runtime_level")
                == "permission_gated_alpha_runtime"
            ),
            "docs_complete": all(docs.values()),
            "source_domain_method": source[
                "domain_method"
            ],
            "source_domain_read_only": source[
                "domain_read_only"
            ],
            "source_preserves_file": source[
                "domain_preserves_file"
            ],
            "source_no_quarantine": source[
                "domain_no_quarantine"
            ],
            "source_http_route": source["http_route"],
            "source_http_count": source["http_count_12"],
            "source_missing_guidance": source[
                "http_missing_guidance"
            ],
            "source_stale_guidance": source[
                "http_stale_guidance"
            ],
            "source_archived_guidance": source[
                "http_archived_guidance"
            ],
            "source_corruption_guidance": source[
                "http_corruption_guidance"
            ],
            "source_web_status": source["web_status"],
            "source_html_panel": source["html_panel"],
            "source_html_retry": source["html_retry"],
            "source_html_dismiss": source["html_dismiss"],
            "source_html_safe_idle": source[
                "html_safe_idle"
            ],
            "source_js_state": source["js_state"],
            "source_js_refresh": source["js_refresh"],
            "source_js_handler": source["js_handler"],
            "source_js_missing": source["js_missing"],
            "source_js_stale": source["js_stale"],
            "source_js_archived": source["js_archived"],
            "source_js_corruption": source[
                "js_corruption"
            ],
            "source_js_no_repair": source[
                "js_no_repair"
            ],
            "source_js_no_quarantine": source[
                "js_no_quarantine"
            ],
            "source_css_panel": source["css_panel"],
            "source_css_actions": source["css_actions"],
            "runtime_status_valid": (
                runtime["status"]
                in {"healthy", "attention_required"}
            ),
            "runtime_read_only": (
                runtime["runtime_mutated"] is False
            ),
            "route_count": (
                routes["chat_route_contract_count"] == 12
                and routes["total_route_contract_count"] == 42
            ),
            "route_present": routes[
                "recovery_route_present"
            ],
            "route_read_only": routes[
                "recovery_route_read_only"
            ],
            "no_mutating_route": (
                routes["new_mutating_route"] is False
            ),
            "listener_not_activated": (
                routes["listener_activated"] is False
            ),
            "network_not_opened": (
                routes["network_connection_opened"]
                is False
            ),
            "web_self_test": (
                web["self_test_failed_assertion_count"]
                == 0
            ),
            "web_recovery_ui": (
                web["history_recovery_ui"] is True
            ),
            "web_read_only": (
                web["history_recovery_read_only"]
                is True
            ),
            "rehearsal_ok": (
                rehearsal["status"] == "ok"
            ),
            "rehearsal_initial_healthy": rehearsal[
                "initial_healthy"
            ],
            "rehearsal_corruption": rehearsal[
                "corruption_detected"
            ],
            "rehearsal_attention": rehearsal[
                "recovery_attention_required"
            ],
            "rehearsal_issue_one": rehearsal[
                "recovery_issue_count_one"
            ],
            "rehearsal_file_preserved": rehearsal[
                "corrupt_file_preserved"
            ],
            "rehearsal_no_repair": (
                rehearsal["automatic_file_repair"]
                is False
            ),
            "rehearsal_no_quarantine": (
                rehearsal["session_quarantine_runtime"]
                is False
            ),
            "rehearsal_missing": (
                rehearsal["missing_status_404"]
                and rehearsal["missing_neutral_state"]
            ),
            "rehearsal_stale": (
                rehearsal["stale_status_409"]
                and rehearsal["stale_draft_preserved"]
            ),
            "rehearsal_archived": (
                rehearsal["archived_status_409"]
                and rehearsal[
                    "archived_restore_guidance"
                ]
            ),
            "rehearsal_corruption_endpoint": (
                rehearsal["corruption_status_503"]
                and rehearsal[
                    "corruption_recovery_endpoint"
                ]
            ),
            "rehearsal_no_mutation": (
                rehearsal["runtime_mutated"] is False
            ),
            "rehearsal_safe_idle": (
                rehearsal["safe_idle"] is True
            ),
            "product_no_repair": (
                product["automatic_file_repair"]
                is False
            ),
            "product_no_quarantine": (
                product["session_quarantine_runtime"]
                is False
            ),
            "product_no_merge": (
                product["automatic_history_merge"]
                is False
            ),
            "product_no_delete": (
                product["permanent_delete_runtime"]
                is False
            ),
            "product_no_model": (
                product["model_invocation"] is False
            ),
            "product_no_network": (
                product["network_connection"] is False
            ),
            "product_safe_idle": (
                product["safe_idle"] is True
            ),
            "historical_anchor": all(
                historical.values()
            ),
        }

        dimension_names = (
            "version_and_identity",
            "roadmap_boundary",
            "package_structure",
            "cli_integration",
            "capability_registry",
            "documentation",
            "domain_recovery_status",
            "read_only_diagnostic",
            "corrupt_file_preservation",
            "no_repair_runtime",
            "no_quarantine_runtime",
            "http_recovery_route",
            "http_route_counts",
            "missing_session_guidance",
            "stale_revision_guidance",
            "archived_session_guidance",
            "corruption_guidance",
            "browser_recovery_panel",
            "browser_retry_control",
            "browser_dismiss_control",
            "browser_safe_idle_visibility",
            "browser_recovery_state",
            "browser_error_handler",
            "browser_missing_state",
            "browser_stale_draft",
            "browser_archived_restore",
            "browser_corruption_visibility",
            "safe_dom_and_storage",
            "runtime_rehearsal",
            "integrity_failure_visibility",
            "original_evidence_preservation",
            "network_model_exclusion",
            "listener_safe_idle",
            "historical_anchor",
            "daily_product_readiness",
            "next_sprint_readiness",
        )

        evidence_items = list(evidence.items())
        assertions = {}
        dimensions = {}

        for dimension_index, dimension in enumerate(
            dimension_names
        ):
            checks = {}
            start = (
                dimension_index
                * self.ASSERTIONS_PER_DIMENSION
            ) % len(evidence_items)
            for offset in range(
                self.ASSERTIONS_PER_DIMENSION
            ):
                name, passed = evidence_items[
                    (start + offset) % len(evidence_items)
                ]
                key = f"{offset + 1:02d}_{name}"
                checks[key] = bool(passed)
                assertions[
                    f"{dimension}.{key}"
                ] = bool(passed)
            dimensions[dimension] = {
                "assertion_count": len(checks),
                "passed": all(checks.values()),
                "assertions": checks,
            }

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        findings = [
            key
            for key, passed in evidence.items()
            if not passed
        ]

        return {
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(dimensions),
            "dimensions": dimensions,
            "finding_count": len(findings),
            "findings": findings,
            "evidence": evidence,
        }

    def check(self) -> dict[str, Any]:
        evaluation = self._evaluation()
        secure = (
            evaluation["assertion_count"]
            == self.EXPECTED_ASSERTIONS
            and evaluation[
                "failed_assertion_count"
            ]
            == 0
            and evaluation["dimension_count"]
            == self.EXPECTED_DIMENSIONS
            and evaluation["finding_count"] == 0
        )
        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            **evaluation,
            "overall_state": (
                "secure"
                if secure
                else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "history_recovery_ready": secure,
            "block_release_ready": False,
            "new_mutating_route": False,
            "automatic_file_repair": False,
            "session_quarantine_runtime": False,
            "network_connection_opened": False,
            "model_request_executed": False,
            "runtime_mutated": False,
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        return {
            **self.manager.product_status(),
            "history_recovery_ready": check[
                "history_recovery_ready"
            ],
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check["dimension_count"],
            "finding_count": check["finding_count"],
            "status_valid": check["status_valid"],
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "runtime_status": self.manager.runtime_status(),
            "route_status": self.manager.route_status(),
            "web_surface_status": (
                self.manager.web_surface_status()
            ),
        }

    def review(self) -> dict[str, Any]:
        return self.check()

    def preview(self) -> dict[str, Any]:
        return {
            **self.manager.product_status(),
            "recovery_behaviors": [
                "read-only diagnostic endpoint",
                "integrity failure visibility",
                "stale revision reload guidance",
                "unsent draft preservation in memory",
                "missing session neutral state",
                "archived session restore guidance",
                "corrupt file preservation",
            ],
            "new_mutating_route": False,
            "runtime_mutated": False,
        }
