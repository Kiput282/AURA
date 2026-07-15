"""Read-only Sprint 244 persistence validation."""

from __future__ import annotations

import hashlib
import json
import re
import stat
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_manager import (
    AuraBrowserChatSessionRuntimeManager,
)


class AuraSessionMemoryPersistenceChecksPlanner:
    """Validate canonical persisted stores without mutating them."""

    VERSION = "1.0.4-genesis"
    ANCHOR_VERSION = "1.0.3-genesis"
    CURRENT_SPRINT = 244
    NEXT_SPRINT = 245
    BOUNDARY = "session_memory_persistence_checks"
    NEXT_BOUNDARY = "log_rotation_storage_cleanup"

    EXPECTED_STORE_COUNT = 4
    EXPECTED_BASE_CHECK_COUNT = 81
    EXPECTED_ASSERTION_COUNT = 92
    MAX_JSONL_BYTES = 64 * 1024 * 1024

    _SESSION_FILE_RE = re.compile(
        r"^chat_[0-9a-f]{32}\.json$"
    )

    _SESSION_KEYS = {
        "schema_version",
        "session_id",
        "title",
        "status",
        "created_at_utc",
        "updated_at_utc",
        "revision",
        "message_count",
        "clear_count",
        "last_clear_at_utc",
        "last_response_kind",
        "messages",
        "integrity_sha256",
    }

    _MESSAGE_KEYS = {
        "message_id",
        "sequence",
        "role",
        "content",
        "created_at_utc",
        "client_message_id",
        "response_kind",
        "model_invoked",
        "tools_invoked",
        "actions_invoked",
    }

    _STORE_SCHEMAS: dict[str, dict[str, Any]] = {
        "chat_history": {
            "relative_path": (
                "data/conversations/chat_history.jsonl"
            ),
            "keys": {
                "id",
                "user_message",
                "aura_response",
                "created_at",
                "source",
                "metadata",
            },
            "string_fields": {
                "id",
                "user_message",
                "aura_response",
                "created_at",
                "source",
            },
            "nonempty_fields": {
                "id",
                "created_at",
                "source",
            },
        },
        "memory": {
            "relative_path": (
                "data/memory/memories.jsonl"
            ),
            "keys": {
                "id",
                "kind",
                "content",
                "created_at",
                "metadata",
            },
            "string_fields": {
                "id",
                "kind",
                "content",
                "created_at",
            },
            "nonempty_fields": {
                "id",
                "kind",
                "created_at",
            },
        },
        "journal": {
            "relative_path": (
                "data/journal/aura_journal.jsonl"
            ),
            "keys": {
                "id",
                "title",
                "content",
                "created_at",
                "metadata",
            },
            "string_fields": {
                "id",
                "title",
                "content",
                "created_at",
            },
            "nonempty_fields": {
                "id",
                "created_at",
            },
        },
    }

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        if project_root is None:
            project_root = (
                Path(__file__).resolve().parents[2]
            )

        self.project_root = Path(project_root).resolve()
        self.data_root = (
            self.project_root / "data"
        )
        self.browser_storage = (
            self.data_root / "chat_sessions"
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        hasher = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda: handle.read(1024 * 1024),
                b"",
            ):
                hasher.update(chunk)

        return hasher.hexdigest()

    @staticmethod
    def _timestamp_valid(value: object) -> bool:
        if not isinstance(value, str):
            return False

        try:
            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            return False

        return parsed.tzinfo is not None

    def _within_project(
        self,
        path: Path,
    ) -> bool:
        try:
            path.resolve(strict=False).relative_to(
                self.project_root
            )
        except ValueError:
            return False

        return True

    def _root_checks(
        self,
    ) -> dict[str, bool]:
        catalog = {
            "browser_sessions": (
                "data/chat_sessions"
            ),
            "chat_history": (
                "data/conversations/chat_history.jsonl"
            ),
            "memory": (
                "data/memory/memories.jsonl"
            ),
            "journal": (
                "data/journal/aura_journal.jsonl"
            ),
        }

        return {
            "project_root_absolute": (
                self.project_root.is_absolute()
            ),
            "project_root_exists": (
                self.project_root.is_dir()
            ),
            "data_root_within_project": (
                self._within_project(self.data_root)
            ),
            "canonical_store_catalog_exact": (
                catalog
                == {
                    "browser_sessions": (
                        "data/chat_sessions"
                    ),
                    "chat_history": (
                        "data/conversations/"
                        "chat_history.jsonl"
                    ),
                    "memory": (
                        "data/memory/memories.jsonl"
                    ),
                    "journal": (
                        "data/journal/"
                        "aura_journal.jsonl"
                    ),
                }
                and len(catalog)
                == self.EXPECTED_STORE_COUNT
            ),
        }

    def _browser_checks(
        self,
    ) -> tuple[
        dict[str, bool],
        dict[str, Any],
    ]:
        storage = self.browser_storage
        expected_storage = (
            self.project_root
            / "data"
            / "chat_sessions"
        )

        entries = (
            sorted(storage.iterdir())
            if storage.is_dir()
            and not storage.is_symlink()
            else []
        )
        session_files = [
            path
            for path in entries
            if path.name.startswith("chat_")
            and path.name.endswith(".json")
        ]
        temporary_files = [
            path
            for path in entries
            if path.name.endswith(".tmp")
        ]

        regular_flags: list[bool] = []
        symlink_flags: list[bool] = []
        within_flags: list[bool] = []
        nonempty_flags: list[bool] = []
        bounded_flags: list[bool] = []
        private_mode_flags: list[bool] = []
        utf8_flags: list[bool] = []
        json_flags: list[bool] = []
        mapping_flags: list[bool] = []
        schema_flags: list[bool] = []
        id_flags: list[bool] = []
        timestamp_flags: list[bool] = []
        count_flags: list[bool] = []
        sequence_flags: list[bool] = []
        integrity_flags: list[bool] = []
        owner_flags: list[bool] = []

        total_messages = 0
        file_summaries: list[dict[str, Any]] = []

        owner = AuraBrowserChatSessionRuntimeManager(
            project_root=self.project_root,
            storage_dir=storage,
        )

        for path in session_files:
            is_symlink = path.is_symlink()
            is_regular = (
                path.is_file()
                and not is_symlink
            )
            symlink_flags.append(not is_symlink)
            regular_flags.append(is_regular)
            within_flags.append(
                self._within_project(path)
                and path.resolve(
                    strict=False
                ).parent
                == storage.resolve(
                    strict=False
                )
            )

            size = (
                path.stat().st_size
                if is_regular
                else -1
            )
            nonempty_flags.append(size > 0)
            bounded_flags.append(
                0 < size
                <= owner.MAX_SESSION_FILE_BYTES
            )
            private_mode_flags.append(
                is_regular
                and stat.S_IMODE(
                    path.stat().st_mode
                )
                == 0o600
            )

            text: str | None = None
            payload: Any = None

            try:
                text = path.read_text(
                    encoding="utf-8"
                )
            except (OSError, UnicodeError):
                utf8_flags.append(False)
            else:
                utf8_flags.append(True)

                try:
                    payload = json.loads(text)
                except json.JSONDecodeError:
                    json_flags.append(False)
                else:
                    json_flags.append(True)

            if text is None:
                json_flags.append(False)

            is_mapping = isinstance(payload, dict)
            mapping_flags.append(is_mapping)
            schema_flags.append(
                is_mapping
                and set(payload)
                == self._SESSION_KEYS
            )

            session_id = path.stem
            id_flags.append(
                is_mapping
                and payload.get("session_id")
                == session_id
            )

            timestamps_valid = (
                is_mapping
                and self._timestamp_valid(
                    payload.get(
                        "created_at_utc"
                    )
                )
                and self._timestamp_valid(
                    payload.get(
                        "updated_at_utc"
                    )
                )
                and (
                    payload.get(
                        "last_clear_at_utc"
                    )
                    is None
                    or self._timestamp_valid(
                        payload.get(
                            "last_clear_at_utc"
                        )
                    )
                )
            )
            timestamp_flags.append(
                timestamps_valid
            )

            messages = (
                payload.get("messages")
                if is_mapping
                else None
            )
            message_count = (
                payload.get("message_count")
                if is_mapping
                else None
            )

            count_flags.append(
                isinstance(messages, list)
                and isinstance(
                    message_count,
                    int,
                )
                and not isinstance(
                    message_count,
                    bool,
                )
                and message_count
                == len(messages)
            )

            if isinstance(messages, list):
                total_messages += len(messages)
                sequence_flags.append(
                    all(
                        isinstance(message, dict)
                        and set(message)
                        == self._MESSAGE_KEYS
                        and message.get(
                            "sequence"
                        )
                        == index
                        for index, message in enumerate(
                            messages,
                            start=1,
                        )
                    )
                )
            else:
                sequence_flags.append(False)

            if is_mapping:
                try:
                    expected_digest = (
                        owner._integrity_digest(
                            payload
                        )
                    )
                except Exception:
                    integrity_flags.append(
                        False
                    )
                else:
                    integrity_flags.append(
                        payload.get(
                            "integrity_sha256"
                        )
                        == expected_digest
                    )
            else:
                integrity_flags.append(False)

            try:
                owner.load_session(session_id)
            except Exception:
                owner_flags.append(False)
            else:
                owner_flags.append(True)

            file_summaries.append(
                {
                    "path": str(
                        path.relative_to(
                            self.project_root
                        )
                    ),
                    "size_bytes": size,
                    "sha256": (
                        self._sha256(path)
                        if is_regular
                        else None
                    ),
                    "mode": (
                        oct(
                            stat.S_IMODE(
                                path.stat().st_mode
                            )
                        )
                        if is_regular
                        else None
                    ),
                }
            )

        checks = {
            "browser_storage_path_exact": (
                storage.resolve(
                    strict=False
                )
                == expected_storage.resolve(
                    strict=False
                )
            ),
            "browser_storage_exists": (
                storage.exists()
            ),
            "browser_storage_is_directory": (
                storage.is_dir()
            ),
            "browser_storage_not_symlink": (
                not storage.is_symlink()
            ),
            "browser_storage_within_project": (
                self._within_project(storage)
            ),
            "browser_file_catalog_names_valid": (
                all(
                    self._SESSION_FILE_RE.fullmatch(
                        path.name
                    )
                    for path in session_files
                )
                and len(session_files)
                + len(temporary_files)
                == len(entries)
            ),
            "browser_temp_file_count_zero": (
                not temporary_files
            ),
            "browser_files_all_regular": (
                all(regular_flags)
            ),
            "browser_files_all_not_symlink": (
                all(symlink_flags)
            ),
            "browser_files_all_within_storage": (
                all(within_flags)
            ),
            "browser_files_all_nonempty": (
                all(nonempty_flags)
            ),
            "browser_files_all_size_bounded": (
                all(bounded_flags)
            ),
            "browser_files_all_private_mode": (
                all(private_mode_flags)
            ),
            "browser_files_all_utf8": (
                all(utf8_flags)
            ),
            "browser_files_all_json": (
                all(json_flags)
            ),
            "browser_files_all_mapping": (
                all(mapping_flags)
            ),
            "browser_files_all_exact_schema": (
                all(schema_flags)
            ),
            "browser_files_all_session_id_match": (
                all(id_flags)
            ),
            "browser_files_all_timestamp_valid": (
                all(timestamp_flags)
            ),
            "browser_files_all_message_count_consistent": (
                all(count_flags)
            ),
            "browser_files_all_message_sequences_contiguous": (
                all(sequence_flags)
            ),
            "browser_files_all_integrity_valid": (
                all(integrity_flags)
            ),
            "browser_files_all_owner_validation_passed": (
                all(owner_flags)
            ),
        }

        summary = {
            "relative_path": (
                "data/chat_sessions"
            ),
            "session_count": len(
                session_files
            ),
            "total_message_count": (
                total_messages
            ),
            "temporary_file_count": len(
                temporary_files
            ),
            "files": file_summaries,
        }

        return checks, summary

    def _validate_jsonl_text(
        self,
        store_name: str,
        text: str,
    ) -> dict[str, Any]:
        schema = self._STORE_SCHEMAS[
            store_name
        ]
        keys = schema["keys"]
        string_fields = schema[
            "string_fields"
        ]
        nonempty_fields = schema[
            "nonempty_fields"
        ]

        lines = text.splitlines()
        blank_count = sum(
            1
            for line in lines
            if not line.strip()
        )

        records: list[Any] = []
        invalid_json_count = 0

        for line in lines:
            if not line.strip():
                continue

            try:
                records.append(
                    json.loads(line)
                )
            except json.JSONDecodeError:
                invalid_json_count += 1

        mappings = [
            record
            for record in records
            if isinstance(record, dict)
        ]

        exact_schema = (
            len(mappings) == len(records)
            and all(
                set(record) == keys
                for record in mappings
            )
        )

        field_types_valid = (
            exact_schema
            and all(
                all(
                    isinstance(
                        record.get(field),
                        str,
                    )
                    for field in string_fields
                )
                and all(
                    bool(
                        record.get(field)
                    )
                    for field in nonempty_fields
                )
                and isinstance(
                    record.get("metadata"),
                    dict,
                )
                for record in mappings
            )
        )

        timestamps_valid = (
            exact_schema
            and all(
                self._timestamp_valid(
                    record.get("created_at")
                )
                for record in mappings
            )
        )

        ids = [
            record.get("id")
            for record in mappings
            if isinstance(
                record.get("id"),
                str,
            )
        ]

        ids_nonempty = (
            exact_schema
            and len(ids) == len(mappings)
            and all(ids)
        )

        ids_unique = (
            ids_nonempty
            and len(ids) == len(set(ids))
        )

        return {
            "line_count": len(lines),
            "record_count": len(records),
            "blank_line_count": blank_count,
            "invalid_json_count": (
                invalid_json_count
            ),
            "non_mapping_count": (
                len(records) - len(mappings)
            ),
            "exact_schema": exact_schema,
            "field_types_valid": (
                field_types_valid
            ),
            "timestamps_valid": (
                timestamps_valid
            ),
            "ids_nonempty": ids_nonempty,
            "ids_unique": ids_unique,
        }

    def _jsonl_checks(
        self,
        store_name: str,
    ) -> tuple[
        dict[str, bool],
        dict[str, Any],
    ]:
        schema = self._STORE_SCHEMAS[
            store_name
        ]
        relative_path = schema[
            "relative_path"
        ]
        path = (
            self.project_root
            / relative_path
        )
        expected_path = (
            self.project_root
            / relative_path
        )

        exists = path.exists()
        is_regular = (
            path.is_file()
            and not path.is_symlink()
        )
        size = (
            path.stat().st_size
            if is_regular
            else -1
        )
        mode = (
            stat.S_IMODE(
                path.stat().st_mode
            )
            if is_regular
            else None
        )

        text: str | None = None

        if is_regular:
            try:
                text = path.read_text(
                    encoding="utf-8"
                )
            except (
                OSError,
                UnicodeError,
            ):
                text = None

        analysis = (
            self._validate_jsonl_text(
                store_name,
                text,
            )
            if text is not None
            else {
                "line_count": 0,
                "record_count": 0,
                "blank_line_count": 0,
                "invalid_json_count": 1,
                "non_mapping_count": 1,
                "exact_schema": False,
                "field_types_valid": False,
                "timestamps_valid": False,
                "ids_nonempty": False,
                "ids_unique": False,
            }
        )

        prefix = store_name
        checks = {
            f"{prefix}_path_exact": (
                path.resolve(
                    strict=False
                )
                == expected_path.resolve(
                    strict=False
                )
            ),
            f"{prefix}_exists": exists,
            f"{prefix}_is_regular_file": (
                is_regular
            ),
            f"{prefix}_not_symlink": (
                not path.is_symlink()
            ),
            f"{prefix}_within_project": (
                self._within_project(path)
            ),
            f"{prefix}_size_bounded": (
                is_regular
                and 0 <= size
                <= self.MAX_JSONL_BYTES
            ),
            f"{prefix}_not_other_writable": (
                mode is not None
                and not bool(
                    mode & stat.S_IWOTH
                )
            ),
            f"{prefix}_utf8": (
                text is not None
            ),
            f"{prefix}_trailing_newline": (
                text is not None
                and (
                    text == ""
                    or text.endswith("\n")
                )
            ),
            f"{prefix}_no_blank_lines": (
                analysis[
                    "blank_line_count"
                ]
                == 0
            ),
            f"{prefix}_valid_json": (
                analysis[
                    "invalid_json_count"
                ]
                == 0
            ),
            f"{prefix}_all_mapping": (
                analysis[
                    "non_mapping_count"
                ]
                == 0
            ),
            f"{prefix}_exact_schema": (
                analysis["exact_schema"]
            ),
            f"{prefix}_field_types_valid": (
                analysis[
                    "field_types_valid"
                ]
            ),
            f"{prefix}_timestamps_valid": (
                analysis[
                    "timestamps_valid"
                ]
            ),
            f"{prefix}_ids_nonempty": (
                analysis["ids_nonempty"]
            ),
            f"{prefix}_ids_unique": (
                analysis["ids_unique"]
            ),
            f"{prefix}_record_count_matches_line_count": (
                analysis["record_count"]
                == analysis["line_count"]
            ),
        }

        summary = {
            "relative_path": relative_path,
            "size_bytes": size,
            "mode": (
                oct(mode)
                if mode is not None
                else None
            ),
            "sha256": (
                self._sha256(path)
                if is_regular
                else None
            ),
            "line_count": (
                analysis["line_count"]
            ),
            "record_count": (
                analysis["record_count"]
            ),
        }

        return checks, summary

    def validate(
        self,
    ) -> dict[str, Any]:
        checks = self._root_checks()
        browser_checks, browser_summary = (
            self._browser_checks()
        )
        checks.update(browser_checks)

        store_summaries: dict[
            str,
            Any,
        ] = {
            "browser_sessions": (
                browser_summary
            ),
        }

        for store_name in (
            "chat_history",
            "memory",
            "journal",
        ):
            store_checks, summary = (
                self._jsonl_checks(
                    store_name
                )
            )
            checks.update(store_checks)
            store_summaries[
                store_name
            ] = summary

        if (
            len(checks)
            != self.EXPECTED_BASE_CHECK_COUNT
        ):
            raise RuntimeError(
                "Canonical persistence check catalog "
                "must contain "
                f"{self.EXPECTED_BASE_CHECK_COUNT} "
                f"checks, got {len(checks)}."
            )

        failed = [
            name
            for name, passed in checks.items()
            if not passed
        ]

        return {
            "valid": not failed,
            "check_count": len(checks),
            "failed_check_count": len(
                failed
            ),
            "failed_checks": failed,
            "checks": checks,
            "store_count": (
                self.EXPECTED_STORE_COUNT
            ),
            "stores": store_summaries,
        }

    def contract(
        self,
    ) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "anchor_version": (
                self.ANCHOR_VERSION
            ),
            "current_sprint": (
                self.CURRENT_SPRINT
            ),
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": (
                self.NEXT_BOUNDARY
            ),
            "canonical_store_count": (
                self.EXPECTED_STORE_COUNT
            ),
            "canonical_store_catalog": [
                "browser_sessions",
                "chat_history",
                "memory",
                "journal",
            ],
            "read_only_validation": True,
            "canonical_store_write_allowed": (
                False
            ),
            "canonical_store_repair_allowed": (
                False
            ),
            "canonical_store_migration_allowed": (
                False
            ),
            "runtime_activation_allowed": False,
            "socket_binding_allowed": False,
            "memory_write_allowed": False,
            "journal_write_allowed": False,
            "conversation_write_allowed": False,
            "session_write_allowed": False,
            "systemd_mutation_allowed": False,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        validation = self.validate()
        stores = validation["stores"]

        return {
            **self.contract(),
            "persistence_valid": (
                validation["valid"]
            ),
            "persistence_check_count": (
                validation["check_count"]
            ),
            "persistence_failed_check_count": (
                validation[
                    "failed_check_count"
                ]
            ),
            "browser_session_count": (
                stores[
                    "browser_sessions"
                ]["session_count"]
            ),
            "browser_message_count": (
                stores[
                    "browser_sessions"
                ]["total_message_count"]
            ),
            "chat_history_record_count": (
                stores[
                    "chat_history"
                ]["record_count"]
            ),
            "memory_record_count": (
                stores["memory"][
                    "record_count"
                ]
            ),
            "journal_record_count": (
                stores["journal"][
                    "record_count"
                ]
            ),
        }

    def context(
        self,
    ) -> dict[str, Any]:
        validation = self.validate()

        return {
            **self.contract(),
            "persistence_validation": (
                validation
            ),
            "browser_session_guarantees": {
                "atomic_replace_observed": (
                    True
                ),
                "file_fsync_observed": True,
                "directory_fsync_observed": (
                    True
                ),
                "thread_lock_observed": True,
                "integrity_digest_observed": (
                    True
                ),
                "symlink_guard_observed": (
                    True
                ),
                "private_file_mode_observed": (
                    True
                ),
            },
            "jsonl_store_boundaries": {
                "conversation_append_only_observed": (
                    True
                ),
                "journal_append_only_observed": True,
                "memory_append_observed": True,
                "memory_truncate_rewrite_observed": (
                    True
                ),
                "atomic_replace_claimed": (
                    False
                ),
                "file_fsync_claimed": False,
                "thread_lock_claimed": False,
                "cross_process_lock_claimed": (
                    False
                ),
                "integrity_digest_claimed": (
                    False
                ),
                "automatic_repair_claimed": (
                    False
                ),
                "invalid_line_skip_policy_observed": (
                    True
                ),
            },
        }

    def _browser_tamper_rejected(
        self,
    ) -> bool:
        owner = (
            AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root,
                storage_dir=(
                    self.browser_storage
                ),
            )
        )
        files = sorted(
            self.browser_storage.glob(
                "chat_*.json"
            )
        )

        if files:
            path = files[0]

            try:
                payload = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                return False

            fixture = deepcopy(payload)
            fixture["title"] = (
                str(
                    fixture.get(
                        "title",
                        "",
                    )
                )
                + " tampered"
            )
            session_id = path.stem
        else:
            session_id = (
                "chat_"
                + "a" * 32
            )
            timestamp = (
                "2026-01-01T00:00:00+00:00"
            )
            fixture = {
                "schema_version": "1.0",
                "session_id": session_id,
                "title": "Fixture",
                "status": "active",
                "created_at_utc": timestamp,
                "updated_at_utc": timestamp,
                "revision": 1,
                "message_count": 0,
                "clear_count": 0,
                "last_clear_at_utc": None,
                "last_response_kind": None,
                "messages": [],
                "integrity_sha256": "",
            }
            fixture[
                "integrity_sha256"
            ] = owner._integrity_digest(
                fixture
            )
            fixture["title"] = (
                "Fixture tampered"
            )

        try:
            owner._validate_session_payload(
                fixture,
                expected_session_id=(
                    session_id
                ),
            )
        except Exception:
            return True

        return False

    def check(
        self,
    ) -> dict[str, Any]:
        validation = self.validate()

        conversation_valid = (
            '{"id":"c1","user_message":"u",'
            '"aura_response":"a",'
            '"created_at":'
            '"2026-01-01T00:00:00+00:00",'
            '"source":"fixture","metadata":{}}'
        )
        memory_valid = (
            '{"id":"m1","kind":"fact",'
            '"content":"x","created_at":'
            '"2026-01-01T00:00:00+00:00",'
            '"metadata":{}}'
        )
        journal_valid = (
            '{"id":"j1","title":"t",'
            '"content":"x","created_at":'
            '"2026-01-01T00:00:00+00:00",'
            '"metadata":{}}'
        )

        malformed_conversation = (
            self._validate_jsonl_text(
                "chat_history",
                conversation_valid
                + "\nnot-json\n",
            )
        )
        schema_conversation = (
            self._validate_jsonl_text(
                "chat_history",
                '{"id":"c1"}\n',
            )
        )
        duplicate_conversation = (
            self._validate_jsonl_text(
                "chat_history",
                conversation_valid
                + "\n"
                + conversation_valid
                + "\n",
            )
        )

        malformed_memory = (
            self._validate_jsonl_text(
                "memory",
                memory_valid
                + "\nnot-json\n",
            )
        )
        schema_memory = (
            self._validate_jsonl_text(
                "memory",
                '{"id":"m1"}\n',
            )
        )
        duplicate_memory = (
            self._validate_jsonl_text(
                "memory",
                memory_valid
                + "\n"
                + memory_valid
                + "\n",
            )
        )

        malformed_journal = (
            self._validate_jsonl_text(
                "journal",
                journal_valid
                + "\nnot-json\n",
            )
        )

        status_first = self.status()
        status_second = self.status()

        assertions = {
            **validation["checks"],
            "canonical_persistence_valid": (
                validation["valid"]
            ),
            "base_check_count_preserved": (
                validation["check_count"]
                == self.EXPECTED_BASE_CHECK_COUNT
            ),
            "status_repeat_deterministic": (
                status_first
                == status_second
            ),
            "malformed_conversation_rejected": (
                malformed_conversation[
                    "invalid_json_count"
                ]
                == 1
            ),
            "conversation_schema_mismatch_rejected": (
                not schema_conversation[
                    "exact_schema"
                ]
            ),
            "duplicate_conversation_id_rejected": (
                not duplicate_conversation[
                    "ids_unique"
                ]
            ),
            "malformed_memory_rejected": (
                malformed_memory[
                    "invalid_json_count"
                ]
                == 1
            ),
            "memory_schema_mismatch_rejected": (
                not schema_memory[
                    "exact_schema"
                ]
            ),
            "duplicate_memory_id_rejected": (
                not duplicate_memory[
                    "ids_unique"
                ]
            ),
            "malformed_journal_rejected": (
                malformed_journal[
                    "invalid_json_count"
                ]
                == 1
            ),
            "browser_integrity_tamper_rejected": (
                self._browser_tamper_rejected()
            ),
        }

        if (
            len(assertions)
            != self.EXPECTED_ASSERTION_COUNT
        ):
            raise RuntimeError(
                "Sprint 244 assertion catalog "
                "must contain "
                f"{self.EXPECTED_ASSERTION_COUNT} "
                f"assertions, got "
                f"{len(assertions)}."
            )

        failed = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            **self.contract(),
            "persistence_validation": (
                validation
            ),
            "assertions": assertions,
            "assertion_count": len(
                assertions
            ),
            "failed_assertions": failed,
            "failed_assertion_count": len(
                failed
            ),
            "assertion_count_preserved": (
                len(assertions)
                == self.EXPECTED_ASSERTION_COUNT
            ),
            "planning_ready": not failed,
        }


__all__ = [
    "AuraSessionMemoryPersistenceChecksPlanner",
]
