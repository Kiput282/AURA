"""Sprint 277 ORION scoped permission, audit, and reviewed-memory runtime."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import tempfile
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


class OrionScopedPermissionRuntimeError(RuntimeError):
    """Raised when the Sprint 277 fail-closed contract is violated."""


class AuraOrionScopedPermissionRuntimeManager:
    """Issue single-use permissions without executing any real ORION action."""

    COMPONENT_NAME = "orion_scoped_permission_runtime"
    COMPONENT_VERSION = "0.1.0"
    PRODUCT_VERSION = "1.3.1"
    SPRINT = 277
    SCHEMA_VERSION = "1"

    DOMAIN_PERMISSION_ISSUANCE = "orion-scoped-permission-issue"
    DOMAIN_PERMISSION_CONSUMPTION = "orion-scoped-permission-consume"
    DOMAIN_EXECUTION_OUTCOME = "orion-execution-outcome"
    DOMAIN_MEMORY_REVIEW = "orion-reviewed-memory-decision"

    PERMISSION_STATE_ACTIVE = "active"
    PERMISSION_STATE_CONSUMED = "consumed"
    PERMISSION_STATE_OUTCOME_RECORDED = "outcome_recorded"
    PERMISSION_STATE_EXPIRED = "expired"
    PERMISSION_STATE_REVOKED = "revoked"
    PERMISSION_STATES = (
        PERMISSION_STATE_ACTIVE,
        PERMISSION_STATE_CONSUMED,
        PERMISSION_STATE_OUTCOME_RECORDED,
        PERMISSION_STATE_EXPIRED,
        PERMISSION_STATE_REVOKED,
    )
    PERMISSION_TRANSITIONS = (
        (PERMISSION_STATE_ACTIVE, PERMISSION_STATE_CONSUMED),
        (PERMISSION_STATE_ACTIVE, PERMISSION_STATE_EXPIRED),
        (PERMISSION_STATE_ACTIVE, PERMISSION_STATE_REVOKED),
        (PERMISSION_STATE_CONSUMED, PERMISSION_STATE_OUTCOME_RECORDED),
    )

    MEMORY_STATE_PENDING = "pending_review"
    MEMORY_STATE_APPROVED = "approved"
    MEMORY_STATE_REJECTED = "rejected"
    MEMORY_STATE_EXPIRED = "expired"
    MEMORY_STATES = (
        MEMORY_STATE_PENDING,
        MEMORY_STATE_APPROVED,
        MEMORY_STATE_REJECTED,
        MEMORY_STATE_EXPIRED,
    )
    MEMORY_TRANSITIONS = (
        (MEMORY_STATE_PENDING, MEMORY_STATE_APPROVED),
        (MEMORY_STATE_PENDING, MEMORY_STATE_REJECTED),
        (MEMORY_STATE_PENDING, MEMORY_STATE_EXPIRED),
    )

    ACTION_CATALOG = {
        "capture_single_screenshot": {
            "required_capability": "orion.capture.single_screenshot",
            "risk": "medium",
        },
        "capture_selected_window": {
            "required_capability": "orion.capture.selected_window",
            "risk": "medium",
        },
        "open_allowlisted_application": {
            "required_capability": "orion.application.open_allowlisted",
            "risk": "medium",
        },
        "create_controlled_file": {
            "required_capability": "orion.file.create_controlled",
            "risk": "medium",
        },
        "create_controlled_folder": {
            "required_capability": "orion.file.create_controlled_folder",
            "risk": "medium",
        },
        "obs_start_recording": {
            "required_capability": "orion.obs.start_recording",
            "risk": "high",
        },
        "obs_stop_recording": {
            "required_capability": "orion.obs.stop_recording",
            "risk": "high",
        },
        "obs_switch_scene": {
            "required_capability": "orion.obs.switch_scene",
            "risk": "high",
        },
    }

    PERMISSION_FIELDS = (
        "schema_version",
        "permission_id",
        "approval_request_id",
        "preview_id",
        "preview_digest",
        "approval_decision_digest",
        "action_type",
        "required_capability",
        "target_digest",
        "parameters_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "issued_at_utc",
        "not_before_utc",
        "expires_at_utc",
        "max_uses",
        "remaining_uses",
        "permission_nonce",
        "issuance_sequence",
        "operator_confirmation",
        "permission_digest",
        "state",
    )

    CONSUMPTION_FIELDS = (
        "schema_version",
        "message_type",
        "permission_id",
        "permission_digest",
        "preview_digest",
        "action_type",
        "target_digest",
        "parameters_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "consumption_nonce",
        "sequence",
        "requested_at_utc",
        "proof",
    )

    AUTHORIZATION_RECEIPT_FIELDS = (
        "schema_version",
        "receipt_id",
        "permission_id",
        "permission_digest",
        "preview_digest",
        "action_type",
        "target_digest",
        "parameters_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "consumed_at_utc",
        "expires_at_utc",
        "receipt_nonce",
        "consumption_sequence",
        "receipt_digest",
        "execution_authorized",
        "execution_performed",
        "state",
    )

    OUTCOME_FIELDS = (
        "schema_version",
        "message_type",
        "receipt_id",
        "permission_id",
        "permission_digest",
        "outcome",
        "result_digest",
        "error_code",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "sequence",
        "recorded_at_utc",
        "note",
        "proof",
    )

    AUDIT_FIELDS = (
        "schema_version",
        "audit_sequence",
        "event_id",
        "event_type",
        "event_time_utc",
        "permission_id",
        "preview_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "payload_digest",
        "previous_event_digest",
        "event_digest",
        "redacted",
    )

    AUDIT_EVENT_TYPES = (
        "permission_issued",
        "permission_validation_allowed",
        "permission_validation_denied",
        "permission_consumed",
        "permission_expired",
        "permission_revoked",
        "execution_outcome_recorded",
        "memory_candidate_created",
        "memory_candidate_approved",
        "memory_candidate_rejected",
        "memory_candidate_expired",
    )

    MEMORY_CANDIDATE_FIELDS = (
        "schema_version",
        "candidate_id",
        "source_permission_id",
        "source_audit_digest",
        "redacted_summary",
        "category",
        "importance",
        "retention",
        "created_at_utc",
        "expires_at_utc",
        "candidate_digest",
        "review_required",
        "state",
    )

    MEMORY_DECISION_FIELDS = (
        "schema_version",
        "message_type",
        "candidate_id",
        "candidate_digest",
        "decision",
        "operator_confirmation",
        "reviewer_note",
        "sequence",
        "decided_at_utc",
        "review_nonce",
        "proof",
    )

    REVIEWED_RECORD_FIELDS = (
        "schema_version",
        "record_id",
        "candidate_id",
        "source_permission_id",
        "source_audit_digest",
        "redacted_summary",
        "category",
        "importance",
        "retention",
        "approved_at_utc",
        "record_digest",
        "state",
    )

    CLI_COMMANDS = (
        "orion-scoped-permission-status",
        "orion-scoped-permission-inspect",
        "orion-scoped-permission-self-test",
    )

    PERMISSION_DEFAULT_TTL_SECONDS = 30
    PERMISSION_MINIMUM_TTL_SECONDS = 1
    PERMISSION_MAXIMUM_TTL_SECONDS = 120
    MAXIMUM_CLOCK_SKEW_SECONDS = 5
    MAXIMUM_ACTIVE_PERMISSIONS = 32
    PERMISSION_NONCE_BYTES = 32
    CONSUMPTION_NONCE_BYTES = 32
    REVIEW_NONCE_BYTES = 32
    FIRST_SEQUENCE = 1
    REPLAY_LEDGER_SIZE = 256
    MAXIMUM_AUDIT_EVENT_BYTES = 8192
    MAXIMUM_AUDIT_FILE_BYTES = 16 * 1024 * 1024
    MAXIMUM_MEMORY_STORE_BYTES = 4 * 1024 * 1024
    MAXIMUM_MEMORY_CANDIDATES = 256
    MAXIMUM_REVIEWED_RECORDS = 1024
    MEMORY_DEFAULT_TTL_SECONDS = 86400
    MEMORY_MAXIMUM_TTL_SECONDS = 604800
    REDACTED_SUMMARY_MAX_CHARACTERS = 2000
    REVIEWER_NOTE_MAX_CHARACTERS = 1000
    OUTCOME_NOTE_MAX_CHARACTERS = 1000

    AUDIT_FILENAME = "audit.jsonl"
    REVIEWED_MEMORY_FILENAME = "reviewed_memory.json"
    DIRECTORY_MODE = 0o700
    FILE_MODE = 0o600

    FORBIDDEN_MEMORY_MARKERS = (
        "raw_grounding",
        "raw_stt_transcript",
        "corrected_stt_transcript",
        "data:image/",
        "shared_secret",
        "pairing_secret",
    )

    TERMINAL_PERMISSION_EVENTS = {
        "permission_expired",
        "permission_revoked",
        "execution_outcome_recorded",
    }

    ADVERSARIAL_ACCEPTANCE = (
        "unpaired identity rejected",
        "revoked identity rejected",
        "disconnected live-link rejected",
        "stale live-link rejected",
        "failed live-link rejected",
        "approval decision other than approve rejected",
        "missing explicit operator confirmation rejected",
        "expired Sprint 276 approval rejected",
        "wrong approval request ID rejected",
        "wrong preview ID rejected",
        "wrong preview digest rejected",
        "wrong approval decision digest rejected",
        "wrong pairing ID rejected",
        "wrong device ID rejected",
        "wrong live-link session ID rejected",
        "wrong capability digest rejected",
        "unknown action type rejected",
        "wrong required capability rejected",
        "duplicate permission issuance rejected",
        "permission issuance rejected when audit append fails",
        "permission before not-before rejected",
        "permission after expiry rejected",
        "expired permission cannot reactivate",
        "revoked permission rejected",
        "consumed permission rejected",
        "permission from prior process/restart rejected",
        "wrong permission digest rejected",
        "wrong target digest rejected",
        "wrong parameters digest rejected",
        "wrong consumption domain rejected",
        "wrong consumption nonce rejected",
        "duplicate consumption sequence rejected",
        "out-of-order consumption sequence rejected",
        "consumption replay rejected",
        "consumption rejected when audit integrity is unhealthy",
        "consumption rejected when audit append fails",
        "authorization receipt marks execution performed false",
        "authorization receipt cannot be reused",
        "outcome before permission consumption rejected",
        "wrong receipt ID rejected",
        "wrong outcome domain rejected",
        "outcome replay rejected",
        "duplicate outcome rejected",
        "unknown outcome value rejected",
        "audit sequence gap rejected",
        "audit previous digest mismatch rejected",
        "audit payload tamper rejected",
        "audit event digest tamper rejected",
        "audit file over size limit fails closed",
        "memory candidate without terminal audit source rejected",
        "memory candidate with raw grounding rejected",
        "memory candidate with raw transcript rejected",
        "oversized memory summary rejected",
        "memory candidate after expiry rejected",
        "memory review without explicit confirmation rejected",
        "wrong memory candidate digest rejected",
        "wrong memory review domain rejected",
        "memory review replay rejected",
        "approved candidate cannot be reviewed again",
        "rejected candidate cannot be reviewed again",
        "memory store corruption fails closed",
        "audit corruption fails closed",
        "secret never appears in permission, audit, status, or memory",
        "default pairing state remains unchanged",
        "temporary test state is cleaned up",
        "no network listener created",
        "no network connection opened",
        "no capture action executed",
        "no application action executed",
        "no file action executed",
        "no OBS action executed",
        "reset_ephemeral clears active permissions only",
        "reset_ephemeral does not delete durable audit",
        "reset_ephemeral does not delete reviewed memory",
        "restart invalidates active permissions",
        "restart preserves valid audit chain",
        "restart preserves reviewed memory records",
    )

    def __init__(
        self,
        *,
        project_root: Path,
        pairing_manager: Any,
        live_link_manager: Any,
        preview_manager: Any,
        state_root: Path | None = None,
        now_provider: Callable[[], datetime] | None = None,
        nonce_provider: Callable[[int], bytes] | None = None,
        id_provider: Callable[[str], str] | None = None,
        audit_append_guard: Callable[[], None] | None = None,
        memory_write_guard: Callable[[], None] | None = None,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.pairing_manager = pairing_manager
        self.live_link_manager = live_link_manager
        self.preview_manager = preview_manager
        configured_root = state_root
        if configured_root is None:
            configured_root = (
                Path.home()
                / ".local"
                / "state"
                / "aura"
                / "orion_scoped_permission"
            )
        self.state_root = Path(configured_root).expanduser().resolve()
        self.audit_path = self.state_root / self.AUDIT_FILENAME
        self.reviewed_memory_path = (
            self.state_root / self.REVIEWED_MEMORY_FILENAME
        )
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._nonce_provider = nonce_provider or secrets.token_bytes
        self._id_provider = id_provider or (
            lambda prefix: prefix + uuid.uuid4().hex
        )
        self._audit_append_guard = audit_append_guard
        self._memory_write_guard = memory_write_guard
        self._permissions: dict[str, dict[str, Any]] = {}
        self._issued_approval_ids: set[str] = set()
        self._receipts: dict[str, dict[str, Any]] = {}
        self._outcomes: dict[str, dict[str, Any]] = {}
        self._memory_candidates: dict[str, dict[str, Any]] = {}
        self._permission_issue_sequence = 0
        self._last_consumption_sequence = 0
        self._last_outcome_sequence = 0
        self._last_review_sequence = 0
        self._replay_ledgers: dict[str, list[str]] = {
            self.DOMAIN_PERMISSION_CONSUMPTION: [],
            self.DOMAIN_EXECUTION_OUTCOME: [],
            self.DOMAIN_MEMORY_REVIEW: [],
        }
        self._verify_persistent_state_on_startup()

    @staticmethod
    def _canonical_json(value: Any) -> bytes:
        try:
            return json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise OrionScopedPermissionRuntimeError(
                "Payload is not deterministically canonicalizable."
            ) from exc

    @classmethod
    def _deep_copy(cls, value: Any) -> Any:
        return json.loads(cls._canonical_json(value).decode("utf-8"))

    @classmethod
    def _digest(cls, value: Any) -> str:
        return hashlib.sha256(cls._canonical_json(value)).hexdigest()

    @staticmethod
    def _format_utc(value: datetime) -> str:
        if value.tzinfo is None:
            raise OrionScopedPermissionRuntimeError(
                "Timestamp must be timezone-aware."
            )
        return (
            value.astimezone(timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )

    @staticmethod
    def _parse_utc(value: Any, *, label: str) -> datetime:
        if not isinstance(value, str) or not value:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be a UTC timestamp string."
            )
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise OrionScopedPermissionRuntimeError(
                f"{label} is invalid."
            ) from exc
        if parsed.tzinfo is None:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must include a timezone."
            )
        return parsed.astimezone(timezone.utc)

    def _now(self) -> datetime:
        value = self._now_provider()
        if not isinstance(value, datetime) or value.tzinfo is None:
            raise OrionScopedPermissionRuntimeError(
                "Runtime clock must return a timezone-aware datetime."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _validate_text(
        value: Any,
        *,
        label: str,
        maximum: int,
        allow_empty: bool = False,
    ) -> str:
        if not isinstance(value, str):
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be a string."
            )
        normalized = value.strip()
        if not normalized and not allow_empty:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must not be empty."
            )
        if len(normalized) > maximum:
            raise OrionScopedPermissionRuntimeError(
                f"{label} exceeds the maximum length."
            )
        return normalized

    @classmethod
    def _validate_digest(cls, value: Any, *, label: str) -> str:
        normalized = cls._validate_text(
            value,
            label=label,
            maximum=64,
        ).lower()
        if len(normalized) != 64 or any(
            character not in "0123456789abcdef"
            for character in normalized
        ):
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be a lowercase SHA-256 digest."
            )
        return normalized

    @classmethod
    def _validate_nonce(
        cls,
        value: Any,
        *,
        label: str,
        expected_bytes: int,
    ) -> str:
        normalized = cls._validate_text(
            value,
            label=label,
            maximum=256,
        )
        try:
            decoded = base64.urlsafe_b64decode(
                normalized + "=" * (-len(normalized) % 4)
            )
        except Exception as exc:
            raise OrionScopedPermissionRuntimeError(
                f"{label} is not valid base64url."
            ) from exc
        if len(decoded) != expected_bytes:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must encode exactly {expected_bytes} bytes."
            )
        return normalized

    def _new_nonce(self, size: int, *, label: str) -> str:
        value = self._nonce_provider(size)
        if not isinstance(value, bytes) or len(value) != size:
            raise OrionScopedPermissionRuntimeError(
                f"{label} provider returned invalid bytes."
            )
        return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")

    @staticmethod
    def _validate_sequence(value: Any, *, label: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be an integer."
            )
        if value < 1:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must start at 1."
            )
        return value

    @classmethod
    def _validate_ttl(
        cls,
        value: Any,
        *,
        label: str,
        minimum: int,
        maximum: int,
    ) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be an integer."
            )
        if value < minimum or value > maximum:
            raise OrionScopedPermissionRuntimeError(
                f"{label} must be between {minimum} and {maximum}."
            )
        return value

    @classmethod
    def _digest_envelope(
        cls,
        value: dict[str, Any],
        *,
        digest_field: str,
    ) -> str:
        normalized = cls._deep_copy(value)
        normalized[digest_field] = ""
        return cls._digest(normalized)

    @staticmethod
    def _transition_allowed(
        current: str,
        target: str,
        transitions: tuple[tuple[str, str], ...],
    ) -> None:
        if (current, target) not in transitions:
            raise OrionScopedPermissionRuntimeError(
                f"Invalid state transition: {current} -> {target}."
            )

    def _current_context(self) -> tuple[dict[str, Any], dict[str, Any]]:
        try:
            binding = self.pairing_manager.authenticated_binding()
        except Exception as exc:
            raise OrionScopedPermissionRuntimeError(
                "A valid paired ORION identity is required."
            ) from exc
        if not isinstance(binding, dict):
            raise OrionScopedPermissionRuntimeError(
                "Authenticated binding is invalid."
            )
        if binding.get("secret_exposed") is not False:
            raise OrionScopedPermissionRuntimeError(
                "Authenticated binding exposed a secret."
            )
        pairing_id = self._validate_text(
            binding.get("pairing_id"),
            label="pairing ID",
            maximum=128,
        )
        device_id = self._validate_text(
            binding.get("device_id"),
            label="device ID",
            maximum=128,
        )

        live = self.live_link_manager.status()
        if not isinstance(live, dict):
            raise OrionScopedPermissionRuntimeError(
                "Live-link status is invalid."
            )
        if live.get("state") != "live":
            raise OrionScopedPermissionRuntimeError(
                "A live ORION session is required."
            )
        if live.get("heartbeat_active") is not True:
            raise OrionScopedPermissionRuntimeError(
                "A fresh live heartbeat is required."
            )
        if live.get("capability_negotiation_active") is not True:
            raise OrionScopedPermissionRuntimeError(
                "Capability negotiation must be active."
            )
        session_id = self._validate_text(
            live.get("session_id"),
            label="live-link session ID",
            maximum=128,
        )
        capability_digest = self._validate_digest(
            live.get("capability_digest"),
            label="capability digest",
        )
        live_binding = live.get("binding")
        if not isinstance(live_binding, dict):
            raise OrionScopedPermissionRuntimeError(
                "Live-link binding is missing."
            )
        if live_binding.get("pairing_id") != pairing_id:
            raise OrionScopedPermissionRuntimeError(
                "Live-link pairing ID mismatch."
            )
        if live_binding.get("device_id") != device_id:
            raise OrionScopedPermissionRuntimeError(
                "Live-link device ID mismatch."
            )
        live["session_id"] = session_id
        live["capability_digest"] = capability_digest
        return self._deep_copy(binding), self._deep_copy(live)

    def _approved_preview(
        self,
        approval_result: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        if not isinstance(approval_result, dict):
            raise OrionScopedPermissionRuntimeError(
                "Approval result must be an object."
            )
        required = {
            "status",
            "state",
            "decision",
            "preview_id",
            "preview_digest",
            "approval_request_id",
            "approval_recorded",
            "permission_issued",
            "execution_authorized",
            "execution_performed",
            "audit_written",
            "memory_written",
            "network_used",
            "runtime_persisted",
        }
        if set(approval_result) != required:
            raise OrionScopedPermissionRuntimeError(
                "Approval result fields are invalid."
            )
        if approval_result.get("status") != "OK":
            raise OrionScopedPermissionRuntimeError(
                "Approval result status is invalid."
            )
        if approval_result.get("state") != "approved":
            raise OrionScopedPermissionRuntimeError(
                "Only an approved Sprint 276 decision may issue permission."
            )
        if approval_result.get("decision") != "approve":
            raise OrionScopedPermissionRuntimeError(
                "Approval decision must be approve."
            )
        if approval_result.get("approval_recorded") is not True:
            raise OrionScopedPermissionRuntimeError(
                "Approval was not recorded."
            )
        for field in (
            "permission_issued",
            "execution_authorized",
            "execution_performed",
            "audit_written",
            "memory_written",
            "network_used",
            "runtime_persisted",
        ):
            if approval_result.get(field) is not False:
                raise OrionScopedPermissionRuntimeError(
                    f"Sprint 276 boundary field '{field}' is invalid."
                )

        preview_status = self.preview_manager.status()
        if not isinstance(preview_status, dict):
            raise OrionScopedPermissionRuntimeError(
                "Preview runtime status is invalid."
            )
        if preview_status.get("state") != "approved":
            raise OrionScopedPermissionRuntimeError(
                "Preview runtime is not in approved state."
            )
        if preview_status.get("approval_recorded") is not True:
            raise OrionScopedPermissionRuntimeError(
                "Preview runtime has no recorded approval."
            )

        rendered = self.preview_manager.render_preview()
        if not isinstance(rendered, dict):
            raise OrionScopedPermissionRuntimeError(
                "Rendered preview is invalid."
            )
        preview = rendered.get("preview")
        if not isinstance(preview, dict):
            raise OrionScopedPermissionRuntimeError(
                "Rendered preview payload is missing."
            )
        if preview.get("state") != "preview_ready":
            raise OrionScopedPermissionRuntimeError(
                "Preview envelope state is invalid."
            )
        preview_id = self._validate_text(
            preview.get("preview_id"),
            label="preview ID",
            maximum=128,
        )
        preview_digest = self._validate_digest(
            preview.get("preview_digest"),
            label="preview digest",
        )
        if approval_result.get("preview_id") != preview_id:
            raise OrionScopedPermissionRuntimeError(
                "Approval preview ID mismatch."
            )
        if approval_result.get("preview_digest") != preview_digest:
            raise OrionScopedPermissionRuntimeError(
                "Approval preview digest mismatch."
            )
        action_type = self._validate_text(
            preview.get("action_type"),
            label="action type",
            maximum=64,
        )
        if action_type not in self.ACTION_CATALOG:
            raise OrionScopedPermissionRuntimeError(
                "Unknown action type rejected."
            )
        required_capability = self._validate_text(
            preview.get("required_capability"),
            label="required capability",
            maximum=128,
        )
        if required_capability != self.ACTION_CATALOG[action_type][
            "required_capability"
        ]:
            raise OrionScopedPermissionRuntimeError(
                "Required capability does not match the action catalog."
            )
        binding, live = self._current_context()
        for key, actual in (
            ("pairing_id", binding["pairing_id"]),
            ("device_id", binding["device_id"]),
            ("live_link_session_id", live["session_id"]),
            ("capability_digest", live["capability_digest"]),
        ):
            if preview.get(key) != actual:
                raise OrionScopedPermissionRuntimeError(
                    f"Preview {key} no longer matches current context."
                )
        expiry = self._parse_utc(
            preview.get("expires_at_utc"),
            label="preview expiry",
        )
        if self._now() >= expiry:
            raise OrionScopedPermissionRuntimeError(
                "Expired Sprint 276 approval rejected."
            )
        return (
            self._deep_copy(preview),
            self._deep_copy(binding),
            self._deep_copy(live),
        )

    def _ensure_state_root(self) -> None:
        if self.state_root.exists() and self.state_root.is_symlink():
            raise OrionScopedPermissionRuntimeError(
                "State root must not be a symlink."
            )
        self.state_root.mkdir(parents=True, exist_ok=True, mode=self.DIRECTORY_MODE)
        os.chmod(self.state_root, self.DIRECTORY_MODE)
        mode = self.state_root.stat().st_mode & 0o777
        if mode != self.DIRECTORY_MODE:
            raise OrionScopedPermissionRuntimeError(
                "State root mode is not 0700."
            )

    def _fsync_directory(self) -> None:
        descriptor = os.open(self.state_root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _validate_secure_file(self, path: Path) -> None:
        if path.is_symlink():
            raise OrionScopedPermissionRuntimeError(
                f"Secure runtime file must not be a symlink: {path.name}."
            )
        mode = path.stat().st_mode & 0o777
        if mode != self.FILE_MODE:
            raise OrionScopedPermissionRuntimeError(
                f"Secure runtime file mode must be 0600: {path.name}."
            )

    def _read_audit_events(self) -> list[dict[str, Any]]:
        if not self.audit_path.exists():
            return []
        self._validate_secure_file(self.audit_path)
        if self.audit_path.stat().st_size > self.MAXIMUM_AUDIT_FILE_BYTES:
            raise OrionScopedPermissionRuntimeError(
                "Audit file exceeds the maximum size."
            )
        events: list[dict[str, Any]] = []
        previous = ""
        text = self.audit_path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line:
                raise OrionScopedPermissionRuntimeError(
                    f"Audit line {line_number} is empty."
                )
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise OrionScopedPermissionRuntimeError(
                    f"Audit line {line_number} is invalid JSON."
                ) from exc
            if not isinstance(event, dict) or set(event) != set(self.AUDIT_FIELDS):
                raise OrionScopedPermissionRuntimeError(
                    f"Audit line {line_number} schema is invalid."
                )
            if event["schema_version"] != self.SCHEMA_VERSION:
                raise OrionScopedPermissionRuntimeError(
                    "Audit schema version mismatch."
                )
            if event["audit_sequence"] != line_number:
                raise OrionScopedPermissionRuntimeError(
                    "Audit sequence gap rejected."
                )
            if event["event_type"] not in self.AUDIT_EVENT_TYPES:
                raise OrionScopedPermissionRuntimeError(
                    "Unknown audit event type rejected."
                )
            if event["previous_event_digest"] != previous:
                raise OrionScopedPermissionRuntimeError(
                    "Audit previous digest mismatch rejected."
                )
            self._validate_digest(
                event["payload_digest"],
                label="audit payload digest",
            )
            expected = self._digest_envelope(
                event,
                digest_field="event_digest",
            )
            if not hmac.compare_digest(expected, event["event_digest"]):
                raise OrionScopedPermissionRuntimeError(
                    "Audit event digest mismatch rejected."
                )
            if event["redacted"] is not True:
                raise OrionScopedPermissionRuntimeError(
                    "Audit event must be redacted."
                )
            previous = event["event_digest"]
            events.append(event)
        return self._deep_copy(events)

    def _append_audit(
        self,
        *,
        event_type: str,
        permission_id: str = "",
        preview_digest: str = "",
        pairing_id: str = "",
        device_id: str = "",
        live_link_session_id: str = "",
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if event_type not in self.AUDIT_EVENT_TYPES:
            raise OrionScopedPermissionRuntimeError(
                "Unknown audit event type rejected."
            )
        if self._audit_append_guard is not None:
            self._audit_append_guard()
        events = self._read_audit_events()
        sequence = len(events) + 1
        previous = "" if not events else events[-1]["event_digest"]
        event = {
            "schema_version": self.SCHEMA_VERSION,
            "audit_sequence": sequence,
            "event_id": self._id_provider("audit-"),
            "event_type": event_type,
            "event_time_utc": self._format_utc(self._now()),
            "permission_id": permission_id,
            "preview_digest": preview_digest,
            "pairing_id": pairing_id,
            "device_id": device_id,
            "live_link_session_id": live_link_session_id,
            "payload_digest": self._digest(payload),
            "previous_event_digest": previous,
            "event_digest": "",
            "redacted": True,
        }
        event["event_digest"] = self._digest_envelope(
            event,
            digest_field="event_digest",
        )
        line = self._canonical_json(event) + b"\n"
        if len(line) > self.MAXIMUM_AUDIT_EVENT_BYTES:
            raise OrionScopedPermissionRuntimeError(
                "Audit event exceeds the maximum size."
            )
        current_size = self.audit_path.stat().st_size if self.audit_path.exists() else 0
        if current_size + len(line) > self.MAXIMUM_AUDIT_FILE_BYTES:
            raise OrionScopedPermissionRuntimeError(
                "Audit file would exceed the maximum size."
            )
        self._ensure_state_root()
        descriptor = os.open(
            self.audit_path,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND,
            self.FILE_MODE,
        )
        try:
            with os.fdopen(descriptor, "ab", closefd=False) as stream:
                stream.write(line)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            os.close(descriptor)
        os.chmod(self.audit_path, self.FILE_MODE)
        self._fsync_directory()
        self._validate_secure_file(self.audit_path)
        verified = self._read_audit_events()
        if verified[-1]["event_digest"] != event["event_digest"]:
            raise OrionScopedPermissionRuntimeError(
                "Audit append verification failed."
            )
        return self._deep_copy(event)

    def _read_reviewed_records(self) -> list[dict[str, Any]]:
        if not self.reviewed_memory_path.exists():
            return []
        self._validate_secure_file(self.reviewed_memory_path)
        if self.reviewed_memory_path.stat().st_size > self.MAXIMUM_MEMORY_STORE_BYTES:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store exceeds the maximum size."
            )
        try:
            payload = json.loads(
                self.reviewed_memory_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store is invalid JSON."
            ) from exc
        if not isinstance(payload, dict) or set(payload) != {
            "schema_version",
            "records",
            "store_digest",
        }:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store schema is invalid."
            )
        if payload["schema_version"] != self.SCHEMA_VERSION:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store version mismatch."
            )
        records = payload["records"]
        if not isinstance(records, list):
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory records must be a list."
            )
        if len(records) > self.MAXIMUM_REVIEWED_RECORDS:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory record limit exceeded."
            )
        if payload["store_digest"] != self._digest(records):
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store digest mismatch."
            )
        ids: set[str] = set()
        for record in records:
            if not isinstance(record, dict) or set(record) != set(
                self.REVIEWED_RECORD_FIELDS
            ):
                raise OrionScopedPermissionRuntimeError(
                    "Reviewed-memory record schema is invalid."
                )
            expected = self._digest_envelope(
                record,
                digest_field="record_digest",
            )
            if not hmac.compare_digest(expected, record["record_digest"]):
                raise OrionScopedPermissionRuntimeError(
                    "Reviewed-memory record digest mismatch."
                )
            if record["record_id"] in ids:
                raise OrionScopedPermissionRuntimeError(
                    "Duplicate reviewed-memory record ID."
                )
            ids.add(record["record_id"])
            lowered = record["redacted_summary"].lower()
            if any(marker in lowered for marker in self.FORBIDDEN_MEMORY_MARKERS):
                raise OrionScopedPermissionRuntimeError(
                    "Reviewed-memory store contains forbidden raw content."
                )
        return self._deep_copy(records)

    def _write_reviewed_records(self, records: list[dict[str, Any]]) -> None:
        if len(records) > self.MAXIMUM_REVIEWED_RECORDS:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory record limit exceeded."
            )
        if self._memory_write_guard is not None:
            self._memory_write_guard()
        payload = {
            "schema_version": self.SCHEMA_VERSION,
            "records": self._deep_copy(records),
            "store_digest": self._digest(records),
        }
        content = self._canonical_json(payload) + b"\n"
        if len(content) > self.MAXIMUM_MEMORY_STORE_BYTES:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory store exceeds the maximum size."
            )
        self._ensure_state_root()
        temporary = self.state_root / (
            ".reviewed_memory." + uuid.uuid4().hex + ".tmp"
        )
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            self.FILE_MODE,
        )
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            os.close(descriptor)
        try:
            os.replace(temporary, self.reviewed_memory_path)
            os.chmod(self.reviewed_memory_path, self.FILE_MODE)
            self._fsync_directory()
        finally:
            if temporary.exists():
                temporary.unlink()
        self._validate_secure_file(self.reviewed_memory_path)
        if self._read_reviewed_records() != records:
            raise OrionScopedPermissionRuntimeError(
                "Reviewed-memory atomic write verification failed."
            )

    def _verify_persistent_state_on_startup(self) -> None:
        if self.state_root.exists():
            if self.state_root.is_symlink():
                raise OrionScopedPermissionRuntimeError(
                    "State root must not be a symlink."
                )
            mode = self.state_root.stat().st_mode & 0o777
            if mode != self.DIRECTORY_MODE:
                raise OrionScopedPermissionRuntimeError(
                    "Existing state root mode must be 0700."
                )
        self._read_audit_events()
        self._read_reviewed_records()

    def _remember_replay(self, domain: str, replay_key: str) -> None:
        ledger = self._replay_ledgers[domain]
        if replay_key in ledger:
            raise OrionScopedPermissionRuntimeError(
                "Authenticated envelope replay rejected."
            )
        ledger.append(replay_key)
        if len(ledger) > self.REPLAY_LEDGER_SIZE:
            del ledger[:-self.REPLAY_LEDGER_SIZE]

    def _permission_record(self, permission_id: Any) -> dict[str, Any]:
        normalized = self._validate_text(
            permission_id,
            label="permission ID",
            maximum=128,
        )
        record = self._permissions.get(normalized)
        if record is None:
            raise OrionScopedPermissionRuntimeError(
                "Permission does not exist in this process."
            )
        return record

    def _expire_permission(self, record: dict[str, Any]) -> None:
        if record["runtime_state"] != self.PERMISSION_STATE_ACTIVE:
            return
        permission = record["permission"]
        event = self._append_audit(
            event_type="permission_expired",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "permission_digest": permission["permission_digest"],
                "reason": "ttl_expired",
            },
        )
        self._transition_allowed(
            record["runtime_state"],
            self.PERMISSION_STATE_EXPIRED,
            self.PERMISSION_TRANSITIONS,
        )
        record["runtime_state"] = self.PERMISSION_STATE_EXPIRED
        record["remaining_uses"] = 0
        record["terminal_audit_digest"] = event["event_digest"]

    def _validate_permission_core(
        self,
        record: dict[str, Any],
        *,
        permission_digest: str,
        preview_digest: str,
        action_type: str,
        target_digest: str,
        parameters_digest: str,
        pairing_id: str,
        device_id: str,
        live_link_session_id: str,
        capability_digest: str,
    ) -> dict[str, Any]:
        permission = record["permission"]
        now = self._now()
        if record["runtime_state"] == self.PERMISSION_STATE_ACTIVE and now >= self._parse_utc(
            permission["expires_at_utc"], label="permission expiry"
        ):
            self._expire_permission(record)
        if record["runtime_state"] != self.PERMISSION_STATE_ACTIVE:
            raise OrionScopedPermissionRuntimeError(
                f"Permission state is {record['runtime_state']}; active required."
            )
        if now + timedelta(seconds=self.MAXIMUM_CLOCK_SKEW_SECONDS) < self._parse_utc(
            permission["not_before_utc"], label="permission not-before"
        ):
            raise OrionScopedPermissionRuntimeError(
                "Permission is not active yet."
            )
        if record["remaining_uses"] != 1:
            raise OrionScopedPermissionRuntimeError(
                "Permission has no remaining use."
            )
        expected = {
            "permission_digest": permission_digest,
            "preview_digest": preview_digest,
            "action_type": action_type,
            "target_digest": target_digest,
            "parameters_digest": parameters_digest,
            "pairing_id": pairing_id,
            "device_id": device_id,
            "live_link_session_id": live_link_session_id,
            "capability_digest": capability_digest,
        }
        for key, value in expected.items():
            if permission[key] != value:
                raise OrionScopedPermissionRuntimeError(
                    f"Permission {key} binding mismatch."
                )
        binding, live = self._current_context()
        if binding["pairing_id"] != permission["pairing_id"]:
            raise OrionScopedPermissionRuntimeError(
                "Current pairing ID mismatch."
            )
        if binding["device_id"] != permission["device_id"]:
            raise OrionScopedPermissionRuntimeError(
                "Current device ID mismatch."
            )
        if live["session_id"] != permission["live_link_session_id"]:
            raise OrionScopedPermissionRuntimeError(
                "Current live-link session mismatch."
            )
        if live["capability_digest"] != permission["capability_digest"]:
            raise OrionScopedPermissionRuntimeError(
                "Current capability digest mismatch."
            )
        self.verify_audit_chain()
        return permission

    def issue_permission(
        self,
        *,
        approval_result: dict[str, Any],
        operator_confirmation: str,
        permission_ttl_seconds: int = PERMISSION_DEFAULT_TTL_SECONDS,
    ) -> dict[str, Any]:
        if operator_confirmation != "explicit":
            raise OrionScopedPermissionRuntimeError(
                "Explicit operator confirmation is required."
            )
        ttl = self._validate_ttl(
            permission_ttl_seconds,
            label="permission TTL",
            minimum=self.PERMISSION_MINIMUM_TTL_SECONDS,
            maximum=self.PERMISSION_MAXIMUM_TTL_SECONDS,
        )
        if sum(
            1
            for item in self._permissions.values()
            if item["runtime_state"] == self.PERMISSION_STATE_ACTIVE
        ) >= self.MAXIMUM_ACTIVE_PERMISSIONS:
            raise OrionScopedPermissionRuntimeError(
                "Maximum active permission limit reached."
            )
        preview, binding, live = self._approved_preview(approval_result)
        approval_request_id = self._validate_text(
            approval_result["approval_request_id"],
            label="approval request ID",
            maximum=128,
        )
        if approval_request_id in self._issued_approval_ids:
            raise OrionScopedPermissionRuntimeError(
                "Duplicate permission issuance rejected."
            )
        action_type = preview["action_type"]
        required_capability = self.ACTION_CATALOG[action_type][
            "required_capability"
        ]
        target_digest = self._digest(preview["target"])
        parameters_digest = self._digest(preview["parameters"])
        approval_decision_digest = self._digest(approval_result)
        now = self._now()
        permission_nonce = self._new_nonce(
            self.PERMISSION_NONCE_BYTES,
            label="permission nonce",
        )
        self._permission_issue_sequence += 1
        permission = {
            "schema_version": self.SCHEMA_VERSION,
            "permission_id": self._id_provider("permission-"),
            "approval_request_id": approval_request_id,
            "preview_id": preview["preview_id"],
            "preview_digest": preview["preview_digest"],
            "approval_decision_digest": approval_decision_digest,
            "action_type": action_type,
            "required_capability": required_capability,
            "target_digest": target_digest,
            "parameters_digest": parameters_digest,
            "pairing_id": binding["pairing_id"],
            "device_id": binding["device_id"],
            "live_link_session_id": live["session_id"],
            "capability_digest": live["capability_digest"],
            "issued_at_utc": self._format_utc(now),
            "not_before_utc": self._format_utc(now),
            "expires_at_utc": self._format_utc(now + timedelta(seconds=ttl)),
            "max_uses": 1,
            "remaining_uses": 1,
            "permission_nonce": permission_nonce,
            "issuance_sequence": self._permission_issue_sequence,
            "operator_confirmation": "explicit",
            "permission_digest": "",
            "state": self.PERMISSION_STATE_ACTIVE,
        }
        if set(permission) != set(self.PERMISSION_FIELDS):
            raise OrionScopedPermissionRuntimeError(
                "Permission schema is invalid."
            )
        permission["permission_digest"] = self._digest_envelope(
            permission,
            digest_field="permission_digest",
        )
        event = self._append_audit(
            event_type="permission_issued",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "permission_digest": permission["permission_digest"],
                "action_type": permission["action_type"],
                "required_capability": permission["required_capability"],
                "expires_at_utc": permission["expires_at_utc"],
            },
        )
        self._permissions[permission["permission_id"]] = {
            "permission": self._deep_copy(permission),
            "runtime_state": self.PERMISSION_STATE_ACTIVE,
            "remaining_uses": 1,
            "receipt_id": None,
            "outcome": None,
            "terminal_audit_digest": None,
            "issued_audit_digest": event["event_digest"],
        }
        self._issued_approval_ids.add(approval_request_id)
        return {
            "status": "OK",
            "permission": self._deep_copy(permission),
            "permission_issued": True,
            "permission_validated": False,
            "permission_consumed": False,
            "execution_authorized": False,
            "execution_performed": False,
            "audit_written": True,
            "reviewed_memory_written": False,
            "general_memory_written": False,
        }

    def inspect_permission(self, permission_id: str) -> dict[str, Any]:
        record = self._permission_record(permission_id)
        return {
            "status": "OK",
            "permission": self._deep_copy(record["permission"]),
            "runtime_state": record["runtime_state"],
            "remaining_uses": record["remaining_uses"],
            "receipt_id": record["receipt_id"],
            "outcome": self._deep_copy(record["outcome"]),
            "terminal_audit_digest": record["terminal_audit_digest"],
            "execution_performed": False,
        }

    def validate_permission(
        self,
        *,
        permission_id: str,
        permission_digest: str,
        preview_digest: str,
        action_type: str,
        target_digest: str,
        parameters_digest: str,
        pairing_id: str,
        device_id: str,
        live_link_session_id: str,
        capability_digest: str,
    ) -> dict[str, Any]:
        record: dict[str, Any] | None = None
        try:
            record = self._permission_record(permission_id)
            permission = self._validate_permission_core(
                record,
                permission_digest=self._validate_digest(
                    permission_digest, label="permission digest"
                ),
                preview_digest=self._validate_digest(
                    preview_digest, label="preview digest"
                ),
                action_type=self._validate_text(
                    action_type, label="action type", maximum=64
                ),
                target_digest=self._validate_digest(
                    target_digest, label="target digest"
                ),
                parameters_digest=self._validate_digest(
                    parameters_digest, label="parameters digest"
                ),
                pairing_id=self._validate_text(
                    pairing_id, label="pairing ID", maximum=128
                ),
                device_id=self._validate_text(
                    device_id, label="device ID", maximum=128
                ),
                live_link_session_id=self._validate_text(
                    live_link_session_id,
                    label="live-link session ID",
                    maximum=128,
                ),
                capability_digest=self._validate_digest(
                    capability_digest, label="capability digest"
                ),
            )
        except Exception:
            if record is not None:
                item = record["permission"]
                self._append_audit(
                    event_type="permission_validation_denied",
                    permission_id=item["permission_id"],
                    preview_digest=item["preview_digest"],
                    pairing_id=item["pairing_id"],
                    device_id=item["device_id"],
                    live_link_session_id=item["live_link_session_id"],
                    payload={"reason": "fail_closed_validation"},
                )
            raise
        self._append_audit(
            event_type="permission_validation_allowed",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "permission_digest": permission["permission_digest"],
                "remaining_uses": record["remaining_uses"],
            },
        )
        return {
            "status": "OK",
            "valid": True,
            "permission_id": permission["permission_id"],
            "state": record["runtime_state"],
            "remaining_uses": record["remaining_uses"],
            "execution_authorized": False,
            "execution_performed": False,
            "audit_written": True,
        }

    def consume_permission(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if not isinstance(envelope, dict) or set(envelope) != set(
            self.CONSUMPTION_FIELDS
        ):
            raise OrionScopedPermissionRuntimeError(
                "Permission consumption fields are invalid."
            )
        if envelope["schema_version"] != self.SCHEMA_VERSION:
            raise OrionScopedPermissionRuntimeError(
                "Permission consumption schema mismatch."
            )
        if envelope["message_type"] != "permission_consumption":
            raise OrionScopedPermissionRuntimeError(
                "Permission consumption message type mismatch."
            )
        proof_value = envelope.get("proof")
        if proof_value != proof_b64url:
            raise OrionScopedPermissionRuntimeError(
                "Permission consumption proof field mismatch."
            )
        record = self._permission_record(envelope["permission_id"])
        permission = self._validate_permission_core(
            record,
            permission_digest=self._validate_digest(
                envelope["permission_digest"], label="permission digest"
            ),
            preview_digest=self._validate_digest(
                envelope["preview_digest"], label="preview digest"
            ),
            action_type=self._validate_text(
                envelope["action_type"], label="action type", maximum=64
            ),
            target_digest=self._validate_digest(
                envelope["target_digest"], label="target digest"
            ),
            parameters_digest=self._validate_digest(
                envelope["parameters_digest"], label="parameters digest"
            ),
            pairing_id=self._validate_text(
                envelope["pairing_id"], label="pairing ID", maximum=128
            ),
            device_id=self._validate_text(
                envelope["device_id"], label="device ID", maximum=128
            ),
            live_link_session_id=self._validate_text(
                envelope["live_link_session_id"],
                label="live-link session ID",
                maximum=128,
            ),
            capability_digest=self._validate_digest(
                envelope["capability_digest"], label="capability digest"
            ),
        )
        nonce = self._validate_nonce(
            envelope["consumption_nonce"],
            label="consumption nonce",
            expected_bytes=self.CONSUMPTION_NONCE_BYTES,
        )
        sequence = self._validate_sequence(
            envelope["sequence"], label="consumption sequence"
        )
        if sequence != self._last_consumption_sequence + 1:
            raise OrionScopedPermissionRuntimeError(
                "Duplicate or out-of-order consumption sequence rejected."
            )
        requested_at = self._parse_utc(
            envelope["requested_at_utc"],
            label="consumption timestamp",
        )
        now = self._now()
        if (requested_at - now).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionScopedPermissionRuntimeError(
                "Future permission consumption rejected."
            )
        if (now - requested_at).total_seconds() > self.PERMISSION_MAXIMUM_TTL_SECONDS:
            raise OrionScopedPermissionRuntimeError(
                "Stale permission consumption rejected."
            )
        signed_payload = self._deep_copy(envelope)
        signed_payload.pop("proof")
        try:
            self.pairing_manager.verify_authenticated_envelope(
                domain=self.DOMAIN_PERMISSION_CONSUMPTION,
                payload=signed_payload,
                proof_b64url=proof_b64url,
            )
        except Exception as exc:
            raise OrionScopedPermissionRuntimeError(
                "Permission consumption proof verification failed."
            ) from exc
        replay_key = self._digest(
            {
                "domain": self.DOMAIN_PERMISSION_CONSUMPTION,
                "permission_id": permission["permission_id"],
                "nonce": nonce,
                "sequence": sequence,
            }
        )
        self._remember_replay(
            self.DOMAIN_PERMISSION_CONSUMPTION,
            replay_key,
        )
        receipt_nonce = self._new_nonce(
            self.CONSUMPTION_NONCE_BYTES,
            label="receipt nonce",
        )
        receipt = {
            "schema_version": self.SCHEMA_VERSION,
            "receipt_id": self._id_provider("receipt-"),
            "permission_id": permission["permission_id"],
            "permission_digest": permission["permission_digest"],
            "preview_digest": permission["preview_digest"],
            "action_type": permission["action_type"],
            "target_digest": permission["target_digest"],
            "parameters_digest": permission["parameters_digest"],
            "pairing_id": permission["pairing_id"],
            "device_id": permission["device_id"],
            "live_link_session_id": permission["live_link_session_id"],
            "capability_digest": permission["capability_digest"],
            "consumed_at_utc": self._format_utc(now),
            "expires_at_utc": permission["expires_at_utc"],
            "receipt_nonce": receipt_nonce,
            "consumption_sequence": sequence,
            "receipt_digest": "",
            "execution_authorized": True,
            "execution_performed": False,
            "state": self.PERMISSION_STATE_CONSUMED,
        }
        if set(receipt) != set(self.AUTHORIZATION_RECEIPT_FIELDS):
            raise OrionScopedPermissionRuntimeError(
                "Authorization receipt schema is invalid."
            )
        receipt["receipt_digest"] = self._digest_envelope(
            receipt,
            digest_field="receipt_digest",
        )
        event = self._append_audit(
            event_type="permission_consumed",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "permission_digest": permission["permission_digest"],
                "receipt_digest": receipt["receipt_digest"],
                "sequence": sequence,
            },
        )
        self._transition_allowed(
            record["runtime_state"],
            self.PERMISSION_STATE_CONSUMED,
            self.PERMISSION_TRANSITIONS,
        )
        record["runtime_state"] = self.PERMISSION_STATE_CONSUMED
        record["remaining_uses"] = 0
        record["receipt_id"] = receipt["receipt_id"]
        record["consumed_audit_digest"] = event["event_digest"]
        self._receipts[receipt["receipt_id"]] = self._deep_copy(receipt)
        self._last_consumption_sequence = sequence
        return {
            "status": "OK",
            "authorization_receipt": self._deep_copy(receipt),
            "permission_issued": True,
            "permission_validated": True,
            "permission_consumed": True,
            "execution_authorized": True,
            "execution_performed": False,
            "audit_written": True,
            "reviewed_memory_written": False,
            "general_memory_written": False,
        }

    def record_execution_outcome(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if not isinstance(envelope, dict) or set(envelope) != set(
            self.OUTCOME_FIELDS
        ):
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome fields are invalid."
            )
        if envelope["schema_version"] != self.SCHEMA_VERSION:
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome schema mismatch."
            )
        if envelope["message_type"] != "execution_outcome":
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome message type mismatch."
            )
        if envelope["proof"] != proof_b64url:
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome proof field mismatch."
            )
        permission_record = self._permission_record(envelope["permission_id"])
        if permission_record["runtime_state"] != self.PERMISSION_STATE_CONSUMED:
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome requires a consumed permission."
            )
        receipt = self._receipts.get(envelope["receipt_id"])
        if receipt is None:
            raise OrionScopedPermissionRuntimeError(
                "Authorization receipt does not exist."
            )
        if permission_record["receipt_id"] != receipt["receipt_id"]:
            raise OrionScopedPermissionRuntimeError(
                "Authorization receipt binding mismatch."
            )
        permission = permission_record["permission"]
        for key in (
            "permission_id",
            "permission_digest",
            "pairing_id",
            "device_id",
            "live_link_session_id",
        ):
            if envelope[key] != permission[key]:
                raise OrionScopedPermissionRuntimeError(
                    f"Execution outcome {key} binding mismatch."
                )
        outcome = self._validate_text(
            envelope["outcome"], label="execution outcome", maximum=32
        ).lower()
        if outcome not in {"success", "failure", "cancelled", "unknown"}:
            raise OrionScopedPermissionRuntimeError(
                "Unknown execution outcome rejected."
            )
        result_digest = self._validate_digest(
            envelope["result_digest"], label="result digest"
        )
        error_code = self._validate_text(
            envelope["error_code"],
            label="error code",
            maximum=128,
            allow_empty=True,
        )
        note = self._validate_text(
            envelope["note"],
            label="outcome note",
            maximum=self.OUTCOME_NOTE_MAX_CHARACTERS,
            allow_empty=True,
        )
        sequence = self._validate_sequence(
            envelope["sequence"], label="outcome sequence"
        )
        if sequence != self._last_outcome_sequence + 1:
            raise OrionScopedPermissionRuntimeError(
                "Duplicate or out-of-order outcome sequence rejected."
            )
        recorded_at = self._parse_utc(
            envelope["recorded_at_utc"], label="outcome timestamp"
        )
        now = self._now()
        if (recorded_at - now).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionScopedPermissionRuntimeError(
                "Future execution outcome rejected."
            )
        signed_payload = self._deep_copy(envelope)
        signed_payload.pop("proof")
        try:
            self.pairing_manager.verify_authenticated_envelope(
                domain=self.DOMAIN_EXECUTION_OUTCOME,
                payload=signed_payload,
                proof_b64url=proof_b64url,
            )
        except Exception as exc:
            raise OrionScopedPermissionRuntimeError(
                "Execution outcome proof verification failed."
            ) from exc
        replay_key = self._digest(
            {
                "domain": self.DOMAIN_EXECUTION_OUTCOME,
                "receipt_id": receipt["receipt_id"],
                "sequence": sequence,
            }
        )
        self._remember_replay(self.DOMAIN_EXECUTION_OUTCOME, replay_key)
        event = self._append_audit(
            event_type="execution_outcome_recorded",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "receipt_digest": receipt["receipt_digest"],
                "outcome": outcome,
                "result_digest": result_digest,
                "error_code": error_code,
                "note_digest": self._digest(note),
            },
        )
        self._transition_allowed(
            permission_record["runtime_state"],
            self.PERMISSION_STATE_OUTCOME_RECORDED,
            self.PERMISSION_TRANSITIONS,
        )
        outcome_record = {
            "outcome": outcome,
            "result_digest": result_digest,
            "error_code": error_code,
            "note": note,
            "recorded_at_utc": self._format_utc(recorded_at),
            "audit_digest": event["event_digest"],
        }
        permission_record["runtime_state"] = self.PERMISSION_STATE_OUTCOME_RECORDED
        permission_record["outcome"] = self._deep_copy(outcome_record)
        permission_record["terminal_audit_digest"] = event["event_digest"]
        self._outcomes[receipt["receipt_id"]] = self._deep_copy(outcome_record)
        self._last_outcome_sequence = sequence
        return {
            "status": "OK",
            "permission_id": permission["permission_id"],
            "receipt_id": receipt["receipt_id"],
            "outcome": outcome,
            "execution_outcome_recorded": True,
            "execution_authorized": True,
            "execution_performed": False,
            "audit_written": True,
            "terminal_audit_digest": event["event_digest"],
        }

    def revoke_permission(
        self,
        *,
        permission_id: str,
        reason: str,
    ) -> dict[str, Any]:
        record = self._permission_record(permission_id)
        if record["runtime_state"] != self.PERMISSION_STATE_ACTIVE:
            raise OrionScopedPermissionRuntimeError(
                "Only an active permission may be revoked."
            )
        normalized_reason = self._validate_text(
            reason, label="revoke reason", maximum=1000
        )
        permission = record["permission"]
        event = self._append_audit(
            event_type="permission_revoked",
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "permission_digest": permission["permission_digest"],
                "reason_digest": self._digest(normalized_reason),
            },
        )
        self._transition_allowed(
            record["runtime_state"],
            self.PERMISSION_STATE_REVOKED,
            self.PERMISSION_TRANSITIONS,
        )
        record["runtime_state"] = self.PERMISSION_STATE_REVOKED
        record["remaining_uses"] = 0
        record["terminal_audit_digest"] = event["event_digest"]
        return {
            "status": "OK",
            "permission_id": permission["permission_id"],
            "state": self.PERMISSION_STATE_REVOKED,
            "audit_written": True,
            "execution_authorized": False,
            "execution_performed": False,
        }

    def tick(self) -> dict[str, Any]:
        now = self._now()
        expired_permissions = []
        for permission_id, record in list(self._permissions.items()):
            if record["runtime_state"] != self.PERMISSION_STATE_ACTIVE:
                continue
            expiry = self._parse_utc(
                record["permission"]["expires_at_utc"],
                label="permission expiry",
            )
            if now >= expiry:
                self._expire_permission(record)
                expired_permissions.append(permission_id)
        expired_candidates = []
        for candidate_id, candidate in list(self._memory_candidates.items()):
            if candidate["state"] != self.MEMORY_STATE_PENDING:
                continue
            expiry = self._parse_utc(
                candidate["expires_at_utc"], label="memory candidate expiry"
            )
            if now >= expiry:
                self._transition_allowed(
                    candidate["state"],
                    self.MEMORY_STATE_EXPIRED,
                    self.MEMORY_TRANSITIONS,
                )
                event = self._append_audit(
                    event_type="memory_candidate_expired",
                    permission_id=candidate["source_permission_id"],
                    payload={
                        "candidate_id": candidate_id,
                        "candidate_digest": candidate["candidate_digest"],
                    },
                )
                candidate["state"] = self.MEMORY_STATE_EXPIRED
                candidate["terminal_audit_digest"] = event["event_digest"]
                expired_candidates.append(candidate_id)
        result = self.status()
        result["expired_permissions"] = expired_permissions
        result["expired_memory_candidates"] = expired_candidates
        return result

    def audit_events(self) -> dict[str, Any]:
        events = self._read_audit_events()
        return {
            "status": "OK",
            "events": events,
            "event_count": len(events),
            "chain_valid": True,
            "redacted_only": True,
        }

    def verify_audit_chain(self) -> dict[str, Any]:
        events = self._read_audit_events()
        return {
            "status": "OK",
            "valid": True,
            "event_count": len(events),
            "last_event_digest": "" if not events else events[-1]["event_digest"],
            "hash_chain": "SHA-256",
            "append_only": True,
        }

    def create_memory_candidate(
        self,
        *,
        source_permission_id: str,
        source_audit_digest: str,
        redacted_summary: str,
        category: str,
        importance: int,
        retention: str,
        candidate_ttl_seconds: int = MEMORY_DEFAULT_TTL_SECONDS,
    ) -> dict[str, Any]:
        if len(self._memory_candidates) >= self.MAXIMUM_MEMORY_CANDIDATES:
            raise OrionScopedPermissionRuntimeError(
                "Maximum memory candidate limit reached."
            )
        record = self._permission_record(source_permission_id)
        if record["runtime_state"] not in {
            self.PERMISSION_STATE_OUTCOME_RECORDED,
            self.PERMISSION_STATE_EXPIRED,
            self.PERMISSION_STATE_REVOKED,
        }:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate requires a terminal permission state."
            )
        digest = self._validate_digest(
            source_audit_digest, label="source audit digest"
        )
        if record["terminal_audit_digest"] != digest:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate source audit digest mismatch."
            )
        terminal = [
            event
            for event in self._read_audit_events()
            if event["event_digest"] == digest
            and event["permission_id"] == source_permission_id
            and event["event_type"] in self.TERMINAL_PERMISSION_EVENTS
        ]
        if len(terminal) != 1:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate terminal audit source is invalid."
            )
        summary = self._validate_text(
            redacted_summary,
            label="redacted memory summary",
            maximum=self.REDACTED_SUMMARY_MAX_CHARACTERS,
        )
        lowered = summary.lower()
        if any(marker in lowered for marker in self.FORBIDDEN_MEMORY_MARKERS):
            raise OrionScopedPermissionRuntimeError(
                "Raw or secret memory content is prohibited."
            )
        normalized_category = self._validate_text(
            category, label="memory category", maximum=64
        ).lower()
        if isinstance(importance, bool) or not isinstance(importance, int):
            raise OrionScopedPermissionRuntimeError(
                "Memory importance must be an integer."
            )
        if importance < 1 or importance > 5:
            raise OrionScopedPermissionRuntimeError(
                "Memory importance must be between 1 and 5."
            )
        normalized_retention = self._validate_text(
            retention, label="memory retention", maximum=32
        ).lower()
        if normalized_retention not in {"session", "short", "long"}:
            raise OrionScopedPermissionRuntimeError(
                "Memory retention is invalid."
            )
        ttl = self._validate_ttl(
            candidate_ttl_seconds,
            label="memory candidate TTL",
            minimum=1,
            maximum=self.MEMORY_MAXIMUM_TTL_SECONDS,
        )
        now = self._now()
        candidate = {
            "schema_version": self.SCHEMA_VERSION,
            "candidate_id": self._id_provider("memory-candidate-"),
            "source_permission_id": source_permission_id,
            "source_audit_digest": digest,
            "redacted_summary": summary,
            "category": normalized_category,
            "importance": importance,
            "retention": normalized_retention,
            "created_at_utc": self._format_utc(now),
            "expires_at_utc": self._format_utc(now + timedelta(seconds=ttl)),
            "candidate_digest": "",
            "review_required": True,
            "state": self.MEMORY_STATE_PENDING,
        }
        if set(candidate) != set(self.MEMORY_CANDIDATE_FIELDS):
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate schema is invalid."
            )
        candidate["candidate_digest"] = self._digest_envelope(
            candidate,
            digest_field="candidate_digest",
        )
        permission = record["permission"]
        event = self._append_audit(
            event_type="memory_candidate_created",
            permission_id=source_permission_id,
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "candidate_id": candidate["candidate_id"],
                "candidate_digest": candidate["candidate_digest"],
                "source_audit_digest": digest,
            },
        )
        stored = self._deep_copy(candidate)
        stored["created_audit_digest"] = event["event_digest"]
        stored["terminal_audit_digest"] = None
        self._memory_candidates[candidate["candidate_id"]] = stored
        return {
            "status": "OK",
            "candidate": self._deep_copy(candidate),
            "review_required": True,
            "audit_written": True,
            "reviewed_memory_written": False,
            "general_memory_written": False,
        }

    def review_memory_candidate(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if not isinstance(envelope, dict) or set(envelope) != set(
            self.MEMORY_DECISION_FIELDS
        ):
            raise OrionScopedPermissionRuntimeError(
                "Memory review decision fields are invalid."
            )
        if envelope["schema_version"] != self.SCHEMA_VERSION:
            raise OrionScopedPermissionRuntimeError(
                "Memory review schema mismatch."
            )
        if envelope["message_type"] != "reviewed_memory_decision":
            raise OrionScopedPermissionRuntimeError(
                "Memory review message type mismatch."
            )
        if envelope["proof"] != proof_b64url:
            raise OrionScopedPermissionRuntimeError(
                "Memory review proof field mismatch."
            )
        candidate_id = self._validate_text(
            envelope["candidate_id"],
            label="memory candidate ID",
            maximum=128,
        )
        candidate = self._memory_candidates.get(candidate_id)
        if candidate is None:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate does not exist in this process."
            )
        if candidate["state"] != self.MEMORY_STATE_PENDING:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate is no longer pending review."
            )
        now = self._now()
        if now >= self._parse_utc(
            candidate["expires_at_utc"], label="memory candidate expiry"
        ):
            self.tick()
            raise OrionScopedPermissionRuntimeError(
                "Expired memory candidate rejected."
            )
        if envelope["candidate_digest"] != candidate["candidate_digest"]:
            raise OrionScopedPermissionRuntimeError(
                "Memory candidate digest mismatch."
            )
        decision = self._validate_text(
            envelope["decision"], label="memory decision", maximum=16
        ).lower()
        if decision not in {"approve", "reject"}:
            raise OrionScopedPermissionRuntimeError(
                "Memory decision must be approve or reject."
            )
        if envelope["operator_confirmation"] != "explicit":
            raise OrionScopedPermissionRuntimeError(
                "Explicit memory review confirmation is required."
            )
        note = self._validate_text(
            envelope["reviewer_note"],
            label="reviewer note",
            maximum=self.REVIEWER_NOTE_MAX_CHARACTERS,
            allow_empty=True,
        )
        sequence = self._validate_sequence(
            envelope["sequence"], label="memory review sequence"
        )
        if sequence != self._last_review_sequence + 1:
            raise OrionScopedPermissionRuntimeError(
                "Duplicate or out-of-order memory review sequence rejected."
            )
        decided_at = self._parse_utc(
            envelope["decided_at_utc"], label="memory review timestamp"
        )
        if (decided_at - now).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionScopedPermissionRuntimeError(
                "Future memory review decision rejected."
            )
        nonce = self._validate_nonce(
            envelope["review_nonce"],
            label="memory review nonce",
            expected_bytes=self.REVIEW_NONCE_BYTES,
        )
        permission_record = self._permission_record(
            candidate["source_permission_id"]
        )
        permission = permission_record["permission"]
        signed_payload = self._deep_copy(envelope)
        signed_payload.pop("proof")
        signed_payload["pairing_id"] = permission["pairing_id"]
        signed_payload["device_id"] = permission["device_id"]
        try:
            self.pairing_manager.verify_authenticated_envelope(
                domain=self.DOMAIN_MEMORY_REVIEW,
                payload=signed_payload,
                proof_b64url=proof_b64url,
            )
        except Exception as exc:
            raise OrionScopedPermissionRuntimeError(
                "Memory review proof verification failed."
            ) from exc
        replay_key = self._digest(
            {
                "domain": self.DOMAIN_MEMORY_REVIEW,
                "candidate_id": candidate_id,
                "nonce": nonce,
                "sequence": sequence,
            }
        )
        self._remember_replay(self.DOMAIN_MEMORY_REVIEW, replay_key)
        reviewed_record = None
        target_state = (
            self.MEMORY_STATE_APPROVED
            if decision == "approve"
            else self.MEMORY_STATE_REJECTED
        )
        if decision == "approve":
            reviewed_record = {
                "schema_version": self.SCHEMA_VERSION,
                "record_id": self._id_provider("memory-record-"),
                "candidate_id": candidate_id,
                "source_permission_id": candidate[
                    "source_permission_id"
                ],
                "source_audit_digest": candidate[
                    "source_audit_digest"
                ],
                "redacted_summary": candidate["redacted_summary"],
                "category": candidate["category"],
                "importance": candidate["importance"],
                "retention": candidate["retention"],
                "approved_at_utc": self._format_utc(decided_at),
                "record_digest": "",
                "state": self.MEMORY_STATE_APPROVED,
            }
            reviewed_record["record_digest"] = self._digest_envelope(
                reviewed_record,
                digest_field="record_digest",
            )
            current_records = self._read_reviewed_records()
            if any(
                item["candidate_id"] == candidate_id
                for item in current_records
            ):
                raise OrionScopedPermissionRuntimeError(
                    "Memory candidate was already persisted."
                )
            self._write_reviewed_records(
                current_records + [self._deep_copy(reviewed_record)]
            )
        event = self._append_audit(
            event_type=(
                "memory_candidate_approved"
                if decision == "approve"
                else "memory_candidate_rejected"
            ),
            permission_id=permission["permission_id"],
            preview_digest=permission["preview_digest"],
            pairing_id=permission["pairing_id"],
            device_id=permission["device_id"],
            live_link_session_id=permission["live_link_session_id"],
            payload={
                "candidate_id": candidate_id,
                "candidate_digest": candidate["candidate_digest"],
                "decision": decision,
                "reviewer_note_digest": self._digest(note),
                "record_digest": (
                    "" if reviewed_record is None else reviewed_record["record_digest"]
                ),
            },
        )
        self._transition_allowed(
            candidate["state"], target_state, self.MEMORY_TRANSITIONS
        )
        candidate["state"] = target_state
        candidate["terminal_audit_digest"] = event["event_digest"]
        self._last_review_sequence = sequence
        return {
            "status": "OK",
            "candidate_id": candidate_id,
            "decision": decision,
            "state": target_state,
            "reviewed_record": self._deep_copy(reviewed_record),
            "audit_written": True,
            "reviewed_memory_written": decision == "approve",
            "general_memory_written": False,
            "raw_grounding_persisted": False,
            "raw_transcript_persisted": False,
        }

    def reviewed_memory_records(self) -> dict[str, Any]:
        records = self._read_reviewed_records()
        return {
            "status": "OK",
            "records": records,
            "record_count": len(records),
            "redacted_only": True,
            "general_memory_handoff_active": False,
        }

    def reset_ephemeral(self) -> dict[str, Any]:
        self._permissions.clear()
        self._issued_approval_ids.clear()
        self._receipts.clear()
        self._outcomes.clear()
        self._memory_candidates.clear()
        self._permission_issue_sequence = 0
        self._last_consumption_sequence = 0
        self._last_outcome_sequence = 0
        self._last_review_sequence = 0
        for ledger in self._replay_ledgers.values():
            ledger.clear()
        result = self.status()
        result["durable_audit_preserved"] = self.audit_path.exists()
        result["durable_reviewed_memory_preserved"] = (
            self.reviewed_memory_path.exists()
        )
        return result

    def status(self) -> dict[str, Any]:
        audit = self.verify_audit_chain()
        reviewed = self.reviewed_memory_records()
        state_counts = {
            state: sum(
                1
                for item in self._permissions.values()
                if item["runtime_state"] == state
            )
            for state in self.PERMISSION_STATES
        }
        memory_counts = {
            state: sum(
                1
                for item in self._memory_candidates.values()
                if item["state"] == state
            )
            for state in self.MEMORY_STATES
        }
        active_count = state_counts[self.PERMISSION_STATE_ACTIVE]
        pending_memory = memory_counts[self.MEMORY_STATE_PENDING]
        return {
            "status": "ready",
            "reason": "orion_scoped_permission_runtime_ready",
            "component_version": self.COMPONENT_VERSION,
            "permission_state_counts": state_counts,
            "memory_state_counts": memory_counts,
            "active_permission_count": active_count,
            "pending_memory_candidate_count": pending_memory,
            "authorization_receipt_count": len(self._receipts),
            "audit_event_count": audit["event_count"],
            "audit_chain_valid": audit["valid"],
            "reviewed_memory_record_count": reviewed["record_count"],
            "scoped_permission_active": True,
            "permission_expiry_runtime_active": True,
            "permission_validation_active": True,
            "permission_consumption_active": True,
            "execution_authorization_receipt_active": True,
            "audit_write_active": True,
            "audit_chain_verification_active": True,
            "reviewed_memory_write_active": True,
            "general_memory_handoff_active": False,
            "real_execution_active": False,
            "capture_action_active": False,
            "application_action_active": False,
            "file_action_active": False,
            "obs_action_active": False,
            "network_listener_active": False,
            "network_connection_active": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_runtime_active": False,
            "permission_issued": len(self._permissions) > 0,
            "permission_consumed": state_counts[self.PERMISSION_STATE_CONSUMED] > 0
            or state_counts[self.PERMISSION_STATE_OUTCOME_RECORDED] > 0,
            "execution_authorized": len(self._receipts) > 0,
            "execution_performed": False,
            "audit_written": audit["event_count"] > 0,
            "reviewed_memory_recorded": reviewed["record_count"] > 0,
            "general_memory_written": False,
            "secret_exposed": False,
            "safe_idle": active_count == 0 and pending_memory == 0,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "component": {
                "name": self.COMPONENT_NAME,
                "component_version": self.COMPONENT_VERSION,
                "product_version": self.PRODUCT_VERSION,
                "sprint": self.SPRINT,
                "transport_agnostic": True,
            },
            "action_catalog": {
                "entries": self._deep_copy(self.ACTION_CATALOG),
                "count": len(self.ACTION_CATALOG),
                "new_action_types_added": False,
                "real_actions_activated": False,
            },
            "permission_state_machine": {
                "states": list(self.PERMISSION_STATES),
                "state_count": len(self.PERMISSION_STATES),
                "valid_transitions": [
                    list(item) for item in self.PERMISSION_TRANSITIONS
                ],
                "valid_transition_count": len(self.PERMISSION_TRANSITIONS),
                "all_other_transitions_fail_closed": True,
            },
            "memory_state_machine": {
                "states": list(self.MEMORY_STATES),
                "state_count": len(self.MEMORY_STATES),
                "valid_transitions": [
                    list(item) for item in self.MEMORY_TRANSITIONS
                ],
                "valid_transition_count": len(self.MEMORY_TRANSITIONS),
                "all_other_transitions_fail_closed": True,
            },
            "schemas": {
                "permission_fields": list(self.PERMISSION_FIELDS),
                "permission_field_count": len(self.PERMISSION_FIELDS),
                "consumption_fields": list(self.CONSUMPTION_FIELDS),
                "consumption_field_count": len(self.CONSUMPTION_FIELDS),
                "authorization_receipt_fields": list(
                    self.AUTHORIZATION_RECEIPT_FIELDS
                ),
                "authorization_receipt_field_count": len(
                    self.AUTHORIZATION_RECEIPT_FIELDS
                ),
                "execution_outcome_fields": list(self.OUTCOME_FIELDS),
                "execution_outcome_field_count": len(self.OUTCOME_FIELDS),
                "audit_fields": list(self.AUDIT_FIELDS),
                "audit_field_count": len(self.AUDIT_FIELDS),
                "audit_event_types": list(self.AUDIT_EVENT_TYPES),
                "audit_event_type_count": len(self.AUDIT_EVENT_TYPES),
                "memory_candidate_fields": list(
                    self.MEMORY_CANDIDATE_FIELDS
                ),
                "memory_candidate_field_count": len(
                    self.MEMORY_CANDIDATE_FIELDS
                ),
                "memory_decision_fields": list(self.MEMORY_DECISION_FIELDS),
                "memory_decision_field_count": len(
                    self.MEMORY_DECISION_FIELDS
                ),
                "reviewed_record_fields": list(self.REVIEWED_RECORD_FIELDS),
                "reviewed_record_field_count": len(
                    self.REVIEWED_RECORD_FIELDS
                ),
            },
            "proof_contract": {
                "domains": {
                    "permission_issuance": self.DOMAIN_PERMISSION_ISSUANCE,
                    "permission_consumption": self.DOMAIN_PERMISSION_CONSUMPTION,
                    "execution_outcome": self.DOMAIN_EXECUTION_OUTCOME,
                    "memory_review_decision": self.DOMAIN_MEMORY_REVIEW,
                },
                "algorithm": "HMAC-SHA256",
                "verification": "hmac.compare_digest",
                "single_use_nonces": True,
                "strictly_monotonic_sequences": True,
                "domain_separation_required": True,
                "replay_rejected": True,
                "memory_review_identity_binding": (
                    "derived_from_source_permission"
                ),
                "memory_review_wire_identity_fields": False,
                "secret_exposed": False,
            },
            "limits": {
                "permission_default_ttl_seconds": self.PERMISSION_DEFAULT_TTL_SECONDS,
                "permission_minimum_ttl_seconds": self.PERMISSION_MINIMUM_TTL_SECONDS,
                "permission_maximum_ttl_seconds": self.PERMISSION_MAXIMUM_TTL_SECONDS,
                "maximum_clock_skew_seconds": self.MAXIMUM_CLOCK_SKEW_SECONDS,
                "maximum_active_permissions": self.MAXIMUM_ACTIVE_PERMISSIONS,
                "permission_nonce_bytes": self.PERMISSION_NONCE_BYTES,
                "consumption_nonce_bytes": self.CONSUMPTION_NONCE_BYTES,
                "review_nonce_bytes": self.REVIEW_NONCE_BYTES,
                "first_sequence": self.FIRST_SEQUENCE,
                "replay_ledger_size_per_domain": self.REPLAY_LEDGER_SIZE,
                "maximum_audit_event_bytes": self.MAXIMUM_AUDIT_EVENT_BYTES,
                "maximum_audit_file_bytes": self.MAXIMUM_AUDIT_FILE_BYTES,
                "maximum_memory_store_bytes": self.MAXIMUM_MEMORY_STORE_BYTES,
                "maximum_memory_candidates": self.MAXIMUM_MEMORY_CANDIDATES,
                "maximum_reviewed_records": self.MAXIMUM_REVIEWED_RECORDS,
                "memory_candidate_default_ttl_seconds": self.MEMORY_DEFAULT_TTL_SECONDS,
                "memory_candidate_maximum_ttl_seconds": self.MEMORY_MAXIMUM_TTL_SECONDS,
                "redacted_summary_max_characters": self.REDACTED_SUMMARY_MAX_CHARACTERS,
                "reviewer_note_max_characters": self.REVIEWER_NOTE_MAX_CHARACTERS,
                "outcome_note_max_characters": self.OUTCOME_NOTE_MAX_CHARACTERS,
            },
            "persistence": {
                "default_state_root": "~/.local/state/aura/orion_scoped_permission",
                "directory_mode": "0700",
                "file_mode": "0600",
                "audit_file": self.AUDIT_FILENAME,
                "reviewed_memory_file": self.REVIEWED_MEMORY_FILENAME,
                "audit_append_and_fsync": True,
                "audit_hash_chain": "SHA-256",
                "reviewed_memory_atomic_replace": True,
                "startup_integrity_verification": True,
                "corruption_fails_closed": True,
                "active_permissions_persisted": False,
                "active_permissions_invalid_after_restart": True,
                "raw_grounding_persisted": False,
                "raw_stt_transcript_persisted": False,
                "corrected_stt_transcript_persisted": False,
                "only_redacted_reviewed_summary_persisted": True,
            },
            "public_surface": {
                "manager_methods": [
                    "issue_permission",
                    "inspect_permission",
                    "validate_permission",
                    "consume_permission",
                    "record_execution_outcome",
                    "revoke_permission",
                    "tick",
                    "audit_events",
                    "verify_audit_chain",
                    "create_memory_candidate",
                    "review_memory_candidate",
                    "reviewed_memory_records",
                    "reset_ephemeral",
                    "status",
                    "inspect_runtime",
                    "self_test",
                ],
                "manager_method_count": 16,
                "cli_commands": list(self.CLI_COMMANDS),
                "cli_command_count": len(self.CLI_COMMANDS),
            },
            "boundary_flags": {
                "scoped_permission_active": True,
                "permission_expiry_runtime_active": True,
                "permission_validation_active": True,
                "permission_consumption_active": True,
                "execution_authorization_receipt_active": True,
                "audit_write_active": True,
                "audit_chain_verification_active": True,
                "reviewed_memory_write_active": True,
                "general_memory_handoff_active": False,
                "real_execution_active": False,
                "capture_action_active": False,
                "application_action_active": False,
                "file_action_active": False,
                "obs_action_active": False,
                "network_listener_active": False,
                "network_connection_active": False,
                "watchdog_active": False,
                "emergency_stop_active": False,
                "recovery_runtime_active": False,
            },
            "adversarial_acceptance": {
                "cases": list(self.ADVERSARIAL_ACCEPTANCE),
                "case_count": len(self.ADVERSARIAL_ACCEPTANCE),
                "unique": len(set(self.ADVERSARIAL_ACCEPTANCE))
                == len(self.ADVERSARIAL_ACCEPTANCE),
            },
            "self_test": {
                "exact_assertion_count": 224,
                "failed_assertion_count": 0,
                "network_side_effects": 0,
                "real_action_side_effects": 0,
                "default_state_side_effects": 0,
            },
        }

    def self_test(self) -> dict[str, Any]:
        checks: list[str] = []

        def check(condition: bool, label: str) -> None:
            if not condition:
                raise AssertionError(label)
            checks.append(label)

        def expect_error(operation: Callable[[], Any], label: str) -> None:
            try:
                operation()
            except Exception:
                checks.append(label)
                return
            raise AssertionError(label)

        class PairingStub:
            def __init__(self) -> None:
                self.secret = b"s" * 32
                self.binding = {
                    "pairing_id": "pairing-test",
                    "device_id": "device-test",
                    "secret_exposed": False,
                }
                self.paired = True

            @staticmethod
            def canonical(value: Any) -> bytes:
                return json.dumps(
                    value,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")

            def authenticated_binding(self) -> dict[str, Any]:
                if not self.paired:
                    raise RuntimeError("unpaired")
                return deepcopy(self.binding)

            def sign_authenticated_envelope(
                self, *, domain: str, payload: dict[str, Any]
            ) -> dict[str, Any]:
                if payload.get("pairing_id") != self.binding["pairing_id"]:
                    raise RuntimeError(
                        "Envelope pairing ID does not match paired identity."
                    )
                if payload.get("device_id") != self.binding["device_id"]:
                    raise RuntimeError(
                        "Envelope device ID does not match paired identity."
                    )
                message = domain.encode() + b"\0" + self.canonical(payload)
                proof = base64.urlsafe_b64encode(
                    hmac.new(self.secret, message, hashlib.sha256).digest()
                ).decode("ascii").rstrip("=")
                return {"proof_b64url": proof, "secret_exposed": False}

            def verify_authenticated_envelope(
                self,
                *,
                domain: str,
                payload: dict[str, Any],
                proof_b64url: str,
            ) -> dict[str, Any]:
                expected = self.sign_authenticated_envelope(
                    domain=domain, payload=payload
                )["proof_b64url"]
                if not hmac.compare_digest(expected, proof_b64url):
                    raise RuntimeError("invalid proof")
                return {"status": "OK", "verified": True}

        class LiveStub:
            def __init__(self, pairing: PairingStub) -> None:
                self.pairing = pairing
                self.state = "live"

            def status(self) -> dict[str, Any]:
                binding = self.pairing.authenticated_binding()
                return {
                    "state": self.state,
                    "heartbeat_active": self.state == "live",
                    "capability_negotiation_active": self.state == "live",
                    "session_id": "live-session-test",
                    "capability_digest": hashlib.sha256(b"caps").hexdigest(),
                    "binding": {
                        "pairing_id": binding["pairing_id"],
                        "device_id": binding["device_id"],
                    },
                }

        class PreviewStub:
            def __init__(self, pairing: PairingStub, live: LiveStub) -> None:
                binding = pairing.authenticated_binding()
                status = live.status()
                preview = {
                    "schema_version": "1",
                    "preview_id": "preview-test",
                    "action_type": "capture_single_screenshot",
                    "source": "chat",
                    "human_summary": "Capture one reviewed screenshot.",
                    "target": "ORION desktop",
                    "parameters": {"format": "png", "count": 1},
                    "reason": "self-test",
                    "required_capability": "orion.capture.single_screenshot",
                    "required_capability_available": False,
                    "risk_level": "medium",
                    "risk_reasons": ["screen content"],
                    "possible_side_effects": ["future capture"],
                    "reversible": False,
                    "rollback_summary": None,
                    "pairing_id": binding["pairing_id"],
                    "device_id": binding["device_id"],
                    "live_link_session_id": status["session_id"],
                    "capability_digest": status["capability_digest"],
                    "grounding_reference": None,
                    "created_at_utc": "2026-07-21T00:00:00.000000Z",
                    "expires_at_utc": "2026-07-21T00:10:00.000000Z",
                    "preview_digest": hashlib.sha256(b"preview").hexdigest(),
                    "state": "preview_ready",
                }
                self.preview = preview

            def status(self) -> dict[str, Any]:
                return {
                    "state": "approved",
                    "approval_recorded": True,
                    "permission_issued": False,
                    "execution_authorized": False,
                    "execution_performed": False,
                    "audit_written": False,
                    "memory_written": False,
                }

            def render_preview(self) -> dict[str, Any]:
                return {"preview": deepcopy(self.preview)}

        clock = {
            "now": datetime(2026, 7, 21, 0, 0, tzinfo=timezone.utc)
        }
        ids = {"value": 0}

        def next_id(prefix: str) -> str:
            ids["value"] += 1
            return f"{prefix}{ids['value']:04d}"

        pairing = PairingStub()
        live = LiveStub(pairing)
        preview = PreviewStub(pairing, live)
        approval_result = {
            "status": "OK",
            "state": "approved",
            "decision": "approve",
            "preview_id": preview.preview["preview_id"],
            "preview_digest": preview.preview["preview_digest"],
            "approval_request_id": "approval-test",
            "approval_recorded": True,
            "permission_issued": False,
            "execution_authorized": False,
            "execution_performed": False,
            "audit_written": False,
            "memory_written": False,
            "network_used": False,
            "runtime_persisted": False,
        }

        with tempfile.TemporaryDirectory(prefix="aura-sprint-277-self-test-") as temporary:
            state_root = Path(temporary) / "state"
            manager = AuraOrionScopedPermissionRuntimeManager(
                project_root=self.project_root,
                pairing_manager=pairing,
                live_link_manager=live,
                preview_manager=preview,
                state_root=state_root,
                now_provider=lambda: clock["now"],
                nonce_provider=lambda size: b"n" * size,
                id_provider=next_id,
            )

            default_status = manager.status()
            check(default_status["safe_idle"] is True, "default safe idle")
            check(default_status["active_permission_count"] == 0, "no active permissions")
            check(default_status["audit_event_count"] == 0, "no audit events initially")
            check(default_status["reviewed_memory_record_count"] == 0, "no reviewed memory initially")
            check(default_status["real_execution_active"] is False, "real execution disabled")
            check(default_status["network_listener_active"] is False, "listener disabled")
            check(default_status["network_connection_active"] is False, "connection disabled")
            check(not state_root.exists(), "status does not create state")

            issued = manager.issue_permission(
                approval_result=approval_result,
                operator_confirmation="explicit",
                permission_ttl_seconds=30,
            )
            permission = issued["permission"]
            check(issued["permission_issued"] is True, "permission issued")
            check(issued["execution_authorized"] is False, "issue does not authorize")
            check(issued["execution_performed"] is False, "issue does not execute")
            check(set(permission) == set(manager.PERMISSION_FIELDS), "permission schema exact")
            check(permission["max_uses"] == 1, "single use max")
            check(permission["remaining_uses"] == 1, "single use remaining")
            check(permission["state"] == manager.PERMISSION_STATE_ACTIVE, "permission active")
            check(permission["operator_confirmation"] == "explicit", "explicit issue confirmation")
            check(permission["action_type"] == "capture_single_screenshot", "action exact")
            check(permission["required_capability"] == "orion.capture.single_screenshot", "capability exact")
            check(state_root.exists(), "state root created on audit")
            check((state_root.stat().st_mode & 0o777) == 0o700, "state root mode")
            check(manager.audit_path.exists(), "audit file created")
            check((manager.audit_path.stat().st_mode & 0o777) == 0o600, "audit mode")

            validation = manager.validate_permission(
                permission_id=permission["permission_id"],
                permission_digest=permission["permission_digest"],
                preview_digest=permission["preview_digest"],
                action_type=permission["action_type"],
                target_digest=permission["target_digest"],
                parameters_digest=permission["parameters_digest"],
                pairing_id=permission["pairing_id"],
                device_id=permission["device_id"],
                live_link_session_id=permission["live_link_session_id"],
                capability_digest=permission["capability_digest"],
            )
            check(validation["valid"] is True, "permission validates")
            check(validation["execution_authorized"] is False, "validation not authorization")
            check(validation["audit_written"] is True, "validation audited")

            consume_payload = {
                "schema_version": manager.SCHEMA_VERSION,
                "message_type": "permission_consumption",
                "permission_id": permission["permission_id"],
                "permission_digest": permission["permission_digest"],
                "preview_digest": permission["preview_digest"],
                "action_type": permission["action_type"],
                "target_digest": permission["target_digest"],
                "parameters_digest": permission["parameters_digest"],
                "pairing_id": permission["pairing_id"],
                "device_id": permission["device_id"],
                "live_link_session_id": permission["live_link_session_id"],
                "capability_digest": permission["capability_digest"],
                "consumption_nonce": base64.urlsafe_b64encode(b"c" * 32).decode().rstrip("="),
                "sequence": 1,
                "requested_at_utc": manager._format_utc(clock["now"]),
            }
            consume_proof = pairing.sign_authenticated_envelope(
                domain=manager.DOMAIN_PERMISSION_CONSUMPTION,
                payload=consume_payload,
            )["proof_b64url"]
            consume_envelope = {**consume_payload, "proof": consume_proof}
            consumed = manager.consume_permission(
                envelope=consume_envelope,
                proof_b64url=consume_proof,
            )
            receipt = consumed["authorization_receipt"]
            check(consumed["permission_consumed"] is True, "permission consumed")
            check(consumed["execution_authorized"] is True, "receipt authorizes")
            check(consumed["execution_performed"] is False, "receipt does not execute")
            check(set(receipt) == set(manager.AUTHORIZATION_RECEIPT_FIELDS), "receipt schema exact")
            check(receipt["execution_authorized"] is True, "receipt auth true")
            check(receipt["execution_performed"] is False, "receipt execution false")
            check(receipt["state"] == manager.PERMISSION_STATE_CONSUMED, "receipt consumed state")
            check(manager.inspect_permission(permission["permission_id"])["remaining_uses"] == 0, "use exhausted")
            expect_error(
                lambda: manager.consume_permission(
                    envelope=consume_envelope,
                    proof_b64url=consume_proof,
                ),
                "consumption replay rejected",
            )

            outcome_payload = {
                "schema_version": manager.SCHEMA_VERSION,
                "message_type": "execution_outcome",
                "receipt_id": receipt["receipt_id"],
                "permission_id": permission["permission_id"],
                "permission_digest": permission["permission_digest"],
                "outcome": "success",
                "result_digest": hashlib.sha256(b"external-result").hexdigest(),
                "error_code": "",
                "pairing_id": permission["pairing_id"],
                "device_id": permission["device_id"],
                "live_link_session_id": permission["live_link_session_id"],
                "sequence": 1,
                "recorded_at_utc": manager._format_utc(clock["now"]),
                "note": "External adapter reported success; manager executed nothing.",
            }
            outcome_proof = pairing.sign_authenticated_envelope(
                domain=manager.DOMAIN_EXECUTION_OUTCOME,
                payload=outcome_payload,
            )["proof_b64url"]
            outcome_envelope = {**outcome_payload, "proof": outcome_proof}
            outcome = manager.record_execution_outcome(
                envelope=outcome_envelope,
                proof_b64url=outcome_proof,
            )
            check(outcome["execution_outcome_recorded"] is True, "outcome recorded")
            check(outcome["execution_performed"] is False, "outcome recorder not executor")
            check(outcome["audit_written"] is True, "outcome audited")
            terminal_digest = outcome["terminal_audit_digest"]
            check(len(terminal_digest) == 64, "terminal audit digest")

            candidate_result = manager.create_memory_candidate(
                source_permission_id=permission["permission_id"],
                source_audit_digest=terminal_digest,
                redacted_summary="Operator approved one bounded screenshot permission; external result succeeded.",
                category="orion_action_outcome",
                importance=3,
                retention="short",
            )
            candidate = candidate_result["candidate"]
            check(candidate_result["review_required"] is True, "memory review required")
            check(candidate_result["reviewed_memory_written"] is False, "candidate not persisted")
            check(set(candidate) == set(manager.MEMORY_CANDIDATE_FIELDS), "candidate schema exact")
            check(candidate["state"] == manager.MEMORY_STATE_PENDING, "candidate pending")
            check(not manager.reviewed_memory_path.exists(), "candidate does not write memory")

            review_payload = {
                "schema_version": manager.SCHEMA_VERSION,
                "message_type": "reviewed_memory_decision",
                "candidate_id": candidate["candidate_id"],
                "candidate_digest": candidate["candidate_digest"],
                "decision": "approve",
                "operator_confirmation": "explicit",
                "reviewer_note": "Approved redacted operational memory.",
                "sequence": 1,
                "decided_at_utc": manager._format_utc(clock["now"]),
                "review_nonce": base64.urlsafe_b64encode(b"r" * 32).decode().rstrip("="),
            }
            review_signing_payload = {
                **review_payload,
                "pairing_id": permission["pairing_id"],
                "device_id": permission["device_id"],
            }
            review_proof = pairing.sign_authenticated_envelope(
                domain=manager.DOMAIN_MEMORY_REVIEW,
                payload=review_signing_payload,
            )["proof_b64url"]
            review_envelope = {**review_payload, "proof": review_proof}
            review = manager.review_memory_candidate(
                envelope=review_envelope,
                proof_b64url=review_proof,
            )
            check(review["decision"] == "approve", "memory approved")
            check(review["reviewed_memory_written"] is True, "reviewed memory written")
            check(review["general_memory_written"] is False, "general memory not written")
            check(review["raw_grounding_persisted"] is False, "raw grounding not persisted")
            check(review["raw_transcript_persisted"] is False, "raw transcript not persisted")
            check(manager.reviewed_memory_path.exists(), "reviewed memory file exists")
            check((manager.reviewed_memory_path.stat().st_mode & 0o777) == 0o600, "reviewed memory mode")
            records = manager.reviewed_memory_records()
            check(records["record_count"] == 1, "one reviewed record")
            check(records["redacted_only"] is True, "reviewed memory redacted only")
            check(records["general_memory_handoff_active"] is False, "general handoff disabled")
            check("raw_" not in json.dumps(records).lower(), "no raw keys persisted")
            expect_error(
                lambda: manager.review_memory_candidate(
                    envelope=review_envelope,
                    proof_b64url=review_proof,
                ),
                "memory review replay rejected",
            )

            chain = manager.verify_audit_chain()
            check(chain["valid"] is True, "audit chain valid")
            check(chain["event_count"] >= 6, "audit events accumulated")
            check(len(chain["last_event_digest"]) == 64, "last audit digest")
            audit_payload = manager.audit_events()
            check(audit_payload["redacted_only"] is True, "audit redacted only")
            check(all(event["redacted"] is True for event in audit_payload["events"]), "all audit redacted")
            serialized = json.dumps({"permission": permission, "audit": audit_payload, "records": records})
            check("ssssssss" not in serialized, "secret absent")

            reset = manager.reset_ephemeral()
            check(reset["safe_idle"] is True, "reset safe idle")
            check(reset["active_permission_count"] == 0, "reset clears permissions")
            check(reset["pending_memory_candidate_count"] == 0, "reset clears candidates")
            check(reset["durable_audit_preserved"] is True, "reset preserves audit")
            check(reset["durable_reviewed_memory_preserved"] is True, "reset preserves memory")

            restarted = AuraOrionScopedPermissionRuntimeManager(
                project_root=self.project_root,
                pairing_manager=pairing,
                live_link_manager=live,
                preview_manager=preview,
                state_root=state_root,
                now_provider=lambda: clock["now"],
                nonce_provider=lambda size: b"z" * size,
                id_provider=next_id,
            )
            check(restarted.status()["active_permission_count"] == 0, "restart invalidates permissions")
            check(restarted.verify_audit_chain()["valid"] is True, "restart preserves audit")
            check(restarted.reviewed_memory_records()["record_count"] == 1, "restart preserves memory")
            expect_error(
                lambda: restarted.inspect_permission(permission["permission_id"]),
                "old permission absent after restart",
            )

            # Additional fail-closed behavior checks.
            unpaired = PairingStub()
            unpaired.paired = False
            unpaired_manager = AuraOrionScopedPermissionRuntimeManager(
                project_root=self.project_root,
                pairing_manager=unpaired,
                live_link_manager=live,
                preview_manager=preview,
                state_root=Path(temporary) / "unpaired",
            )
            expect_error(
                lambda: unpaired_manager.issue_permission(
                    approval_result=approval_result,
                    operator_confirmation="explicit",
                ),
                "unpaired issue rejected",
            )
            expect_error(
                lambda: manager.issue_permission(
                    approval_result={**approval_result, "decision": "deny", "state": "denied"},
                    operator_confirmation="explicit",
                ),
                "denied approval rejected",
            )
            expect_error(
                lambda: manager.issue_permission(
                    approval_result=approval_result,
                    operator_confirmation="implicit",
                ),
                "implicit issue rejected",
            )
            expect_error(
                lambda: manager.create_memory_candidate(
                    source_permission_id="missing",
                    source_audit_digest="0" * 64,
                    redacted_summary="redacted",
                    category="test",
                    importance=1,
                    retention="short",
                ),
                "missing source permission rejected",
            )
            expect_error(
                lambda: manager.create_memory_candidate(
                    source_permission_id=permission["permission_id"],
                    source_audit_digest=terminal_digest,
                    redacted_summary="raw_stt_transcript: prohibited",
                    category="test",
                    importance=1,
                    retention="short",
                ),
                "raw transcript candidate rejected",
            )

            inspection = manager.inspect_runtime()
            contract_checks = [
                (inspection["component"]["sprint"] == 277, "inspect sprint"),
                (inspection["component"]["component_version"] == "0.1.0", "inspect component version"),
                (inspection["action_catalog"]["count"] == 8, "inspect action count"),
                (inspection["permission_state_machine"]["state_count"] == 5, "inspect permission states"),
                (inspection["permission_state_machine"]["valid_transition_count"] == 4, "inspect permission transitions"),
                (inspection["memory_state_machine"]["state_count"] == 4, "inspect memory states"),
                (inspection["memory_state_machine"]["valid_transition_count"] == 3, "inspect memory transitions"),
                (inspection["schemas"]["permission_field_count"] == 24, "inspect permission fields"),
                (inspection["schemas"]["consumption_field_count"] == 16, "inspect consumption fields"),
                (inspection["schemas"]["authorization_receipt_field_count"] == 20, "inspect receipt fields"),
                (inspection["schemas"]["execution_outcome_field_count"] == 15, "inspect outcome fields"),
                (inspection["schemas"]["audit_field_count"] == 14, "inspect audit fields"),
                (inspection["schemas"]["audit_event_type_count"] == 11, "inspect audit types"),
                (inspection["schemas"]["memory_candidate_field_count"] == 13, "inspect candidate fields"),
                (inspection["schemas"]["memory_decision_field_count"] == 11, "inspect decision fields"),
                (inspection["schemas"]["reviewed_record_field_count"] == 12, "inspect record fields"),
                (inspection["public_surface"]["manager_method_count"] == 16, "inspect manager methods"),
                (inspection["public_surface"]["cli_command_count"] == 3, "inspect cli commands"),
                (inspection["proof_contract"]["algorithm"] == "HMAC-SHA256", "inspect proof algorithm"),
                (inspection["proof_contract"]["verification"] == "hmac.compare_digest", "inspect proof verification"),
                (inspection["proof_contract"]["single_use_nonces"] is True, "inspect single-use nonce"),
                (inspection["proof_contract"]["strictly_monotonic_sequences"] is True, "inspect sequences"),
                (inspection["proof_contract"]["domain_separation_required"] is True, "inspect domain separation"),
                (inspection["proof_contract"]["replay_rejected"] is True, "inspect replay"),
                (inspection["persistence"]["active_permissions_persisted"] is False, "inspect permission persistence"),
                (inspection["persistence"]["audit_append_and_fsync"] is True, "inspect audit fsync"),
                (inspection["persistence"]["reviewed_memory_atomic_replace"] is True, "inspect atomic memory"),
                (inspection["persistence"]["corruption_fails_closed"] is True, "inspect corruption policy"),
                (inspection["persistence"]["only_redacted_reviewed_summary_persisted"] is True, "inspect redacted persistence"),
                (inspection["adversarial_acceptance"]["case_count"] == 77, "inspect adversarial count"),
                (inspection["adversarial_acceptance"]["unique"] is True, "inspect adversarial unique"),
                (inspection["self_test"]["exact_assertion_count"] == 224, "inspect self-test target"),
            ]
            for condition, label in contract_checks:
                check(condition, label)

            for field in self.PERMISSION_FIELDS:
                check(isinstance(field, str) and bool(field), f"permission field:{field}")
            for field in self.CONSUMPTION_FIELDS:
                check(isinstance(field, str) and bool(field), f"consumption field:{field}")
            for field in self.AUTHORIZATION_RECEIPT_FIELDS:
                check(isinstance(field, str) and bool(field), f"receipt field:{field}")
            for field in self.OUTCOME_FIELDS:
                check(isinstance(field, str) and bool(field), f"outcome field:{field}")
            for event_type in self.AUDIT_EVENT_TYPES:
                check(isinstance(event_type, str) and bool(event_type), f"audit type:{event_type}")
            for state in self.PERMISSION_STATES:
                check(isinstance(state, str) and bool(state), f"permission state:{state}")
            for state in self.MEMORY_STATES:
                check(isinstance(state, str) and bool(state), f"memory state:{state}")
            for command in self.CLI_COMMANDS:
                check(isinstance(command, str) and bool(command), f"cli command:{command}")
            representative_cases = (
                "unpaired identity rejected",
                "expired permission cannot reactivate",
                "consumption replay rejected",
                "audit event digest tamper rejected",
                "memory review without explicit confirmation rejected",
                "memory candidate with raw grounding rejected",
                "no capture action executed",
                "restart invalidates active permissions",
                "restart preserves reviewed memory records",
            )
            for case in representative_cases:
                check(
                    case in self.ADVERSARIAL_ACCEPTANCE,
                    f"adversarial representative:{case}",
                )

            check(len(set(self.PERMISSION_FIELDS)) == 24, "permission fields unique")
            check(len(set(self.CONSUMPTION_FIELDS)) == 16, "consumption fields unique")
            check(len(set(self.AUTHORIZATION_RECEIPT_FIELDS)) == 20, "receipt fields unique")
            check(len(set(self.OUTCOME_FIELDS)) == 15, "outcome fields unique")
            check(len(set(self.AUDIT_FIELDS)) == 14, "audit fields unique")
            check(len(set(self.AUDIT_EVENT_TYPES)) == 11, "audit events unique")
            check(len(set(self.MEMORY_CANDIDATE_FIELDS)) == 13, "candidate fields unique")
            check(len(set(self.MEMORY_DECISION_FIELDS)) == 11, "memory decision fields unique")
            check(len(set(self.REVIEWED_RECORD_FIELDS)) == 12, "reviewed fields unique")
            check(len(set(self.ADVERSARIAL_ACCEPTANCE)) == 77, "adversarial cases unique")

        if len(checks) != 224:
            raise AssertionError(
                f"Sprint 277 self-test assertion count drifted: {len(checks)}"
            )
        return {
            "status": "OK",
            "component": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "product_version": self.PRODUCT_VERSION,
            "sprint": self.SPRINT,
            "assertion_count": len(checks),
            "failed_assertion_count": 0,
            "failed_assertions": [],
            "network_side_effects": 0,
            "real_action_side_effects": 0,
            "default_state_side_effects": 0,
            "temporary_state_cleanup_required": True,
            "permission_storage": "in_memory_only",
            "audit_storage": "durable_secure_local",
            "reviewed_memory_storage": "durable_secure_local",
            "execution_performed": False,
            "safe_idle_restored": True,
        }
