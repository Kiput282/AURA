"""Sprint 262 operational browser-chat model handoff contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import ast
import re

from aura.capability_registry.capability_registry_manager import (
    CapabilityRegistryManager,
)

from .operational_browser_chat_model_handoff_alpha_manager import (
    OperationalBrowserChatModelHandoffAlphaManager,
)


class OperationalBrowserChatModelHandoffError(
    RuntimeError
):
    """Raised when the Sprint 262 boundary is not secure."""


class OperationalBrowserChatModelHandoffContract:
    VERSION = "1.2.2"
    ANCHOR_VERSION = "1.2.1"
    CURRENT_SPRINT = 262
    NEXT_SPRINT = 263
    BOUNDARY = "operational_browser_chat_model_handoff"
    NEXT_BOUNDARY = "session_list_resume_rename_archive_restore"
    EXPECTED_DIMENSIONS = 32
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 384

    REQUIRED_PACKAGE_FILES = {
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

    REQUIRED_DOCS = (
        "README.md",
        (
            "docs/"
            "AURA_OPERATIONAL_BROWSER_CHAT_MODEL_HANDOFF.md"
        ),
        (
            "docs/"
            "AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md"
        ),
        "docs/AURA_CAPABILITY_REGISTRY.md",
        "docs/AURA_MASTER_ROADMAP.md",
        (
            "docs/"
            "AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md"
        ),
        (
            "docs/"
            "AURA_GENESIS_TO_POST_GENESIS_PRODUCT_PLAN.md"
        ),
        "docs/AURA_LOCAL_MODEL_ROUTER_ACTIVATION.md",
        (
            "docs/"
            "AURA_ACTIVE_LOCAL_RUNTIME_INTEGRATION_"
            "STABILIZATION.md"
        ),
        (
            "docs/"
            "AURA_ROADMAP_RECONFIRMATION_AFTER_V1_2_0.md"
        ),
        "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
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
            OperationalBrowserChatModelHandoffAlphaManager(
                project_root=self.project_root
            )
        )

    def _read(
        self,
        relative: str,
    ) -> str:
        path = self.project_root / relative

        if not path.is_file():
            return ""

        return path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    def _identity_version(
        self,
    ) -> str | None:
        matches = re.findall(
            r"(?m)^version:\s*([^\s#]+)",
            self._read(
                "aura/personality/identity.yaml"
            ),
        )

        return matches[-1] if matches else None

    def _package_files(
        self,
    ) -> set[str]:
        package = (
            self.project_root
            / "aura"
            / "operational_browser_chat_model_handoff"
        )

        if not package.is_dir():
            return set()

        return {
            path.name
            for path in package.glob("*.py")
            if path.is_file()
        }

    def _cli_state(
        self,
    ) -> dict[str, int]:
        path = (
            self.project_root
            / "aura"
            / "core"
            / "cli.py"
        )
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
                    "operational_browser_chat_model_handoff."
                    "operational_browser_chat_model_handoff_cli"
                )
            ):
                imports += 1
            elif isinstance(node, ast.Call):
                function = node.func

                if (
                    isinstance(function, ast.Name)
                    and function.id
                    == (
                        "handle_operational_browser_chat_"
                        "model_handoff_command"
                    )
                ):
                    handlers += 1

        return {
            "imports": imports,
            "handlers": handlers,
        }

    def _registry_entry(
        self,
    ) -> dict[str, Any] | None:
        matches = [
            item
            for item in (
                CapabilityRegistryManager()
                .capability_catalog()
            )
            if item.get("id")
            == "operational_browser_chat_model_handoff"
        ]

        return (
            matches[0]
            if len(matches) == 1
            else None
        )

    def _documents_valid(
        self,
    ) -> bool:
        texts = [
            self._read(path)
            for path in self.REQUIRED_DOCS
        ]
        combined = "\n".join(texts)

        return (
            all(texts)
            and "v1.2.2" in combined
            and "Sprint 262" in combined
            and self.BOUNDARY in combined
            and self.NEXT_BOUNDARY in combined
            and "companion" in combined
            and (
                "native process-role classification"
                in combined
            )
            and "count allowance removed" in combined
            and "live model handoff rehearsal" in combined
        )

    def _facts(
        self,
    ) -> dict[str, bool]:
        product = self.manager.product_status()
        browser = self.manager.browser_route_status()
        roles = self.manager.process_role_status()
        rehearsal = self.manager.isolated_rehearsal()
        cli = self._cli_state()
        registry = self._registry_entry()

        manual = self._read(
            "aura/manual_start_stop_status_runtime/"
            "manual_start_stop_status_runtime_executor.py"
        )
        active = self._read(
            "aura/"
            "active_local_runtime_integration_stabilization/"
            "active_local_runtime_integration_contract.py"
        )
        http = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_http_runtime_manager.py"
        )
        session = self._read(
            "aura/browser_chat_session_runtime/"
            "aura_browser_chat_session_runtime_manager.py"
        )

        facts = {
            "identity_version": (
                self._identity_version()
                == self.VERSION
            ),
            "current_sprint": (
                product["current_sprint"]
                == self.CURRENT_SPRINT
            ),
            "boundary": (
                product["boundary"]
                == self.BOUNDARY
            ),
            "next_sprint": (
                product["next_sprint"]
                == self.NEXT_SPRINT
            ),
            "next_boundary": (
                product["next_boundary"]
                == self.NEXT_BOUNDARY
            ),
            "primary_interface": (
                product["primary_interface"]
                == "browser_control_center"
            ),
            "primary_route": (
                product["primary_route"]
                == "companion"
            ),
            "model_endpoint": (
                product["model_endpoint"].endswith(
                    "/model-messages"
                )
            ),
            "explicit_confirmation": (
                product[
                    "explicit_model_confirmation_required"
                ]
                is True
            ),
            "save_only_fallback": (
                product[
                    "save_only_fallback_available"
                ]
                is True
            ),
            "browser_route_available": (
                browser[
                    "model_message_route_available"
                ]
                is True
            ),
            "browser_connected": (
                browser["browser_chat_connected"]
                is True
            ),
            "text_only": (
                browser["model_output_text_only"]
                is True
            ),
            "no_tools": (
                browser["tool_calling_runtime"]
                is False
            ),
            "no_actions": (
                browser["action_dispatch_runtime"]
                is False
            ),
            "no_memory": (
                browser["aura_memory_write_runtime"]
                is False
            ),
            "pair_persistence": (
                "submit_local_model_message"
                in session
                and "LOCAL_MODEL_RESPONSE_KIND"
                in session
            ),
            "http_metadata": (
                "operational_model_handoff_status"
                in http
                and "PRIMARY_MODEL_ROUTE"
                in http
            ),
            "role_source": (
                "classify_main_process_role"
                in manual
                and "PROCESS_ROLE_CONTROL_PLANE"
                in manual
            ),
            "role_live": (
                roles[
                    "native_process_role_classification"
                ]
                is True
            ),
            "runtime_role": (
                roles["synthetic_runtime_role"]
                == "service_runtime"
            ),
            "control_role": (
                roles[
                    "synthetic_control_plane_role"
                ]
                == "control_plane"
            ),
            "foreign_role": (
                roles["synthetic_foreign_role"]
                == "unclassified_main"
            ),
            "strict_count": (
                roles["strict_main_process_count"]
                == 0
            ),
            "allowance_method_removed": (
                "_control_plane_self_allowance"
                not in active
            ),
            "allowance_fields_removed": all(
                marker not in active
                for marker in (
                    (
                        "control_plane_main_"
                        "process_allowance"
                    ),
                    (
                        "effective_strict_"
                        "main_process_count"
                    ),
                    (
                        "control_plane_"
                        "conflict_normalized"
                    ),
                    (
                        "control_plane_"
                        "override_applied"
                    ),
                )
            ),
            "package_files": (
                self._package_files()
                == self.REQUIRED_PACKAGE_FILES
            ),
            "cli_import": (
                cli["imports"] == 1
            ),
            "cli_handler": (
                cli["handlers"] == 1
            ),
            "registry_runtime": (
                isinstance(registry, dict)
                and registry.get("state")
                == "online"
                and registry.get("runtime_level")
                == 'permission_gated_alpha_runtime'
            ),
            "documents": self._documents_valid(),
            "isolated_rehearsal": (
                rehearsal["ok"] is True
                and rehearsal[
                    "model_generate_count"
                ]
                == 1
                and rehearsal["message_count"] == 2
                and rehearsal[
                    "idempotent_replay"
                ]
                is True
            ),
        }

        if len(facts) != self.EXPECTED_DIMENSIONS:
            raise (
                OperationalBrowserChatModelHandoffError(
                    "Sprint 262 dimension count drifted."
                )
            )

        return facts

    def _evaluation(
        self,
    ) -> dict[str, Any]:
        facts = self._facts()
        product = self.manager.product_status()
        browser = self.manager.browser_route_status()
        roles = self.manager.process_role_status()

        common = (
            self._identity_version() == self.VERSION,
            (
                self._package_files()
                == self.REQUIRED_PACKAGE_FILES
            ),
            self._cli_state()["imports"] == 1,
            self._cli_state()["handlers"] == 1,
            self._registry_entry() is not None,
            product["runtime_mutated"] is False,
            browser["runtime_mutated"] is False,
            roles["runtime_mutated"] is False,
            product["localhost_only"] is True,
            product["model_download_enabled"] is False,
            (
                product["network_fallback_enabled"]
                is False
            ),
        )

        dimensions = {}
        assertion_count = 0
        failed_count = 0

        for name, primary in facts.items():
            checks = (primary, *common)

            if (
                len(checks)
                != self.ASSERTIONS_PER_DIMENSION
            ):
                raise (
                    OperationalBrowserChatModelHandoffError(
                        "Sprint 262 assertion shape drifted."
                    )
                )

            passed = sum(
                value is True
                for value in checks
            )
            failed = len(checks) - passed
            assertion_count += len(checks)
            failed_count += failed
            dimensions[name] = {
                "assertion_count": len(checks),
                "passed_assertion_count": passed,
                "failed_assertion_count": failed,
                "secure": failed == 0,
            }

        findings = [
            name
            for name, value in dimensions.items()
            if not value["secure"]
        ]

        return {
            "dimensions": dimensions,
            "assertion_count": assertion_count,
            "failed_assertion_count": failed_count,
            "dimension_count": len(dimensions),
            "finding_count": len(findings),
            "findings": findings,
        }

    def check(
        self,
    ) -> dict[str, Any]:
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
            "operational_handoff_ready": secure,
            "block_release_ready": False,
            "live_model_handoff_rehearsal_required": True,
            "runtime_activated": False,
            "network_connection_opened": False,
            "model_request_executed": False,
            "runtime_mutated": False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        check = self.check()

        return {
            **self.manager.product_status(),
            "operational_handoff_ready": (
                check["operational_handoff_ready"]
            ),
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check[
                "dimension_count"
            ],
            "status_valid": check["status_valid"],
        }

    def context(
        self,
    ) -> dict[str, Any]:
        return {
            **self.manager.product_status(),
            "browser_route": (
                self.manager.browser_route_status()
            ),
            "process_roles": (
                self.manager.process_role_status()
            ),
            "live_model_handoff_rehearsal_required": True,
            "runtime_mutated": False,
        }

    def review(
        self,
    ) -> dict[str, Any]:
        check = self.check()

        return {
            "ok": check["status_valid"],
            "review_state": (
                "approved"
                if check["status_valid"]
                else "changes_required"
            ),
            "finding_count": check[
                "finding_count"
            ],
            "findings": check["findings"],
            "native_process_role_classification": True,
            "count_allowance_removed": True,
            "runtime_mutated": False,
        }

    def preview(
        self,
    ) -> dict[str, Any]:
        return {
            "status": "preview",
            "product": self.manager.product_status(),
            "browser_route": (
                self.manager.browser_route_status()
            ),
            "process_roles": (
                self.manager.process_role_status()
            ),
            "source_mutated": False,
            "runtime_activated": False,
            "network_connection_opened": False,
            "model_request_executed": False,
            "repository_committed": False,
            "repository_pushed": False,
        }
