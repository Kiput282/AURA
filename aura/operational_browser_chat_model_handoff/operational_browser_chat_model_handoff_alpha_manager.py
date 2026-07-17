"""Read-only and isolated Sprint 262 handoff manager."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from aura.browser_chat_session_runtime.aura_browser_chat_session_http_runtime_manager import (
    AuraBrowserChatSessionHttpRuntimeManager,
)
from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
)
from aura.manual_start_stop_status_runtime.manual_start_stop_status_runtime_executor import (
    ManualStartStopStatusRuntimeExecutor,
)


class OperationalBrowserChatModelHandoffAlphaManager:
    """Expose the operational browser/model and process-role boundary."""

    VERSION = "1.2.2"
    CURRENT_SPRINT = 262
    NEXT_SPRINT = 263
    BOUNDARY = "operational_browser_chat_model_handoff"
    NEXT_BOUNDARY = "session_list_resume_rename_archive_restore"
    PRIMARY_ROUTE = "companion"
    MODEL_ENDPOINT = "/api/chat/sessions/{session_id}/model-messages"

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
            "primary_route": self.PRIMARY_ROUTE,
            "model_endpoint": self.MODEL_ENDPOINT,
            "explicit_model_confirmation_required": True,
            "save_only_fallback_available": True,
            "localhost_only": True,
            "model_download_enabled": False,
            "network_fallback_enabled": False,
            "tool_execution_enabled": False,
            "action_dispatch_enabled": False,
            "memory_write_enabled": False,
            "runtime_mutated": False,
        }

    def browser_route_status(self) -> dict[str, Any]:
        manager = AuraBrowserChatSessionHttpRuntimeManager(
            project_root=self.project_root
        )
        return {
            **manager.operational_model_handoff_status(),
            "primary_route": self.PRIMARY_ROUTE,
            "runtime_mutated": False,
        }

    def process_role_status(self) -> dict[str, Any]:
        owner = ManualStartStopStatusRuntimeExecutor(
            project_root=self.project_root
        )
        live = owner.status(probe_health=False)

        return {
            "native_process_role_classification": live.get(
                "native_process_role_classification"
            ),
            "strict_main_process_count": live.get(
                "strict_main_process_count"
            ),
            "control_plane_process_count": live.get(
                "control_plane_process_count"
            ),
            "observed_main_process_count": live.get(
                "observed_main_process_count"
            ),
            "synthetic_runtime_role": (
                owner.classify_main_process_role(
                    list(owner.expected_argv),
                    str(owner.project_root),
                )
            ),
            "synthetic_control_plane_role": (
                owner.classify_main_process_role(
                    [
                        str(owner.python_path),
                        str(owner.main_path),
                        (
                            "operational-browser-chat-"
                            "model-handoff-check"
                        ),
                    ],
                    str(owner.project_root),
                )
            ),
            "synthetic_foreign_role": (
                owner.classify_main_process_role(
                    [
                        str(owner.python_path),
                        "/tmp/main.py",
                        "unknown",
                    ],
                    "/tmp",
                )
            ),
            "safe_idle": live.get("safe_idle"),
            "runtime_mutated": False,
        }

    def isolated_rehearsal(self) -> dict[str, Any]:
        """Exercise atomic model-pair persistence without network access."""

        with TemporaryDirectory(
            prefix="aura-sprint-262-"
        ) as temporary_text:
            manager = AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root,
                storage_dir=(
                    Path(temporary_text)
                    / "chat_sessions"
                ),
            )
            created = manager.create_session(
                title="Sprint 262 isolated handoff"
            )["session"]
            session_id = created["session_id"]
            invocation_count = 0

            def response_factory(
                messages: list[dict[str, str]],
            ) -> Mapping[str, Any]:
                nonlocal invocation_count
                invocation_count += 1

                return {
                    "content": (
                        "AURA isolated operational "
                        "handoff response."
                    ),
                    "request_id": "request_sprint262",
                    "provider": "isolated",
                    "base_url": "http://127.0.0.1:1",
                    "configured_model": (
                        "isolated-sprint-262"
                    ),
                    "response_model": (
                        "isolated-sprint-262"
                    ),
                    "elapsed_ms": 0,
                    "input_message_count": len(messages),
                    "input_character_count": sum(
                        len(item["content"])
                        for item in messages
                    ),
                    "model_invoked": True,
                    "network_fallback_used": False,
                    "streaming_used": False,
                    "tool_schema_sent": False,
                    "tool_calls_accepted": False,
                    "tools_invoked": False,
                    "actions_invoked": False,
                    "commands_invoked": False,
                    "aura_memory_written": False,
                }

            first = manager.submit_local_model_message(
                session_id,
                content=(
                    "Verify the isolated browser handoff."
                ),
                client_message_id="client_sprint262",
                expected_revision=created["revision"],
                system_prompt=(
                    "You are AURA in an isolated "
                    "contract rehearsal."
                ),
                response_factory=response_factory,
            )
            duplicate = manager.submit_local_model_message(
                session_id,
                content=(
                    "Verify the isolated browser handoff."
                ),
                client_message_id="client_sprint262",
                expected_revision=created["revision"],
                system_prompt=(
                    "You are AURA in an isolated "
                    "contract rehearsal."
                ),
                response_factory=response_factory,
            )
            stored = manager.load_session(session_id)
            roles = self.process_role_status()

            ok = (
                first["accepted"] is True
                and first["model_invoked"] is True
                and first["aura_memory_written"] is False
                and duplicate[
                    "idempotent_replay"
                ]
                is True
                and duplicate["model_reinvoked"] is False
                and invocation_count == 1
                and stored["message_count"] == 2
                and stored["revision"] == 2
                and stored["last_response_kind"]
                == "local_model_response"
                and roles["synthetic_runtime_role"]
                == "service_runtime"
                and roles[
                    "synthetic_control_plane_role"
                ]
                == "control_plane"
                and roles["synthetic_foreign_role"]
                == "unclassified_main"
            )

            return {
                "status": (
                    "completed"
                    if ok
                    else "failed"
                ),
                "ok": ok,
                "model_generate_count": invocation_count,
                "message_count": stored[
                    "message_count"
                ],
                "revision": stored["revision"],
                "idempotent_replay": duplicate[
                    "idempotent_replay"
                ],
                "model_reinvoked": duplicate[
                    "model_reinvoked"
                ],
                "response_kind": stored[
                    "last_response_kind"
                ],
                "native_process_role_classification": (
                    roles[
                        "native_process_role_classification"
                    ]
                ),
                "network_connection_opened": False,
                "model_request_executed": False,
                "canonical_runtime_used": False,
                "source_mutated": False,
                "runtime_activated": False,
                "repository_committed": False,
                "repository_pushed": False,
            }
