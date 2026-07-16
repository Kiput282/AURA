from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import json
import os
import stat

from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
    BrowserChatSessionCorruptionError,
)


class PersistentLocalChatSessionContract:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.session_root = (
            self.project_root
            / "data"
            / "chat_sessions"
        )

    def storage_posture(self) -> dict[str, Any]:
        path = self.session_root

        if path.is_symlink():
            return {
                "ok": False,
                "state": "symlink_rejected",
                "path": str(path),
                "exists": True,
                "is_symlink": True,
                "migration_required": False,
                "mutation_performed": False,
            }

        if not path.exists():
            return {
                "ok": True,
                "state": "absent_ready_for_secure_creation",
                "path": str(path),
                "exists": False,
                "is_symlink": False,
                "migration_required": False,
                "target_mode": "0700",
                "mutation_performed": False,
            }

        metadata = path.stat()
        mode = stat.S_IMODE(
            metadata.st_mode
        )
        files = []
        invalid = 0
        broad = 0
        symlinks = 0

        for item in sorted(
            path.glob("chat_*.json")
        ):
            if item.is_symlink():
                symlinks += 1
                continue

            item_metadata = item.stat()
            item_mode = stat.S_IMODE(
                item_metadata.st_mode
            )

            if item_mode & 0o077:
                broad += 1

            try:
                packet = json.loads(
                    item.read_text(
                        encoding="utf-8"
                    )
                )
            except (
                UnicodeError,
                json.JSONDecodeError,
                OSError,
            ):
                invalid += 1
                packet = None

            files.append(
                {
                    "name": item.name,
                    "mode": oct(item_mode),
                    "uid_matches": (
                        item_metadata.st_uid
                        == os.getuid()
                    ),
                    "json_valid": (
                        isinstance(packet, dict)
                    ),
                    "schema_keys": (
                        sorted(packet.keys())
                        if isinstance(packet, dict)
                        else []
                    ),
                }
            )

        private = (mode & 0o077) == 0
        owner_matches = (
            metadata.st_uid == os.getuid()
        )
        ready = (
            stat.S_ISDIR(metadata.st_mode)
            and owner_matches
            and private
            and invalid == 0
            and broad == 0
            and symlinks == 0
        )

        return {
            "ok": (
                stat.S_ISDIR(metadata.st_mode)
                and owner_matches
                and invalid == 0
                and broad == 0
                and symlinks == 0
            ),
            "state": (
                "ready"
                if ready
                else (
                    "mode_migration_required"
                    if (
                        stat.S_ISDIR(
                            metadata.st_mode
                        )
                        and owner_matches
                        and not private
                        and invalid == 0
                        and broad == 0
                        and symlinks == 0
                    )
                    else "review_required"
                )
            ),
            "path": str(path),
            "exists": True,
            "is_symlink": False,
            "is_directory": stat.S_ISDIR(
                metadata.st_mode
            ),
            "uid": metadata.st_uid,
            "uid_matches": owner_matches,
            "mode": oct(mode),
            "target_mode": "0700",
            "private_mode": private,
            "migration_required": (
                not private
                and owner_matches
                and stat.S_ISDIR(
                    metadata.st_mode
                )
            ),
            "session_file_count": len(files),
            "invalid_json_count": invalid,
            "broad_file_count": broad,
            "symlink_file_count": symlinks,
            "sessions": files,
            "contents_logged": False,
            "mutation_performed": False,
        }

    def migration_preview(self) -> dict[str, Any]:
        posture = self.storage_posture()

        return {
            "ok": posture["ok"],
            "review_only": True,
            "path": str(
                self.session_root
            ),
            "current_state": posture["state"],
            "current_mode": posture.get(
                "mode"
            ),
            "target_mode": "0700",
            "required": posture.get(
                "migration_required",
                False,
            ),
            "preconditions": [
                "path is a real directory",
                "path is owned by the current uid",
                "all chat_*.json files are regular",
                "all chat_*.json files are owned by the current uid",
                "all chat_*.json files use private permissions",
                "all session JSON and integrity hashes validate",
                "content hashes are snapshotted before mode change",
            ],
            "planned_action": (
                f"chmod 0700 -- {self.session_root}"
            ),
            "content_rewrite_planned": False,
            "session_delete_planned": False,
            "session_content_logging": False,
            "executed": False,
        }

    def history_preview(
        self,
        *,
        limit: int = 20,
    ) -> dict[str, Any]:
        bounded_limit = max(
            1,
            min(int(limit), 100),
        )
        manager = (
            AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root
            )
        )
        status = manager.status()
        sessions = list(
            status.get("sessions", [])
        )
        sessions.sort(
            key=lambda item: str(
                item.get("updated_at_utc", "")
            ),
            reverse=True,
        )

        return {
            "ok": not status.get(
                "degraded",
                False,
            ),
            "read_only": True,
            "bounded_limit": bounded_limit,
            "returned_count": len(
                sessions[:bounded_limit]
            ),
            "sessions": (
                sessions[:bounded_limit]
            ),
            "message_contents_included": False,
            "exact_session_load_available": True,
            "automatic_memory_handoff": False,
            "model_invoked": False,
            "network_accessed": False,
            "mutation_performed": False,
        }

    def isolated_rehearsal(self) -> dict[str, Any]:
        counter = 0

        def identifier() -> str:
            nonlocal counter
            counter += 1
            return f"{counter:032x}"

        with TemporaryDirectory(
            prefix="aura-sprint-256-chat-"
        ) as temporary_text:
            temporary = Path(temporary_text)
            storage = (
                temporary
                / "data"
                / "chat_sessions"
            )
            first = (
                AuraBrowserChatSessionRuntimeManager(
                    project_root=temporary,
                    storage_dir=storage,
                    id_factory=identifier,
                )
            )
            created = first.create_session(
                title="Sprint 256 isolated rehearsal"
            )
            session_id = created[
                "session"
            ]["session_id"]
            submitted = first.submit_message(
                session_id,
                content=(
                    "isolated persistence rehearsal"
                ),
                client_message_id=(
                    "client_sprint_256"
                ),
                expected_revision=1,
            )
            second = (
                AuraBrowserChatSessionRuntimeManager(
                    project_root=temporary,
                    storage_dir=storage,
                    id_factory=identifier,
                )
            )
            loaded = second.load_session(
                session_id
            )
            listed = second.list_sessions()
            session_path = (
                storage
                / f"{session_id}.json"
            )
            file_metadata = session_path.stat()
            directory_metadata = storage.stat()

            symlink_target = (
                temporary
                / "symlink-target.json"
            )
            symlink_target.write_text(
                session_path.read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            symlink_session = (
                "chat_"
                + "f" * 32
            )
            symlink_path = (
                storage
                / f"{symlink_session}.json"
            )
            symlink_path.symlink_to(
                symlink_target
            )
            symlink_rejected = False

            try:
                second.load_session(
                    symlink_session
                )
            except BrowserChatSessionCorruptionError:
                symlink_rejected = True

            symlink_path.unlink()

            return {
                "created": (
                    created["status"]
                    == "created"
                ),
                "submitted": (
                    submitted["status"]
                    == "accepted"
                ),
                "cross_instance_load": (
                    loaded["session_id"]
                    == session_id
                ),
                "cross_instance_list": (
                    len(listed) == 1
                    and listed[0][
                        "session_id"
                    ]
                    == session_id
                ),
                "message_count": loaded[
                    "message_count"
                ],
                "revision": loaded[
                    "revision"
                ],
                "integrity_valid": (
                    loaded[
                        "integrity_sha256"
                    ]
                    == second._integrity_digest(
                        loaded
                    )
                ),
                "directory_mode": stat.S_IMODE(
                    directory_metadata.st_mode
                ),
                "file_mode": stat.S_IMODE(
                    file_metadata.st_mode
                ),
                "directory_uid": (
                    directory_metadata.st_uid
                ),
                "file_uid": file_metadata.st_uid,
                "symlink_rejected": (
                    symlink_rejected
                ),
                "temporary_storage_removed_after": True,
                "canonical_storage_mutated": False,
                "model_invoked": False,
                "network_accessed": False,
                "memory_written": False,
            }
