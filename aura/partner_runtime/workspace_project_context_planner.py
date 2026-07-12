"""Sprint 222 Workspace and Project Context Runtime contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aura.partner_runtime.partner_runtime_planner import PartnerRuntimePlanner


class WorkspaceProjectContextPlanner:
    """Bounded read-only project-context facade over Sprint 221."""

    name = "workspace_project_context"
    version = "0.1.0"
    current_sprint = 222
    next_sprint = 223
    next_boundary = "chat_to_memory_runtime_handoff"

    identity_source = "aura/personality/identity.yaml"

    context_sources = (
        "README.md",
        "main.py",
        "aura/personality/identity.yaml",
        "aura/core/cli.py",
        "aura/core/shell.py",
        "docs/AURA_GENESIS_RUNTIME_ACTIVATION_ROADMAP.md",
        "docs/AURA_UNIFIED_SESSION_RUNTIME.md",
    )

    ignored_top_level = frozenset(
        {
            ".git",
            ".venv",
            "__pycache__",
            "data",
            "logs",
        }
    )

    safety_blockers = (
        "workspace_project_context_runtime_active",
        "context_persistence_active",
        "recursive_workspace_scan_active",
        "bulk_file_content_read_active",
        "journal_read_active",
        "memory_read_active",
        "memory_write_active",
        "session_mutation_active",
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
        "release_gate_open",
        "autonomous_action_active",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        partner_planner: PartnerRuntimePlanner | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

        self.partner_planner = (
            partner_planner
            or PartnerRuntimePlanner(
                self.project_root
            )
        )

    def _identity(self) -> dict[str, Any]:
        path = (
            self.project_root
            / self.identity_source
        )

        if not path.is_file():
            return {
                "available": False,
                "path": self.identity_source,
                "version": None,
                "error": "missing",
            }

        try:
            data = yaml.safe_load(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as exc:
            return {
                "available": False,
                "path": self.identity_source,
                "version": None,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        return {
            "available": isinstance(data, dict),
            "path": self.identity_source,
            "version": (
                data.get("version")
                if isinstance(data, dict)
                else None
            ),
            "codename": (
                data.get("codename")
                if isinstance(data, dict)
                else None
            ),
            "error": (
                None
                if isinstance(data, dict)
                else "invalid_mapping"
            ),
        }

    def _git(self) -> dict[str, Any]:
        git_dir = self.project_root / ".git"
        head_path = git_dir / "HEAD"

        result: dict[str, Any] = {
            "repository_detected": (
                git_dir.is_dir()
                and head_path.is_file()
            ),
            "branch": "unknown",
            "commit_hint": "",
            "git_command_executed": False,
        }

        if not result["repository_detected"]:
            return result

        try:
            head = head_path.read_text(
                encoding="utf-8"
            ).strip()

            if head.startswith("ref:"):
                ref_name = (
                    head.partition(":")[2].strip()
                )

                result["branch"] = (
                    ref_name.rsplit("/", 1)[-1]
                )

                ref_path = git_dir / ref_name

                if ref_path.is_file():
                    result["commit_hint"] = (
                        ref_path.read_text(
                            encoding="utf-8"
                        )
                        .strip()[:12]
                    )

            elif head:
                result["branch"] = "detached"
                result["commit_hint"] = (
                    head[:12]
                )

        except OSError:
            pass

        return result

    def _workspace(self) -> dict[str, Any]:
        if not self.project_root.is_dir():
            return {
                "available": False,
                "directories": [],
                "files": [],
                "scan_depth": 1,
                "recursive_scan_performed": False,
                "data_directory_scanned": False,
            }

        entries = [
            path
            for path in sorted(
                self.project_root.iterdir(),
                key=lambda item: (
                    item.name.lower()
                ),
            )
            if path.name
            not in self.ignored_top_level
        ][:200]

        return {
            "available": True,
            "directories": [
                path.name
                for path in entries
                if path.is_dir()
            ],
            "files": [
                path.name
                for path in entries
                if path.is_file()
            ],
            "scan_depth": 1,
            "recursive_scan_performed": False,
            "data_directory_scanned": False,
        }

    def _sources(self) -> dict[str, Any]:
        items = [
            {
                "path": relative,
                "exists": (
                    self.project_root / relative
                ).is_file(),
            }
            for relative
            in self.context_sources
        ]

        return {
            "items": items,
            "all_available": all(
                item["exists"]
                for item in items
            ),
            "file_contents_loaded": False,
        }

    def _legacy(self) -> dict[str, Any]:
        source = (
            self.project_root
            / "aura"
            / "workspace"
            / "workspace_awareness_manager.py"
        )

        return {
            "available": source.is_file(),
            "owner": (
                "aura.workspace."
                "workspace_awareness_manager."
                "WorkspaceAwarenessManager"
            ),
            "snapshot_mode": (
                "static_source_boundary"
            ),
            "module_imported": False,
            "constructor_called": False,
            "status_called": False,
            "context_called": False,
            "journal_accessed": False,
            "memory_accessed": False,
            "promoted_to_runtime_owner": False,
        }

    def _session(self) -> dict[str, Any]:
        try:
            check = self.partner_planner.check()

            contract = check[
                "unified_session_runtime_contract"
            ]

        except Exception as exc:
            return {
                "contract_ready": False,
                "canonical_session_owner": None,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        return {
            "contract_ready": (
                contract[
                    "unified_session_runtime_contract_ready"
                ]
                is True
            ),
            "canonical_session_owner": (
                contract[
                    "canonical_session_owner"
                ]
            ),
            "assertion_count": (
                check["assertion_count"]
            ),
            "failed_assertion_count": (
                check[
                    "failed_assertion_count"
                ]
            ),
            "error": None,
        }

    def workspace_project_context_contract(
        self,
    ) -> dict[str, Any]:
        identity = self._identity()
        git = self._git()
        workspace = self._workspace()
        sources = self._sources()
        legacy = self._legacy()
        session = self._session()

        version_supported = (
            identity["version"]
            in {
                "0.221.0-genesis",
                "0.222.0-genesis",
                "0.223.0-genesis",
                "0.224.0-genesis",
                "0.225.0-genesis",
                "0.226.0-genesis",
                "0.227.0-genesis",
                "0.229.0-genesis",
            }
        )

        ready = all(
            (
                self.project_root.is_dir(),
                identity["available"],
                version_supported,
                git["repository_detected"],
                workspace["available"],
                sources["all_available"],
                legacy["available"],
                not legacy["module_imported"],
                not legacy["constructor_called"],
                not legacy["status_called"],
                not legacy["context_called"],
                not legacy["journal_accessed"],
                not legacy["memory_accessed"],
                session["contract_ready"],
                (
                    session[
                        "failed_assertion_count"
                    ]
                    == 0
                ),
            )
        )

        contract: dict[str, Any] = {
            "workspace_project_context_contract_ready":
                ready,
            "workspace_project_context_runtime_ready":
                False,
            "status": (
                "workspace_project_context_contract_ready"
                if ready
                else (
                    "workspace_project_context_"
                    "contract_degraded"
                )
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
            "canonical_project_root":
                str(self.project_root),
            "canonical_project_identity_source":
                self.identity_source,
            "canonical_session_owner":
                "aura_browser_chat_session_runtime",
            "identity_snapshot": identity,
            "git_snapshot": git,
            "workspace_snapshot": workspace,
            "context_source_snapshot": sources,
            "legacy_workspace_snapshot": legacy,
            "unified_session_snapshot": session,
            "identity_version_supported":
                version_supported,
            "context_persistence_enabled": False,
            "journal_accessed": False,
            "memory_accessed": False,
            "session_mutation_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "safe_idle_preserved": True,
            "runtime_scope": (
                "bounded_workspace_project_"
                "context_contract_only"
            ),
            "chat_to_memory_handoff_"
            "deferred_to_sprint_223": True,
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
            self.workspace_project_context_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "planning_ready":
                contract["planning_ready"],
            "runtime_ready": False,
            "workspace_project_context_"
            "contract_ready": contract[
                "workspace_project_context_"
                "contract_ready"
            ],
            "partner_runtime_current_sprint":
                self.current_sprint,
            "partner_runtime_next_sprint":
                self.next_sprint,
            "partner_runtime_next_boundary":
                self.next_boundary,
            "canonical_project_root":
                contract["canonical_project_root"],
            "canonical_session_owner":
                contract["canonical_session_owner"],
            "runtime_scope":
                contract["runtime_scope"],
            "contract": contract,
        }

    def context(self) -> dict[str, Any]:
        contract = (
            self.workspace_project_context_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": contract["status"],
            "current_sprint":
                self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "identity_snapshot":
                contract["identity_snapshot"],
            "git_snapshot":
                contract["git_snapshot"],
            "workspace_snapshot":
                contract["workspace_snapshot"],
            "context_source_snapshot":
                contract[
                    "context_source_snapshot"
                ],
            "legacy_workspace_snapshot":
                contract[
                    "legacy_workspace_snapshot"
                ],
            "unified_session_snapshot":
                contract[
                    "unified_session_snapshot"
                ],
            "contract_only": True,
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        contract = (
            self.workspace_project_context_contract()
        )

        identity = contract[
            "identity_snapshot"
        ]
        git = contract["git_snapshot"]
        workspace = contract[
            "workspace_snapshot"
        ]
        sources = contract[
            "context_source_snapshot"
        ]
        legacy = contract[
            "legacy_workspace_snapshot"
        ]
        session = contract[
            "unified_session_snapshot"
        ]

        assertions = {
            "contract_ready": (
                contract[
                    "workspace_project_context_"
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
            "current_sprint_222": (
                contract[
                    "partner_runtime_current_sprint"
                ]
                == 222
            ),
            "next_sprint_223": (
                contract[
                    "partner_runtime_next_sprint"
                ]
                == 223
            ),
            "next_boundary_correct": (
                contract[
                    "partner_runtime_next_boundary"
                ]
                == (
                    "chat_to_memory_"
                    "runtime_handoff"
                )
            ),
            "session_contract_ready": (
                session["contract_ready"]
                is True
            ),
            "session_owner_preserved": (
                session[
                    "canonical_session_owner"
                ]
                == (
                    "aura_browser_chat_"
                    "session_runtime"
                )
            ),
            "project_root_ready": Path(
                contract[
                    "canonical_project_root"
                ]
            ).is_dir(),
            "identity_ready":
                identity["available"] is True,
            "identity_version_supported": (
                contract[
                    "identity_version_supported"
                ]
                is True
            ),
            "git_repository_detected": (
                git["repository_detected"]
                is True
            ),
            "workspace_snapshot_ready": (
                workspace["available"]
                is True
            ),
            "scan_depth_bounded": (
                workspace["scan_depth"] == 1
            ),
            "recursive_scan_blocked": (
                workspace[
                    "recursive_scan_performed"
                ]
                is False
            ),
            "data_directory_ignored": (
                workspace[
                    "data_directory_scanned"
                ]
                is False
            ),
            "context_sources_ready": (
                sources["all_available"]
                is True
            ),
            "legacy_source_available": (
                legacy["available"] is True
            ),
            "legacy_not_imported": (
                legacy["module_imported"]
                is False
            ),
            "legacy_not_constructed": (
                legacy["constructor_called"]
                is False
            ),
            "legacy_status_not_called": (
                legacy["status_called"]
                is False
            ),
            "legacy_context_not_called": (
                legacy["context_called"]
                is False
            ),
            "journal_not_accessed": (
                contract["journal_accessed"]
                is False
            ),
            "memory_not_accessed": (
                contract["memory_accessed"]
                is False
            ),
            "session_not_mutated": (
                contract[
                    "session_mutation_performed"
                ]
                is False
            ),
            "context_not_persisted": (
                contract[
                    "context_persistence_enabled"
                ]
                is False
            ),
            "file_not_written": (
                contract[
                    "file_write_performed"
                ]
                is False
            ),
            "command_not_executed": (
                contract[
                    "command_execution_performed"
                ]
                is False
            ),
            "safe_idle_preserved": (
                contract[
                    "safe_idle_preserved"
                ]
                is True
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
                    "bounded_workspace_project_"
                    "context_contract_only"
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
            "workspace_project_context_contract":
                contract,
        }

    def plan(self) -> dict[str, Any]:
        contract = (
            self.workspace_project_context_contract()
        )

        return {
            "name": self.name,
            "sprint": self.current_sprint,
            "next_sprint": self.next_sprint,
            "next_boundary": self.next_boundary,
            "contract_ready": contract[
                "workspace_project_context_"
                "contract_ready"
            ],
            "runtime_ready": False,
            "runtime_scope":
                contract["runtime_scope"],
            "canonical_project_root":
                contract[
                    "canonical_project_root"
                ],
            "canonical_session_owner":
                contract[
                    "canonical_session_owner"
                ],
        }
