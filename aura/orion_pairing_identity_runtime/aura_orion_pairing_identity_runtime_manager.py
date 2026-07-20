"""Authenticated ORION pairing and device identity runtime.

Sprint 274 provides a local, explicit pairing workflow. It persists a
device identity and a 256-bit shared secret outside the repository,
issues a fresh single-use challenge, and verifies an HMAC-SHA256 proof
with constant-time comparison.

This runtime does not bind a network listener, open a connection,
exchange heartbeats, negotiate capabilities, preview or approve
actions, activate permissions, write audit records, execute actions,
or activate watchdog/recovery behavior.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import stat
import tempfile
import uuid
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


class OrionPairingIdentityRuntimeError(RuntimeError):
    """Raised when pairing or identity validation fails closed."""


@dataclass(frozen=True, slots=True)
class OrionDeviceIdentity:
    schema_version: int
    device_id: str
    display_name: str
    platform: str
    device_role: str
    identity_version: str
    created_at_utc: str
    credential_id: str
    credential_fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "OrionDeviceIdentity":
        return cls(
            schema_version=int(payload["schema_version"]),
            device_id=str(payload["device_id"]),
            display_name=str(payload["display_name"]),
            platform=str(payload["platform"]),
            device_role=str(payload["device_role"]),
            identity_version=str(payload["identity_version"]),
            created_at_utc=str(payload["created_at_utc"]),
            credential_id=str(payload["credential_id"]),
            credential_fingerprint=str(
                payload["credential_fingerprint"]
            ),
        )


@dataclass(frozen=True, slots=True)
class OrionPairingChallenge:
    challenge_id: str
    challenge_b64url: str
    issued_at_utc: str
    expires_at_utc: str
    used_at_utc: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        payload: dict[str, Any],
    ) -> "OrionPairingChallenge":
        return cls(
            challenge_id=str(payload["challenge_id"]),
            challenge_b64url=str(payload["challenge_b64url"]),
            issued_at_utc=str(payload["issued_at_utc"]),
            expires_at_utc=str(payload["expires_at_utc"]),
            used_at_utc=(
                None
                if payload.get("used_at_utc") is None
                else str(payload["used_at_utc"])
            ),
        )


@dataclass(frozen=True, slots=True)
class OrionPairingRecord:
    schema_version: int
    state: str
    pairing_id: str
    device: OrionDeviceIdentity
    created_at_utc: str
    paired_at_utc: str | None
    revoked_at_utc: str | None
    active_challenge: OrionPairingChallenge | None
    used_challenge_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "state": self.state,
            "pairing_id": self.pairing_id,
            "device": self.device.to_dict(),
            "created_at_utc": self.created_at_utc,
            "paired_at_utc": self.paired_at_utc,
            "revoked_at_utc": self.revoked_at_utc,
            "active_challenge": (
                None
                if self.active_challenge is None
                else self.active_challenge.to_dict()
            ),
            "used_challenge_ids": list(self.used_challenge_ids),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "OrionPairingRecord":
        challenge_payload = payload.get("active_challenge")
        return cls(
            schema_version=int(payload["schema_version"]),
            state=str(payload["state"]),
            pairing_id=str(payload["pairing_id"]),
            device=OrionDeviceIdentity.from_dict(
                dict(payload["device"])
            ),
            created_at_utc=str(payload["created_at_utc"]),
            paired_at_utc=(
                None
                if payload.get("paired_at_utc") is None
                else str(payload["paired_at_utc"])
            ),
            revoked_at_utc=(
                None
                if payload.get("revoked_at_utc") is None
                else str(payload["revoked_at_utc"])
            ),
            active_challenge=(
                None
                if challenge_payload is None
                else OrionPairingChallenge.from_dict(
                    dict(challenge_payload)
                )
            ),
            used_challenge_ids=tuple(
                str(item)
                for item in payload.get("used_challenge_ids", [])
            ),
        )


class AuraOrionPairingIdentityRuntimeManager:
    """Manage local authenticated pairing without network activation."""

    SCHEMA_VERSION = 1
    COMPONENT_VERSION = "0.1.0"
    IDENTITY_VERSION = "orion-device-identity-v1"
    DEVICE_ROLE = "ORION_AGENT"
    PLATFORM = "windows"

    STATE_UNPAIRED = "unpaired"
    STATE_CHALLENGE_ISSUED = "challenge_issued"
    STATE_PAIRED = "paired"
    STATE_REVOKED = "revoked"
    STATES = (
        STATE_UNPAIRED,
        STATE_CHALLENGE_ISSUED,
        STATE_PAIRED,
        STATE_REVOKED,
    )

    SECRET_BYTES = 32
    CHALLENGE_BYTES = 32
    CHALLENGE_TTL_SECONDS = 300
    REPLAY_LEDGER_LIMIT = 256
    MAX_STATE_FILE_BYTES = 131_072

    STATE_FILE_NAME = "pairing_state.json"
    SECRET_FILE_NAME = "pairing_secret.key"
    DIRECTORY_MODE = 0o700
    FILE_MODE = 0o600

    DEFERRED_FALSE_FIELDS = (
        "network_listener_active",
        "network_connection_active",
        "heartbeat_active",
        "capability_negotiation_active",
        "live_grounding_active",
        "action_preview_active",
        "approval_active",
        "permission_active",
        "audit_write_active",
        "real_action_execution_active",
        "watchdog_active",
        "emergency_stop_active",
        "recovery_active",
    )

    VALID_TRANSITIONS = (
        ("unpaired", "begin_pairing", "challenge_issued"),
        ("revoked", "begin_pairing", "challenge_issued"),
        (
            "challenge_issued",
            "complete_with_valid_proof",
            "paired",
        ),
        ("challenge_issued", "cancel", "unpaired"),
        ("challenge_issued", "expire", "unpaired"),
        ("paired", "revoke", "revoked"),
    )

    def __init__(
        self,
        project_root: Path,
        *,
        state_root: Path | None = None,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        configured = (
            Path(state_root).expanduser()
            if state_root is not None
            else self._default_state_root()
        )
        if configured.exists() and configured.is_symlink():
            raise OrionPairingIdentityRuntimeError(
                "Pairing state root must not be a symbolic link."
            )
        self.state_root = configured.resolve(strict=False)
        if (
            self.state_root == self.project_root
            or self.project_root in self.state_root.parents
        ):
            raise OrionPairingIdentityRuntimeError(
                "Pairing state must remain outside the repository."
            )

        self.state_file = self.state_root / self.STATE_FILE_NAME
        self.secret_file = self.state_root / self.SECRET_FILE_NAME
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )

    @staticmethod
    def _default_state_root() -> Path:
        xdg = os.environ.get("XDG_STATE_HOME")
        base = (
            Path(xdg).expanduser()
            if xdg
            else Path.home() / ".local" / "state"
        )
        return base / "aura" / "orion_pairing"

    def _now(self) -> datetime:
        value = self._now_provider()
        if value.tzinfo is None:
            raise OrionPairingIdentityRuntimeError(
                "Pairing clock must be timezone-aware."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        return (
            value.astimezone(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

    @staticmethod
    def _parse_utc(value: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise OrionPairingIdentityRuntimeError(
                f"Invalid UTC timestamp: {value}"
            ) from exc
        if parsed.tzinfo is None:
            raise OrionPairingIdentityRuntimeError(
                f"Timestamp is not timezone-aware: {value}"
            )
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _b64url_encode(value: bytes) -> str:
        return (
            base64.urlsafe_b64encode(value)
            .decode("ascii")
            .rstrip("=")
        )

    @staticmethod
    def _b64url_decode(value: str) -> bytes:
        if not value or re_fullmatch_b64url(value) is False:
            raise OrionPairingIdentityRuntimeError(
                "Value is not valid base64url."
            )
        padding = "=" * (-len(value) % 4)
        try:
            return base64.urlsafe_b64decode(value + padding)
        except (ValueError, TypeError) as exc:
            raise OrionPairingIdentityRuntimeError(
                "Value is not valid base64url."
            ) from exc

    @staticmethod
    def _validate_display_name(value: str) -> str:
        normalized = " ".join(str(value).split())
        if not 1 <= len(normalized) <= 80:
            raise OrionPairingIdentityRuntimeError(
                "Device display name must contain 1-80 characters."
            )
        if any(ord(char) < 32 for char in normalized):
            raise OrionPairingIdentityRuntimeError(
                "Device display name contains control characters."
            )
        return normalized

    @classmethod
    def _validate_platform(cls, value: str) -> str:
        normalized = str(value).strip().lower()
        if normalized != cls.PLATFORM:
            raise OrionPairingIdentityRuntimeError(
                "Sprint 274 ORION pairing requires platform 'windows'."
            )
        return normalized

    @staticmethod
    def _validate_identifier(
        value: str,
        *,
        prefix: str,
        label: str,
    ) -> str:
        normalized = str(value).strip()
        expected_length = len(prefix) + 32
        if (
            len(normalized) != expected_length
            or not normalized.startswith(prefix)
            or any(
                char not in "0123456789abcdef"
                for char in normalized[len(prefix):]
            )
        ):
            raise OrionPairingIdentityRuntimeError(
                f"Invalid {label}."
            )
        return normalized

    def _ensure_root(self) -> None:
        if self.state_root.exists():
            if self.state_root.is_symlink():
                raise OrionPairingIdentityRuntimeError(
                    "Pairing state root must not be a symbolic link."
                )
            if not self.state_root.is_dir():
                raise OrionPairingIdentityRuntimeError(
                    "Pairing state root is not a directory."
                )
            mode = stat.S_IMODE(self.state_root.stat().st_mode)
            if mode != self.DIRECTORY_MODE:
                raise OrionPairingIdentityRuntimeError(
                    "Pairing state root mode must be 0700."
                )
            return

        self.state_root.mkdir(
            parents=True,
            mode=self.DIRECTORY_MODE,
            exist_ok=False,
        )
        os.chmod(self.state_root, self.DIRECTORY_MODE)

    def _validate_root_if_present(self) -> bool:
        if not self.state_root.exists():
            return False
        if self.state_root.is_symlink():
            raise OrionPairingIdentityRuntimeError(
                "Pairing state root must not be a symbolic link."
            )
        if not self.state_root.is_dir():
            raise OrionPairingIdentityRuntimeError(
                "Pairing state root is not a directory."
            )
        mode = stat.S_IMODE(self.state_root.stat().st_mode)
        if mode != self.DIRECTORY_MODE:
            raise OrionPairingIdentityRuntimeError(
                "Pairing state root mode must be 0700."
            )
        return True

    def _validate_secure_file(
        self,
        path: Path,
        *,
        expected_mode: int,
    ) -> None:
        if path.is_symlink():
            raise OrionPairingIdentityRuntimeError(
                f"Pairing file must not be a symbolic link: {path.name}"
            )
        if not path.is_file():
            raise OrionPairingIdentityRuntimeError(
                f"Pairing path is not a regular file: {path.name}"
            )
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode != expected_mode:
            raise OrionPairingIdentityRuntimeError(
                f"Pairing file mode must be {expected_mode:04o}: "
                f"{path.name}"
            )

    def _fsync_root(self) -> None:
        descriptor = os.open(
            self.state_root,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _atomic_write(
        self,
        path: Path,
        payload: bytes,
        *,
        mode: int,
    ) -> None:
        self._ensure_root()
        if path.exists() and path.is_symlink():
            raise OrionPairingIdentityRuntimeError(
                f"Refusing to replace symbolic link: {path.name}"
            )

        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            dir=self.state_root,
        )
        temporary_path = Path(temporary_name)
        try:
            os.fchmod(descriptor, mode)
            with os.fdopen(descriptor, "wb", closefd=True) as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, path)
            os.chmod(path, mode)
            self._fsync_root()
        except Exception:
            try:
                os.close(descriptor)
            except OSError:
                pass
            temporary_path.unlink(missing_ok=True)
            raise

    def _unlink_secure(self, path: Path) -> None:
        if not path.exists():
            return
        if path.is_symlink():
            raise OrionPairingIdentityRuntimeError(
                f"Refusing to unlink symbolic link: {path.name}"
            )
        if not path.is_file():
            raise OrionPairingIdentityRuntimeError(
                f"Refusing to unlink non-file: {path.name}"
            )
        path.unlink()
        if self.state_root.exists():
            self._fsync_root()

    def _write_record(self, record: OrionPairingRecord) -> None:
        self._validate_record(record)
        payload = (
            json.dumps(
                record.to_dict(),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        self._atomic_write(
            self.state_file,
            payload,
            mode=self.FILE_MODE,
        )

    def _write_secret(self, secret: bytes) -> None:
        if len(secret) != self.SECRET_BYTES:
            raise OrionPairingIdentityRuntimeError(
                "Pairing secret must be exactly 32 bytes."
            )
        self._atomic_write(
            self.secret_file,
            secret,
            mode=self.FILE_MODE,
        )

    def _read_secret(self) -> bytes:
        if not self._validate_root_if_present():
            raise OrionPairingIdentityRuntimeError(
                "Pairing state root does not exist."
            )
        if not self.secret_file.exists():
            raise OrionPairingIdentityRuntimeError(
                "Pairing secret is missing."
            )
        self._validate_secure_file(
            self.secret_file,
            expected_mode=self.FILE_MODE,
        )
        secret = self.secret_file.read_bytes()
        if len(secret) != self.SECRET_BYTES:
            raise OrionPairingIdentityRuntimeError(
                "Pairing secret has an invalid length."
            )
        return secret

    def _load_record(self) -> OrionPairingRecord | None:
        root_exists = self._validate_root_if_present()
        if not root_exists:
            return None

        state_exists = self.state_file.exists()
        secret_exists = self.secret_file.exists()

        if not state_exists:
            if secret_exists:
                raise OrionPairingIdentityRuntimeError(
                    "Orphaned pairing secret detected."
                )
            return None

        self._validate_secure_file(
            self.state_file,
            expected_mode=self.FILE_MODE,
        )
        if self.state_file.stat().st_size > self.MAX_STATE_FILE_BYTES:
            raise OrionPairingIdentityRuntimeError(
                "Pairing state file exceeds the size limit."
            )

        try:
            payload = json.loads(
                self.state_file.read_text(encoding="utf-8")
            )
            if not isinstance(payload, dict):
                raise TypeError("Pairing state is not an object.")
            record = OrionPairingRecord.from_dict(payload)
        except (
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            raise OrionPairingIdentityRuntimeError(
                "Pairing state file is invalid."
            ) from exc

        self._validate_record(record)

        if record.state in (
            self.STATE_CHALLENGE_ISSUED,
            self.STATE_PAIRED,
        ):
            if not secret_exists:
                raise OrionPairingIdentityRuntimeError(
                    "Active pairing state has no credential."
                )
            self._validate_secure_file(
                self.secret_file,
                expected_mode=self.FILE_MODE,
            )
        elif secret_exists:
            raise OrionPairingIdentityRuntimeError(
                "Inactive pairing state retains a credential."
            )

        return record

    def _validate_record(self, record: OrionPairingRecord) -> None:
        if record.schema_version != self.SCHEMA_VERSION:
            raise OrionPairingIdentityRuntimeError(
                "Unsupported pairing schema version."
            )
        if record.state not in self.STATES:
            raise OrionPairingIdentityRuntimeError(
                "Pairing state is invalid."
            )

        self._validate_identifier(
            record.pairing_id,
            prefix="pair-",
            label="pairing ID",
        )
        self._validate_identifier(
            record.device.device_id,
            prefix="orion-",
            label="device ID",
        )
        self._validate_identifier(
            record.device.credential_id,
            prefix="cred-",
            label="credential ID",
        )
        self._validate_display_name(record.device.display_name)
        self._validate_platform(record.device.platform)

        if record.device.schema_version != self.SCHEMA_VERSION:
            raise OrionPairingIdentityRuntimeError(
                "Device identity schema version is invalid."
            )
        if record.device.device_role != self.DEVICE_ROLE:
            raise OrionPairingIdentityRuntimeError(
                "Device identity role is invalid."
            )
        if record.device.identity_version != self.IDENTITY_VERSION:
            raise OrionPairingIdentityRuntimeError(
                "Device identity version is invalid."
            )
        if (
            len(record.device.credential_fingerprint) != 32
            or any(
                char not in "0123456789abcdef"
                for char in record.device.credential_fingerprint
            )
        ):
            raise OrionPairingIdentityRuntimeError(
                "Credential fingerprint is invalid."
            )

        self._parse_utc(record.created_at_utc)
        self._parse_utc(record.device.created_at_utc)
        if record.paired_at_utc is not None:
            self._parse_utc(record.paired_at_utc)
        if record.revoked_at_utc is not None:
            self._parse_utc(record.revoked_at_utc)

        if len(record.used_challenge_ids) > self.REPLAY_LEDGER_LIMIT:
            raise OrionPairingIdentityRuntimeError(
                "Replay ledger exceeds its bound."
            )
        if len(set(record.used_challenge_ids)) != len(
            record.used_challenge_ids
        ):
            raise OrionPairingIdentityRuntimeError(
                "Replay ledger contains duplicate challenge IDs."
            )
        for challenge_id in record.used_challenge_ids:
            self._validate_identifier(
                challenge_id,
                prefix="challenge-",
                label="used challenge ID",
            )

        if record.state == self.STATE_CHALLENGE_ISSUED:
            if record.active_challenge is None:
                raise OrionPairingIdentityRuntimeError(
                    "Challenge-issued state has no active challenge."
                )
            self._validate_challenge(record.active_challenge)
            if record.active_challenge.used_at_utc is not None:
                raise OrionPairingIdentityRuntimeError(
                    "Active challenge is already marked used."
                )
        elif record.active_challenge is not None:
            raise OrionPairingIdentityRuntimeError(
                "Inactive state retains an active challenge."
            )

        if record.state == self.STATE_PAIRED:
            if record.paired_at_utc is None:
                raise OrionPairingIdentityRuntimeError(
                    "Paired state has no paired timestamp."
                )
            if record.revoked_at_utc is not None:
                raise OrionPairingIdentityRuntimeError(
                    "Paired state has a revoked timestamp."
                )
        elif record.state == self.STATE_REVOKED:
            if record.revoked_at_utc is None:
                raise OrionPairingIdentityRuntimeError(
                    "Revoked state has no revoked timestamp."
                )

    def _validate_challenge(
        self,
        challenge: OrionPairingChallenge,
    ) -> None:
        self._validate_identifier(
            challenge.challenge_id,
            prefix="challenge-",
            label="challenge ID",
        )
        raw = self._b64url_decode(challenge.challenge_b64url)
        if len(raw) != self.CHALLENGE_BYTES:
            raise OrionPairingIdentityRuntimeError(
                "Challenge has an invalid length."
            )
        issued = self._parse_utc(challenge.issued_at_utc)
        expires = self._parse_utc(challenge.expires_at_utc)
        if expires <= issued:
            raise OrionPairingIdentityRuntimeError(
                "Challenge expiry must follow issue time."
            )
        if challenge.used_at_utc is not None:
            self._parse_utc(challenge.used_at_utc)

    def _canonical_message(
        self,
        record: OrionPairingRecord,
        challenge: OrionPairingChallenge,
    ) -> bytes:
        return "\n".join(
            [
                str(self.SCHEMA_VERSION),
                record.pairing_id,
                record.device.device_id,
                challenge.challenge_id,
                challenge.challenge_b64url,
                challenge.issued_at_utc,
                challenge.expires_at_utc,
            ]
        ).encode("utf-8")

    def _public_record(
        self,
        record: OrionPairingRecord | None,
    ) -> dict[str, Any] | None:
        if record is None:
            return None
        return record.to_dict()

    def status(self) -> dict[str, Any]:
        record = self._load_record()
        state = (
            self.STATE_UNPAIRED
            if record is None
            else record.state
        )
        payload = {
            "status": "ready",
            "reason": "orion_pairing_identity_runtime_ready",
            "state": state,
            "paired": state == self.STATE_PAIRED,
            "authenticated": state == self.STATE_PAIRED,
            "device_identity_bound": state == self.STATE_PAIRED,
            "provisional_device_identity": (
                state == self.STATE_CHALLENGE_ISSUED
            ),
            "credential_present": self.secret_file.exists(),
            "device": (
                None
                if record is None
                else record.device.to_dict()
            ),
            "pairing_id": (
                None
                if record is None
                else record.pairing_id
            ),
            "active_challenge": (
                None
                if record is None
                or record.active_challenge is None
                else {
                    "challenge_id": (
                        record.active_challenge.challenge_id
                    ),
                    "issued_at_utc": (
                        record.active_challenge.issued_at_utc
                    ),
                    "expires_at_utc": (
                        record.active_challenge.expires_at_utc
                    ),
                    "used_at_utc": (
                        record.active_challenge.used_at_utc
                    ),
                }
            ),
            "used_challenge_count": (
                0
                if record is None
                else len(record.used_challenge_ids)
            ),
            "state_root": str(self.state_root),
            "safe_idle": True,
        }
        payload.update(
            {
                field: False
                for field in self.DEFERRED_FALSE_FIELDS
            }
        )
        return payload

    def inspect_runtime(self) -> dict[str, Any]:
        status = self.status()
        return {
            "component": {
                "name": "aura_orion_pairing_identity_runtime",
                "component_version": self.COMPONENT_VERSION,
                "sprint": 274,
                "boundary": (
                    "authenticated_pairing_and_device_identity"
                ),
            },
            "status": status,
            "state_machine": {
                "states": list(self.STATES),
                "valid_transitions": [
                    {
                        "from": source,
                        "event": event,
                        "to": target,
                    }
                    for source, event, target in self.VALID_TRANSITIONS
                ],
                "default_state": self.STATE_UNPAIRED,
            },
            "schema": {
                "identity_fields": list(
                    OrionDeviceIdentity.__dataclass_fields__
                ),
                "pairing_record_fields": list(
                    OrionPairingRecord.__dataclass_fields__
                ),
                "challenge_fields": list(
                    OrionPairingChallenge.__dataclass_fields__
                ),
            },
            "crypto": {
                "secret_bytes": self.SECRET_BYTES,
                "challenge_bytes": self.CHALLENGE_BYTES,
                "challenge_ttl_seconds": (
                    self.CHALLENGE_TTL_SECONDS
                ),
                "proof_algorithm": "HMAC-SHA256",
                "proof_verification": "hmac.compare_digest",
                "challenge_single_use": True,
                "replay_ledger_limit": self.REPLAY_LEDGER_LIMIT,
                "secret_exposed": False,
            },
            "persistence": {
                "state_root": str(self.state_root),
                "inside_repository": False,
                "directory_mode": "0700",
                "state_file": str(self.state_file),
                "state_file_mode": "0600",
                "secret_file": str(self.secret_file),
                "secret_file_mode": "0600",
                "atomic_write": True,
                "secret_exposed": False,
            },
            "deferred_boundaries": {
                "sprint_275": [
                    "heartbeat",
                    "capability_negotiation",
                    "live_grounding",
                ],
                "sprint_276": [
                    "action_preview",
                    "explicit_approval",
                ],
                "sprint_277": [
                    "scoped_permission",
                    "permission_expiry",
                    "audit_write",
                    "reviewed_memory",
                ],
                "sprint_278": [
                    "orion_capture_actions",
                    "orion_app_actions",
                    "orion_file_actions",
                    "orion_obs_actions",
                ],
                "sprint_279": [
                    "watchdog",
                    "emergency_stop_runtime",
                    "recovery_execution",
                    "dialogue_evaluation",
                ],
            },
        }

    def begin_pairing(
        self,
        *,
        display_name: str,
        platform: str,
    ) -> dict[str, Any]:
        current = self._load_record()
        if current is not None and current.state not in (
            self.STATE_UNPAIRED,
            self.STATE_REVOKED,
        ):
            raise OrionPairingIdentityRuntimeError(
                f"Cannot begin pairing from state '{current.state}'."
            )

        display_name = self._validate_display_name(display_name)
        platform = self._validate_platform(platform)

        now = self._now()
        now_text = self._format_utc(now)
        expires_text = self._format_utc(
            now + timedelta(seconds=self.CHALLENGE_TTL_SECONDS)
        )

        secret = secrets.token_bytes(self.SECRET_BYTES)
        challenge_bytes = secrets.token_bytes(
            self.CHALLENGE_BYTES
        )
        pairing_id = "pair-" + uuid.uuid4().hex
        device_id = "orion-" + uuid.uuid4().hex
        credential_id = "cred-" + uuid.uuid4().hex
        challenge_id = "challenge-" + uuid.uuid4().hex

        identity = OrionDeviceIdentity(
            schema_version=self.SCHEMA_VERSION,
            device_id=device_id,
            display_name=display_name,
            platform=platform,
            device_role=self.DEVICE_ROLE,
            identity_version=self.IDENTITY_VERSION,
            created_at_utc=now_text,
            credential_id=credential_id,
            credential_fingerprint=hashlib.sha256(
                secret
            ).hexdigest()[:32],
        )
        challenge = OrionPairingChallenge(
            challenge_id=challenge_id,
            challenge_b64url=self._b64url_encode(
                challenge_bytes
            ),
            issued_at_utc=now_text,
            expires_at_utc=expires_text,
            used_at_utc=None,
        )
        record = OrionPairingRecord(
            schema_version=self.SCHEMA_VERSION,
            state=self.STATE_CHALLENGE_ISSUED,
            pairing_id=pairing_id,
            device=identity,
            created_at_utc=now_text,
            paired_at_utc=None,
            revoked_at_utc=None,
            active_challenge=challenge,
            used_challenge_ids=(),
        )

        self._write_secret(secret)
        self._write_record(record)

        return {
            "status": "OK",
            "state": record.state,
            "enrollment_bundle_once": True,
            "pairing_id": pairing_id,
            "device": identity.to_dict(),
            "credential": {
                "credential_id": credential_id,
                "shared_secret_b64url": self._b64url_encode(
                    secret
                ),
                "secret_bytes": self.SECRET_BYTES,
                "displayed_once": True,
            },
            "challenge": challenge.to_dict(),
            "proof_contract": {
                "algorithm": "HMAC-SHA256",
                "verification": "hmac.compare_digest",
                "canonical_message_fields": [
                    "schema_version",
                    "pairing_id",
                    "device_id",
                    "challenge_id",
                    "challenge_b64url",
                    "issued_at_utc",
                    "expires_at_utc",
                ],
            },
        }

    def complete_pairing(
        self,
        *,
        pairing_id: str,
        device_id: str,
        challenge_id: str,
        proof_b64url: str,
    ) -> dict[str, Any]:
        record = self._load_record()
        if (
            record is None
            or record.state != self.STATE_CHALLENGE_ISSUED
            or record.active_challenge is None
        ):
            raise OrionPairingIdentityRuntimeError(
                "No active pairing challenge exists."
            )

        pairing_id = self._validate_identifier(
            pairing_id,
            prefix="pair-",
            label="pairing ID",
        )
        device_id = self._validate_identifier(
            device_id,
            prefix="orion-",
            label="device ID",
        )
        challenge_id = self._validate_identifier(
            challenge_id,
            prefix="challenge-",
            label="challenge ID",
        )

        challenge = record.active_challenge
        if pairing_id != record.pairing_id:
            raise OrionPairingIdentityRuntimeError(
                "Pairing ID does not match the active challenge."
            )
        if device_id != record.device.device_id:
            raise OrionPairingIdentityRuntimeError(
                "Device ID does not match the active challenge."
            )
        if challenge_id != challenge.challenge_id:
            raise OrionPairingIdentityRuntimeError(
                "Challenge ID does not match the active challenge."
            )
        if challenge_id in record.used_challenge_ids:
            raise OrionPairingIdentityRuntimeError(
                "Challenge replay was rejected."
            )

        if self._now() >= self._parse_utc(
            challenge.expires_at_utc
        ):
            self._unlink_secure(self.secret_file)
            self._unlink_secure(self.state_file)
            raise OrionPairingIdentityRuntimeError(
                "Pairing challenge expired and was cleared."
            )

        proof = self._b64url_decode(proof_b64url)
        if len(proof) != hashlib.sha256().digest_size:
            raise OrionPairingIdentityRuntimeError(
                "Pairing proof has an invalid length."
            )

        secret = self._read_secret()
        expected = hmac.new(
            secret,
            self._canonical_message(record, challenge),
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(proof, expected):
            raise OrionPairingIdentityRuntimeError(
                "Pairing proof verification failed."
            )

        now_text = self._format_utc(self._now())
        used_ids = (
            *record.used_challenge_ids,
            challenge.challenge_id,
        )[-self.REPLAY_LEDGER_LIMIT :]
        paired_record = replace(
            record,
            state=self.STATE_PAIRED,
            paired_at_utc=now_text,
            revoked_at_utc=None,
            active_challenge=None,
            used_challenge_ids=tuple(used_ids),
        )
        self._write_record(paired_record)
        return self.status()

    def cancel_pairing(self) -> dict[str, Any]:
        record = self._load_record()
        if (
            record is None
            or record.state != self.STATE_CHALLENGE_ISSUED
        ):
            raise OrionPairingIdentityRuntimeError(
                "Pairing can only be cancelled while a challenge is active."
            )
        self._unlink_secure(self.secret_file)
        self._unlink_secure(self.state_file)
        return self.status()

    def revoke_pairing(
        self,
        *,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != "REVOKE":
            raise OrionPairingIdentityRuntimeError(
                "Revocation requires exact confirmation 'REVOKE'."
            )
        record = self._load_record()
        if record is None or record.state != self.STATE_PAIRED:
            raise OrionPairingIdentityRuntimeError(
                "Only a paired device can be revoked."
            )

        now_text = self._format_utc(self._now())
        self._unlink_secure(self.secret_file)
        revoked_record = replace(
            record,
            state=self.STATE_REVOKED,
            revoked_at_utc=now_text,
            active_challenge=None,
        )
        self._write_record(revoked_record)
        return self.status()

    def reset_pairing(
        self,
        *,
        confirmation: str,
    ) -> dict[str, Any]:
        if confirmation != "RESET":
            raise OrionPairingIdentityRuntimeError(
                "Reset requires exact confirmation 'RESET'."
            )
        record = self._load_record()
        if record is not None and record.state not in (
            self.STATE_UNPAIRED,
            self.STATE_REVOKED,
        ):
            raise OrionPairingIdentityRuntimeError(
                "Reset is allowed only from unpaired or revoked state."
            )
        self._unlink_secure(self.secret_file)
        self._unlink_secure(self.state_file)
        return self.status()

    def self_test(self) -> dict[str, Any]:
        assertions: list[tuple[str, bool]] = []

        def check(name: str, condition: bool) -> None:
            assertions.append((name, bool(condition)))

        def expect_error(
            name: str,
            operation: Callable[[], Any],
            contains: str | None = None,
        ) -> None:
            try:
                operation()
            except OrionPairingIdentityRuntimeError as exc:
                check(name, contains is None or contains in str(exc))
            else:
                check(name, False)

        with tempfile.TemporaryDirectory(
            prefix="aura-orion-pairing-self-test-"
        ) as temporary:
            temporary_path = Path(temporary)
            state_root = temporary_path / "state"
            manager = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=state_root,
            )

            initial = manager.status()
            check("initial_state_unpaired", initial["state"] == "unpaired")
            check("initial_paired_false", initial["paired"] is False)
            check(
                "initial_authenticated_false",
                initial["authenticated"] is False,
            )
            check(
                "initial_identity_bound_false",
                initial["device_identity_bound"] is False,
            )
            check(
                "initial_credential_absent",
                initial["credential_present"] is False,
            )
            check("initial_safe_idle", initial["safe_idle"] is True)
            for field in self.DEFERRED_FALSE_FIELDS:
                check(
                    f"initial_deferred_false_{field}",
                    initial[field] is False,
                )

            inspect_initial = manager.inspect_runtime()
            check(
                "inspect_component_version",
                inspect_initial["component"]["component_version"]
                == self.COMPONENT_VERSION,
            )
            check(
                "inspect_sprint",
                inspect_initial["component"]["sprint"] == 274,
            )
            check(
                "inspect_boundary",
                inspect_initial["component"]["boundary"]
                == "authenticated_pairing_and_device_identity",
            )
            check(
                "inspect_secret_not_exposed",
                inspect_initial["crypto"]["secret_exposed"] is False,
            )
            check(
                "inspect_storage_outside_repo",
                inspect_initial["persistence"]["inside_repository"]
                is False,
            )
            check(
                "inspect_transition_count",
                len(
                    inspect_initial["state_machine"][
                        "valid_transitions"
                    ]
                )
                == 6,
            )
            check(
                "inspect_states",
                inspect_initial["state_machine"]["states"]
                == list(self.STATES),
            )
            for field in OrionDeviceIdentity.__dataclass_fields__:
                check(
                    f"identity_schema_field_{field}",
                    field
                    in inspect_initial["schema"]["identity_fields"],
                )
            for field in OrionPairingRecord.__dataclass_fields__:
                check(
                    f"record_schema_field_{field}",
                    field
                    in inspect_initial["schema"][
                        "pairing_record_fields"
                    ],
                )
            for field in OrionPairingChallenge.__dataclass_fields__:
                check(
                    f"challenge_schema_field_{field}",
                    field
                    in inspect_initial["schema"][
                        "challenge_fields"
                    ],
                )

            expect_error(
                "repository_state_root_rejected",
                lambda: AuraOrionPairingIdentityRuntimeManager(
                    self.project_root,
                    state_root=self.project_root / ".pairing-state",
                ),
                "outside the repository",
            )
            expect_error(
                "empty_display_name_rejected",
                lambda: manager.begin_pairing(
                    display_name="",
                    platform="windows",
                ),
            )
            expect_error(
                "wrong_platform_rejected",
                lambda: manager.begin_pairing(
                    display_name="ORION",
                    platform="linux",
                ),
            )

            enrollment = manager.begin_pairing(
                display_name="ORION Test",
                platform="windows",
            )
            check(
                "begin_status_ok",
                enrollment["status"] == "OK",
            )
            check(
                "begin_state_challenge",
                enrollment["state"] == "challenge_issued",
            )
            check(
                "begin_bundle_once",
                enrollment["enrollment_bundle_once"] is True,
            )
            secret_b64url = enrollment["credential"][
                "shared_secret_b64url"
            ]
            secret = self._b64url_decode(secret_b64url)
            check("begin_secret_length", len(secret) == 32)
            check(
                "begin_secret_displayed_once",
                enrollment["credential"]["displayed_once"] is True,
            )
            check(
                "begin_device_prefix",
                enrollment["device"]["device_id"].startswith("orion-"),
            )
            check(
                "begin_pairing_prefix",
                enrollment["pairing_id"].startswith("pair-"),
            )
            check(
                "begin_credential_prefix",
                enrollment["credential"]["credential_id"].startswith(
                    "cred-"
                ),
            )
            check(
                "begin_challenge_prefix",
                enrollment["challenge"]["challenge_id"].startswith(
                    "challenge-"
                ),
            )
            check(
                "state_root_created",
                state_root.is_dir(),
            )
            check(
                "state_root_mode_0700",
                stat.S_IMODE(state_root.stat().st_mode) == 0o700,
            )
            check(
                "state_file_mode_0600",
                stat.S_IMODE(manager.state_file.stat().st_mode)
                == 0o600,
            )
            check(
                "secret_file_mode_0600",
                stat.S_IMODE(manager.secret_file.stat().st_mode)
                == 0o600,
            )

            challenge_status = manager.status()
            check(
                "challenge_status",
                challenge_status["state"] == "challenge_issued",
            )
            check(
                "challenge_provisional_identity",
                challenge_status["provisional_device_identity"]
                is True,
            )
            check(
                "challenge_not_authenticated",
                challenge_status["authenticated"] is False,
            )
            check(
                "challenge_credential_present",
                challenge_status["credential_present"] is True,
            )
            serialized_status = json.dumps(
                challenge_status,
                sort_keys=True,
            )
            serialized_inspect = json.dumps(
                manager.inspect_runtime(),
                sort_keys=True,
            )
            check(
                "status_redacts_secret_value",
                secret_b64url not in serialized_status,
            )
            check(
                "inspect_redacts_secret_value",
                secret_b64url not in serialized_inspect,
            )

            expect_error(
                "begin_while_challenge_rejected",
                lambda: manager.begin_pairing(
                    display_name="ORION Duplicate",
                    platform="windows",
                ),
                "Cannot begin pairing",
            )

            record = manager._load_record()
            check("record_loaded", record is not None)
            assert record is not None
            challenge = record.active_challenge
            check("active_challenge_loaded", challenge is not None)
            assert challenge is not None

            message = manager._canonical_message(record, challenge)
            proof = hmac.new(
                secret,
                message,
                hashlib.sha256,
            ).digest()
            proof_b64url = manager._b64url_encode(proof)
            wrong_proof = manager._b64url_encode(
                hmac.new(
                    secrets.token_bytes(32),
                    message,
                    hashlib.sha256,
                ).digest()
            )

            expect_error(
                "wrong_pairing_id_rejected",
                lambda: manager.complete_pairing(
                    pairing_id="pair-" + "0" * 32,
                    device_id=record.device.device_id,
                    challenge_id=challenge.challenge_id,
                    proof_b64url=proof_b64url,
                ),
                "Pairing ID",
            )
            expect_error(
                "wrong_device_id_rejected",
                lambda: manager.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id="orion-" + "0" * 32,
                    challenge_id=challenge.challenge_id,
                    proof_b64url=proof_b64url,
                ),
                "Device ID",
            )
            expect_error(
                "wrong_challenge_id_rejected",
                lambda: manager.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id=record.device.device_id,
                    challenge_id="challenge-" + "0" * 32,
                    proof_b64url=proof_b64url,
                ),
                "Challenge ID",
            )
            expect_error(
                "wrong_secret_proof_rejected",
                lambda: manager.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id=record.device.device_id,
                    challenge_id=challenge.challenge_id,
                    proof_b64url=wrong_proof,
                ),
                "proof verification failed",
            )
            expect_error(
                "invalid_proof_encoding_rejected",
                lambda: manager.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id=record.device.device_id,
                    challenge_id=challenge.challenge_id,
                    proof_b64url="***",
                ),
                "base64url",
            )

            paired = manager.complete_pairing(
                pairing_id=record.pairing_id,
                device_id=record.device.device_id,
                challenge_id=challenge.challenge_id,
                proof_b64url=proof_b64url,
            )
            check("paired_state", paired["state"] == "paired")
            check("paired_true", paired["paired"] is True)
            check(
                "paired_authenticated_true",
                paired["authenticated"] is True,
            )
            check(
                "paired_identity_bound_true",
                paired["device_identity_bound"] is True,
            )
            check(
                "paired_no_active_challenge",
                paired["active_challenge"] is None,
            )
            check(
                "paired_used_challenge_count",
                paired["used_challenge_count"] == 1,
            )
            check(
                "paired_secret_still_present",
                manager.secret_file.is_file(),
            )

            restarted = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=state_root,
            )
            restarted_status = restarted.status()
            check(
                "restart_state_paired",
                restarted_status["state"] == "paired",
            )
            check(
                "restart_identity_stable",
                restarted_status["device"]["device_id"]
                == record.device.device_id,
            )
            check(
                "restart_pairing_id_stable",
                restarted_status["pairing_id"]
                == record.pairing_id,
            )

            expect_error(
                "replay_complete_rejected",
                lambda: restarted.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id=record.device.device_id,
                    challenge_id=challenge.challenge_id,
                    proof_b64url=proof_b64url,
                ),
                "No active pairing challenge",
            )
            expect_error(
                "begin_while_paired_rejected",
                lambda: restarted.begin_pairing(
                    display_name="ORION Again",
                    platform="windows",
                ),
                "Cannot begin pairing",
            )
            expect_error(
                "reset_while_paired_rejected",
                lambda: restarted.reset_pairing(
                    confirmation="RESET"
                ),
                "only from unpaired or revoked",
            )
            expect_error(
                "revoke_wrong_confirmation_rejected",
                lambda: restarted.revoke_pairing(
                    confirmation="yes"
                ),
                "REVOKE",
            )

            revoked = restarted.revoke_pairing(
                confirmation="REVOKE"
            )
            check("revoked_state", revoked["state"] == "revoked")
            check(
                "revoked_authenticated_false",
                revoked["authenticated"] is False,
            )
            check(
                "revoked_identity_bound_false",
                revoked["device_identity_bound"] is False,
            )
            check(
                "revoked_secret_removed",
                not restarted.secret_file.exists(),
            )
            check(
                "revoked_state_retained",
                restarted.state_file.is_file(),
            )

            restarted_revoked = (
                AuraOrionPairingIdentityRuntimeManager(
                    self.project_root,
                    state_root=state_root,
                )
            )
            check(
                "restart_revoked_state",
                restarted_revoked.status()["state"] == "revoked",
            )
            expect_error(
                "complete_after_revoke_rejected",
                lambda: restarted_revoked.complete_pairing(
                    pairing_id=record.pairing_id,
                    device_id=record.device.device_id,
                    challenge_id=challenge.challenge_id,
                    proof_b64url=proof_b64url,
                ),
                "No active pairing challenge",
            )

            reenrollment = restarted_revoked.begin_pairing(
                display_name="ORION Reenrolled",
                platform="windows",
            )
            check(
                "begin_from_revoked_allowed",
                reenrollment["state"] == "challenge_issued",
            )
            check(
                "reenrollment_device_id_rotated",
                reenrollment["device"]["device_id"]
                != record.device.device_id,
            )
            check(
                "reenrollment_pairing_id_rotated",
                reenrollment["pairing_id"] != record.pairing_id,
            )
            check(
                "reenrollment_credential_rotated",
                reenrollment["credential"]["credential_id"]
                != record.device.credential_id,
            )

            cancelled = restarted_revoked.cancel_pairing()
            check("cancel_returns_unpaired", cancelled["state"] == "unpaired")
            check(
                "cancel_removes_state",
                not restarted_revoked.state_file.exists(),
            )
            check(
                "cancel_removes_secret",
                not restarted_revoked.secret_file.exists(),
            )

            expect_error(
                "cancel_without_challenge_rejected",
                lambda: restarted_revoked.cancel_pairing(),
                "only be cancelled",
            )
            check(
                "restart_after_cancel_unpaired",
                AuraOrionPairingIdentityRuntimeManager(
                    self.project_root,
                    state_root=state_root,
                ).status()["state"]
                == "unpaired",
            )

            expiry_start = datetime(
                2026,
                7,
                20,
                0,
                0,
                0,
                tzinfo=timezone.utc,
            )
            expiry_clock = {"now": expiry_start}
            expiry_manager = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=state_root,
                now_provider=lambda: expiry_clock["now"],
            )
            expiry_enrollment = expiry_manager.begin_pairing(
                display_name="ORION Expiry",
                platform="windows",
            )
            expiry_record = expiry_manager._load_record()
            assert (
                expiry_record is not None
                and expiry_record.active_challenge is not None
            )
            expiry_challenge = expiry_record.active_challenge
            expiry_secret = expiry_manager._read_secret()
            expiry_proof = expiry_manager._b64url_encode(
                hmac.new(
                    expiry_secret,
                    expiry_manager._canonical_message(
                        expiry_record,
                        expiry_challenge,
                    ),
                    hashlib.sha256,
                ).digest()
            )
            expiry_clock["now"] = expiry_start + timedelta(
                seconds=self.CHALLENGE_TTL_SECONDS + 1
            )
            expect_error(
                "expired_challenge_rejected",
                lambda: expiry_manager.complete_pairing(
                    pairing_id=expiry_enrollment["pairing_id"],
                    device_id=expiry_enrollment["device"]["device_id"],
                    challenge_id=expiry_challenge.challenge_id,
                    proof_b64url=expiry_proof,
                ),
                "expired",
            )
            check(
                "expiry_clears_state",
                not expiry_manager.state_file.exists(),
            )
            check(
                "expiry_clears_secret",
                not expiry_manager.secret_file.exists(),
            )

            reset_manager = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=state_root,
            )
            reset_status = reset_manager.reset_pairing(
                confirmation="RESET"
            )
            check(
                "reset_unpaired_idempotent",
                reset_status["state"] == "unpaired",
            )
            expect_error(
                "reset_wrong_confirmation_rejected",
                lambda: reset_manager.reset_pairing(
                    confirmation="yes"
                ),
                "RESET",
            )

            orphan_root = temporary_path / "orphan"
            orphan_manager = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=orphan_root,
            )
            orphan_manager._write_secret(secrets.token_bytes(32))
            expect_error(
                "orphan_secret_fail_closed",
                lambda: orphan_manager.status(),
                "Orphaned pairing secret",
            )

            corrupt_root = temporary_path / "corrupt"
            corrupt_manager = AuraOrionPairingIdentityRuntimeManager(
                self.project_root,
                state_root=corrupt_root,
            )
            corrupt_manager._ensure_root()
            corrupt_manager._atomic_write(
                corrupt_manager.state_file,
                b"{not-json",
                mode=0o600,
            )
            expect_error(
                "corrupt_state_fail_closed",
                lambda: corrupt_manager.status(),
                "state file is invalid",
            )

            permission_root = temporary_path / "permissions"
            permission_manager = (
                AuraOrionPairingIdentityRuntimeManager(
                    self.project_root,
                    state_root=permission_root,
                )
            )
            permission_enrollment = permission_manager.begin_pairing(
                display_name="ORION Permissions",
                platform="windows",
            )
            check(
                "permission_enrollment_created",
                permission_enrollment["state"]
                == "challenge_issued",
            )
            os.chmod(permission_manager.state_file, 0o644)
            expect_error(
                "insecure_state_mode_rejected",
                lambda: permission_manager.status(),
                "mode must be 0600",
            )

            root_mode_root = temporary_path / "root-mode"
            root_mode_manager = (
                AuraOrionPairingIdentityRuntimeManager(
                    self.project_root,
                    state_root=root_mode_root,
                )
            )
            root_mode_manager._ensure_root()
            os.chmod(root_mode_root, 0o755)
            expect_error(
                "insecure_root_mode_rejected",
                lambda: root_mode_manager.status(),
                "mode must be 0700",
            )

        failed = [
            name for name, passed in assertions if not passed
        ]
        payload = {
            "status": "OK" if not failed else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "component": {
                "name": "aura_orion_pairing_identity_runtime",
                "component_version": self.COMPONENT_VERSION,
                "sprint": 274,
                "boundary": (
                    "authenticated_pairing_and_device_identity"
                ),
            },
            "contract": {
                "states": list(self.STATES),
                "valid_transitions": len(self.VALID_TRANSITIONS),
                "secret_bytes": self.SECRET_BYTES,
                "challenge_bytes": self.CHALLENGE_BYTES,
                "challenge_ttl_seconds": (
                    self.CHALLENGE_TTL_SECONDS
                ),
                "proof_algorithm": "HMAC-SHA256",
                "proof_verification": "hmac.compare_digest",
                "replay_ledger_limit": self.REPLAY_LEDGER_LIMIT,
                "directory_mode": "0700",
                "file_mode": "0600",
                "network_listener_active": False,
                "network_connection_active": False,
                "real_action_execution_active": False,
            },
        }
        if failed:
            raise OrionPairingIdentityRuntimeError(
                "ORION pairing identity self-test failed: "
                + ", ".join(failed)
            )
        return payload


def re_fullmatch_b64url(value: str) -> bool:
    return all(
        char.isalnum() or char in "-_"
        for char in value
    )
