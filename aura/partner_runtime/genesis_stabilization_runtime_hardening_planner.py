from __future__ import annotations

import ast
import hashlib
import time
from pathlib import Path
from typing import Any

from .genesis_final_release_alpha_manager import (
    GenesisFinalReleaseAlphaManager,
)


class GenesisStabilizationRuntimeHardeningPlanner:
    """Read-only Sprint 241 hardening regression owner."""

    VERSION = "1.0.1-genesis"
    CANONICAL_ANCHOR_VERSION = "1.0.0-genesis"

    CURRENT_SPRINT = 241
    NEXT_SPRINT = 242

    BOUNDARY = "genesis_stabilization_runtime_hardening"
    NEXT_BOUNDARY = "service_lifecycle_determinism"

    STATUS_LATENCY_LIMIT_SECONDS = 0.5

    REQUIRED_REGRESSIONS = (
        "codebase_command_allowlist_exact",
        "codebase_unknown_command_guard_before_construction",
        "genesis_final_status_avoids_deep_contract",
        "genesis_final_status_returns_projection",
        "status_projection_repeat_deterministic",
        "status_projection_matches_deep_contract",
        "first_status_within_latency_limit",
        "second_status_within_latency_limit",
        "memory_hash_unchanged",
        "journal_hash_unchanged",
        "runtime_safety_boundary_preserved",
    )

    def __init__(
        self,
        project_root: Path | str | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str | None:
        if not path.exists():
            return None

        hasher = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda: handle.read(1024 * 1024),
                b"",
            ):
                hasher.update(chunk)

        return hasher.hexdigest()

    @staticmethod
    def _class_method(
        tree: ast.Module,
        class_name: str,
        method_name: str,
    ) -> ast.FunctionDef:
        class_node = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef)
                and node.name == class_name
            ),
            None,
        )

        if class_node is None:
            raise RuntimeError(
                f"Class not found: {class_name}"
            )

        method_node = next(
            (
                node
                for node in class_node.body
                if isinstance(node, ast.FunctionDef)
                and node.name == method_name
            ),
            None,
        )

        if method_node is None:
            raise RuntimeError(
                f"Method not found: "
                f"{class_name}.{method_name}"
            )

        return method_node

    @staticmethod
    def _first_executable_statement(
        method: ast.FunctionDef,
    ) -> ast.stmt | None:
        body = list(method.body)

        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(
                body[0].value,
                ast.Constant,
            )
            and isinstance(
                body[0].value.value,
                str,
            )
        ):
            body = body[1:]

        return body[0] if body else None

    def _source_assertions(
        self,
    ) -> dict[str, bool]:
        cli_path = (
            self.project_root
            / "aura/core/cli.py"
        )

        final_planner_path = (
            self.project_root
            / "aura/partner_runtime/"
            "genesis_final_release_planner.py"
        )

        cli_source = cli_path.read_text(
            encoding="utf-8",
        )

        final_source = final_planner_path.read_text(
            encoding="utf-8",
        )

        cli_tree = ast.parse(
            cli_source,
            filename=str(cli_path),
        )

        final_tree = ast.parse(
            final_source,
            filename=str(final_planner_path),
        )

        codebase_handler = self._class_method(
            cli_tree,
            "AuraCLI",
            "handle_codebase_compat_cli_command",
        )

        executable_body = list(
            codebase_handler.body
        )

        if (
            executable_body
            and isinstance(
                executable_body[0],
                ast.Expr,
            )
            and isinstance(
                executable_body[0].value,
                ast.Constant,
            )
            and isinstance(
                executable_body[0].value.value,
                str,
            )
        ):
            executable_body = executable_body[1:]

        allowlist_statement = (
            executable_body[0]
            if len(executable_body) >= 1
            else None
        )

        guard_statement = (
            executable_body[1]
            if len(executable_body) >= 2
            else None
        )

        expected_commands = {
            "codebase-change-status",
            "codebase-change-plan",
            "codebase-impact-review",
            "codebase-patch-proposal-status",
            "codebase-patch-proposal",
            "codebase-patch-safety-packet",
            "codebase-validation-gate-status",
            "codebase-validation-gate-plan",
            "codebase-validation-preflight-gate",
        }

        allowlist_commands: set[str] = set()

        if isinstance(
            allowlist_statement,
            ast.Assign,
        ):
            target_found = any(
                isinstance(target, ast.Name)
                and target.id == "codebase_commands"
                for target in allowlist_statement.targets
            )

            value = allowlist_statement.value

            if (
                target_found
                and isinstance(
                    value,
                    (ast.Set, ast.Tuple, ast.List),
                )
            ):
                allowlist_commands = {
                    item.value
                    for item in value.elts
                    if isinstance(
                        item,
                        ast.Constant,
                    )
                    and isinstance(
                        item.value,
                        str,
                    )
                }

        routed_commands: set[str] = set()

        for node in ast.walk(codebase_handler):
            if (
                isinstance(node, ast.Compare)
                and isinstance(
                    node.left,
                    ast.Name,
                )
                and node.left.id == "command"
                and len(node.ops) == 1
                and isinstance(node.ops[0], ast.Eq)
                and len(node.comparators) == 1
                and isinstance(
                    node.comparators[0],
                    ast.Constant,
                )
                and isinstance(
                    node.comparators[0].value,
                    str,
                )
            ):
                routed_commands.add(
                    node.comparators[0].value
                )

        guard_source = (
            ast.get_source_segment(
                cli_source,
                guard_statement,
            )
            if guard_statement is not None
            else ""
        ) or ""

        guard_returns_false = (
            guard_statement is not None
            and any(
                isinstance(node, ast.Return)
                and isinstance(
                    node.value,
                    ast.Constant,
                )
                and node.value.value is False
                for node in ast.walk(
                    guard_statement
                )
            )
        )

        def called_name(
            node: ast.AST,
        ) -> str:
            if isinstance(node, ast.Name):
                return node.id

            if isinstance(node, ast.Attribute):
                prefix = called_name(node.value)

                return (
                    f"{prefix}.{node.attr}"
                    if prefix
                    else node.attr
                )

            return ""

        constructor_lines: list[int] = []

        for node in ast.walk(codebase_handler):
            if not isinstance(node, ast.Call):
                continue

            leaf = called_name(
                node.func
            ).rsplit(".", 1)[-1]

            if leaf.endswith(
                (
                    "Manager",
                    "Planner",
                    "Registry",
                    "Router",
                    "Store",
                    "Journal",
                )
            ):
                constructor_lines.append(
                    node.lineno
                )

        first_constructor_line = (
            min(constructor_lines)
            if constructor_lines
            else None
        )

        guard_before_construction = (
            guard_statement is not None
            and first_constructor_line is not None
            and guard_statement.end_lineno
            < first_constructor_line
        )

        status_method = self._class_method(
            final_tree,
            "GenesisFinalReleasePlanner",
            "status",
        )

        status_contract_calls = [
            node
            for node in ast.walk(status_method)
            if isinstance(node, ast.Call)
            and (
                (
                    isinstance(
                        node.func,
                        ast.Attribute,
                    )
                    and node.func.attr
                    == "contract"
                )
                or (
                    isinstance(
                        node.func,
                        ast.Name,
                    )
                    and node.func.id
                    == "contract"
                )
            )
        ]

        status_returns = [
            node
            for node in ast.walk(status_method)
            if isinstance(node, ast.Return)
        ]

        return {
            "codebase_command_allowlist_exact": (
                allowlist_commands
                == expected_commands
                and routed_commands
                == expected_commands
            ),
            (
                "codebase_unknown_command_guard_"
                "before_construction"
            ): (
                isinstance(
                    guard_statement,
                    ast.If,
                )
                and "not raw_args" in guard_source
                and (
                    "not in codebase_commands"
                    in guard_source
                )
                and guard_returns_false
                and guard_before_construction
            ),
            "genesis_final_status_avoids_deep_contract": (
                not status_contract_calls
            ),
            "genesis_final_status_returns_projection": (
                len(status_returns) == 1
                and isinstance(
                    status_returns[0].value,
                    ast.Dict,
                )
            ),
        }

    def contract(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version": (
                self.CANONICAL_ANCHOR_VERSION
            ),
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "title": (
                "Genesis Stabilization Runtime Hardening"
            ),
            "status_latency_limit_seconds": (
                self.STATUS_LATENCY_LIMIT_SECONDS
            ),
            "required_regressions": list(
                self.REQUIRED_REGRESSIONS
            ),
            "required_regression_count": len(
                self.REQUIRED_REGRESSIONS
            ),
            "dispatch_pollution_forbidden": True,
            "deep_status_evaluation_forbidden": True,
            "deep_contract_preserved": True,
            "deep_check_preserved": True,
            "memory_write_allowed": False,
            "journal_write_allowed": False,
            "runtime_activation_allowed": False,
            "runtime_activated": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version": (
                self.CANONICAL_ANCHOR_VERSION
            ),
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "dispatch_hardening_applied": True,
            "status_projection_hardening_applied": True,
            "deep_contract_preserved": True,
            "deep_check_preserved": True,
            "regression_check_ready": True,
            "runtime_activation_allowed": False,
            "runtime_activated": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = self.contract()

        return {
            **contract,
            "cli_path": (
                "aura/core/cli.py"
            ),
            "genesis_final_planner_path": (
                "aura/partner_runtime/"
                "genesis_final_release_planner.py"
            ),
            "source_assertions": (
                self._source_assertions()
            ),
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "parts": [
                "reject unrelated command families early",
                (
                    "serve immutable finalized-release "
                    "status projection"
                ),
                (
                    "preserve explicit deep contract "
                    "and deep check paths"
                ),
                (
                    "enforce permanent source and "
                    "runtime regressions"
                ),
            ],
            "runtime_activation_allowed": False,
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        memory_path = (
            self.project_root
            / "data/memory/memories.jsonl"
        )

        journal_path = (
            self.project_root
            / "data/journal/aura_journal.jsonl"
        )

        memory_before = self._sha256(memory_path)
        journal_before = self._sha256(journal_path)

        source_assertions = self._source_assertions()

        manager = GenesisFinalReleaseAlphaManager(
            project_root=self.project_root,
        )

        started = time.perf_counter()
        first_status = manager.status()
        first_status_seconds = (
            time.perf_counter() - started
        )

        started = time.perf_counter()
        second_status = manager.status()
        second_status_seconds = (
            time.perf_counter() - started
        )

        started = time.perf_counter()
        deep_contract = manager.contract()
        deep_contract_seconds = (
            time.perf_counter() - started
        )

        contract_projection = {
            key: deep_contract[key]
            for key in first_status
        }

        memory_after = self._sha256(memory_path)
        journal_after = self._sha256(journal_path)

        assertions = {
            **source_assertions,
            "status_projection_repeat_deterministic": (
                first_status == second_status
            ),
            "status_projection_matches_deep_contract": (
                first_status == contract_projection
            ),
            "first_status_within_latency_limit": (
                first_status_seconds
                < self.STATUS_LATENCY_LIMIT_SECONDS
            ),
            "second_status_within_latency_limit": (
                second_status_seconds
                < self.STATUS_LATENCY_LIMIT_SECONDS
            ),
            "memory_hash_unchanged": (
                memory_before == memory_after
            ),
            "journal_hash_unchanged": (
                journal_before == journal_after
            ),
            "runtime_safety_boundary_preserved": (
                first_status[
                    "runtime_activation_allowed"
                ]
                is False
                and first_status[
                    "runtime_activated"
                ]
                is False
                and first_status[
                    "release_gate_open"
                ]
                is False
                and first_status[
                    "runtime_ready"
                ]
                is False
            ),
        }

        failed_assertions = [
            name
            for name, passed in assertions.items()
            if not passed
        ]

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(
                failed_assertions
            ),
            "failed_assertions": failed_assertions,
            "assertions": assertions,
            "first_status_seconds": (
                first_status_seconds
            ),
            "second_status_seconds": (
                second_status_seconds
            ),
            "deep_contract_seconds": (
                deep_contract_seconds
            ),
            "status_key_count": len(first_status),
            "memory_hash_unchanged": (
                memory_before == memory_after
            ),
            "journal_hash_unchanged": (
                journal_before == journal_after
            ),
            "runtime_activation_allowed": False,
            "runtime_activated": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }
