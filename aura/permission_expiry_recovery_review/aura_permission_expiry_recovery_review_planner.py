
from __future__ import annotations

import ast
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuraPermissionExpiryRecoveryReviewPlanner:
    VERSION = "1.0.9-genesis"
    ANCHOR_VERSION = "1.0.8-genesis"
    CURRENT_SPRINT = 249
    NEXT_SPRINT = 250
    NEXT_VERSION = "1.1.0"
    BOUNDARY = "permission_expiry_recovery_review"
    NEXT_BOUNDARY = "backup_restore_rehearsal"
    OWNER = "AuraPermissionExpiryRecoveryReviewPlanner"
    CONTRACT_MODE = "read_only_permission_lifecycle_review"
    REVIEW_MODE = "source_contract_evidence_snapshot"
    EXPECTED_ASSERTION_COUNT = 96
    ACTIVE_PERMISSION_ANCHOR_ASSERTIONS = 3115
    REVIEW_STATES = (
        "secure",
        "review",
        "warning",
        "unavailable",
    )
    STATE_PRIORITY = {
        "secure": 0,
        "review": 1,
        "warning": 2,
        "unavailable": 3,
    }
    DIMENSION_ORDER = (
        "grant_lifecycle",
        "expiry_enforcement",
        "stale_grant_rejection",
        "denial_lifecycle",
        "revoke_visibility",
        "recovery_visibility",
        "rollback_emergency_stop_linkage",
        "audit_linkage",
    )
    DIMENSION_SPECS = {
        "grant_lifecycle": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_runtime_grant_gate_review/aura_permission_runtime_grant_gate_review_foundation_manager.py",
            ),
            "groups": (
                ("grant_create_or_apply", ("grant_create", "grant_apply", "grant_created", "grant_applied")),
                ("manual_approval", ("manual_approval", "explicit_approval", "creator_approval")),
                ("scope_binding", ("scope_binding", "grant_scope", "permission_scope")),
                ("default_deny", ("default_deny", "deny_by_default", "permission_denied")),
            ),
        },
        "expiry_enforcement": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_runtime_grant_gate_review/aura_permission_runtime_grant_gate_review_foundation_manager.py",
                "aura/permission_workflow/unified_permission_workflow_manager.py",
            ),
            "groups": (
                ("expiry_contract", ("grant_expiry", "permission_expiry", "expiry_boundary")),
                ("expired_state", ("expired_grant", "expired_planned", "expired")),
                ("expiry_blocks_reuse", ("no_expired_grant_reuse", "expired_grant_reuse_allowed", "expired_grant_blocks")),
                ("expiry_visibility", ("dashboard_visibility_expired", "expiry_visible", "expiry_status")),
            ),
        },
        "stale_grant_rejection": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/service_permission_gate_runtime_boundary/aura_service_permission_gate_runtime_boundary_manager.py",
            ),
            "groups": (
                ("stale_marker", ("stale_grant", "stale permission", "stale_permission")),
                ("reuse_rejected", ("no_expired_grant_reuse", "reuse_blocked", "reuse_denied")),
                ("safe_idle_fallback", ("stale_grant_returns_safe_idle", "safe_idle", "safe-idle")),
                ("audit_visibility", ("stale_grant_audit", "audit_link", "audit_visibility")),
            ),
        },
        "denial_lifecycle": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_workflow/unified_permission_workflow_manager.py",
                "aura/permission_runtime_grant_gate_review/aura_permission_runtime_grant_gate_review_foundation_manager.py",
            ),
            "groups": (
                ("denial_state", ("denial", "denied_planned", "permission_denied")),
                ("denial_reason", ("denial_reason", "deny_reason", "reason_required")),
                ("denial_safe_idle", ("denial_safe_idle", "safe_idle", "safe-idle")),
                ("denial_visibility", ("dashboard_visibility_denied", "denial_visibility", "denial_status")),
            ),
        },
        "revoke_visibility": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_runtime_grant_gate_review/aura_permission_runtime_grant_gate_review_foundation_manager.py",
                "aura/permission_audit_recovery_visibility_runtime/aura_permission_audit_recovery_visibility_runtime_manager.py",
            ),
            "groups": (
                ("revoke_contract", ("grant_revoke", "grant_revocation", "revoke_runtime")),
                ("revoked_state", ("revoked_grant", "grants_revoked", "permission_scopes_revoked")),
                ("revoke_visibility", ("dashboard_visibility_revoked", "revoke_visibility", "revoke_status")),
                ("revoke_no_mutation", ("no_permission_grant_revoked_runtime", "revoke_disabled", "runtime_permission_grants_revoked")),
            ),
        },
        "recovery_visibility": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_audit_recovery_visibility_runtime/aura_permission_audit_recovery_visibility_runtime_manager.py",
                "aura/runtime_recovery_drill_boundary_review/aura_runtime_recovery_drill_boundary_review_foundation_manager.py",
            ),
            "groups": (
                ("recovery_snapshot", ("recovery_snapshot", "recovery_status", "recovery_visibility")),
                ("safe_idle_recovery", ("safe_idle_recovery", "safe-idle recovery", "safe_idle")),
                ("recovery_drill", ("recovery_drill", "drill_boundary", "recovery rehearsal")),
                ("no_recovery_execute", ("no_recovery_execute", "recovery_runtime_disabled", "runtime_safe_idle_recoveries_started")),
            ),
        },
        "rollback_emergency_stop_linkage": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_audit_recovery_visibility_runtime/aura_permission_audit_recovery_visibility_runtime_manager.py",
            ),
            "groups": (
                ("rollback_contract", ("rollback_emergency_stop_recovery", "rollback_request_schema", "rollback_preview_schema")),
                ("emergency_stop", ("emergency_stop", "emergency-stop", "emergency stop")),
                ("safe_idle_destination", ("safe_idle_destination", "safe_idle_transition", "safe-idle")),
                ("no_rollback_execute", ("no_rollback_execution", "rollback_execution_active", "rollback_execution_runtime")),
            ),
        },
        "audit_linkage": {
            "sources": (
                "aura/permissions/active_permission_runtime_planner.py",
                "aura/permissions/active_permission_runtime_alpha_manager.py",
                "aura/permission_audit_recovery_visibility_runtime/aura_permission_audit_recovery_visibility_runtime_manager.py",
                "aura/runtime_permission_audit_writer_boundary_review/aura_runtime_permission_audit_writer_boundary_review_foundation_manager.py",
            ),
            "groups": (
                ("audit_link", ("audit_link", "permission_audit", "audit_reference")),
                ("audit_visibility", ("audit_snapshot", "audit_visibility", "audit_status")),
                ("audit_failure_safe_idle", ("audit_failure_safe_idle", "safe_idle_on_audit", "audit_failure")),
                ("audit_write_disabled", ("audit_write_disabled", "no_audit_write", "audit_writer_runtime")),
            ),
        },
    }

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self._source_cache: dict[str, dict[str, Any]] = {}
        self._packet = self._build_review_packet()
        self._packet["review_digest"] = self._packet_digest(self._packet)

    @classmethod
    def _state_valid(cls, value: object) -> bool:
        return value in cls.REVIEW_STATES

    @classmethod
    def _worst_state(
        cls,
        states: list[str] | tuple[str, ...],
    ) -> str:
        if not states:
            return "unavailable"

        return max(
            states,
            key=lambda state: cls.STATE_PRIORITY.get(
                state,
                cls.STATE_PRIORITY["unavailable"],
            ),
        )

    @staticmethod
    def _packet_digest(packet: dict[str, Any]) -> str:
        canonical = json.dumps(
            packet,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    @staticmethod
    def _timestamp_valid(value: object) -> bool:
        if not isinstance(value, str):
            return False

        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return False

        return (
            parsed.tzinfo is not None
            and parsed.utcoffset() is not None
        )

    def _source_packet(self, relative: str) -> dict[str, Any]:
        cached = self._source_cache.get(relative)

        if cached is not None:
            return cached

        path = self.project_root / relative
        exists = path.is_file()
        readable = exists and os.access(path, os.R_OK)
        text = ""
        ast_valid = False
        sha256 = None
        class_names: list[str] = []
        function_names: list[str] = []

        if readable:
            text = path.read_text(
                encoding="utf-8",
                errors="strict",
            )
            sha256 = hashlib.sha256(
                text.encode("utf-8")
            ).hexdigest()

            try:
                tree = ast.parse(text, filename=str(path))
            except SyntaxError:
                ast_valid = False
            else:
                ast_valid = True
                class_names = sorted(
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef)
                )
                function_names = sorted(
                    {
                        node.name
                        for node in ast.walk(tree)
                        if isinstance(
                            node,
                            (
                                ast.FunctionDef,
                                ast.AsyncFunctionDef,
                            ),
                        )
                    }
                )

        packet = {
            "relative_path": relative,
            "exists": exists,
            "readable": readable,
            "ast_valid": ast_valid,
            "sha256": sha256,
            "size_bytes": len(text.encode("utf-8")),
            "class_count": len(class_names),
            "function_count": len(function_names),
            "class_names": class_names[:20],
            "function_names": function_names[:40],
            "_text": text,
        }
        self._source_cache[relative] = packet
        return packet

    @staticmethod
    def _group_evidence(
        text: str,
        markers: tuple[str, ...],
    ) -> dict[str, Any]:
        lowered = text.lower()
        hits = [
            marker
            for marker in markers
            if marker.lower() in lowered
        ]

        return {
            "markers": list(markers),
            "hit_count": len(hits),
            "hits": hits,
            "satisfied": bool(hits),
        }

    def _dimension_packet(
        self,
        dimension_id: str,
        spec: dict[str, Any],
    ) -> dict[str, Any]:
        sources = [
            self._source_packet(relative)
            for relative in spec["sources"]
        ]
        combined = "\n".join(
            source["_text"]
            for source in sources
            if source["readable"]
        )
        groups = [
            {
                "id": group_id,
                **self._group_evidence(
                    combined,
                    markers,
                ),
            }
            for group_id, markers in spec["groups"]
        ]
        readable_count = sum(
            source["readable"]
            for source in sources
        )
        ast_valid_count = sum(
            source["ast_valid"]
            for source in sources
        )
        satisfied_count = sum(
            group["satisfied"]
            for group in groups
        )

        if readable_count == 0:
            state = "unavailable"
        elif satisfied_count == len(groups):
            state = "secure"
        elif satisfied_count > 0:
            state = "review"
        else:
            state = "warning"

        public_sources = [
            {
                key: value
                for key, value in source.items()
                if key != "_text"
            }
            for source in sources
        ]

        return {
            "id": dimension_id,
            "state": state,
            "source_count": len(sources),
            "readable_source_count": readable_count,
            "ast_valid_source_count": ast_valid_count,
            "required_group_count": len(groups),
            "satisfied_group_count": satisfied_count,
            "missing_group_ids": [
                group["id"]
                for group in groups
                if not group["satisfied"]
            ],
            "groups": groups,
            "sources": public_sources,
        }

    @staticmethod
    def _runtime_boundary() -> dict[str, bool]:
        return {
            "permission_store_mutation_enabled": False,
            "grant_creation_enabled": False,
            "grant_application_enabled": False,
            "grant_revocation_enabled": False,
            "expiry_application_enabled": False,
            "denial_creation_enabled": False,
            "denial_application_enabled": False,
            "recovery_execution_enabled": False,
            "rollback_execution_enabled": False,
            "emergency_stop_execution_enabled": False,
            "audit_write_enabled": False,
            "file_write_enabled": False,
            "network_access_enabled": False,
            "process_control_enabled": False,
            "service_activation_enabled": False,
            "socket_activation_enabled": False,
            "systemd_mutation_enabled": False,
            "command_execution_enabled": False,
        }

    def _data_topology(self) -> dict[str, Any]:
        candidates = (
            "data/permissions",
            "data/audit",
            "data/recovery",
        )
        records = []

        for relative in candidates:
            path = self.project_root / relative
            records.append(
                {
                    "relative_path": relative,
                    "exists": path.exists(),
                    "is_directory": path.is_dir(),
                }
            )

        return {
            "candidate_count": len(records),
            "records": records,
            "existing_count": sum(
                record["exists"]
                for record in records
            ),
            "content_read": False,
            "mutation_performed": False,
        }

    def _build_review_packet(self) -> dict[str, Any]:
        dimensions = [
            self._dimension_packet(
                dimension_id,
                self.DIMENSION_SPECS[dimension_id],
            )
            for dimension_id in self.DIMENSION_ORDER
        ]
        state_counts = {
            state: sum(
                item["state"] == state
                for item in dimensions
            )
            for state in self.REVIEW_STATES
        }
        overall_state = self._worst_state(
            [
                item["state"]
                for item in dimensions
            ]
        )
        findings = [
            {
                "dimension": item["id"],
                "state": item["state"],
                "missing_group_ids": list(
                    item["missing_group_ids"]
                ),
            }
            for item in dimensions
            if item["state"] != "secure"
        ]

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "review_mode": self.REVIEW_MODE,
            "captured_at": datetime.now(
                timezone.utc
            ).astimezone().isoformat(),
            "project_root": str(self.project_root),
            "active_permission_anchor_assertions": (
                self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS
            ),
            "review_states": list(self.REVIEW_STATES),
            "dimension_count": len(dimensions),
            "dimensions": dimensions,
            "overall_state": overall_state,
            "state_counts": state_counts,
            "finding_count": len(findings),
            "findings": findings,
            "runtime_boundary": self._runtime_boundary(),
            "data_topology": self._data_topology(),
            "source_contract": {
                "python_source_read_only": True,
                "ast_inspection_only": True,
                "permission_store_content_read": False,
                "audit_store_content_read": False,
                "recovery_store_content_read": False,
                "permission_runtime_imported": False,
                "permission_runtime_executed": False,
                "subprocess_used": False,
                "network_access_used": False,
                "file_mutation_used": False,
            },
        }

    def snapshot(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._packet))

    def review(self) -> dict[str, Any]:
        return self.snapshot()

    def status(self) -> dict[str, Any]:
        packet = self._packet
        valid = all(
            (
                self._timestamp_valid(
                    packet["captured_at"]
                ),
                self._state_valid(
                    packet["overall_state"]
                ),
                packet["dimension_count"] == 8,
                sum(
                    packet["state_counts"].values()
                )
                == packet["dimension_count"],
                len(packet["review_digest"]) == 64,
            )
        )

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "review_mode": self.REVIEW_MODE,
            "status_valid": valid,
            "alpha_ready": valid,
            "captured_at": packet["captured_at"],
            "overall_state": packet["overall_state"],
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            **packet["runtime_boundary"],
        }

    def context(self) -> dict[str, Any]:
        packet = self._packet

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "review_states": list(
                self.REVIEW_STATES
            ),
            "dimension_ids": [
                item["id"]
                for item in packet["dimensions"]
            ],
            "active_permission_anchor_assertions": (
                self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS
            ),
            "runtime_boundary": dict(
                packet["runtime_boundary"]
            ),
            "source_contract": dict(
                packet["source_contract"]
            ),
            "scope_boundary": {
                "read_only_review_only": True,
                "permission_store_mutation_deferred": True,
                "grant_and_denial_mutation_deferred": True,
                "expiry_application_deferred": True,
                "recovery_and_rollback_execution_deferred": True,
                "audit_write_deferred": True,
                "backup_restore_rehearsal_next": True,
            },
        }

    def check(self) -> dict[str, Any]:
        packet = self._packet
        status = self.status()
        context = self.context()
        dimensions = packet["dimensions"]
        runtime = packet["runtime_boundary"]
        source = packet["source_contract"]
        topology = packet["data_topology"]
        dimension_map = {
            item["id"]: item
            for item in dimensions
        }
        expected_ids = set(self.DIMENSION_ORDER)
        checks: list[tuple[str, bool]] = []

        def add(name: str, value: object) -> None:
            checks.append((name, value is True))

        # Core contract: 16.
        add("version", status["version"] == self.VERSION)
        add(
            "anchor_version",
            status["anchor_version"]
            == self.ANCHOR_VERSION,
        )
        add(
            "current_sprint",
            status["current_sprint"]
            == self.CURRENT_SPRINT,
        )
        add(
            "next_sprint",
            status["next_sprint"]
            == self.NEXT_SPRINT,
        )
        add(
            "next_version",
            status["next_version"]
            == self.NEXT_VERSION,
        )
        add(
            "boundary",
            status["boundary"] == self.BOUNDARY,
        )
        add(
            "next_boundary",
            status["next_boundary"]
            == self.NEXT_BOUNDARY,
        )
        add(
            "contract_mode",
            status["contract_mode"]
            == self.CONTRACT_MODE,
        )
        add(
            "review_mode",
            status["review_mode"]
            == self.REVIEW_MODE,
        )
        add("owner", status["owner"] == self.OWNER)
        add(
            "captured_at_valid",
            self._timestamp_valid(
                status["captured_at"]
            ),
        )
        add(
            "status_valid",
            status["status_valid"] is True,
        )
        add(
            "alpha_ready",
            status["alpha_ready"] is True,
        )
        add(
            "overall_state_valid",
            self._state_valid(
                status["overall_state"]
            ),
        )
        add(
            "dimension_count",
            status["dimension_count"] == 8,
        )
        add(
            "state_count_total",
            sum(status["state_counts"].values())
            == 8,
        )

        # Dimension structure: 16.
        add(
            "dimension_ids_exact",
            set(dimension_map) == expected_ids,
        )
        add(
            "dimension_order_exact",
            tuple(
                item["id"]
                for item in dimensions
            )
            == self.DIMENSION_ORDER,
        )
        add(
            "dimension_states_valid",
            all(
                self._state_valid(item["state"])
                for item in dimensions
            ),
        )
        add(
            "dimension_source_counts_positive",
            all(
                item["source_count"] >= 3
                for item in dimensions
            ),
        )
        add(
            "dimension_readable_sources_positive",
            all(
                item["readable_source_count"] >= 1
                for item in dimensions
            ),
        )
        add(
            "dimension_ast_sources_positive",
            all(
                item["ast_valid_source_count"] >= 1
                for item in dimensions
            ),
        )
        add(
            "dimension_group_counts_exact",
            all(
                item["required_group_count"] == 4
                for item in dimensions
            ),
        )
        add(
            "dimension_evidence_present",
            all(
                item["satisfied_group_count"] >= 1
                for item in dimensions
            ),
        )
        add(
            "dimension_missing_groups_valid",
            all(
                len(item["missing_group_ids"])
                == (
                    item["required_group_count"]
                    - item["satisfied_group_count"]
                )
                for item in dimensions
            ),
        )
        add(
            "dimension_source_metadata_valid",
            all(
                source_item["exists"]
                and source_item["readable"]
                and source_item["ast_valid"]
                and isinstance(
                    source_item["sha256"],
                    str,
                )
                and len(source_item["sha256"]) == 64
                for item in dimensions
                for source_item in item["sources"]
            ),
        )
        add(
            "dimension_source_sizes_positive",
            all(
                source_item["size_bytes"] > 0
                for item in dimensions
                for source_item in item["sources"]
            ),
        )
        add(
            "dimension_group_ids_unique",
            all(
                len(
                    {
                        group["id"]
                        for group in item["groups"]
                    }
                )
                == item["required_group_count"]
                for item in dimensions
            ),
        )
        add(
            "dimension_group_hit_counts_valid",
            all(
                group["hit_count"]
                == len(group["hits"])
                for item in dimensions
                for group in item["groups"]
            ),
        )
        add(
            "dimension_group_satisfaction_valid",
            all(
                group["satisfied"]
                is bool(group["hits"])
                for item in dimensions
                for group in item["groups"]
            ),
        )
        add(
            "finding_count_consistent",
            packet["finding_count"]
            == sum(
                item["state"] != "secure"
                for item in dimensions
            ),
        )
        add(
            "overall_state_consistent",
            packet["overall_state"]
            == self._worst_state(
                [
                    item["state"]
                    for item in dimensions
                ]
            ),
        )

        # Per-dimension evidence: 16.
        for dimension_id in self.DIMENSION_ORDER:
            item = dimension_map[dimension_id]
            add(
                f"{dimension_id}_readable",
                item["readable_source_count"] >= 1,
            )
            add(
                f"{dimension_id}_evidence",
                item["satisfied_group_count"] >= 1,
            )

        # State-count and topology: 12.
        for state in self.REVIEW_STATES:
            add(
                f"{state}_count_consistent",
                packet["state_counts"][state]
                == sum(
                    item["state"] == state
                    for item in dimensions
                ),
            )
        add(
            "health_count_sum",
            sum(packet["state_counts"].values())
            == len(dimensions),
        )
        add(
            "review_digest_length",
            len(packet["review_digest"]) == 64,
        )
        add(
            "anchor_assertion_count",
            packet[
                "active_permission_anchor_assertions"
            ]
            == self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS,
        )
        add(
            "topology_candidate_count",
            topology["candidate_count"] == 3,
        )
        add(
            "topology_records_count",
            len(topology["records"]) == 3,
        )
        add(
            "topology_content_not_read",
            topology["content_read"] is False,
        )
        add(
            "topology_not_mutated",
            topology["mutation_performed"] is False,
        )
        add(
            "context_dimension_ids",
            set(context["dimension_ids"])
            == expected_ids,
        )

        # Source boundaries: 10.
        add(
            "python_source_read_only",
            source["python_source_read_only"]
            is True,
        )
        add(
            "ast_inspection_only",
            source["ast_inspection_only"] is True,
        )
        add(
            "permission_store_content_not_read",
            source[
                "permission_store_content_read"
            ]
            is False,
        )
        add(
            "audit_store_content_not_read",
            source["audit_store_content_read"]
            is False,
        )
        add(
            "recovery_store_content_not_read",
            source["recovery_store_content_read"]
            is False,
        )
        add(
            "permission_runtime_not_imported",
            source["permission_runtime_imported"]
            is False,
        )
        add(
            "permission_runtime_not_executed",
            source["permission_runtime_executed"]
            is False,
        )
        add(
            "subprocess_not_used",
            source["subprocess_used"] is False,
        )
        add(
            "network_not_used",
            source["network_access_used"] is False,
        )
        add(
            "file_mutation_not_used",
            source["file_mutation_used"] is False,
        )

        # Runtime mutation boundary: 18.
        for key, value in runtime.items():
            add(
                f"{key}_disabled",
                value is False,
            )

        # Cross-boundary requirements: 8.
        scope = context["scope_boundary"]
        add(
            "scope_read_only",
            scope["read_only_review_only"] is True,
        )
        add(
            "permission_store_mutation_deferred",
            scope[
                "permission_store_mutation_deferred"
            ]
            is True,
        )
        add(
            "grant_denial_mutation_deferred",
            scope[
                "grant_and_denial_mutation_deferred"
            ]
            is True,
        )
        add(
            "expiry_application_deferred",
            scope["expiry_application_deferred"]
            is True,
        )
        add(
            "recovery_rollback_deferred",
            scope[
                "recovery_and_rollback_execution_deferred"
            ]
            is True,
        )
        add(
            "audit_write_deferred",
            scope["audit_write_deferred"] is True,
        )
        add(
            "backup_restore_next",
            scope["backup_restore_rehearsal_next"]
            is True,
        )
        add(
            "next_version_v1_1_0",
            context["next_version"] == "1.1.0",
        )

        failed = [
            name
            for name, passed in checks
            if not passed
        ]

        return {
            "owner": self.OWNER,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": self.CONTRACT_MODE,
            "review_mode": self.REVIEW_MODE,
            "base_check_count": len(checks),
            "assertion_count": len(checks),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "status_valid": status["status_valid"],
            "alpha_ready": (
                len(checks)
                == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "overall_state": packet["overall_state"],
            "dimension_count": packet[
                "dimension_count"
            ],
            "state_counts": dict(
                packet["state_counts"]
            ),
            "finding_count": packet[
                "finding_count"
            ],
            "review_digest": packet[
                "review_digest"
            ],
            "active_permission_anchor_assertions": (
                self.ACTIVE_PERMISSION_ANCHOR_ASSERTIONS
            ),
            **runtime,
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in checks
            ],
        }

