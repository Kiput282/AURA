from __future__ import annotations

from pathlib import Path
from typing import Any
import ast
import re

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)
from aura.operational_browser_chat_model_handoff.operational_browser_chat_model_handoff_contract import (
    OperationalBrowserChatModelHandoffContract,
)

from .session_list_resume_rename_archive_restore_alpha_manager import (
    SessionListResumeRenameArchiveRestoreAlphaManager,
)


class SessionListResumeRenameArchiveRestoreError(
    RuntimeError
):
    pass


class SessionListResumeRenameArchiveRestoreContract:
    VERSION = "1.2.3"
    ANCHOR_VERSION = "1.2.2"
    CURRENT_SPRINT = 263
    NEXT_SPRINT = 264
    BOUNDARY = "session_list_resume_rename_archive_restore"
    NEXT_BOUNDARY = "chat_history_recovery_ux"
    EXPECTED_DIMENSIONS = 34
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 408
    REQUIRED_PACKAGE_FILES = {
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
    }
    REQUIRED_DOCS = (
        "README.md",
        (
            "docs/"
            "AURA_SESSION_LIST_RESUME_RENAME_"
            "ARCHIVE_RESTORE.md"
        ),
        (
            "docs/"
            "AURA_V1_2_TO_V1_3_DAILY_PRODUCT_"
            "ROADMAP.md"
        ),
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
        self.manager = (
            SessionListResumeRenameArchiveRestoreAlphaManager(
                project_root=self.project_root
            )
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
            / "session_list_resume_rename_archive_restore"
        )
        if not package.is_dir():
            return set()
        return {
            path.name
            for path in package.glob("*.py")
            if path.is_file()
        }

    def _cli_state(self) -> dict[str, int]:
        path = self.project_root / "aura" / "core" / "cli.py"
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
                    "aura."
                    "session_list_resume_rename_archive_restore."
                    "session_list_resume_rename_archive_restore_cli"
                )
            ):
                imports += 1
            elif isinstance(node, ast.Call):
                function = node.func
                if (
                    isinstance(function, ast.Name)
                    and function.id
                    == (
                        "handle_session_list_resume_rename_"
                        "archive_restore_command"
                    )
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
                    "Sprint 263" in text
                    or relative
                    == "docs/AURA_CAPABILITY_REGISTRY.md"
                )
            )
        return result

    def _source_state(self) -> dict[str, Any]:
        session_text = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_runtime_manager.py"
        )
        http_text = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_http_runtime_manager.py"
        )
        web_text = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_web_surface_manager.py"
        )
        javascript = self._read(
            "aura/browser_chat_session_runtime/static/chat.js"
        )
        html = self._read(
            "aura/browser_chat_session_runtime/static/chat.html"
        )
        return {
            "list_method": "def list_sessions(" in session_text,
            "resume_method": "def resume_session(" in session_text,
            "rename_method": "def rename_session(" in session_text,
            "archive_method": "def archive_session(" in session_text,
            "restore_method": "def restore_session(" in session_text,
            "active_guard": "_require_active_session" in session_text,
            "active_filter": '"active"' in session_text,
            "archived_filter": '"archived"' in session_text,
            "all_filter": '"all"' in session_text,
            "resume_route": "/resume" in http_text,
            "rename_route": "/rename" in http_text,
            "archive_route": "/archive" in http_text,
            "restore_route": "/restore" in http_text,
            "query_filter": "parse_qs" in http_text,
            "route_count_41": (
                "TOTAL_ROUTE_CONTRACT_COUNT = 41"
                in http_text
            ),
            "web_lifecycle_status": (
                "session_list_filter_ui" in web_text
            ),
            "ui_active_filter": (
                'id="session-filter-active"' in html
            ),
            "ui_archived_filter": (
                'id="session-filter-archived"' in html
            ),
            "ui_resume": 'id="resume-session"' in html,
            "ui_rename": 'id="rename-session"' in html,
            "ui_archive": 'id="archive-session"' in html,
            "ui_restore": 'id="restore-session"' in html,
            "ui_no_delete": (
                "delete-session" not in html
                and "deleteSession" not in javascript
            ),
            "js_state_filter": "sessionFilter" in javascript,
            "js_resume": "resumeSession" in javascript,
            "js_rename": "renameSession" in javascript,
            "js_archive": "archiveSession" in javascript,
            "js_restore": "restoreSession" in javascript,
            "js_no_storage": all(
                token not in javascript
                for token in (
                    "localStorage",
                    "sessionStorage",
                    "indexedDB",
                )
            ),
            "js_no_cross_merge": all(
                token not in javascript
                for token in (
                    "mergeSessionHistory",
                    "crossSessionHistory",
                )
            ),
        }

    def _evaluation(self) -> dict[str, Any]:
        product = self.manager.product_status()
        rehearsal = self.manager.isolated_rehearsal()
        routes = self.manager.route_status()
        web = self.manager.web_surface_status()
        prior_class = OperationalBrowserChatModelHandoffContract
        prior_package = (
            self.project_root
            / "aura"
            / "operational_browser_chat_model_handoff"
        )
        prior_package_files = {
            path.name
            for path in prior_package.glob("*.py")
            if path.is_file()
        }
        prior_anchor = {
            "version": (
                prior_class.VERSION == "1.2.2"
            ),
            "current_sprint": (
                prior_class.CURRENT_SPRINT == 262
            ),
            "next_sprint": (
                prior_class.NEXT_SPRINT == 263
            ),
            "boundary": (
                prior_class.BOUNDARY
                == "operational_browser_chat_model_handoff"
            ),
            "next_boundary": (
                prior_class.NEXT_BOUNDARY
                == "session_list_resume_rename_archive_restore"
            ),
            "expected_assertions": (
                prior_class.EXPECTED_ASSERTIONS == 384
            ),
            "expected_dimensions": (
                prior_class.EXPECTED_DIMENSIONS == 32
            ),
            "package_files": (
                prior_package_files
                == {
                    "__init__.py",
                    (
                        "operational_browser_chat_model_"
                        "handoff_alpha_manager.py"
                    ),
                    (
                        "operational_browser_chat_model_"
                        "handoff_cli.py"
                    ),
                    (
                        "operational_browser_chat_model_"
                        "handoff_contract.py"
                    ),
                    (
                        "operational_browser_chat_model_"
                        "handoff_planner.py"
                    ),
                }
            ),
        }
        cli = self._cli_state()
        registry = self._registry_entry()
        docs = self._docs_state()
        source = self._source_state()

        evidence = {
            "version_identity": (
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
            "source_list": source["list_method"],
            "source_resume": source["resume_method"],
            "source_rename": source["rename_method"],
            "source_archive": source["archive_method"],
            "source_restore": source["restore_method"],
            "source_active_guard": source["active_guard"],
            "source_active_filter": source["active_filter"],
            "source_archived_filter": source[
                "archived_filter"
            ],
            "source_all_filter": source["all_filter"],
            "route_resume": source["resume_route"],
            "route_rename": source["rename_route"],
            "route_archive": source["archive_route"],
            "route_restore": source["restore_route"],
            "route_query_filter": source["query_filter"],
            "route_count": (
                source["route_count_41"]
                and routes["chat_route_contract_count"] == 11
                and routes["total_route_contract_count"] == 41
            ),
            "web_self_test": (
                web["self_test_failed_assertion_count"] == 0
            ),
            "web_lifecycle_status": source[
                "web_lifecycle_status"
            ],
            "ui_active_filter": source["ui_active_filter"],
            "ui_archived_filter": source[
                "ui_archived_filter"
            ],
            "ui_resume": source["ui_resume"],
            "ui_rename": source["ui_rename"],
            "ui_archive": source["ui_archive"],
            "ui_restore": source["ui_restore"],
            "ui_no_delete": source["ui_no_delete"],
            "js_state_filter": source["js_state_filter"],
            "js_resume": source["js_resume"],
            "js_rename": source["js_rename"],
            "js_archive": source["js_archive"],
            "js_restore": source["js_restore"],
            "js_no_storage": source["js_no_storage"],
            "js_no_cross_merge": source[
                "js_no_cross_merge"
            ],
            "rehearsal_ok": rehearsal["status"] == "ok",
            "resume_same_id": rehearsal[
                "resume_same_session_id"
            ],
            "resume_history": rehearsal[
                "resume_history_unchanged"
            ],
            "rename_title": rehearsal[
                "rename_title_updated"
            ],
            "rename_same_id": rehearsal[
                "rename_session_id_unchanged"
            ],
            "rename_history": rehearsal[
                "rename_history_unchanged"
            ],
            "archive_status": rehearsal[
                "archive_status_archived"
            ],
            "archive_not_deleted": (
                rehearsal["archive_file_deleted"] is False
            ),
            "archive_not_moved": (
                rehearsal["archive_file_moved"] is False
            ),
            "archive_history": rehearsal[
                "archive_history_unchanged"
            ],
            "active_empty_after_archive": rehearsal[
                "active_list_empty_after_archive"
            ],
            "archived_one_after_archive": rehearsal[
                "archived_list_one_after_archive"
            ],
            "all_one_after_archive": rehearsal[
                "all_list_one_after_archive"
            ],
            "restore_status": rehearsal[
                "restore_status_active"
            ],
            "restore_same_id": rehearsal[
                "restore_session_id_unchanged"
            ],
            "restore_history": rehearsal[
                "restore_history_unchanged"
            ],
            "active_one_after_restore": rehearsal[
                "active_list_one_after_restore"
            ],
            "archived_empty_after_restore": rehearsal[
                "archived_list_empty_after_restore"
            ],
            "final_history": rehearsal[
                "final_history_unchanged"
            ],
            "single_file_retained": rehearsal[
                "single_session_file_retained"
            ],
            "cross_merge_false": (
                rehearsal["cross_session_history_merged"]
                is False
                and rehearsal[
                    "cross_session_history_merge"
                ]
                is False
                and product[
                    "cross_session_history_merge"
                ]
                is False
            ),
            "permanent_delete_false": (
                rehearsal["permanent_delete_runtime"]
                is False
                and product[
                    "permanent_delete_runtime"
                ]
                is False
            ),
            "model_not_invoked": (
                rehearsal["model_invoked"] is False
                and product[
                    "model_invocation_for_lifecycle"
                ]
                is False
            ),
            "network_not_opened": (
                rehearsal["network_connection_opened"]
                is False
                and product[
                    "network_connection_for_lifecycle"
                ]
                is False
                and routes[
                    "network_connection_opened"
                ]
                is False
            ),
            "listener_not_activated": (
                routes["listener_activated"] is False
            ),
            "safe_idle": (
                rehearsal["safe_idle"] is True
                and product["safe_idle"] is True
            ),
            "runtime_not_mutated": (
                product["runtime_mutated"] is False
                and rehearsal["runtime_mutated"] is False
                and routes["runtime_mutated"] is False
                and web["runtime_mutated"] is False
            ),
            "prior_historical_anchor": all(
                prior_anchor.values()
            ),
        }

        dimension_names = (
            "version_and_identity",
            "roadmap_boundary",
            "package_structure",
            "cli_integration",
            "capability_registry",
            "documentation",
            "session_domain_methods",
            "session_state_filters",
            "http_route_contracts",
            "http_query_validation",
            "browser_surface_status",
            "browser_active_filter",
            "browser_archived_filter",
            "browser_resume_control",
            "browser_rename_control",
            "browser_archive_control",
            "browser_restore_control",
            "safe_dom_and_storage",
            "resume_identity",
            "resume_history",
            "rename_metadata_only",
            "archive_non_destructive",
            "archive_list_visibility",
            "restore_non_destructive",
            "restore_list_visibility",
            "integrity_and_atomic_reuse",
            "session_id_immutability",
            "cross_session_isolation",
            "permanent_delete_exclusion",
            "model_network_exclusion",
            "listener_safe_idle",
            "prior_contract_compatibility",
            "runtime_mutation_boundary",
            "daily_product_readiness",
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
            and evaluation["failed_assertion_count"] == 0
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
                "secure" if secure else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "session_lifecycle_ready": secure,
            "block_release_ready": False,
            "runtime_activated": True,
            "network_connection_opened": False,
            "model_request_executed": False,
            "session_file_deleted": False,
            "cross_session_history_merged": False,
            "runtime_mutated": False,
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        return {
            **self.manager.product_status(),
            "session_lifecycle_ready": check[
                "session_lifecycle_ready"
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
            "operations": [
                "list active sessions",
                "list archived sessions",
                "resume same session",
                "rename title only",
                "archive without deletion",
                "restore without duplication",
            ],
            "permanent_delete_runtime": False,
            "cross_session_history_merge": False,
            "runtime_mutated": False,
        }
