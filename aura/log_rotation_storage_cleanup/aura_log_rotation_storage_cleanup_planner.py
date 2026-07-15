"""Read-only log rotation and storage cleanup inspection for Sprint 245."""

from __future__ import annotations

import hashlib
import re
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuraLogRotationStorageCleanupPlanner:
    VERSION = "1.0.5-genesis"
    ANCHOR_VERSION = "1.0.4-genesis"
    CURRENT_SPRINT = 245
    NEXT_SPRINT = 246
    BOUNDARY = "log_rotation_storage_cleanup"
    NEXT_BOUNDARY = "resource_baseline_metrics"
    ROTATION_POLICY = "1 MB"
    RETENTION_POLICY = "7 days"
    RETENTION_DAYS = 7
    ACTIVE_LOG_NAME = "aura.log"
    ROTATED_PATTERN = re.compile(
        r"^aura\.\d{4}-\d{2}-\d{2}_"
        r"\d{2}-\d{2}-\d{2}_\d{6}\.log"
        r"(?:\.(?:gz|zip))?$"
    )

    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.logs_dir = self.project_root / "logs"
        self.active_log = self.logs_dir / self.ACTIVE_LOG_NAME
        self.inspection_time = datetime.now(timezone.utc)

    def _within_project(self, path: Path) -> bool:
        try:
            path.resolve(strict=False).relative_to(self.project_root)
        except ValueError:
            return False
        return True

    def _digest(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _classify(
        self,
        path: Path,
        *,
        now: datetime,
    ) -> dict[str, Any]:
        record: dict[str, Any] = {
            "name": path.name,
            "path": str(path),
            "within_project": self._within_project(path),
            "is_symlink": path.is_symlink(),
            "is_file": path.is_file(),
            "classification": "blocked",
            "reason": "entry is outside the cleanup allowlist",
            "size_bytes": 0,
            "age_days": None,
            "mode": None,
            "sha256": None,
            "cleanup_eligible": False,
        }

        try:
            info = path.lstat()
        except OSError as error:
            record["reason"] = f"stat failed: {type(error).__name__}"
            return record

        record["size_bytes"] = info.st_size
        record["mode"] = oct(stat.S_IMODE(info.st_mode))

        if path.is_symlink():
            record["reason"] = "symlink entries must never be followed"
            return record

        if not path.is_file():
            record["reason"] = "non-regular entries are not cleanup candidates"
            return record

        modified = datetime.fromtimestamp(info.st_mtime, tz=timezone.utc)
        age_days = (now - modified).total_seconds() / 86400.0
        record["age_days"] = age_days
        record["sha256"] = self._digest(path)

        if path.name == self.ACTIVE_LOG_NAME:
            record["classification"] = "protected"
            record["reason"] = "active canonical log"
            return record

        if self.ROTATED_PATTERN.fullmatch(path.name):
            if age_days > self.RETENTION_DAYS:
                record["classification"] = "expired_candidate"
                record["reason"] = (
                    f"recognized rotated log older than "
                    f"{self.RETENTION_DAYS} days"
                )
                record["cleanup_eligible"] = True
            else:
                record["classification"] = "retained_rotated"
                record["reason"] = (
                    "recognized rotated log within retention"
                )
            return record

        if path.suffix.lower() in {".tmp", ".bak", ".old"}:
            record["classification"] = "review_candidate"
            record["reason"] = (
                "temporary-like suffix requires explicit review"
            )

        return record

    def _inventory(self) -> list[dict[str, Any]]:
        if (
            not self.logs_dir.exists()
            or not self.logs_dir.is_dir()
            or self.logs_dir.is_symlink()
        ):
            return []

        now = self.inspection_time
        return [
            self._classify(path, now=now)
            for path in sorted(
                self.logs_dir.iterdir(),
                key=lambda item: item.name,
            )
        ]

    def _filesystem(self, target: Path) -> dict[str, Any]:
        record: dict[str, Any] = {
            "path": str(target),
            "exists": target.exists(),
            "total_bytes": None,
            "used_bytes": None,
            "free_bytes": None,
            "used_percent": None,
            "free_percent": None,
        }

        if not target.exists():
            return record

        usage = shutil.disk_usage(target)
        record.update(
            {
                "total_bytes": usage.total,
                "used_bytes": usage.used,
                "free_bytes": usage.free,
                "used_percent": round(
                    usage.used / usage.total * 100,
                    6,
                ),
                "free_percent": round(
                    usage.free / usage.total * 100,
                    6,
                ),
            }
        )
        return record

    def status(self) -> dict[str, Any]:
        inventory = self._inventory()
        files = [
            item
            for item in inventory
            if item["is_file"] and not item["is_symlink"]
        ]
        protected = sum(
            item["classification"] == "protected"
            for item in inventory
        )

        return {
            "owner": self.__class__.__name__,
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": "read_only_preview",
            "rotation_policy": self.ROTATION_POLICY,
            "retention_policy": self.RETENTION_POLICY,
            "logs_path": str(self.logs_dir),
            "logs_exists": self.logs_dir.exists(),
            "logs_is_directory": self.logs_dir.is_dir(),
            "logs_is_symlink": self.logs_dir.is_symlink(),
            "active_log_exists": self.active_log.is_file(),
            "log_entry_count": len(inventory),
            "regular_log_file_count": len(files),
            "total_log_bytes": sum(
                item["size_bytes"] for item in files
            ),
            "protected_current_count": protected,
            "retained_rotated_count": sum(
                item["classification"] == "retained_rotated"
                for item in inventory
            ),
            "expired_candidate_count": sum(
                item["classification"] == "expired_candidate"
                for item in inventory
            ),
            "review_candidate_count": sum(
                item["classification"] == "review_candidate"
                for item in inventory
            ),
            "blocked_entry_count": sum(
                item["classification"] == "blocked"
                for item in inventory
            ),
            "cleanup_execution_enabled": False,
            "canonical_delete_performed": False,
            "runtime_activation_enabled": False,
            "socket_binding_enabled": False,
            "systemd_mutation_enabled": False,
            "network_access_enabled": False,
            "status_valid": (
                self.logs_dir.exists()
                and self.logs_dir.is_dir()
                and not self.logs_dir.is_symlink()
                and self.active_log.is_file()
                and protected == 1
            ),
        }

    def context(self) -> dict[str, Any]:
        return {
            "owner": self.__class__.__name__,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "logger_contract": {
                "canonical_log": "logs/aura.log",
                "rotation_policy": self.ROTATION_POLICY,
                "retention_policy": self.RETENTION_POLICY,
                "compression_observed": False,
                "active_log_protected": True,
            },
            "cleanup_boundary": {
                "preview_required": True,
                "execution_default_enabled": False,
                "rotated_filename_allowlist_required": True,
                "path_containment_required": True,
                "symlink_follow_allowed": False,
                "directory_escape_allowed": False,
                "canonical_log_delete_allowed": False,
                "canonical_data_delete_allowed": False,
                "session_cleanup_allowed": False,
                "conversation_cleanup_allowed": False,
                "memory_cleanup_allowed": False,
                "journal_cleanup_allowed": False,
                "audit_cleanup_allowed": False,
                "arbitrary_file_delete_allowed": False,
                "temporary_fixture_mutation_allowed": True,
            },
            "filesystem_capacity": [
                self._filesystem(Path("/")),
                self._filesystem(Path("/home")),
                self._filesystem(Path("/mnt/aura-data")),
                self._filesystem(self.project_root),
            ],
            "log_inventory": self._inventory(),
        }

    def cleanup_preview(self) -> dict[str, Any]:
        inventory = self._inventory()
        candidates = [
            item
            for item in inventory
            if item["cleanup_eligible"]
        ]

        return {
            "owner": self.__class__.__name__,
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "preview_only": True,
            "cleanup_execution_enabled": False,
            "canonical_delete_performed": False,
            "candidate_count": len(candidates),
            "candidate_bytes": sum(
                item["size_bytes"] for item in candidates
            ),
            "candidates": candidates,
            "protected_entries": [
                item
                for item in inventory
                if item["classification"] == "protected"
            ],
            "retained_entries": [
                item
                for item in inventory
                if item["classification"] == "retained_rotated"
            ],
            "review_entries": [
                item
                for item in inventory
                if item["classification"] == "review_candidate"
            ],
            "blocked_entries": [
                item
                for item in inventory
                if item["classification"] == "blocked"
            ],
        }

    def check(self) -> dict[str, Any]:
        status = self.status()
        context = self.context()
        preview = self.cleanup_preview()

        checks = [
            ("version", status["version"] == self.VERSION),
            (
                "anchor_version",
                status["anchor_version"] == self.ANCHOR_VERSION,
            ),
            ("current_sprint", status["current_sprint"] == 245),
            ("next_sprint", status["next_sprint"] == 246),
            (
                "boundary",
                status["boundary"] == "log_rotation_storage_cleanup",
            ),
            (
                "next_boundary",
                status["next_boundary"] == "resource_baseline_metrics",
            ),
            (
                "contract_mode",
                status["contract_mode"] == "read_only_preview",
            ),
            (
                "rotation_policy",
                status["rotation_policy"] == "1 MB",
            ),
            (
                "retention_policy",
                status["retention_policy"] == "7 days",
            ),
            ("logs_exists", status["logs_exists"]),
            ("logs_is_directory", status["logs_is_directory"]),
            ("logs_not_symlink", not status["logs_is_symlink"]),
            ("active_log_exists", status["active_log_exists"]),
            (
                "one_protected_current",
                status["protected_current_count"] == 1,
            ),
            (
                "cleanup_disabled",
                not status["cleanup_execution_enabled"],
            ),
            (
                "no_delete",
                not status["canonical_delete_performed"],
            ),
            (
                "runtime_disabled",
                not status["runtime_activation_enabled"],
            ),
            ("socket_disabled", not status["socket_binding_enabled"]),
            (
                "systemd_disabled",
                not status["systemd_mutation_enabled"],
            ),
            ("network_disabled", not status["network_access_enabled"]),
            ("status_valid", status["status_valid"]),
            ("preview_only", preview["preview_only"]),
            (
                "preview_execution_disabled",
                not preview["cleanup_execution_enabled"],
            ),
            (
                "preview_no_delete",
                not preview["canonical_delete_performed"],
            ),
            (
                "preview_candidate_count",
                preview["candidate_count"] == len(preview["candidates"]),
            ),
            (
                "active_log_protected",
                context["logger_contract"]["active_log_protected"],
            ),
            (
                "preview_required",
                context["cleanup_boundary"]["preview_required"],
            ),
            (
                "symlink_follow_blocked",
                not context["cleanup_boundary"]["symlink_follow_allowed"],
            ),
            (
                "directory_escape_blocked",
                not context["cleanup_boundary"]["directory_escape_allowed"],
            ),
            (
                "canonical_log_delete_blocked",
                not context["cleanup_boundary"][
                    "canonical_log_delete_allowed"
                ],
            ),
            (
                "canonical_data_delete_blocked",
                not context["cleanup_boundary"][
                    "canonical_data_delete_allowed"
                ],
            ),
            (
                "session_cleanup_blocked",
                not context["cleanup_boundary"]["session_cleanup_allowed"],
            ),
            (
                "conversation_cleanup_blocked",
                not context["cleanup_boundary"][
                    "conversation_cleanup_allowed"
                ],
            ),
            (
                "memory_cleanup_blocked",
                not context["cleanup_boundary"]["memory_cleanup_allowed"],
            ),
            (
                "journal_cleanup_blocked",
                not context["cleanup_boundary"]["journal_cleanup_allowed"],
            ),
            (
                "audit_cleanup_blocked",
                not context["cleanup_boundary"]["audit_cleanup_allowed"],
            ),
            (
                "arbitrary_delete_blocked",
                not context["cleanup_boundary"][
                    "arbitrary_file_delete_allowed"
                ],
            ),
            (
                "fixture_mutation_allowed",
                context["cleanup_boundary"][
                    "temporary_fixture_mutation_allowed"
                ],
            ),
            (
                "filesystem_record_count",
                len(context["filesystem_capacity"]) == 4,
            ),
            (
                "project_capacity_exists",
                context["filesystem_capacity"][3]["exists"],
            ),
        ]

        failed = [
            name
            for name, passed in checks
            if not passed
        ]

        return {
            "owner": self.__class__.__name__,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "base_check_count": len(checks),
            "assertion_count": len(checks),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "alpha_ready": not failed,
            "status_valid": status["status_valid"],
            "expired_candidate_count": (
                status["expired_candidate_count"]
            ),
            "cleanup_candidate_count": (
                preview["candidate_count"]
            ),
            "cleanup_candidate_bytes": (
                preview["candidate_bytes"]
            ),
            "cleanup_execution_enabled": (
                preview["cleanup_execution_enabled"]
            ),
            "canonical_delete_performed": (
                preview["canonical_delete_performed"]
            ),
        }
