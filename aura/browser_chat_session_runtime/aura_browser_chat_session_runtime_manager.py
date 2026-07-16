"""AURA Sprint 186 Browser Chat Session Runtime core.

This module provides bounded local session persistence and deterministic,
honest response delivery without invoking a model, tool, action, command,
desktop operation, network fallback, or AURA long-term memory.
"""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import re
import stat
import tempfile
import threading
import unicodedata
import uuid
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


class BrowserChatSessionError(RuntimeError):
    """Base error for the local browser chat session runtime."""


class BrowserChatValidationError(BrowserChatSessionError):
    """Raised when an input or persisted schema is invalid."""


class BrowserChatSessionNotFoundError(BrowserChatSessionError):
    """Raised when a requested session does not exist."""


class BrowserChatSessionConflictError(BrowserChatSessionError):
    """Raised when an optimistic revision check fails."""


class BrowserChatSessionCorruptionError(BrowserChatSessionError):
    """Raised when persisted session integrity cannot be verified."""


class BrowserChatClearConfirmationError(BrowserChatSessionError):
    """Raised when clear-session confirmation is missing or invalid."""


class AuraBrowserChatSessionRuntimeManager:
    """Manage bounded, local, persistent chat sessions without a model."""

    name = "aura_browser_chat_session_runtime"
    component_version = "0.2.0-alpha"
    sprint = 186
    schema_version = "1.0"
    persistent_activation_version = "1.1.6"
    persistent_activation_sprint = 256

    MAX_TITLE_CHARS = 120
    MAX_MESSAGE_CHARS = 8192
    MAX_MESSAGE_BYTES = 32768
    MAX_MESSAGES_PER_SESSION = 500
    MAX_SESSION_FILE_BYTES = 2 * 1024 * 1024
    STORAGE_DIRECTORY_MODE = 0o700
    SESSION_FILE_MODE = 0o600
    RESPONSE_KIND = "model_bridge_unavailable"
    LOCAL_MODEL_RESPONSE_KIND = "local_model_response"
    CLEAR_PREFIX = "CLEAR "

    _SESSION_ID_RE = re.compile(r"^chat_[0-9a-f]{32}$")
    _MESSAGE_ID_RE = re.compile(r"^msg_[0-9a-f]{32}$")
    _CLIENT_MESSAGE_ID_RE = re.compile(
        r"^client_[A-Za-z0-9_-]{1,64}$"
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        storage_dir: str | Path | None = None,
        now_factory: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root).resolve()
        if storage_dir is None:
            storage_dir = (
                self.project_root
                / "data"
                / "chat_sessions"
            )

        self.storage_dir = Path(storage_dir).resolve(
            strict=False
        )
        self._now_factory = now_factory or (
            lambda: datetime.now(timezone.utc)
        )
        self._id_factory = id_factory or (
            lambda: uuid.uuid4().hex
        )
        self._lock = threading.RLock()

    @staticmethod
    def _private_mode(
        metadata: os.stat_result,
    ) -> bool:
        return (
            stat.S_IMODE(metadata.st_mode)
            & 0o077
        ) == 0

    def _prepare_storage_directory(
        self,
    ) -> None:
        if self.storage_dir.is_symlink():
            raise BrowserChatSessionCorruptionError(
                "Storage directory symlinks are not allowed."
            )

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True,
            mode=self.STORAGE_DIRECTORY_MODE,
        )
        os.chmod(
            self.storage_dir,
            self.STORAGE_DIRECTORY_MODE,
        )
        metadata = self.storage_dir.stat()

        if not stat.S_ISDIR(
            metadata.st_mode
        ):
            raise BrowserChatSessionCorruptionError(
                "Chat session storage is not a directory."
            )

        if metadata.st_uid != os.getuid():
            raise BrowserChatSessionCorruptionError(
                "Chat session storage has the wrong owner."
            )

        if not self._private_mode(metadata):
            raise BrowserChatSessionCorruptionError(
                "Chat session storage permissions are too broad."
            )

    @contextmanager
    def _storage_lock(
        self,
        *,
        exclusive: bool,
        create: bool,
    ):
        if create:
            self._prepare_storage_directory()
        elif not self.storage_dir.exists():
            yield None
            return

        flags = (
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )

        try:
            descriptor = os.open(
                self.storage_dir,
                flags,
            )
        except OSError as exc:
            code = (
                "storage directory symlink rejected"
                if exc.errno == errno.ELOOP
                else "storage directory open failed"
            )
            raise BrowserChatSessionCorruptionError(
                f"{code}: {type(exc).__name__}"
            ) from exc

        try:
            metadata = os.fstat(descriptor)

            if not stat.S_ISDIR(
                metadata.st_mode
            ):
                raise BrowserChatSessionCorruptionError(
                    "Chat session storage descriptor is not a directory."
                )

            if metadata.st_uid != os.getuid():
                raise BrowserChatSessionCorruptionError(
                    "Chat session storage descriptor has the wrong owner."
                )

            if exclusive and not self._private_mode(
                metadata
            ):
                raise BrowserChatSessionCorruptionError(
                    "Chat session storage must be private before mutation."
                )

            fcntl.flock(
                descriptor,
                (
                    fcntl.LOCK_EX
                    if exclusive
                    else fcntl.LOCK_SH
                ),
            )
            yield descriptor
        finally:
            try:
                fcntl.flock(
                    descriptor,
                    fcntl.LOCK_UN,
                )
            finally:
                os.close(descriptor)

    def _validate_session_metadata(
        self,
        metadata: os.stat_result,
        *,
        path: Path,
    ) -> None:
        if not stat.S_ISREG(
            metadata.st_mode
        ):
            raise BrowserChatSessionCorruptionError(
                f"Session path is not a regular file: {path.name}"
            )

        if metadata.st_uid != os.getuid():
            raise BrowserChatSessionCorruptionError(
                f"Session file has the wrong owner: {path.name}"
            )

        if not self._private_mode(metadata):
            raise BrowserChatSessionCorruptionError(
                f"Session file permissions are too broad: {path.name}"
            )

        if metadata.st_size > self.MAX_SESSION_FILE_BYTES:
            raise BrowserChatSessionCorruptionError(
                "Session file exceeds the size limit."
            )

    @staticmethod
    def _canonical_bytes(
        payload: dict[str, Any],
    ) -> bytes:
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    @classmethod
    def _integrity_digest(
        cls,
        payload: dict[str, Any],
    ) -> str:
        unsigned = dict(payload)
        unsigned.pop("integrity_sha256", None)
        return hashlib.sha256(
            cls._canonical_bytes(unsigned)
        ).hexdigest()

    @staticmethod
    def _normalize_text(value: str) -> str:
        return unicodedata.normalize("NFKC", value)

    @staticmethod
    def _utc_text(value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return (
            value.astimezone(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

    def _now(self) -> str:
        return self._utc_text(self._now_factory())

    def _new_identifier(self, prefix: str) -> str:
        token = str(self._id_factory()).lower()
        if not re.fullmatch(r"[0-9a-f]{32}", token):
            raise BrowserChatValidationError(
                "id_factory must return exactly 32 lowercase "
                "hexadecimal characters."
            )
        return prefix + token

    @classmethod
    def _validate_session_id(cls, session_id: Any) -> str:
        if not isinstance(session_id, str):
            raise BrowserChatValidationError(
                "session_id must be a string."
            )
        if not cls._SESSION_ID_RE.fullmatch(session_id):
            raise BrowserChatValidationError(
                "session_id must match chat_<32 lowercase hex>."
            )
        return session_id

    @classmethod
    def _validate_message_id(cls, message_id: Any) -> str:
        if not isinstance(message_id, str):
            raise BrowserChatValidationError(
                "message_id must be a string."
            )
        if not cls._MESSAGE_ID_RE.fullmatch(message_id):
            raise BrowserChatValidationError(
                "message_id must match msg_<32 lowercase hex>."
            )
        return message_id

    @classmethod
    def _validate_client_message_id(
        cls,
        client_message_id: Any,
    ) -> str | None:
        if client_message_id is None:
            return None
        if not isinstance(client_message_id, str):
            raise BrowserChatValidationError(
                "client_message_id must be a string or null."
            )
        if not cls._CLIENT_MESSAGE_ID_RE.fullmatch(
            client_message_id
        ):
            raise BrowserChatValidationError(
                "client_message_id must match "
                "client_<1-64 safe characters>."
            )
        return client_message_id

    @classmethod
    def _validate_title(cls, title: Any) -> str:
        if title is None:
            return "New local session"
        if not isinstance(title, str):
            raise BrowserChatValidationError(
                "title must be a string or null."
            )

        normalized = cls._normalize_text(title).strip()
        if not normalized:
            raise BrowserChatValidationError(
                "title must not be empty."
            )
        if len(normalized) > cls.MAX_TITLE_CHARS:
            raise BrowserChatValidationError(
                f"title exceeds {cls.MAX_TITLE_CHARS} characters."
            )
        if any(ord(char) < 32 for char in normalized):
            raise BrowserChatValidationError(
                "title contains a control character."
            )
        return normalized

    @classmethod
    def _validate_message_content(cls, content: Any) -> str:
        if not isinstance(content, str):
            raise BrowserChatValidationError(
                "message content must be a string."
            )

        normalized = cls._normalize_text(content).strip()
        if not normalized:
            raise BrowserChatValidationError(
                "message content must not be empty."
            )
        if len(normalized) > cls.MAX_MESSAGE_CHARS:
            raise BrowserChatValidationError(
                "message content exceeds the character limit."
            )
        if (
            len(normalized.encode("utf-8"))
            > cls.MAX_MESSAGE_BYTES
        ):
            raise BrowserChatValidationError(
                "message content exceeds the byte limit."
            )

        invalid_controls = [
            char
            for char in normalized
            if ord(char) < 32
            and char not in ("\n", "\t")
        ]
        if invalid_controls:
            raise BrowserChatValidationError(
                "message content contains a disallowed "
                "control character."
            )
        return normalized

    @staticmethod
    def _validate_expected_revision(
        expected_revision: Any,
    ) -> int | None:
        if expected_revision is None:
            return None
        if (
            isinstance(expected_revision, bool)
            or not isinstance(expected_revision, int)
            or expected_revision < 1
        ):
            raise BrowserChatValidationError(
                "expected_revision must be a positive integer."
            )
        return expected_revision

    def _session_path(self, session_id: str) -> Path:
        validated = self._validate_session_id(
            session_id
        )
        path = (
            self.storage_dir
            / f"{validated}.json"
        )

        if path.parent != self.storage_dir:
            raise BrowserChatValidationError(
                "session path escapes the storage directory."
            )

        return path

    @staticmethod
    def _metadata(
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "schema_version": payload["schema_version"],
            "session_id": payload["session_id"],
            "title": payload["title"],
            "status": payload["status"],
            "created_at_utc": payload["created_at_utc"],
            "updated_at_utc": payload["updated_at_utc"],
            "revision": payload["revision"],
            "message_count": payload["message_count"],
            "clear_count": payload["clear_count"],
            "last_clear_at_utc": payload[
                "last_clear_at_utc"
            ],
            "last_response_kind": payload[
                "last_response_kind"
            ],
        }

    @classmethod
    def clear_confirmation_phrase(
        cls,
        session_id: str,
    ) -> str:
        validated = cls._validate_session_id(session_id)
        return cls.CLEAR_PREFIX + validated

    def _validate_message(
        self,
        message: Any,
        *,
        expected_sequence: int,
    ) -> None:
        if not isinstance(message, dict):
            raise BrowserChatSessionCorruptionError(
                "Persisted message is not an object."
            )

        required = {
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
        if set(message) != required:
            raise BrowserChatSessionCorruptionError(
                "Persisted message schema is invalid."
            )

        try:
            self._validate_message_id(message["message_id"])
            self._validate_message_content(message["content"])
            self._validate_client_message_id(
                message["client_message_id"]
            )
        except BrowserChatValidationError as exc:
            raise BrowserChatSessionCorruptionError(
                str(exc)
            ) from exc

        if message["sequence"] != expected_sequence:
            raise BrowserChatSessionCorruptionError(
                "Persisted message sequence is not contiguous."
            )
        if message["role"] not in {"user", "assistant"}:
            raise BrowserChatSessionCorruptionError(
                "Persisted message role is invalid."
            )
        if not isinstance(message["created_at_utc"], str):
            raise BrowserChatSessionCorruptionError(
                "Persisted message timestamp is invalid."
            )
        for key in (
            "model_invoked",
            "tools_invoked",
            "actions_invoked",
        ):
            if not isinstance(message[key], bool):
                raise BrowserChatSessionCorruptionError(
                    f"Persisted message {key} must be boolean."
                )

        if message["role"] == "user":
            if message["response_kind"] is not None:
                raise BrowserChatSessionCorruptionError(
                    "User message response_kind must be null."
                )
        else:
            response_kind = message["response_kind"]
            if response_kind not in {
                self.RESPONSE_KIND,
                self.LOCAL_MODEL_RESPONSE_KIND,
            }:
                raise BrowserChatSessionCorruptionError(
                    "Assistant response kind is invalid."
                )

            if response_kind == self.RESPONSE_KIND:
                if message["model_invoked"]:
                    raise BrowserChatSessionCorruptionError(
                        "Placeholder response cannot mark a model invocation."
                    )
            elif not message["model_invoked"]:
                raise BrowserChatSessionCorruptionError(
                    "Local model response must mark model_invoked true."
                )

            if (
                message["tools_invoked"]
                or message["actions_invoked"]
            ):
                raise BrowserChatSessionCorruptionError(
                    "Assistant response cannot invoke tools or actions."
                )

    def _validate_session_payload(
        self,
        payload: Any,
        *,
        expected_session_id: str,
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise BrowserChatSessionCorruptionError(
                "Persisted session is not an object."
            )

        required = {
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
        if set(payload) != required:
            raise BrowserChatSessionCorruptionError(
                "Persisted session schema is invalid."
            )

        if payload["schema_version"] != self.schema_version:
            raise BrowserChatSessionCorruptionError(
                "Persisted session schema version is unsupported."
            )
        if payload["session_id"] != expected_session_id:
            raise BrowserChatSessionCorruptionError(
                "Persisted session id does not match its filename."
            )

        try:
            self._validate_session_id(payload["session_id"])
            self._validate_title(payload["title"])
        except BrowserChatValidationError as exc:
            raise BrowserChatSessionCorruptionError(
                str(exc)
            ) from exc

        if payload["status"] != "active":
            raise BrowserChatSessionCorruptionError(
                "Persisted session status is invalid."
            )
        if (
            not isinstance(payload["created_at_utc"], str)
            or not isinstance(payload["updated_at_utc"], str)
        ):
            raise BrowserChatSessionCorruptionError(
                "Persisted session timestamp is invalid."
            )
        if (
            isinstance(payload["revision"], bool)
            or not isinstance(payload["revision"], int)
            or payload["revision"] < 1
        ):
            raise BrowserChatSessionCorruptionError(
                "Persisted session revision is invalid."
            )
        if (
            isinstance(payload["clear_count"], bool)
            or not isinstance(payload["clear_count"], int)
            or payload["clear_count"] < 0
        ):
            raise BrowserChatSessionCorruptionError(
                "Persisted clear_count is invalid."
            )
        if (
            payload["last_clear_at_utc"] is not None
            and not isinstance(
                payload["last_clear_at_utc"],
                str,
            )
        ):
            raise BrowserChatSessionCorruptionError(
                "Persisted last_clear_at_utc is invalid."
            )
        if payload["last_response_kind"] not in {
            None,
            self.RESPONSE_KIND,
            self.LOCAL_MODEL_RESPONSE_KIND,
        }:
            raise BrowserChatSessionCorruptionError(
                "Persisted last_response_kind is invalid."
            )
        if not isinstance(payload["messages"], list):
            raise BrowserChatSessionCorruptionError(
                "Persisted messages must be a list."
            )
        if len(payload["messages"]) > self.MAX_MESSAGES_PER_SESSION:
            raise BrowserChatSessionCorruptionError(
                "Persisted message count exceeds the limit."
            )
        if payload["message_count"] != len(payload["messages"]):
            raise BrowserChatSessionCorruptionError(
                "Persisted message_count does not match messages."
            )

        for sequence, message in enumerate(
            payload["messages"],
            start=1,
        ):
            self._validate_message(
                message,
                expected_sequence=sequence,
            )

        expected_digest = self._integrity_digest(payload)
        if payload["integrity_sha256"] != expected_digest:
            raise BrowserChatSessionCorruptionError(
                "Persisted session integrity hash does not match."
            )

        return payload

    def _read_session_unlocked(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        validated = self._validate_session_id(
            session_id
        )
        path = self._session_path(validated)
        filename = f"{validated}.json"

        with self._storage_lock(
            exclusive=False,
            create=False,
        ) as directory_fd:
            if directory_fd is None:
                raise BrowserChatSessionNotFoundError(
                    f"Session not found: {validated}"
                )

            flags = (
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )

            try:
                descriptor = os.open(
                    filename,
                    flags,
                    dir_fd=directory_fd,
                )
            except FileNotFoundError as exc:
                raise BrowserChatSessionNotFoundError(
                    f"Session not found: {validated}"
                ) from exc
            except OSError as exc:
                if exc.errno == errno.ELOOP:
                    raise BrowserChatSessionCorruptionError(
                        "Session file symlinks are not allowed."
                    ) from exc

                raise BrowserChatSessionCorruptionError(
                    "Session file could not be opened safely: "
                    f"{type(exc).__name__}"
                ) from exc

            try:
                before = os.fstat(descriptor)
                self._validate_session_metadata(
                    before,
                    path=path,
                )

                with os.fdopen(
                    descriptor,
                    "rb",
                ) as handle:
                    descriptor = -1
                    raw = handle.read(
                        self.MAX_SESSION_FILE_BYTES + 1
                    )
                    after = os.fstat(
                        handle.fileno()
                    )
            finally:
                if descriptor >= 0:
                    os.close(descriptor)

        if (
            before.st_dev != after.st_dev
            or before.st_ino != after.st_ino
        ):
            raise BrowserChatSessionCorruptionError(
                "Session file identity changed during read."
            )

        if len(raw) > self.MAX_SESSION_FILE_BYTES:
            raise BrowserChatSessionCorruptionError(
                "Session file exceeds the size limit."
            )

        try:
            payload = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeError,
            json.JSONDecodeError,
        ) as exc:
            raise BrowserChatSessionCorruptionError(
                "Session file cannot be decoded: "
                f"{type(exc).__name__}"
            ) from exc

        return self._validate_session_payload(
            payload,
            expected_session_id=validated,
        )

    def _write_session_unlocked(
        self,
        payload: dict[str, Any],
        *,
        expected_absent: bool = False,
    ) -> None:
        session_id = self._validate_session_id(
            payload.get("session_id")
        )
        path = self._session_path(session_id)
        filename = f"{session_id}.json"

        payload = deepcopy(payload)
        payload["integrity_sha256"] = (
            self._integrity_digest(payload)
        )
        self._validate_session_payload(
            payload,
            expected_session_id=session_id,
        )

        body = (
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

        if len(body) > self.MAX_SESSION_FILE_BYTES:
            raise BrowserChatValidationError(
                "Serialized session exceeds the size limit."
            )

        temporary_name = (
            f".{session_id}."
            f"{os.getpid()}."
            f"{threading.get_ident()}."
            f"{uuid.uuid4().hex}.tmp"
        )

        with self._storage_lock(
            exclusive=True,
            create=True,
        ) as directory_fd:
            if directory_fd is None:
                raise BrowserChatSessionCorruptionError(
                    "Chat session storage could not be prepared."
                )

            existing = None

            try:
                existing = os.stat(
                    filename,
                    dir_fd=directory_fd,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                existing = None
            except OSError as exc:
                raise BrowserChatSessionCorruptionError(
                    "Existing session metadata could not be inspected."
                ) from exc

            if (
                expected_absent
                and existing is not None
            ):
                raise BrowserChatSessionConflictError(
                    "Generated session id already exists."
                )

            if existing is not None:
                self._validate_session_metadata(
                    existing,
                    path=path,
                )

            flags = (
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = -1
            temporary_created = False

            try:
                descriptor = os.open(
                    temporary_name,
                    flags,
                    self.SESSION_FILE_MODE,
                    dir_fd=directory_fd,
                )
                temporary_created = True
                metadata = os.fstat(descriptor)
                self._validate_session_metadata(
                    metadata,
                    path=Path(temporary_name),
                )

                with os.fdopen(
                    descriptor,
                    "wb",
                ) as handle:
                    descriptor = -1
                    handle.write(body)
                    handle.flush()
                    os.fsync(
                        handle.fileno()
                    )

                os.replace(
                    temporary_name,
                    filename,
                    src_dir_fd=directory_fd,
                    dst_dir_fd=directory_fd,
                )
                temporary_created = False

                os.chmod(
                    filename,
                    self.SESSION_FILE_MODE,
                    dir_fd=directory_fd,
                    follow_symlinks=False,
                )
                os.fsync(directory_fd)
            except BrowserChatSessionError:
                raise
            except OSError as exc:
                raise BrowserChatSessionCorruptionError(
                    "Session file could not be committed safely: "
                    f"{type(exc).__name__}"
                ) from exc
            finally:
                if descriptor >= 0:
                    os.close(descriptor)

                if temporary_created:
                    try:
                        os.unlink(
                            temporary_name,
                            dir_fd=directory_fd,
                        )
                    except FileNotFoundError:
                        pass
                    except OSError:
                        pass

    def contract_snapshot(self) -> dict[str, Any]:
        """Return metadata-only state without loading session payloads."""

        boundary = self.safety_boundary()

        storage_exists = self.storage_dir.exists()
        storage_is_directory = (
            self.storage_dir.is_dir()
            if storage_exists
            else True
        )
        storage_is_symlink = (
            self.storage_dir.is_symlink()
        )

        degraded = (
            storage_is_symlink
            or not storage_is_directory
        )

        return {
            "name":
                "aura_browser_chat_session_runtime",
            "component_version":
                getattr(
                    self,
                    "component_version",
                    None,
                ),
            "sprint":
                getattr(self, "sprint", 186),
            "schema_version":
                getattr(
                    self,
                    "schema_version",
                    "1.0",
                ),
            "status": (
                "contract_snapshot_ready"
                if not degraded
                else
                "contract_snapshot_degraded"
            ),
            "degraded": degraded,
            "storage_path":
                str(self.storage_dir),
            "storage_exists":
                storage_exists,
            "storage_is_directory":
                storage_is_directory,
            "storage_is_symlink":
                storage_is_symlink,
            "session_count": 0,
            "total_message_count": 0,
            "error_count": 0,
            "errors": [],
            "session_metrics_available": False,
            "session_metrics_inspected": False,
            "session_payloads_read": 0,
            "inspection_read_only": True,
            "metadata_only": True,
            "safety_boundary": boundary,
        }

    def status(self) -> dict[str, Any]:
        """Inspect storage without creating or changing it."""

        sessions: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []

        if self.storage_dir.exists():
            if self.storage_dir.is_symlink():
                errors.append(
                    {
                        "code": "storage_symlink_blocked",
                        "detail": (
                            "Chat session storage directory is "
                            "a symlink."
                        ),
                    }
                )
            elif not self.storage_dir.is_dir():
                errors.append(
                    {
                        "code": "storage_not_directory",
                        "detail": (
                            "Chat session storage path is not "
                            "a directory."
                        ),
                    }
                )
            else:
                for path in sorted(
                    self.storage_dir.glob("chat_*.json")
                ):
                    try:
                        session_id = path.stem
                        payload = self.load_session(session_id)
                        sessions.append(
                            self._metadata(payload)
                        )
                    except BrowserChatSessionError as exc:
                        errors.append(
                            {
                                "code": "session_unreadable",
                                "detail": (
                                    f"{path.name}: "
                                    f"{type(exc).__name__}: {exc}"
                                ),
                            }
                        )

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ok" if not errors else "degraded",
            "degraded": bool(errors),
            "storage_path": str(self.storage_dir),
            "storage_exists": self.storage_dir.exists(),
            "session_count": len(sessions),
            "total_message_count": sum(
                int(item["message_count"])
                for item in sessions
            ),
            "sessions": sessions,
            "error_count": len(errors),
            "errors": errors,
            "max_title_chars": self.MAX_TITLE_CHARS,
            "max_message_chars": self.MAX_MESSAGE_CHARS,
            "max_message_bytes": self.MAX_MESSAGE_BYTES,
            "max_messages_per_session": (
                self.MAX_MESSAGES_PER_SESSION
            ),
            "model_bridge_active": False,
            "placeholder_response_delivery": True,
            "http_routes_active": False,
            "browser_ui_active": False,
            "read_only": False,
            "bounded_session_mutation": True,
            "safety_boundary": self.safety_boundary(),
        }

    def safety_boundary(self) -> dict[str, Any]:
        """Return the explicit Sprint 186 Part A safety boundary."""

        return {
            "browser_chat_session_core": True,
            "session_creation_runtime": True,
            "validated_message_submission": True,
            "deterministic_response_delivery": True,
            "local_history_persistence": True,
            "session_reload_runtime": True,
            "explicit_clear_confirmation": True,
            "optimistic_revision_control": True,
            "idempotent_client_message_submission": True,
            "atomic_session_writes": True,
            "descriptor_safe_session_reads": True,
            "cross_process_directory_locking": True,
            "private_session_directory_on_write": True,
            "private_session_files": True,
            "session_integrity_hash": True,
            "bounded_session_mutation": True,
            "aura_long_term_memory_write": False,
            "model_bridge_runtime": False,
            "model_inference_runtime": False,
            "network_fallback_runtime": False,
            "browser_http_session_routes": False,
            "control_center_chat_ui": False,
            "browser_auto_launch_runtime": False,
            "tool_execution": False,
            "action_dispatch": False,
            "command_execution": False,
            "arbitrary_file_read": False,
            "arbitrary_file_write": False,
            "desktop_control": False,
            "permission_mutation_runtime": False,
            "audit_writer_runtime": False,
            "background_service_runtime": False,
            "systemd_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
            "autonomous_action": False,
            "safe_idle": True,
        }

    def create_session(
        self,
        *,
        title: str | None = None,
    ) -> dict[str, Any]:
        """Create one bounded local chat session."""

        validated_title = self._validate_title(title)

        with self._lock:
            for _ in range(8):
                session_id = self._new_identifier("chat_")
                path = self._session_path(session_id)
                if not path.exists():
                    break
            else:
                raise BrowserChatSessionConflictError(
                    "Could not allocate a unique session id."
                )

            timestamp = self._now()
            payload = {
                "schema_version": self.schema_version,
                "session_id": session_id,
                "title": validated_title,
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
            self._write_session_unlocked(
                payload,
                expected_absent=True,
            )
            stored = self._read_session_unlocked(session_id)

        return {
            "status": "created",
            "session": deepcopy(stored),
            "clear_confirmation": (
                self.clear_confirmation_phrase(session_id)
            ),
            "model_bridge_active": False,
            "tools_invoked": False,
            "actions_invoked": False,
        }

    def load_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Reload one session from local persistent storage."""

        validated = self._validate_session_id(session_id)
        with self._lock:
            payload = self._read_session_unlocked(validated)
        return deepcopy(payload)

    def list_sessions(self) -> list[dict[str, Any]]:
        """List readable local session metadata."""

        status = self.status()
        if status["degraded"]:
            raise BrowserChatSessionCorruptionError(
                "One or more local chat sessions are unreadable."
            )
        return deepcopy(status["sessions"])

    def submit_message(
        self,
        session_id: str,
        *,
        content: str,
        client_message_id: str | None = None,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        """Persist a user message and deliver an honest runtime notice."""

        validated_session_id = self._validate_session_id(
            session_id
        )
        validated_content = self._validate_message_content(
            content
        )
        validated_client_id = (
            self._validate_client_message_id(
                client_message_id
            )
        )
        validated_revision = (
            self._validate_expected_revision(
                expected_revision
            )
        )

        with self._lock:
            payload = self._read_session_unlocked(
                validated_session_id
            )

            if validated_client_id is not None:
                messages = payload["messages"]
                for index, message in enumerate(messages):
                    if (
                        message["role"] == "user"
                        and message["client_message_id"]
                        == validated_client_id
                    ):
                        response = (
                            messages[index + 1]
                            if index + 1 < len(messages)
                            else None
                        )
                        if (
                            response is None
                            or response["role"] != "assistant"
                        ):
                            raise BrowserChatSessionCorruptionError(
                                "Idempotent submission response pair "
                                "is incomplete."
                            )
                        return {
                            "status": "duplicate",
                            "accepted": True,
                            "idempotent_replay": True,
                            "session": self._metadata(payload),
                            "submitted_message": deepcopy(message),
                            "delivered_response": deepcopy(response),
                            "model_bridge_active": False,
                            "tools_invoked": False,
                            "actions_invoked": False,
                        }

            if (
                validated_revision is not None
                and payload["revision"] != validated_revision
            ):
                raise BrowserChatSessionConflictError(
                    "Session revision changed before submission."
                )

            if (
                payload["message_count"] + 2
                > self.MAX_MESSAGES_PER_SESSION
            ):
                raise BrowserChatValidationError(
                    "Session message limit would be exceeded."
                )

            timestamp = self._now()
            user_message = {
                "message_id": self._new_identifier("msg_"),
                "sequence": payload["message_count"] + 1,
                "role": "user",
                "content": validated_content,
                "created_at_utc": timestamp,
                "client_message_id": validated_client_id,
                "response_kind": None,
                "model_invoked": False,
                "tools_invoked": False,
                "actions_invoked": False,
            }
            assistant_message = {
                "message_id": self._new_identifier("msg_"),
                "sequence": payload["message_count"] + 2,
                "role": "assistant",
                "content": (
                    "Your message was saved in this local session. "
                    "The local model bridge is not active yet, so "
                    "a generated model response is unavailable until "
                    "Sprint 187."
                ),
                "created_at_utc": timestamp,
                "client_message_id": None,
                "response_kind": self.RESPONSE_KIND,
                "model_invoked": False,
                "tools_invoked": False,
                "actions_invoked": False,
            }

            payload["messages"].extend(
                [user_message, assistant_message]
            )
            payload["message_count"] = len(
                payload["messages"]
            )
            payload["revision"] += 1
            payload["updated_at_utc"] = timestamp
            payload["last_response_kind"] = self.RESPONSE_KIND

            self._write_session_unlocked(payload)
            stored = self._read_session_unlocked(
                validated_session_id
            )

        return {
            "status": "accepted",
            "accepted": True,
            "idempotent_replay": False,
            "session": self._metadata(stored),
            "submitted_message": deepcopy(
                stored["messages"][-2]
            ),
            "delivered_response": deepcopy(
                stored["messages"][-1]
            ),
            "model_bridge_active": False,
            "tools_invoked": False,
            "actions_invoked": False,
        }

    def submit_local_model_message(
        self,
        session_id: str,
        *,
        content: str,
        client_message_id: str,
        expected_revision: int,
        system_prompt: str,
        response_factory: Callable[
            [list[dict[str, str]]],
            Mapping[str, Any],
        ],
    ) -> dict[str, Any]:
        # Persist one user/model pair with atomic idempotency protection.

        validated_session_id = self._validate_session_id(
            session_id
        )
        validated_content = self._validate_message_content(
            content
        )
        validated_client_id = (
            self._validate_client_message_id(
                client_message_id
            )
        )
        if validated_client_id is None:
            raise BrowserChatValidationError(
                "client_message_id is required for model requests."
            )
        validated_revision = (
            self._validate_expected_revision(
                expected_revision
            )
        )
        if validated_revision is None:
            raise BrowserChatValidationError(
                "expected_revision is required for model requests."
            )
        validated_system_prompt = (
            self._validate_message_content(
                system_prompt
            )
        )
        if not callable(response_factory):
            raise BrowserChatValidationError(
                "response_factory must be callable."
            )

        with self._lock:
            payload = self._read_session_unlocked(
                validated_session_id
            )
            messages = payload["messages"]

            for index, message in enumerate(messages):
                if (
                    message["role"] == "user"
                    and message["client_message_id"]
                    == validated_client_id
                ):
                    response = (
                        messages[index + 1]
                        if index + 1 < len(messages)
                        else None
                    )
                    if (
                        response is None
                        or response["role"] != "assistant"
                    ):
                        raise BrowserChatSessionCorruptionError(
                            "Idempotent model response pair is incomplete."
                        )
                    return {
                        "status": "duplicate",
                        "accepted": True,
                        "idempotent_replay": True,
                        "model_reinvoked": False,
                        "session": self._metadata(payload),
                        "submitted_message": deepcopy(message),
                        "delivered_response": deepcopy(response),
                        "model_bridge_active": bool(
                            response["model_invoked"]
                        ),
                        "model_invoked": bool(
                            response["model_invoked"]
                        ),
                        "tools_invoked": False,
                        "actions_invoked": False,
                        "commands_invoked": False,
                        "aura_memory_written": False,
                        "bridge_response": None,
                    }

            if payload["revision"] != validated_revision:
                raise BrowserChatSessionConflictError(
                    "Session revision changed before model submission."
                )

            if (
                payload["message_count"] + 2
                > self.MAX_MESSAGES_PER_SESSION
            ):
                raise BrowserChatValidationError(
                    "Session message limit would be exceeded."
                )

            model_messages: list[dict[str, str]] = [
                {
                    "role": "system",
                    "content": validated_system_prompt,
                }
            ]
            for message in payload["messages"]:
                if message["role"] == "user":
                    model_messages.append(
                        {
                            "role": "user",
                            "content": message["content"],
                        }
                    )
                elif (
                    message["role"] == "assistant"
                    and message["response_kind"]
                    == self.LOCAL_MODEL_RESPONSE_KIND
                ):
                    model_messages.append(
                        {
                            "role": "assistant",
                            "content": message["content"],
                        }
                    )

            model_messages.append(
                {
                    "role": "user",
                    "content": validated_content,
                }
            )

            bridge_response = response_factory(
                model_messages
            )
            if not isinstance(bridge_response, Mapping):
                raise BrowserChatValidationError(
                    "Local model bridge response must be an object."
                )

            safe_flags = {
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
            for key, expected in safe_flags.items():
                if bridge_response.get(key) is not expected:
                    raise BrowserChatValidationError(
                        "Local model bridge returned an unsafe "
                        f"or missing flag: {key}."
                    )

            response_content = (
                self._validate_message_content(
                    bridge_response.get("content")
                )
            )
            timestamp = self._now()

            user_message = {
                "message_id": self._new_identifier("msg_"),
                "sequence": payload["message_count"] + 1,
                "role": "user",
                "content": validated_content,
                "created_at_utc": timestamp,
                "client_message_id": validated_client_id,
                "response_kind": None,
                "model_invoked": False,
                "tools_invoked": False,
                "actions_invoked": False,
            }
            assistant_message = {
                "message_id": self._new_identifier("msg_"),
                "sequence": payload["message_count"] + 2,
                "role": "assistant",
                "content": response_content,
                "created_at_utc": timestamp,
                "client_message_id": None,
                "response_kind": (
                    self.LOCAL_MODEL_RESPONSE_KIND
                ),
                "model_invoked": True,
                "tools_invoked": False,
                "actions_invoked": False,
            }

            payload["messages"].extend(
                [user_message, assistant_message]
            )
            payload["message_count"] = len(
                payload["messages"]
            )
            payload["revision"] += 1
            payload["updated_at_utc"] = timestamp
            payload["last_response_kind"] = (
                self.LOCAL_MODEL_RESPONSE_KIND
            )

            self._write_session_unlocked(payload)
            stored = self._read_session_unlocked(
                validated_session_id
            )

        bridge_summary = {
            key: bridge_response.get(key)
            for key in (
                "request_id",
                "provider",
                "base_url",
                "configured_model",
                "response_model",
                "elapsed_ms",
                "input_message_count",
                "input_character_count",
            )
        }

        return {
            "status": "accepted",
            "accepted": True,
            "idempotent_replay": False,
            "model_reinvoked": True,
            "session": self._metadata(stored),
            "submitted_message": deepcopy(
                stored["messages"][-2]
            ),
            "delivered_response": deepcopy(
                stored["messages"][-1]
            ),
            "model_bridge_active": True,
            "model_invoked": True,
            "tools_invoked": False,
            "actions_invoked": False,
            "commands_invoked": False,
            "aura_memory_written": False,
            "bridge_response": bridge_summary,
        }

    def clear_session(
        self,
        session_id: str,
        *,
        confirmation: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        """Clear local session history after exact confirmation."""

        validated_session_id = self._validate_session_id(
            session_id
        )
        validated_revision = (
            self._validate_expected_revision(
                expected_revision
            )
        )
        expected_confirmation = (
            self.clear_confirmation_phrase(
                validated_session_id
            )
        )

        if confirmation != expected_confirmation:
            raise BrowserChatClearConfirmationError(
                "Clear confirmation must exactly match: "
                + expected_confirmation
            )

        with self._lock:
            payload = self._read_session_unlocked(
                validated_session_id
            )

            if (
                validated_revision is not None
                and payload["revision"] != validated_revision
            ):
                raise BrowserChatSessionConflictError(
                    "Session revision changed before clear."
                )

            timestamp = self._now()
            removed_count = payload["message_count"]
            payload["messages"] = []
            payload["message_count"] = 0
            payload["clear_count"] += 1
            payload["last_clear_at_utc"] = timestamp
            payload["last_response_kind"] = None
            payload["revision"] += 1
            payload["updated_at_utc"] = timestamp

            self._write_session_unlocked(payload)
            stored = self._read_session_unlocked(
                validated_session_id
            )

        return {
            "status": "cleared",
            "session": deepcopy(stored),
            "removed_message_count": removed_count,
            "confirmation_verified": True,
            "model_bridge_active": False,
            "tools_invoked": False,
            "actions_invoked": False,
        }

    def self_test(self) -> dict[str, Any]:
        """Validate persistence, schema, safety, and failure behavior."""

        assertions: dict[str, bool] = {}
        counter = 0

        def identifier() -> str:
            nonlocal counter
            counter += 1
            return f"{counter:032x}"

        clock_counter = 0

        def clock() -> datetime:
            nonlocal clock_counter
            clock_counter += 1
            return datetime(
                2026,
                7,
                10,
                9,
                0,
                min(clock_counter, 59),
                tzinfo=timezone.utc,
            )

        with tempfile.TemporaryDirectory(
            prefix="aura-s186-chat-core-"
        ) as temporary:
            root = Path(temporary)
            storage = root / "data" / "chat_sessions"
            manager = AuraBrowserChatSessionRuntimeManager(
                project_root=root,
                storage_dir=storage,
                now_factory=clock,
                id_factory=identifier,
            )

            initial = manager.status()
            assertions["initial_status_ok"] = (
                initial["status"] == "ok"
            )
            assertions["initial_not_degraded"] = (
                initial["degraded"] is False
            )
            assertions["initial_storage_absent"] = (
                initial["storage_exists"] is False
            )
            assertions["initial_session_zero"] = (
                initial["session_count"] == 0
            )
            assertions["initial_messages_zero"] = (
                initial["total_message_count"] == 0
            )
            assertions["initial_status_no_write"] = (
                not storage.exists()
            )
            assertions["status_sprint_186"] = (
                initial["sprint"] == 186
            )
            assertions["status_schema_one"] = (
                initial["schema_version"] == "1.0"
            )
            assertions["status_model_false"] = (
                initial["model_bridge_active"] is False
            )
            assertions["status_placeholder_true"] = (
                initial[
                    "placeholder_response_delivery"
                ]
                is True
            )
            assertions["status_http_false"] = (
                initial["http_routes_active"] is False
            )
            assertions["status_ui_false"] = (
                initial["browser_ui_active"] is False
            )
            assertions["status_bounded_mutation_true"] = (
                initial["bounded_session_mutation"]
                is True
            )

            created = manager.create_session(
                title="  Local Test Session  "
            )
            session = created["session"]
            session_id = session["session_id"]
            session_path = manager._session_path(session_id)

            assertions["create_status"] = (
                created["status"] == "created"
            )
            assertions["create_title_normalized"] = (
                session["title"] == "Local Test Session"
            )
            assertions["create_session_id_valid"] = bool(
                manager._SESSION_ID_RE.fullmatch(session_id)
            )
            assertions["create_revision_one"] = (
                session["revision"] == 1
            )
            assertions["create_messages_zero"] = (
                session["message_count"] == 0
                and session["messages"] == []
            )
            assertions["create_clear_zero"] = (
                session["clear_count"] == 0
            )
            assertions["create_hash_valid"] = (
                session["integrity_sha256"]
                == manager._integrity_digest(session)
            )
            assertions["create_file_exists"] = (
                session_path.is_file()
            )
            assertions["create_file_mode_600"] = (
                stat.S_IMODE(
                    session_path.stat().st_mode
                )
                == 0o600
            )
            assertions["create_confirmation_exact"] = (
                created["clear_confirmation"]
                == f"CLEAR {session_id}"
            )
            assertions["create_no_model"] = (
                created["model_bridge_active"] is False
            )
            assertions["create_no_tools"] = (
                created["tools_invoked"] is False
            )
            assertions["create_no_actions"] = (
                created["actions_invoked"] is False
            )

            reloaded = manager.load_session(session_id)
            assertions["reload_equal_create"] = (
                reloaded == session
            )
            assertions["reload_schema"] = (
                reloaded["schema_version"] == "1.0"
            )
            assertions["reload_status_active"] = (
                reloaded["status"] == "active"
            )

            submission = manager.submit_message(
                session_id,
                content="  Hello AURA\nlocal session test.  ",
                client_message_id="client_message_001",
                expected_revision=1,
            )
            submitted = submission["submitted_message"]
            delivered = submission["delivered_response"]

            assertions["submit_status"] = (
                submission["status"] == "accepted"
            )
            assertions["submit_accepted"] = (
                submission["accepted"] is True
            )
            assertions["submit_not_replay"] = (
                submission["idempotent_replay"] is False
            )
            assertions["submit_revision_two"] = (
                submission["session"]["revision"] == 2
            )
            assertions["submit_message_count_two"] = (
                submission["session"]["message_count"] == 2
            )
            assertions["submit_user_role"] = (
                submitted["role"] == "user"
            )
            assertions["submit_user_sequence"] = (
                submitted["sequence"] == 1
            )
            assertions["submit_content_normalized"] = (
                submitted["content"]
                == "Hello AURA\nlocal session test."
            )
            assertions["submit_client_id"] = (
                submitted["client_message_id"]
                == "client_message_001"
            )
            assertions["submit_response_null"] = (
                submitted["response_kind"] is None
            )
            assertions["submit_user_no_model"] = (
                submitted["model_invoked"] is False
            )
            assertions["submit_user_no_tools"] = (
                submitted["tools_invoked"] is False
            )
            assertions["submit_user_no_actions"] = (
                submitted["actions_invoked"] is False
            )
            assertions["deliver_assistant_role"] = (
                delivered["role"] == "assistant"
            )
            assertions["deliver_sequence_two"] = (
                delivered["sequence"] == 2
            )
            assertions["deliver_kind_honest"] = (
                delivered["response_kind"]
                == manager.RESPONSE_KIND
            )
            assertions["deliver_mentions_sprint_187"] = (
                "Sprint 187" in delivered["content"]
            )
            assertions["deliver_model_unavailable"] = (
                "model bridge is not active"
                in delivered["content"]
            )
            assertions["deliver_no_model"] = (
                delivered["model_invoked"] is False
            )
            assertions["deliver_no_tools"] = (
                delivered["tools_invoked"] is False
            )
            assertions["deliver_no_actions"] = (
                delivered["actions_invoked"] is False
            )
            assertions["envelope_model_false"] = (
                submission["model_bridge_active"] is False
            )
            assertions["envelope_tools_false"] = (
                submission["tools_invoked"] is False
            )
            assertions["envelope_actions_false"] = (
                submission["actions_invoked"] is False
            )

            persisted = manager.load_session(session_id)
            assertions["persisted_count_two"] = (
                persisted["message_count"] == 2
            )
            assertions["persisted_messages_two"] = (
                len(persisted["messages"]) == 2
            )
            assertions["persisted_revision_two"] = (
                persisted["revision"] == 2
            )
            assertions["persisted_response_kind"] = (
                persisted["last_response_kind"]
                == manager.RESPONSE_KIND
            )
            assertions["persisted_hash_valid"] = (
                persisted["integrity_sha256"]
                == manager._integrity_digest(persisted)
            )
            assertions["persisted_sequences"] = (
                [
                    item["sequence"]
                    for item in persisted["messages"]
                ]
                == [1, 2]
            )

            before_duplicate = session_path.read_bytes()
            duplicate = manager.submit_message(
                session_id,
                content="Different text is ignored on replay",
                client_message_id="client_message_001",
                expected_revision=1,
            )
            after_duplicate = session_path.read_bytes()

            assertions["duplicate_status"] = (
                duplicate["status"] == "duplicate"
            )
            assertions["duplicate_replay_true"] = (
                duplicate["idempotent_replay"] is True
            )
            assertions["duplicate_revision_unchanged"] = (
                duplicate["session"]["revision"] == 2
            )
            assertions["duplicate_count_unchanged"] = (
                duplicate["session"]["message_count"] == 2
            )
            assertions["duplicate_user_same"] = (
                duplicate["submitted_message"]["message_id"]
                == submitted["message_id"]
            )
            assertions["duplicate_response_same"] = (
                duplicate["delivered_response"]["message_id"]
                == delivered["message_id"]
            )
            assertions["duplicate_file_unchanged"] = (
                before_duplicate == after_duplicate
            )

            conflict_seen = False
            before_conflict = session_path.read_bytes()
            try:
                manager.submit_message(
                    session_id,
                    content="Conflict",
                    expected_revision=1,
                )
            except BrowserChatSessionConflictError:
                conflict_seen = True
            assertions["submit_revision_conflict"] = conflict_seen
            assertions["submit_conflict_no_write"] = (
                session_path.read_bytes() == before_conflict
            )

            validation_cases = {
                "empty_message": {
                    "content": "   ",
                },
                "oversized_message": {
                    "content": "x" * (
                        manager.MAX_MESSAGE_CHARS + 1
                    ),
                },
                "control_message": {
                    "content": "bad\x00message",
                },
                "invalid_client_id": {
                    "content": "valid",
                    "client_message_id": "../unsafe",
                },
                "invalid_revision_bool": {
                    "content": "valid",
                    "expected_revision": True,
                },
            }
            for label, kwargs in validation_cases.items():
                caught = False
                before_invalid = session_path.read_bytes()
                try:
                    manager.submit_message(
                        session_id,
                        **kwargs,
                    )
                except BrowserChatValidationError:
                    caught = True
                assertions[
                    f"validation_{label}_blocked"
                ] = caught
                assertions[
                    f"validation_{label}_no_write"
                ] = (
                    session_path.read_bytes()
                    == before_invalid
                )

            title_cases = {
                "empty_title": " ",
                "long_title": "t" * (
                    manager.MAX_TITLE_CHARS + 1
                ),
                "control_title": "bad\nname",
            }
            for label, title in title_cases.items():
                caught = False
                try:
                    manager.create_session(title=title)
                except BrowserChatValidationError:
                    caught = True
                assertions[
                    f"validation_{label}_blocked"
                ] = caught

            invalid_session_cases = [
                "../escape",
                "chat_nothex",
                "chat_" + "a" * 31,
                "CHAT_" + "a" * 32,
            ]
            for index, invalid_id in enumerate(
                invalid_session_cases,
                start=1,
            ):
                caught = False
                try:
                    manager.load_session(invalid_id)
                except BrowserChatValidationError:
                    caught = True
                assertions[
                    f"invalid_session_id_{index}_blocked"
                ] = caught

            not_found = False
            valid_missing = "chat_" + "f" * 32
            try:
                manager.load_session(valid_missing)
            except BrowserChatSessionNotFoundError:
                not_found = True
            assertions["valid_missing_not_found"] = not_found

            second = manager.create_session()
            second_id = second["session"]["session_id"]
            listed = manager.list_sessions()
            assertions["list_two_sessions"] = (
                len(listed) == 2
            )
            assertions["list_metadata_only"] = all(
                "messages" not in item
                and "integrity_sha256" not in item
                for item in listed
            )
            assertions["list_sorted_ids"] = (
                [item["session_id"] for item in listed]
                == sorted(
                    [session_id, second_id]
                )
            )
            assertions["default_title"] = (
                second["session"]["title"]
                == "New local session"
            )

            wrong_clear = False
            before_wrong_clear = session_path.read_bytes()
            try:
                manager.clear_session(
                    session_id,
                    confirmation="CLEAR wrong",
                    expected_revision=2,
                )
            except BrowserChatClearConfirmationError:
                wrong_clear = True
            assertions["wrong_clear_blocked"] = wrong_clear
            assertions["wrong_clear_no_write"] = (
                session_path.read_bytes()
                == before_wrong_clear
            )

            clear_conflict = False
            try:
                manager.clear_session(
                    session_id,
                    confirmation=f"CLEAR {session_id}",
                    expected_revision=1,
                )
            except BrowserChatSessionConflictError:
                clear_conflict = True
            assertions["clear_revision_conflict"] = clear_conflict
            assertions["clear_conflict_no_write"] = (
                session_path.read_bytes()
                == before_wrong_clear
            )

            cleared = manager.clear_session(
                session_id,
                confirmation=f"CLEAR {session_id}",
                expected_revision=2,
            )
            assertions["clear_status"] = (
                cleared["status"] == "cleared"
            )
            assertions["clear_confirmation_verified"] = (
                cleared["confirmation_verified"] is True
            )
            assertions["clear_removed_two"] = (
                cleared["removed_message_count"] == 2
            )
            assertions["clear_revision_three"] = (
                cleared["session"]["revision"] == 3
            )
            assertions["clear_count_one"] = (
                cleared["session"]["clear_count"] == 1
            )
            assertions["clear_messages_zero"] = (
                cleared["session"]["message_count"] == 0
                and cleared["session"]["messages"] == []
            )
            assertions["clear_last_response_null"] = (
                cleared["session"]["last_response_kind"]
                is None
            )
            assertions["clear_timestamp_present"] = (
                isinstance(
                    cleared["session"]["last_clear_at_utc"],
                    str,
                )
            )
            assertions["clear_hash_valid"] = (
                cleared["session"]["integrity_sha256"]
                == manager._integrity_digest(
                    cleared["session"]
                )
            )
            assertions["clear_no_model"] = (
                cleared["model_bridge_active"] is False
            )
            assertions["clear_no_tools"] = (
                cleared["tools_invoked"] is False
            )
            assertions["clear_no_actions"] = (
                cleared["actions_invoked"] is False
            )

            reload_after_clear = manager.load_session(session_id)
            assertions["reload_after_clear_equal"] = (
                reload_after_clear == cleared["session"]
            )

            status_after = manager.status()
            assertions["status_after_ok"] = (
                status_after["status"] == "ok"
            )
            assertions["status_after_sessions_two"] = (
                status_after["session_count"] == 2
            )
            assertions["status_after_messages_zero"] = (
                status_after["total_message_count"] == 0
            )
            assertions["status_after_storage_true"] = (
                status_after["storage_exists"] is True
            )
            assertions["status_after_errors_zero"] = (
                status_after["error_count"] == 0
            )

            temporary_files = list(
                storage.glob("*.tmp")
            ) + list(storage.glob(".*.tmp"))
            assertions["atomic_temp_files_zero"] = (
                temporary_files == []
            )

            corrupt_path = manager._session_path(second_id)
            corrupt_payload = json.loads(
                corrupt_path.read_text(encoding="utf-8")
            )
            corrupt_payload["title"] = "Tampered title"
            corrupt_path.write_text(
                json.dumps(
                    corrupt_payload,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

            corruption_seen = False
            try:
                manager.load_session(second_id)
            except BrowserChatSessionCorruptionError:
                corruption_seen = True
            assertions["integrity_corruption_detected"] = (
                corruption_seen
            )

            degraded = manager.status()
            assertions["degraded_status_visible"] = (
                degraded["status"] == "degraded"
            )
            assertions["degraded_true"] = (
                degraded["degraded"] is True
            )
            assertions["degraded_error_one"] = (
                degraded["error_count"] == 1
            )
            assertions["degraded_readable_session_one"] = (
                degraded["session_count"] == 1
            )

            list_corruption_seen = False
            try:
                manager.list_sessions()
            except BrowserChatSessionCorruptionError:
                list_corruption_seen = True
            assertions["list_fails_closed_on_corruption"] = (
                list_corruption_seen
            )

            boundary = manager.safety_boundary()
            enabled_keys = (
                "browser_chat_session_core",
                "session_creation_runtime",
                "validated_message_submission",
                "deterministic_response_delivery",
                "local_history_persistence",
                "session_reload_runtime",
                "explicit_clear_confirmation",
                "optimistic_revision_control",
                "idempotent_client_message_submission",
                "atomic_session_writes",
                "session_integrity_hash",
                "bounded_session_mutation",
                "safe_idle",
            )
            for key in enabled_keys:
                assertions[
                    "boundary_enabled_" + key
                ] = boundary[key] is True

            disabled_keys = (
                "aura_long_term_memory_write",
                "model_bridge_runtime",
                "model_inference_runtime",
                "network_fallback_runtime",
                "browser_http_session_routes",
                "control_center_chat_ui",
                "browser_auto_launch_runtime",
                "tool_execution",
                "action_dispatch",
                "command_execution",
                "arbitrary_file_read",
                "arbitrary_file_write",
                "desktop_control",
                "permission_mutation_runtime",
                "audit_writer_runtime",
                "background_service_runtime",
                "systemd_runtime",
                "public_listener_runtime",
                "lan_listener_runtime",
                "autonomous_action",
            )
            for key in disabled_keys:
                assertions[
                    "boundary_disabled_" + key
                ] = boundary[key] is False

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise BrowserChatSessionError(
                "Browser Chat Session Runtime self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "schema_version": self.schema_version,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "session_creation_verified": True,
            "message_submission_verified": True,
            "response_delivery_verified": True,
            "history_persistence_verified": True,
            "session_reload_verified": True,
            "clear_confirmation_verified": True,
            "input_limits_verified": True,
            "optimistic_revision_verified": True,
            "idempotent_submission_verified": True,
            "atomic_write_verified": True,
            "integrity_corruption_verified": True,
            "degraded_state_verified": True,
            "model_bridge_active": False,
            "http_routes_active": False,
            "browser_ui_active": False,
            "tools_invoked": False,
            "actions_invoked": False,
        }
