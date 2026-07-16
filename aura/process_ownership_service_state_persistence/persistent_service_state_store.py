from __future__ import annotations

from pathlib import Path
from typing import Any
import errno
import json
import os
import stat
import time


class PersistentServiceStateError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = str(code)
        self.details = dict(details or {})


class PersistentServiceStateStore:
    SCHEMA_VERSION = 2
    FILE_MODE = 0o600
    DIRECTORY_MODE = 0o700

    def __init__(
        self,
        project_root: str | Path,
        *,
        state_path: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
        ).resolve()
        self.state_path = Path(
            state_path
            if state_path is not None
            else (
                self.project_root
                / "data"
                / "runtime"
                / "service_state.json"
            )
        )

    @staticmethod
    def boot_id() -> str | None:
        path = Path(
            "/proc/sys/kernel/random/boot_id"
        )

        try:
            value = path.read_text(
                encoding="utf-8"
            ).strip()
        except (
            FileNotFoundError,
            PermissionError,
            OSError,
        ):
            return None

        return value or None

    @staticmethod
    def _private(
        metadata: os.stat_result,
    ) -> bool:
        return (
            stat.S_IMODE(metadata.st_mode)
            & 0o077
        ) == 0

    @staticmethod
    def _close(
        descriptor: int,
    ) -> None:
        try:
            os.close(descriptor)
        except OSError:
            pass

    @staticmethod
    def _fsync_directory(
        path: Path,
    ) -> None:
        descriptor = os.open(
            path,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )

        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _prepare_parent(self) -> None:
        parent = self.state_path.parent
        parent.mkdir(
            parents=True,
            exist_ok=True,
            mode=self.DIRECTORY_MODE,
        )
        os.chmod(
            parent,
            self.DIRECTORY_MODE,
        )
        metadata = parent.stat()

        if not stat.S_ISDIR(
            metadata.st_mode
        ):
            raise PersistentServiceStateError(
                "state_directory_type_rejected",
                "Persistent state parent is not a directory.",
                details={"path": str(parent)},
            )

        if metadata.st_uid != os.getuid():
            raise PersistentServiceStateError(
                "state_directory_owner_rejected",
                "Persistent state parent has the wrong owner.",
                details={
                    "path": str(parent),
                    "uid": metadata.st_uid,
                },
            )

        if not self._private(metadata):
            raise PersistentServiceStateError(
                "state_directory_mode_rejected",
                "Persistent state parent permissions are too broad.",
                details={
                    "path": str(parent),
                    "mode": oct(
                        stat.S_IMODE(
                            metadata.st_mode
                        )
                    ),
                },
            )

    def _open_read(
        self,
    ) -> tuple[int, os.stat_result]:
        flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )

        try:
            descriptor = os.open(
                self.state_path,
                flags,
            )
        except FileNotFoundError:
            raise
        except OSError as exc:
            code = (
                "state_symlink_rejected"
                if exc.errno == errno.ELOOP
                else "state_read_failed"
            )
            raise PersistentServiceStateError(
                code,
                "Persistent state could not be opened safely.",
                details={
                    "path": str(
                        self.state_path
                    ),
                    "reason": str(exc),
                },
            ) from exc

        metadata = os.fstat(descriptor)

        if not stat.S_ISREG(
            metadata.st_mode
        ):
            self._close(descriptor)
            raise PersistentServiceStateError(
                "state_type_rejected",
                "Persistent state is not a regular file.",
                details={
                    "path": str(
                        self.state_path
                    ),
                },
            )

        if metadata.st_uid != os.getuid():
            self._close(descriptor)
            raise PersistentServiceStateError(
                "state_owner_rejected",
                "Persistent state has the wrong owner.",
                details={
                    "path": str(
                        self.state_path
                    ),
                    "uid": metadata.st_uid,
                },
            )

        if not self._private(metadata):
            self._close(descriptor)
            raise PersistentServiceStateError(
                "state_mode_rejected",
                "Persistent state permissions are too broad.",
                details={
                    "path": str(
                        self.state_path
                    ),
                    "mode": oct(
                        stat.S_IMODE(
                            metadata.st_mode
                        )
                    ),
                },
            )

        return descriptor, metadata

    def read(self) -> dict[str, Any] | None:
        try:
            descriptor, before = (
                self._open_read()
            )
        except FileNotFoundError:
            return None

        with os.fdopen(
            descriptor,
            "rb",
        ) as handle:
            raw = handle.read()
            after = os.fstat(
                handle.fileno()
            )

        if (
            before.st_dev != after.st_dev
            or before.st_ino != after.st_ino
        ):
            raise PersistentServiceStateError(
                "state_identity_changed",
                "Persistent state changed during read.",
                details={
                    "path": str(
                        self.state_path
                    ),
                },
            )

        try:
            packet = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise PersistentServiceStateError(
                "state_invalid_json",
                "Persistent state is not valid JSON.",
                details={
                    "path": str(
                        self.state_path
                    ),
                },
            ) from exc

        if not isinstance(packet, dict):
            raise PersistentServiceStateError(
                "state_invalid_type",
                "Persistent state is not an object.",
                details={
                    "path": str(
                        self.state_path
                    ),
                },
            )

        return packet

    def write(
        self,
        packet: dict[str, Any],
    ) -> None:
        self._prepare_parent()
        temporary = self.state_path.with_name(
            "."
            + self.state_path.name
            + f".tmp-{os.getpid()}-{time.monotonic_ns()}"
        )
        raw = (
            json.dumps(
                packet,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = -1

        try:
            descriptor = os.open(
                temporary,
                flags,
                self.FILE_MODE,
            )
            metadata = os.fstat(
                descriptor
            )

            if not stat.S_ISREG(
                metadata.st_mode
            ):
                raise PersistentServiceStateError(
                    "state_temp_type_rejected",
                    "Persistent state temporary file is not regular.",
                )

            if metadata.st_uid != os.getuid():
                raise PersistentServiceStateError(
                    "state_temp_owner_rejected",
                    "Persistent state temporary file has the wrong owner.",
                )

            if not self._private(metadata):
                raise PersistentServiceStateError(
                    "state_temp_mode_rejected",
                    "Persistent state temporary file permissions are too broad.",
                )

            with os.fdopen(
                descriptor,
                "wb",
            ) as handle:
                descriptor = -1
                handle.write(raw)
                handle.flush()
                os.fsync(
                    handle.fileno()
                )

            os.replace(
                temporary,
                self.state_path,
            )
            os.chmod(
                self.state_path,
                self.FILE_MODE,
            )
            self._fsync_directory(
                self.state_path.parent
            )
        except PersistentServiceStateError:
            raise
        except OSError as exc:
            raise PersistentServiceStateError(
                "state_write_failed",
                "Persistent state could not be committed.",
                details={
                    "path": str(
                        self.state_path
                    ),
                    "reason": str(exc),
                },
            ) from exc
        finally:
            if descriptor >= 0:
                self._close(descriptor)

            try:
                temporary.unlink(
                    missing_ok=True
                )
            except OSError:
                pass

    def remove(self) -> None:
        try:
            metadata = self.state_path.lstat()
        except FileNotFoundError:
            return

        if stat.S_ISLNK(
            metadata.st_mode
        ):
            raise PersistentServiceStateError(
                "state_symlink_rejected",
                "Persistent state symlink removal was rejected.",
            )

        if not stat.S_ISREG(
            metadata.st_mode
        ):
            raise PersistentServiceStateError(
                "state_type_rejected",
                "Persistent state is not a regular file.",
            )

        if metadata.st_uid != os.getuid():
            raise PersistentServiceStateError(
                "state_owner_rejected",
                "Persistent state has the wrong owner.",
            )

        try:
            self.state_path.unlink()
            self._fsync_directory(
                self.state_path.parent
            )
        except OSError as exc:
            raise PersistentServiceStateError(
                "state_remove_failed",
                "Persistent state could not be removed.",
                details={
                    "path": str(
                        self.state_path
                    ),
                    "reason": str(exc),
                },
            ) from exc

    def classify(
        self,
        record: dict[str, Any] | None,
        *,
        matches_process: bool,
    ) -> str:
        if record is None:
            return "absent"

        if matches_process:
            return "current_owned_process"

        record_uid = record.get(
            "host_uid",
            record.get("owner_uid"),
        )

        if record_uid != os.getuid():
            return "foreign_user_record"

        if record.get("boot_id") != self.boot_id():
            return "previous_boot_record"

        return "stale_or_changed_process_record"
