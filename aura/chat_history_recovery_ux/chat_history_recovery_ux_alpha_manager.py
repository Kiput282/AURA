from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import json

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    AuraBrowserChatSessionHttpRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
    BrowserChatSessionConflictError,
    BrowserChatSessionCorruptionError,
    BrowserChatSessionNotFoundError,
)
from aura.browser_chat_session_runtime.aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
)


class ChatHistoryRecoveryUxAlphaManager:
    VERSION = "1.2.4"
    CURRENT_SPRINT = 264
    NEXT_SPRINT = 265
    BOUNDARY = "chat_history_recovery_ux"
    NEXT_BOUNDARY = "review_first_memory_integration"

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def product_status(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "primary_interface": "browser_control_center",
            "recovery_endpoint": "/api/chat/recovery",
            "recovery_runtime_kind": (
                "read_only_diagnostic_and_guidance"
            ),
            "stale_revision_reload_guidance": True,
            "stale_draft_preserved_in_memory": True,
            "missing_session_neutral_state": True,
            "archived_session_restore_guidance": True,
            "corrupt_file_preserved": True,
            "automatic_file_repair": False,
            "session_quarantine_runtime": False,
            "automatic_session_replacement": False,
            "automatic_history_merge": False,
            "permanent_delete_runtime": False,
            "model_invocation": False,
            "network_connection": False,
            "safe_idle": True,
            "runtime_mutated": False,
        }

    def runtime_status(self) -> dict[str, Any]:
        manager = AuraBrowserChatSessionRuntimeManager(
            project_root=self.project_root
        )
        return {
            **manager.recovery_status(),
            "runtime_mutated": False,
        }

    def route_status(self) -> dict[str, Any]:
        manager = AuraBrowserChatSessionHttpRuntimeManager(
            project_root=self.project_root
        )
        return {
            "chat_route_contracts": list(
                manager.CHAT_ROUTE_CONTRACTS
            ),
            "chat_route_contract_count": len(
                manager.CHAT_ROUTE_CONTRACTS
            ),
            "total_route_contract_count": (
                manager.TOTAL_ROUTE_CONTRACT_COUNT
            ),
            "recovery_route_present": (
                "GET /api/chat/recovery"
                in manager.CHAT_ROUTE_CONTRACTS
            ),
            "recovery_route_read_only": True,
            "new_mutating_route": False,
            "listener_activated": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
        }

    def web_surface_status(self) -> dict[str, Any]:
        manager = AuraBrowserChatWebSurfaceManager(
            project_root=self.project_root
        )
        status = manager.status()
        self_test = manager.self_test()
        return {
            **status,
            "self_test_assertion_count": self_test[
                "assertion_count"
            ],
            "self_test_failed_assertion_count": self_test[
                "failed_assertion_count"
            ],
            "runtime_mutated": False,
        }

    def isolated_rehearsal(self) -> dict[str, Any]:
        with TemporaryDirectory(
            prefix="aura-s264-recovery-"
        ) as temporary_text:
            root = Path(temporary_text)
            storage = root / "chat_sessions"
            identifiers = iter(
                f"{value:032x}"
                for value in range(1, 100)
            )
            manager = AuraBrowserChatSessionRuntimeManager(
                project_root=root,
                storage_dir=storage,
                id_factory=lambda: next(identifiers),
            )

            initial = manager.recovery_status()
            created = manager.create_session(
                title="Sprint 264 recovery rehearsal"
            )["session"]
            session_id = created["session_id"]
            path = storage / f"{session_id}.json"

            payload = json.loads(
                path.read_text(encoding="utf-8")
            )
            payload["title"] = "Tampered without hash update"
            path.write_text(
                json.dumps(
                    payload,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            before = path.read_bytes()
            before_hash = sha256(before).hexdigest()

            corruption_seen = False
            try:
                manager.load_session(session_id)
            except BrowserChatSessionCorruptionError:
                corruption_seen = True

            recovery = manager.recovery_status()
            after = path.read_bytes()
            after_hash = sha256(after).hexdigest()

            http = AuraBrowserChatSessionHttpRuntimeManager(
                project_root=root,
                chat_storage_dir=storage,
            )
            missing_status, missing = (
                http._chat_error_payload(
                    BrowserChatSessionNotFoundError(
                        "Session not found"
                    )
                )
            )
            stale_status, stale = (
                http._chat_error_payload(
                    BrowserChatSessionConflictError(
                        "Session revision changed before submit."
                    )
                )
            )
            archived_status, archived = (
                http._chat_error_payload(
                    BrowserChatSessionConflictError(
                        "Session is archived; restore before submit."
                    )
                )
            )
            corruption_status, corruption = (
                http._chat_error_payload(
                    BrowserChatSessionCorruptionError(
                        "Persisted session integrity hash "
                        "does not match."
                    )
                )
            )

        return {
            "status": "ok",
            "initial_healthy": (
                initial["status"] == "healthy"
            ),
            "initial_storage_not_created": (
                initial["runtime_mutated"] is False
            ),
            "corruption_detected": corruption_seen,
            "recovery_attention_required": (
                recovery["status"]
                == "attention_required"
            ),
            "recovery_issue_count_one": (
                recovery["issue_count"] == 1
            ),
            "corrupt_file_preserved": (
                before == after
                and before_hash == after_hash
            ),
            "automatic_file_repair": recovery[
                "automatic_file_repair"
            ],
            "session_quarantine_runtime": recovery[
                "session_quarantine_runtime"
            ],
            "missing_status_404": missing_status == 404,
            "missing_neutral_state": (
                missing["recovery"]["target_state"]
                == "neutral_no_session"
            ),
            "stale_status_409": stale_status == 409,
            "stale_draft_preserved": (
                stale["recovery"][
                    "preserve_unsent_draft_in_memory"
                ]
                is True
            ),
            "archived_status_409": archived_status == 409,
            "archived_restore_guidance": (
                archived["recovery"]["action"]
                == "restore_session"
            ),
            "corruption_status_503": (
                corruption_status == 503
            ),
            "corruption_recovery_endpoint": (
                corruption["recovery"]["endpoint"]
                == "/api/chat/recovery"
            ),
            "new_mutating_route": False,
            "model_invocation": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }
