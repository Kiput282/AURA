from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    AuraBrowserChatSessionHttpRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_web_surface_manager import (
    AuraBrowserChatWebSurfaceManager,
)


class SessionListResumeRenameArchiveRestoreAlphaManager:
    VERSION = "1.2.3"
    CURRENT_SPRINT = 263
    NEXT_SPRINT = 264
    BOUNDARY = "session_list_resume_rename_archive_restore"
    NEXT_BOUNDARY = "chat_history_recovery_ux"

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
            "active_list_default": True,
            "archived_list_explicit": True,
            "resume_same_session": True,
            "rename_title_only": True,
            "archive_non_destructive": True,
            "restore_non_destructive": True,
            "session_id_immutable": True,
            "cross_session_history_merge": False,
            "permanent_delete_runtime": False,
            "model_invocation_for_lifecycle": False,
            "network_connection_for_lifecycle": False,
            "safe_idle": True,
            "runtime_mutated": False,
        }

    def runtime_status(self) -> dict[str, Any]:
        manager = AuraBrowserChatSessionRuntimeManager(
            project_root=self.project_root
        )
        status = manager.status()
        return {
            "session_count": status["session_count"],
            "active_session_count": status[
                "active_session_count"
            ],
            "archived_session_count": status[
                "archived_session_count"
            ],
            "safety_boundary": deepcopy(
                status["safety_boundary"]
            ),
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
            "safety_boundary": manager.safety_boundary(),
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
            prefix="aura-sprint-263-"
        ) as temporary_text:
            storage = Path(temporary_text) / "chat_sessions"
            identifiers = iter(
                f"{value:032x}"
                for value in range(1, 100)
            )
            manager = AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root,
                storage_dir=storage,
                id_factory=lambda: next(identifiers),
            )

            created = manager.create_session(
                title="Sprint 263 lifecycle rehearsal"
            )["session"]
            session_id = created["session_id"]

            manager.submit_message(
                session_id,
                content="Preserve this session history.",
                client_message_id="client_sprint263",
                expected_revision=created["revision"],
            )
            before = manager.load_session(session_id)
            messages_before = deepcopy(before["messages"])

            resumed = manager.resume_session(
                session_id,
                expected_revision=before["revision"],
            )
            renamed = manager.rename_session(
                session_id,
                title="Sprint 263 renamed session",
                expected_revision=before["revision"],
            )
            archived = manager.archive_session(
                session_id,
                expected_revision=(
                    renamed["session"]["revision"]
                ),
            )
            active_after_archive = manager.list_sessions()
            archived_after_archive = manager.list_sessions(
                state="archived"
            )
            all_after_archive = manager.list_sessions(
                state="all"
            )
            restored = manager.restore_session(
                session_id,
                expected_revision=(
                    archived["session"]["revision"]
                ),
            )
            active_after_restore = manager.list_sessions()
            archived_after_restore = manager.list_sessions(
                state="archived"
            )
            final = manager.load_session(session_id)
            files = sorted(storage.glob("chat_*.json"))
            status = manager.status()

        return {
            "status": "ok",
            "session_id": session_id,
            "resume_same_session_id": (
                resumed["session"]["session_id"]
                == session_id
            ),
            "resume_history_unchanged": (
                resumed["session"]["messages"]
                == messages_before
            ),
            "cross_session_history_merged": resumed[
                "cross_session_history_merged"
            ],
            "rename_title_updated": (
                renamed["session"]["title"]
                == "Sprint 263 renamed session"
            ),
            "rename_session_id_unchanged": (
                renamed["session"]["session_id"]
                == session_id
            ),
            "rename_history_unchanged": (
                renamed["session"]["messages"]
                == messages_before
            ),
            "archive_status_archived": (
                archived["session"]["status"]
                == "archived"
            ),
            "archive_file_deleted": archived[
                "session_file_deleted"
            ],
            "archive_file_moved": archived[
                "session_file_moved"
            ],
            "archive_history_unchanged": (
                archived["session"]["messages"]
                == messages_before
            ),
            "active_list_empty_after_archive": (
                active_after_archive == []
            ),
            "archived_list_one_after_archive": (
                len(archived_after_archive) == 1
            ),
            "all_list_one_after_archive": (
                len(all_after_archive) == 1
            ),
            "restore_status_active": (
                restored["session"]["status"]
                == "active"
            ),
            "restore_session_id_unchanged": (
                restored["session"]["session_id"]
                == session_id
            ),
            "restore_history_unchanged": (
                restored["session"]["messages"]
                == messages_before
            ),
            "active_list_one_after_restore": (
                len(active_after_restore) == 1
            ),
            "archived_list_empty_after_restore": (
                archived_after_restore == []
            ),
            "final_history_unchanged": (
                final["messages"] == messages_before
            ),
            "single_session_file_retained": (
                len(files) == 1
            ),
            "permanent_delete_runtime": status[
                "safety_boundary"
            ]["session_permanent_delete_runtime"],
            "cross_session_history_merge": status[
                "safety_boundary"
            ]["cross_session_history_merge"],
            "safe_idle": status[
                "safety_boundary"
            ]["safe_idle"],
            "model_invoked": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
        }
