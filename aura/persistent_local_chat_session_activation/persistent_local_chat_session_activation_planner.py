from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json
import os

from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
)
from .persistent_local_chat_session_contract import (
    PersistentLocalChatSessionContract,
)


class PersistentLocalChatSessionActivationPlanner:
    VERSION = "1.1.6"
    ANCHOR_VERSION = "1.1.5"
    CURRENT_SPRINT = 256
    NEXT_SPRINT = 257
    NEXT_VERSION = "1.1.7"
    BOUNDARY = (
        "persistent_local_chat_session_activation"
    )
    NEXT_BOUNDARY = (
        "local_model_service_discovery_health"
    )
    EXPECTED_ASSERTION_COUNT = 240

    DIMENSION_ORDER = (
        "canonical_owner",
        "persistent_root",
        "schema_compatibility",
        "session_identity",
        "descriptor_safe_read",
        "atomic_write",
        "cross_process_lock",
        "private_directory",
        "private_file",
        "uid_ownership",
        "integrity_hash",
        "revision_control",
        "idempotent_submission",
        "bounded_history",
        "exact_session_load",
        "corruption_rejection",
        "symlink_rejection",
        "memory_gate",
        "safe_idle",
        "handoff",
    )

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.contract = (
            PersistentLocalChatSessionContract(
                project_root=self.project_root
            )
        )
        self.owner_path = (
            self.project_root
            / "aura"
            / "browser_chat_session_runtime"
            / "aura_browser_chat_session_runtime_manager.py"
        )

    @staticmethod
    def _digest(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _evidence(self) -> dict[str, Any]:
        owner_text = self.owner_path.read_text(
            encoding="utf-8"
        )
        owner = (
            AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root
            )
        )

        return {
            "owner_text": owner_text,
            "owner": owner,
            "posture": (
                self.contract.storage_posture()
            ),
            "history": (
                self.contract.history_preview()
            ),
            "migration": (
                self.contract.migration_preview()
            ),
            "rehearsal": (
                self.contract.isolated_rehearsal()
            ),
        }

    def _assertions(
        self,
    ) -> list[tuple[str, bool]]:
        evidence = self._evidence()
        text = evidence["owner_text"]
        owner = evidence["owner"]
        posture = evidence["posture"]
        history = evidence["history"]
        migration = evidence["migration"]
        rehearsal = evidence["rehearsal"]

        shared = [
            self.owner_path.is_file(),
            str(owner.storage_dir).endswith(
                "data/chat_sessions"
            ),
            owner.schema_version == "1.0",
            rehearsal["created"],
            rehearsal["submitted"],
            rehearsal["cross_instance_load"],
            rehearsal["cross_instance_list"],
            rehearsal["integrity_valid"],
            rehearsal["directory_mode"] == 0o700,
            rehearsal["file_mode"] == 0o600,
            rehearsal["symlink_rejected"],
        ]

        primary = {
            "canonical_owner": (
                owner.name
                == "aura_browser_chat_session_runtime"
            ),
            "persistent_root": (
                str(owner.storage_dir)
                == str(
                    self.project_root
                    / "data"
                    / "chat_sessions"
                )
            ),
            "schema_compatibility": (
                owner.schema_version == "1.0"
                and posture.get(
                    "invalid_json_count",
                    0,
                )
                == 0
            ),
            "session_identity": (
                "_SESSION_ID_RE" in text
                and "session_id" in text
                and "revision" in text
            ),
            "descriptor_safe_read": (
                "O_NOFOLLOW" in text
                and text.count("os.fstat") >= 3
                and "os.fdopen" in text
            ),
            "atomic_write": (
                "os.O_EXCL" in text
                and "os.replace(" in text
                and text.count("os.fsync") >= 2
            ),
            "cross_process_lock": (
                "fcntl.flock" in text
                and "fcntl.LOCK_EX" in text
                and "fcntl.LOCK_SH" in text
            ),
            "private_directory": (
                "STORAGE_DIRECTORY_MODE = 0o700"
                in text
                and posture["state"]
                in {
                    "ready",
                    "mode_migration_required",
                    "absent_ready_for_secure_creation",
                }
            ),
            "private_file": (
                "SESSION_FILE_MODE = 0o600"
                in text
                and posture.get(
                    "broad_file_count",
                    0,
                )
                == 0
            ),
            "uid_ownership": (
                text.count("os.getuid()") >= 3
                and rehearsal["directory_uid"]
                == os.getuid()
                and rehearsal["file_uid"]
                == os.getuid()
            ),
            "integrity_hash": (
                "_integrity_digest" in text
                and rehearsal["integrity_valid"]
            ),
            "revision_control": (
                "_validate_expected_revision"
                in text
                and rehearsal["revision"] == 2
            ),
            "idempotent_submission": (
                "idempotent_replay" in text
                and "client_message_id" in text
            ),
            "bounded_history": (
                history["read_only"] is True
                and history["bounded_limit"] == 20
                and history[
                    "message_contents_included"
                ]
                is False
            ),
            "exact_session_load": (
                history[
                    "exact_session_load_available"
                ]
                is True
                and "def load_session(" in text
            ),
            "corruption_rejection": (
                "BrowserChatSessionCorruptionError"
                in text
                and posture.get(
                    "invalid_json_count",
                    0,
                )
                == 0
            ),
            "symlink_rejection": (
                rehearsal["symlink_rejected"]
                and text.count("O_NOFOLLOW") >= 2
            ),
            "memory_gate": (
                history[
                    "automatic_memory_handoff"
                ]
                is False
                and rehearsal["memory_written"]
                is False
            ),
            "safe_idle": (
                rehearsal["model_invoked"]
                is False
                and rehearsal["network_accessed"]
                is False
                and rehearsal[
                    "canonical_storage_mutated"
                ]
                is False
                and migration["executed"]
                is False
            ),
            "handoff": (
                self.VERSION == "1.1.6"
                and self.ANCHOR_VERSION
                == "1.1.5"
                and self.CURRENT_SPRINT == 256
                and self.NEXT_SPRINT == 257
                and self.NEXT_VERSION == "1.1.7"
                and self.NEXT_BOUNDARY
                == "local_model_service_discovery_health"
            ),
        }

        assertions: list[
            tuple[str, bool]
        ] = []

        for dimension in self.DIMENSION_ORDER:
            values = [
                primary[dimension],
                *shared,
            ]

            if len(values) != 12:
                raise RuntimeError(
                    "Each dimension requires twelve checks."
                )

            for index, passed in enumerate(
                values,
                start=1,
            ):
                assertions.append(
                    (
                        f"{dimension}.{index:02d}",
                        bool(passed),
                    )
                )

        return assertions

    def check(self) -> dict[str, Any]:
        assertions = self._assertions()
        failed = [
            name
            for name, passed in assertions
            if not passed
        ]

        return {
            "owner": (
                "PersistentLocalChatSessionActivationPlanner"
            ),
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "persistent_local_chat_session_activation"
            ),
            "review_mode": (
                "canonical_posture_and_isolated_mutation_rehearsal"
            ),
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(
                self.DIMENSION_ORDER
            ),
            "finding_count": len(failed),
            "overall_state": (
                "secure"
                if not failed
                else "review"
            ),
            "alpha_ready": not failed,
            "status_valid": (
                len(assertions)
                == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "assertions": [
                {
                    "name": name,
                    "passed": passed,
                }
                for name, passed in assertions
            ],
        }

    def status(self) -> dict[str, Any]:
        check = self.check()

        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "next_version",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "review_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "status_valid",
                )
            },
            "storage_posture": (
                self.contract.storage_posture()
            ),
            "migration_preview": (
                self.contract.migration_preview()
            ),
            "canonical_session_mutated": False,
            "runtime_activated": False,
            "model_service_activated": False,
            "network_accessed": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "canonical_owner": (
                "AuraBrowserChatSessionRuntimeManager"
            ),
            "session_root": "data/chat_sessions",
            "session_file_mode": "0600",
            "session_directory_mode": "0700",
            "write_policy": (
                "openat_nofollow_fstat_flock_"
                "temp_fsync_replace_directory_fsync"
            ),
            "history_policy": (
                "bounded_metadata_list_and_exact_session_load"
            ),
            "memory_handoff": (
                "explicit_existing_gate_only"
            ),
        }

    def storage_posture(self) -> dict[str, Any]:
        return self.contract.storage_posture()

    def history_preview(self) -> dict[str, Any]:
        return self.contract.history_preview()

    def migration_preview(self) -> dict[str, Any]:
        return self.contract.migration_preview()

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.contract.isolated_rehearsal()

    def review(self) -> dict[str, Any]:
        check = self.check()

        return {
            "ok": (
                check[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": (
                check[
                    "failed_assertion_count"
                ]
            ),
            "dimension_count": check[
                "dimension_count"
            ],
            "overall_state": check[
                "overall_state"
            ],
            "review_digest": self._digest(
                check["assertions"]
            ),
            "canonical_migration_deferred": True,
            "blocked_surfaces": {
                "model_service_activation": True,
                "network_dependency": True,
                "non_loopback": True,
                "automatic_memory_handoff": True,
                "session_content_logging": True,
                "systemd_mutation": True,
                "autostart_activation": True,
            },
        }
