"""Sprint 261 roadmap reconfirmation contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import ast
import json
import re

from .roadmap_reconfirmation_alpha_manager import (
    RoadmapReconfirmationAlphaManager,
)


class RoadmapReconfirmationError(RuntimeError):
    """Raised when the canonical roadmap is not ready."""


class RoadmapReconfirmationContract:
    """Validate the v1.2.1 to v1.3.0 product roadmap."""

    VERSION = "1.2.1"
    ANCHOR_VERSION = "1.2.0"
    CURRENT_SPRINT = 261
    NEXT_SPRINT = 262
    BOUNDARY = "roadmap_reconfirmation_after_v1_2_0"
    NEXT_BOUNDARY = "operational_browser_chat_model_handoff"
    BLOCK = "daily_chat_control_center_productization"
    BLOCK_START = 261
    BLOCK_END = 270
    RELEASE_TARGET = "1.3.0"
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_DIMENSIONS = 30
    EXPECTED_ASSERTIONS = 360

    REQUIRED_PACKAGE_FILES = (
        "__init__.py",
        "roadmap_reconfirmation_alpha_manager.py",
        "roadmap_reconfirmation_cli.py",
        "roadmap_reconfirmation_contract.py",
        "roadmap_reconfirmation_planner.py",
    )

    REQUIRED_DOCS = (
        "README.md",
        "docs/AURA_ROADMAP_RECONFIRMATION_AFTER_V1_2_0.md",
        "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
        "docs/AURA_CAPABILITY_REGISTRY.md",
        "docs/AURA_ACTIVE_LOCAL_RUNTIME_INTEGRATION_STABILIZATION.md",
        "docs/AURA_MASTER_ROADMAP.md",
        "docs/AURA_GENESIS_FINAL_AND_POST_GENESIS_ROADMAP.md",
        "docs/AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md",
        "docs/AURA_GENESIS_TO_POST_GENESIS_PRODUCT_PLAN.md",
        "docs/AURA_LOCAL_MODEL_ROUTER_ACTIVATION.md",
        "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
    )

    REQUIRED_COMMANDS = (
        "roadmap-reconfirmation-status",
        "roadmap-reconfirmation-context",
        "roadmap-reconfirmation-check",
        "roadmap-reconfirmation-review",
        "roadmap-reconfirmation-preview",
        "roadmap-live-acceptance-policy",
        "roadmap-gap-ownership",
        "roadmap-reconfirmation-isolated-rehearsal",
    )

    def __init__(
        self,
        *,
        project_root: Path | None = None,
    ) -> None:
        self.project_root = (
            project_root or Path.cwd()
        ).resolve()
        self.manager = (
            RoadmapReconfirmationAlphaManager(
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
        text = self._read(
            "aura/personality/identity.yaml"
        )
        matches = re.findall(
            r"(?m)^version:\s*([^\s#]+)",
            text,
        )

        return (
            matches[-1]
            if matches
            else None
        )

    def _package_files(
        self,
    ) -> set[str]:
        package = (
            self.project_root
            / "aura"
            / "roadmap_reconfirmation_after_v1_2_0"
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
    ) -> dict[str, Any]:
        path = (
            self.project_root
            / "aura"
            / "core"
            / "cli.py"
        )

        if not path.is_file():
            return {
                "import_count": 0,
                "handler_call_count": 0,
            }

        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        import_count = 0
        handler_call_count = 0

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                == (
                    "aura."
                    "roadmap_reconfirmation_after_v1_2_0."
                    "roadmap_reconfirmation_cli"
                )
            ):
                import_count += 1
            elif isinstance(node, ast.Call):
                function = node.func

                if (
                    isinstance(function, ast.Name)
                    and function.id
                    == (
                        "handle_roadmap_reconfirmation_"
                        "after_v1_2_0_command"
                    )
                ):
                    handler_call_count += 1

        return {
            "import_count": import_count,
            "handler_call_count": handler_call_count,
        }

    def _registry_entry(
        self,
    ) -> dict[str, Any] | None:
        path = (
            self.project_root
            / "aura"
            / "capability_registry"
            / "capability_registry_manager.py"
        )

        if not path.is_file():
            return None

        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )

        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue

            try:
                packet = ast.literal_eval(node)
            except (
                ValueError,
                TypeError,
                SyntaxError,
            ):
                continue

            if (
                isinstance(packet, dict)
                and packet.get("id")
                == (
                    "roadmap_reconfirmation_"
                    "after_v1_2_0"
                )
            ):
                return packet

        return None

    def _document_state(
        self,
    ) -> dict[str, Any]:
        documents = {
            relative: self._read(relative)
            for relative in self.REQUIRED_DOCS
        }
        combined = "\n".join(
            documents.values()
        )

        sequence = self.manager.sprint_sequence()
        sequence_present = all(
            (
                f"Sprint {item['sprint']}"
                in combined
                and item["boundary"]
                in combined
            )
            for item in sequence
        )

        return {
            "all_documents_exist": all(
                bool(text)
                for text in documents.values()
            ),
            "version_present": (
                "v1.2.1" in combined
            ),
            "sprint_261_present": (
                "Sprint 261" in combined
            ),
            "next_sprint_present": (
                "Sprint 262" in combined
            ),
            "boundary_present": (
                self.BOUNDARY in combined
            ),
            "next_boundary_present": (
                self.NEXT_BOUNDARY in combined
            ),
            "block_present": (
                self.BLOCK in combined
            ),
            "release_target_present": (
                "v1.3.0" in combined
            ),
            "sequence_present": sequence_present,
            "acceptance_policy_present": all(
                marker in combined
                for marker in (
                    "live end-to-end acceptance",
                    "failure/recovery",
                    "safe-idle",
                    "contract-only",
                )
            ),
            "gap_ownership_present": all(
                marker in combined
                for marker in (
                    "Sprint 262",
                    "Sprint 263",
                    "Sprint 269",
                    "Sprint 270",
                    "process-role classification",
                    "rename/archive/restore",
                    "release harness",
                )
            ),
        }

    def _facts(
        self,
    ) -> dict[str, bool]:
        direction = self.manager.product_direction()
        policy = (
            self.manager.live_acceptance_policy()
        )
        ownership = self.manager.gap_ownership()
        package_files = self._package_files()
        cli = self._cli_state()
        registry = self._registry_entry()
        docs = self._document_state()

        facts = {
            "identity_version": (
                self._identity_version()
                == self.VERSION
            ),
            "current_sprint": (
                direction["current_sprint"]
                == self.CURRENT_SPRINT
            ),
            "boundary": (
                direction["boundary"]
                == self.BOUNDARY
            ),
            "next_sprint": (
                direction["next_sprint"]
                == self.NEXT_SPRINT
            ),
            "next_boundary": (
                direction["next_boundary"]
                == self.NEXT_BOUNDARY
            ),
            "block": (
                direction["block"]
                == self.BLOCK
            ),
            "block_start": (
                direction["block_start_sprint"]
                == self.BLOCK_START
            ),
            "block_end": (
                direction["block_end_sprint"]
                == self.BLOCK_END
            ),
            "release_target": (
                direction["release_target"]
                == self.RELEASE_TARGET
            ),
            "primary_interface": (
                direction["primary_interface"]
                == "browser_control_center"
            ),
            "model_route": (
                direction["primary_model_route"]
                == "companion"
            ),
            "autostart_default": (
                direction["autostart_default"]
                == "disabled"
            ),
            "memory_policy": (
                direction["memory_write_policy"]
                == "review_first"
            ),
            "acceptance_required": (
                policy["required"] is True
            ),
            "real_functionality": (
                policy[
                    "must_prove_real_functionality"
                ]
                is True
            ),
            "user_visible_result": (
                policy[
                    "must_verify_user_visible_results"
                ]
                is True
            ),
            "failure_recovery": (
                policy[
                    "must_test_relevant_failure_recovery"
                ]
                is True
            ),
            "restore_safe_idle": (
                policy["must_restore_safe_idle"]
                is True
            ),
            "before_next_block": (
                policy[
                    "must_finish_before_next_block"
                ]
                is True
            ),
            "contract_only_insufficient": (
                policy["contract_only_is_insufficient"]
                is True
            ),
            "gap_process_owned": (
                ownership["ownership"].get(
                    "native_process_role_classification"
                )
                == 262
            ),
            "gap_session_owned": (
                ownership["ownership"].get(
                    "session_rename_archive_restore"
                )
                == 263
            ),
            "gap_harness_owned": (
                ownership["ownership"].get(
                    "reusable_release_harness"
                )
                == 269
            ),
            "gap_acceptance_owned": (
                ownership["ownership"].get(
                    "live_end_to_end_acceptance"
                )
                == 270
            ),
            "package_files": (
                package_files
                == set(self.REQUIRED_PACKAGE_FILES)
            ),
            "cli_import": (
                cli["import_count"] == 1
            ),
            "cli_dispatch": (
                cli["handler_call_count"] == 1
            ),
            "registry_entry": (
                isinstance(registry, dict)
            ),
            "registry_review_only": (
                isinstance(registry, dict)
                and registry.get("state")
                == "online"
                and (
                    registry.get("runtime_level")
                    == "review_only"
                    or registry.get("review_only")
                    is True
                )
            ),
            "documents": (
                all(docs.values())
            ),
        }

        if len(facts) != self.EXPECTED_DIMENSIONS:
            raise RoadmapReconfirmationError(
                "Roadmap dimension count drifted."
            )

        return facts

    def _evaluation(
        self,
    ) -> dict[str, Any]:
        facts = self._facts()
        common = (
            self._identity_version()
            == self.VERSION,
            self._package_files()
            == set(self.REQUIRED_PACKAGE_FILES),
            self._cli_state()["import_count"] == 1,
            self._cli_state()["handler_call_count"] == 1,
            self._registry_entry() is not None,
            self.manager.product_direction()[
                "runtime_mutated"
            ]
            is False,
            self.manager.live_acceptance_policy()[
                "runtime_mutated"
            ]
            is False,
            self.manager.gap_ownership()[
                "runtime_mutated"
            ]
            is False,
            self.manager.product_direction()[
                "autostart_default"
            ]
            == "disabled",
            self.manager.product_direction()[
                "primary_model_route"
            ]
            == "companion",
            self.manager.live_acceptance_policy()[
                "must_restore_safe_idle"
            ]
            is True,
        )

        dimensions = {}
        assertion_count = 0
        failed_assertion_count = 0

        for name, primary in facts.items():
            checks = (
                primary,
                *common,
            )

            if (
                len(checks)
                != self.ASSERTIONS_PER_DIMENSION
            ):
                raise RoadmapReconfirmationError(
                    "Assertion shape drifted."
                )

            passed = sum(
                1
                for value in checks
                if value is True
            )
            failed = len(checks) - passed
            assertion_count += len(checks)
            failed_assertion_count += failed
            dimensions[name] = {
                "assertion_count": len(checks),
                "passed_assertion_count": passed,
                "failed_assertion_count": failed,
                "secure": failed == 0,
            }

        findings = [
            name
            for name, item in dimensions.items()
            if not item["secure"]
        ]

        return {
            "dimensions": dimensions,
            "assertion_count": assertion_count,
            "failed_assertion_count": (
                failed_assertion_count
            ),
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
            "block": self.BLOCK,
            "block_start_sprint": self.BLOCK_START,
            "block_end_sprint": self.BLOCK_END,
            "release_target": self.RELEASE_TARGET,
            **evaluation,
            "overall_state": (
                "secure"
                if secure
                else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "roadmap_reconfirmed": secure,
            "block_release_ready": False,
            "end_block_live_acceptance_required": True,
            "runtime_activated": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        check = self.check()

        return {
            **self.manager.product_direction(),
            "roadmap_reconfirmed": check[
                "roadmap_reconfirmed"
            ],
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check[
                "dimension_count"
            ],
            "status_valid": check[
                "status_valid"
            ],
        }

    def context(
        self,
    ) -> dict[str, Any]:
        return {
            **self.manager.product_direction(),
            "sequence": (
                self.manager.sprint_sequence()
            ),
            "gap_ownership": (
                self.manager.gap_ownership()
            ),
            "live_acceptance_policy": (
                self.manager.live_acceptance_policy()
            ),
            "roadmap_reconfirmation_complete": (
                self.check()["roadmap_reconfirmed"]
            ),
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
            "roadmap_reconfirmed": check[
                "roadmap_reconfirmed"
            ],
            "gap_ownership_complete": (
                self.manager.gap_ownership()[
                    "all_gaps_owned"
                ]
            ),
            "live_acceptance_required": True,
            "finding_count": check[
                "finding_count"
            ],
            "findings": check["findings"],
            "runtime_mutated": False,
        }

    def preview(
        self,
    ) -> dict[str, Any]:
        return {
            "status": "preview",
            "product_direction": (
                self.manager.product_direction()
            ),
            "sequence": (
                self.manager.sprint_sequence()
            ),
            "gap_ownership": (
                self.manager.gap_ownership()
            ),
            "live_acceptance_policy": (
                self.manager.live_acceptance_policy()
            ),
            "roadmap_reconfirmed": (
                self.check()["roadmap_reconfirmed"]
            ),
            "source_mutated": False,
            "runtime_activated": False,
            "network_connection_opened": False,
            "repository_committed": False,
            "repository_pushed": False,
        }

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        check = self.check()
        status = self.status()
        context = self.context()
        review = self.review()
        preview = self.preview()

        ok = (
            check["status_valid"] is True
            and status["status_valid"] is True
            and context[
                "roadmap_reconfirmation_complete"
            ]
            is True
            and review["ok"] is True
            and preview[
                "roadmap_reconfirmed"
            ]
            is True
        )

        return {
            "status": (
                "completed"
                if ok
                else "failed"
            ),
            "ok": ok,
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check[
                "dimension_count"
            ],
            "canonical_runtime_used": False,
            "source_mutated": False,
            "runtime_activated": False,
            "network_connection_opened": False,
            "repository_committed": False,
            "repository_pushed": False,
        }
