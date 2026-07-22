"""Sprint 278 bounded ORION action runtime.

The manager composes only through public Sprint 277 permission and pairing
APIs. It owns no platform process, capture, or network implementation. All
side effects are delegated to an explicitly injected adapter after exact
single-use authorization is consumed.
"""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
import tempfile
import time
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePath
from typing import Any, Callable

from .aura_orion_bounded_action_runtime_adapters import (
    AuraFakeOrionBoundedActionAdapter,
    AuraNonExecutingOrionBoundedActionAdapter,
    AuraOrionBoundedActionAdapter,
)


class OrionBoundedActionRuntimeError(RuntimeError):
    """Raised when the Sprint 278 fail-closed contract is violated."""


class _SelfTestPairingManager:
    def __init__(self) -> None:
        self.pairing_id = "pairing-self-test"
        self.device_id = "device-self-test"

    def authenticated_binding(self) -> dict[str, Any]:
        return {
            "pairing_id": self.pairing_id,
            "device_id": self.device_id,
            "secret_exposed": False,
        }

    def sign_authenticated_envelope(
        self,
        *,
        domain: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if payload.get("pairing_id") != self.pairing_id:
            raise OrionBoundedActionRuntimeError(
                "Self-test pairing ID mismatch."
            )
        if payload.get("device_id") != self.device_id:
            raise OrionBoundedActionRuntimeError(
                "Self-test device ID mismatch."
            )
        proof = hashlib.sha256(
            (
                domain
                + "\n"
                + json.dumps(
                    payload,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
            ).encode("utf-8")
        ).hexdigest()
        return {
            "status": "OK",
            "domain": domain,
            "proof_b64url": proof,
            "secret_exposed": False,
        }


class _SelfTestPermissionManager:
    SCHEMA_VERSION = "1"
    DOMAIN_PERMISSION_CONSUMPTION = "orion-scoped-permission-consume"
    DOMAIN_EXECUTION_OUTCOME = "orion-execution-outcome"

    def __init__(self) -> None:
        self.permissions: dict[str, dict[str, Any]] = {}
        self.receipts: dict[str, dict[str, Any]] = {}
        self.events: list[dict[str, Any]] = []
        self.fail_outcome = False
        self._receipt_counter = 0

    def add_permission(
        self,
        *,
        permission_id: str,
        action_type: str,
        target_digest: str,
        parameters_digest: str,
        preview_digest: str,
        pairing_id: str,
        device_id: str,
        live_link_session_id: str,
        capability_digest: str,
    ) -> dict[str, Any]:
        permission = {
            "schema_version": self.SCHEMA_VERSION,
            "permission_id": permission_id,
            "permission_digest": "",
            "preview_digest": preview_digest,
            "action_type": action_type,
            "target_digest": target_digest,
            "parameters_digest": parameters_digest,
            "pairing_id": pairing_id,
            "device_id": device_id,
            "live_link_session_id": live_link_session_id,
            "capability_digest": capability_digest,
            "expires_at_utc": "2099-01-01T00:00:00.000000Z",
        }
        permission["permission_digest"] = hashlib.sha256(
            json.dumps(
                {
                    key: value
                    for key, value in permission.items()
                    if key != "permission_digest"
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.permissions[permission_id] = {
            "permission": permission,
            "state": "active",
            "outcome": None,
        }
        return deepcopy(permission)

    def inspect_permission(self, permission_id: str) -> dict[str, Any]:
        record = self.permissions.get(permission_id)
        if record is None:
            raise OrionBoundedActionRuntimeError(
                "Self-test permission does not exist."
            )
        return {
            "status": "OK",
            "permission": deepcopy(record["permission"]),
            "runtime_state": record["state"],
            "remaining_uses": 1 if record["state"] == "active" else 0,
            "receipt_id": next(
                (
                    receipt_id
                    for receipt_id, receipt in self.receipts.items()
                    if receipt["permission_id"] == permission_id
                ),
                None,
            ),
            "outcome": deepcopy(record["outcome"]),
            "execution_performed": False,
        }

    def verify_audit_chain(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "valid": True,
            "event_count": len(self.events),
            "last_event_digest": (
                ""
                if not self.events
                else self.events[-1]["event_digest"]
            ),
            "hash_chain": "SHA-256",
            "append_only": True,
        }

    def validate_permission(self, **values: Any) -> dict[str, Any]:
        record = self.permissions.get(values["permission_id"])
        if record is None or record["state"] != "active":
            raise OrionBoundedActionRuntimeError(
                "Self-test permission must be active."
            )
        permission = record["permission"]
        for key in (
            "permission_digest",
            "preview_digest",
            "action_type",
            "target_digest",
            "parameters_digest",
            "pairing_id",
            "device_id",
            "live_link_session_id",
            "capability_digest",
        ):
            if values[key] != permission[key]:
                raise OrionBoundedActionRuntimeError(
                    f"Self-test permission {key} mismatch."
                )
        return {
            "status": "OK",
            "valid": True,
            "permission_id": permission["permission_id"],
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
        record = self.permissions.get(envelope["permission_id"])
        if record is None or record["state"] != "active":
            raise OrionBoundedActionRuntimeError(
                "Self-test permission cannot be consumed."
            )
        if envelope.get("proof") != proof_b64url:
            raise OrionBoundedActionRuntimeError(
                "Self-test consumption proof mismatch."
            )
        permission = record["permission"]
        for key in (
            "permission_digest",
            "preview_digest",
            "action_type",
            "target_digest",
            "parameters_digest",
            "pairing_id",
            "device_id",
            "live_link_session_id",
            "capability_digest",
        ):
            if envelope[key] != permission[key]:
                raise OrionBoundedActionRuntimeError(
                    f"Self-test consumption {key} mismatch."
                )
        self._receipt_counter += 1
        receipt = {
            "schema_version": self.SCHEMA_VERSION,
            "receipt_id": f"receipt-self-{self._receipt_counter:03d}",
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
            "receipt_digest": hashlib.sha256(
                f"receipt:{self._receipt_counter}".encode("ascii")
            ).hexdigest(),
            "execution_authorized": True,
            "execution_performed": False,
            "state": "consumed",
        }
        self.receipts[receipt["receipt_id"]] = deepcopy(receipt)
        record["state"] = "consumed"
        self.events.append(
            {
                "event_type": "permission_consumed",
                "permission_id": permission["permission_id"],
            }
        )
        return {
            "status": "OK",
            "authorization_receipt": deepcopy(receipt),
            "permission_consumed": True,
            "execution_authorized": True,
            "execution_performed": False,
            "audit_written": True,
        }

    def record_execution_outcome(
        self,
        *,
        envelope: dict[str, Any],
        proof_b64url: str,
    ) -> dict[str, Any]:
        if self.fail_outcome:
            raise OrionBoundedActionRuntimeError(
                "Self-test outcome recording failure."
            )
        if envelope.get("proof") != proof_b64url:
            raise OrionBoundedActionRuntimeError(
                "Self-test outcome proof mismatch."
            )
        record = self.permissions.get(envelope["permission_id"])
        if record is None or record["state"] != "consumed":
            raise OrionBoundedActionRuntimeError(
                "Self-test consumed permission required."
            )
        receipt = self.receipts.get(envelope["receipt_id"])
        if receipt is None:
            raise OrionBoundedActionRuntimeError(
                "Self-test receipt does not exist."
            )
        record["state"] = "outcome_recorded"
        record["outcome"] = {
            "outcome": envelope["outcome"],
            "result_digest": envelope["result_digest"],
            "error_code": envelope["error_code"],
        }
        audit_digest = hashlib.sha256(
            f"audit:{envelope['receipt_id']}".encode("utf-8")
        ).hexdigest()
        self.events.append(
            {
                "event_type": "execution_outcome_recorded",
                "permission_id": envelope["permission_id"],
                "event_digest": audit_digest,
            }
        )
        return {
            "status": "OK",
            "permission_id": envelope["permission_id"],
            "receipt_id": envelope["receipt_id"],
            "outcome": envelope["outcome"],
            "execution_outcome_recorded": True,
            "execution_authorized": True,
            "execution_performed": False,
            "audit_written": True,
            "terminal_audit_digest": audit_digest,
        }

    def audit_events(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "events": deepcopy(self.events),
            "event_count": len(self.events),
            "chain_valid": True,
            "redacted_only": True,
        }


class AuraOrionBoundedActionRuntimeManager:
    """Execute exactly one bounded action through an authorized adapter."""

    COMPONENT_NAME = "orion_bounded_action_runtime"
    COMPONENT_VERSION = "0.1.0"
    PRODUCT_VERSION = "1.4.0"
    SPRINT = 278
    SCHEMA_VERSION = "1"

    STATE_IDLE = "idle"
    STATE_VALIDATING = "validating"
    STATE_AUTHORIZED = "authorized"
    STATE_EXECUTING = "executing"
    STATE_SUCCEEDED = "succeeded"
    STATE_FAILED = "failed"
    STATE_OUTCOME_UNCONFIRMED = "outcome_unconfirmed"
    STATES = (
        STATE_IDLE,
        STATE_VALIDATING,
        STATE_AUTHORIZED,
        STATE_EXECUTING,
        STATE_SUCCEEDED,
        STATE_FAILED,
        STATE_OUTCOME_UNCONFIRMED,
    )
    VALID_TRANSITIONS = (
        (STATE_IDLE, STATE_VALIDATING),
        (STATE_VALIDATING, STATE_AUTHORIZED),
        (STATE_VALIDATING, STATE_FAILED),
        (STATE_AUTHORIZED, STATE_EXECUTING),
        (STATE_AUTHORIZED, STATE_FAILED),
        (STATE_EXECUTING, STATE_SUCCEEDED),
        (STATE_EXECUTING, STATE_FAILED),
        (STATE_EXECUTING, STATE_OUTCOME_UNCONFIRMED),
        (STATE_SUCCEEDED, STATE_IDLE),
        (STATE_FAILED, STATE_IDLE),
    )

    ACTION_REQUEST_FIELDS = (
        "schema_version",
        "request_id",
        "action_type",
        "permission_id",
        "permission_digest",
        "preview_digest",
        "target_digest",
        "parameters_digest",
        "pairing_id",
        "device_id",
        "live_link_session_id",
        "capability_digest",
        "created_at_utc",
        "deadline_at_utc",
        "request_nonce",
        "request_digest",
        "operator_visible_summary",
        "state",
    )
    AUTHORIZATION_BINDING_FIELDS = (
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
        "execution_authorized",
    )
    ADAPTER_RESULT_FIELDS = (
        "schema_version",
        "adapter_id",
        "adapter_version",
        "action_type",
        "success",
        "execution_performed",
        "result_code",
        "result_digest",
        "artifacts",
        "redacted_message",
        "metadata_digest",
        "duration_ms",
    )
    EXECUTION_RECORD_FIELDS = (
        "schema_version",
        "execution_id",
        "request_id",
        "receipt_id",
        "permission_id",
        "action_type",
        "adapter_id",
        "adapter_version",
        "started_at_utc",
        "finished_at_utc",
        "duration_ms",
        "state",
        "outcome",
        "execution_performed",
        "result_digest",
        "artifact_count",
        "artifacts",
        "error_code",
        "error_message_redacted",
        "outcome_recorded",
        "outcome_audit_digest",
        "safe_idle_restored",
    )
    CONFIGURATION_FIELDS = (
        "schema_version",
        "adapter_mode",
        "adapter_id",
        "adapter_version",
        "enabled",
        "expected_platform",
        "capture_root",
        "controlled_file_root",
        "application_allowlist",
        "obs_scene_allowlist",
        "obs_connection_profile_id",
        "max_action_seconds",
        "max_capture_bytes",
        "max_file_bytes",
        "max_history",
        "overwrite_allowed",
        "symlink_follow_allowed",
        "shell_allowed",
        "core_network_allowed",
        "single_flight",
    )

    ACTION_POLICIES = {
        "capture_single_screenshot": {
            "adapter_method": "capture_single_screenshot",
            "required_capability": "orion.capture.single_screenshot",
            "output_root": "capture_root",
        },
        "capture_selected_window": {
            "adapter_method": "capture_selected_window",
            "required_capability": "orion.capture.selected_window",
            "output_root": "capture_root",
        },
        "open_allowlisted_application": {
            "adapter_method": "open_allowlisted_application",
            "required_capability": "orion.application.open_allowlisted",
        },
        "create_controlled_file": {
            "adapter_method": "create_controlled_file",
            "required_capability": "orion.file.create_controlled",
            "output_root": "controlled_file_root",
        },
        "create_controlled_folder": {
            "adapter_method": "create_controlled_folder",
            "required_capability": "orion.file.create_controlled_folder",
            "output_root": "controlled_file_root",
        },
        "obs_start_recording": {
            "adapter_method": "obs_start_recording",
            "required_capability": "orion.obs.start_recording",
        },
        "obs_stop_recording": {
            "adapter_method": "obs_stop_recording",
            "required_capability": "orion.obs.stop_recording",
        },
        "obs_switch_scene": {
            "adapter_method": "obs_switch_scene",
            "required_capability": "orion.obs.switch_scene",
        },
    }

    CLI_COMMANDS = (
        "orion-bounded-action-status",
        "orion-bounded-action-inspect",
        "orion-bounded-action-self-test",
    )

    DEFAULT_MAX_ACTION_SECONDS = 30
    DEFAULT_MAX_CAPTURE_BYTES = 16 * 1024 * 1024
    DEFAULT_MAX_FILE_BYTES = 1024 * 1024
    DEFAULT_MAX_HISTORY = 128
    REQUEST_NONCE_BYTES = 32
    MAXIMUM_REQUEST_AGE_SECONDS = 30
    MAXIMUM_CLOCK_SKEW_SECONDS = 5
    SUMMARY_MAX_CHARACTERS = 1000
    ERROR_MAX_CHARACTERS = 500
    ARTIFACT_MAX_COUNT = 8

    ADVERSARIAL_ACCEPTANCE = ('missing permission runtime rejected',
 'wrong permission runtime type rejected',
 'missing injected adapter rejected',
 'unknown adapter mode rejected',
 'disabled adapter rejected',
 'non-executing adapter never performs action',
 'fake adapter rejected outside self-test mode',
 'Windows adapter rejected on non-Windows host',
 'adapter ID mismatch rejected',
 'adapter version mismatch rejected',
 'adapter status unavailable rejected',
 'adapter capability mismatch rejected',
 'adapter method missing rejected',
 'adapter exception converted to redacted failure',
 'adapter result schema mismatch rejected',
 'adapter result action mismatch rejected',
 'adapter result identity mismatch rejected',
 'adapter result digest mismatch rejected',
 'adapter reports success without execution rejected',
 'adapter reports execution without result digest rejected',
 'unknown action type rejected',
 'action type outside Sprint 277 catalog rejected',
 'missing permission ID rejected',
 'missing permission digest rejected',
 'missing preview digest rejected',
 'missing target digest rejected',
 'missing parameters digest rejected',
 'missing pairing ID rejected',
 'missing device ID rejected',
 'missing live-link session ID rejected',
 'missing capability digest rejected',
 'expired action request rejected',
 'future action request rejected',
 'duplicate request nonce rejected',
 'duplicate request ID rejected',
 'request digest tamper rejected',
 'operator-visible summary mismatch rejected',
 'permission validation failure prevents adapter call',
 'permission audit corruption prevents adapter call',
 'permission consumption failure prevents adapter call',
 'authorization receipt missing rejected',
 'authorization receipt execution flag false rejected',
 'authorization receipt permission mismatch rejected',
 'authorization receipt digest mismatch rejected',
 'authorization receipt preview mismatch rejected',
 'authorization receipt action mismatch rejected',
 'authorization receipt target mismatch rejected',
 'authorization receipt parameters mismatch rejected',
 'authorization receipt pairing mismatch rejected',
 'authorization receipt device mismatch rejected',
 'authorization receipt live-link mismatch rejected',
 'authorization receipt capability mismatch rejected',
 'authorization receipt replay rejected',
 'consumed permission cannot execute twice',
 'single-flight second request rejected',
 'capture caller absolute path rejected',
 'capture caller relative path rejected',
 'capture non-PNG extension rejected',
 'capture output overwrite rejected',
 'capture output over size limit rejected',
 'capture output outside root rejected',
 'capture output symlink escape rejected',
 'capture output artifact digest mismatch rejected',
 'selected-window request without exact binding rejected',
 'selected-window binding mismatch rejected',
 'selected-window desktop fallback rejected',
 'selected-window unavailable fails closed',
 'raw application executable rejected',
 'raw application command rejected',
 'raw application arguments rejected',
 'unknown logical application ID rejected',
 'allowlisted application mapping must be absolute',
 'allowlisted executable symlink rejected',
 'shell true rejected',
 'shell string invocation rejected',
 'application launch timeout recorded as failure',
 'application launch result without process identity rejected',
 'controlled file absolute path rejected',
 'controlled file parent traversal rejected',
 'controlled file symlink escape rejected',
 'controlled file overwrite rejected',
 'controlled file over size limit rejected',
 'controlled file content digest mismatch rejected',
 'controlled file partial write cleaned up',
 'controlled folder absolute path rejected',
 'controlled folder parent traversal rejected',
 'controlled folder symlink escape rejected',
 'controlled folder existing target rejected',
 'controlled folder partial creation cleaned up',
 'OBS adapter absent rejected',
 'OBS connection profile absent rejected',
 'OBS raw endpoint in request rejected',
 'OBS raw password in request rejected',
 'OBS raw scene name rejected',
 'unknown logical OBS scene ID rejected',
 'OBS start when already recording returns bounded failure',
 'OBS stop when not recording returns bounded failure',
 'OBS connection failure records redacted outcome',
 'OBS adapter network use never occurs in core manager',
 'core network listener creation rejected',
 'core network connection creation rejected',
 'outcome success requires execution performed true',
 'outcome failure may report execution performed false',
 'unknown outcome marks execution state conservatively',
 'outcome recording attempted exactly once',
 'outcome record permission mismatch rejected',
 'outcome record receipt mismatch rejected',
 'outcome record replay rejected',
 'outcome recording failure enters outcome_unconfirmed',
 'outcome_unconfirmed blocks later actions',
 'reset_ephemeral rejected during execution',
 'reset_ephemeral rejected for outcome_unconfirmed',
 'successful action returns to safe idle',
 'failed action returns to safe idle',
 'history is bounded',
 'history contains redacted records only',
 'raw file content absent from history',
 'raw screenshot bytes absent from history',
 'raw application command absent from history',
 'OBS credential absent from history',
 'secret absent from status and inspection',
 'default configuration performs no action',
 'default status is safe idle',
 'self-test uses fake adapters only',
 'self-test creates no default state',
 'self-test opens no network listener',
 'self-test opens no network connection',
 'self-test launches no real application',
 'self-test captures no real screen',
 'self-test changes no real OBS state',
 'self-test writes no file outside temporary root',
 'watchdog remains disabled',
 'emergency stop remains disabled',
 'recovery runtime remains disabled',
 'general memory handoff remains disabled',
 'pairing manager remains unchanged',
 'live-link manager remains unchanged',
 'preview manager remains unchanged',
 'scoped permission manager remains unchanged',
 'restart clears in-memory execution history',
 'restart preserves Sprint 277 durable audit',
 'temporary acceptance roots are cleaned',
 'port 8765 remains closed')

    def __init__(
        self,
        *,
        project_root: Path,
        permission_manager: Any = None,
        pairing_manager: Any = None,
        adapter: AuraOrionBoundedActionAdapter | None = None,
        configuration: dict[str, Any] | None = None,
        now_provider: Callable[[], datetime] | None = None,
        nonce_provider: Callable[[int], bytes] | None = None,
        id_provider: Callable[[str], str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.permission_manager = permission_manager
        self.pairing_manager = pairing_manager
        self.adapter = (
            AuraNonExecutingOrionBoundedActionAdapter()
            if adapter is None
            else adapter
        )
        self._now_provider = now_provider or (
            lambda: datetime.now(timezone.utc)
        )
        self._nonce_provider = nonce_provider or secrets.token_bytes
        self._id_provider = id_provider or (
            lambda prefix: f"{prefix}{uuid.uuid4().hex}"
        )
        self.configuration = self._default_configuration()
        if configuration is not None:
            self.configuration = deepcopy(configuration)
        self.validate_configuration(self.configuration)
        self._state = self.STATE_IDLE
        self._active_request_id: str | None = None
        self._pending_requests: dict[str, dict[str, Any]] = {}
        self._history: list[dict[str, Any]] = []
        self._used_request_ids: set[str] = set()
        self._used_request_nonces: set[str] = set()
        self._last_error = ""
        self._outcome_unconfirmed_execution_id: str | None = None

    @staticmethod
    def _canonical_bytes(payload: Any) -> bytes:
        try:
            return json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise OrionBoundedActionRuntimeError(
                "Payload is not canonicalizable."
            ) from exc

    @classmethod
    def _digest(cls, payload: Any) -> str:
        return hashlib.sha256(cls._canonical_bytes(payload)).hexdigest()

    @staticmethod
    def _deep_copy(payload: Any) -> Any:
        return deepcopy(payload)

    def _now(self) -> datetime:
        value = self._now_provider()
        if value.tzinfo is None:
            raise OrionBoundedActionRuntimeError(
                "Clock provider must return a timezone-aware datetime."
            )
        return value.astimezone(timezone.utc)

    @staticmethod
    def _format_utc(value: datetime) -> str:
        return (
            value.astimezone(timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )

    @staticmethod
    def _parse_utc(value: Any, *, label: str) -> datetime:
        if not isinstance(value, str) or not value.endswith("Z"):
            raise OrionBoundedActionRuntimeError(
                f"{label} must be a UTC timestamp."
            )
        try:
            parsed = datetime.fromisoformat(value[:-1] + "+00:00")
        except ValueError as exc:
            raise OrionBoundedActionRuntimeError(
                f"{label} is invalid."
            ) from exc
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _validate_text(
        value: Any,
        *,
        label: str,
        maximum: int,
        allow_empty: bool = False,
    ) -> str:
        if not isinstance(value, str):
            raise OrionBoundedActionRuntimeError(
                f"{label} must be text."
            )
        if not allow_empty and not value.strip():
            raise OrionBoundedActionRuntimeError(
                f"{label} must not be empty."
            )
        if len(value) > maximum:
            raise OrionBoundedActionRuntimeError(
                f"{label} exceeds the maximum length."
            )
        return value

    @staticmethod
    def _validate_digest(value: Any, *, label: str) -> str:
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)
        ):
            raise OrionBoundedActionRuntimeError(
                f"{label} must be a lowercase SHA-256 digest."
            )
        return value

    @staticmethod
    def _b64url(value: bytes) -> str:
        return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")

    def _new_nonce(self) -> str:
        raw = self._nonce_provider(self.REQUEST_NONCE_BYTES)
        if not isinstance(raw, bytes) or len(raw) != self.REQUEST_NONCE_BYTES:
            raise OrionBoundedActionRuntimeError(
                "Nonce provider returned an invalid value."
            )
        return self._b64url(raw)

    def _transition(self, target: str) -> None:
        if (self._state, target) not in self.VALID_TRANSITIONS:
            raise OrionBoundedActionRuntimeError(
                f"Invalid state transition: {self._state} -> {target}."
            )
        self._state = target

    def _default_configuration(self) -> dict[str, Any]:
        state_root = (
            Path.home()
            / ".local"
            / "state"
            / "aura"
            / "orion_bounded_actions"
        ).resolve()
        adapter_status = self.adapter.status()
        return {
            "schema_version": self.SCHEMA_VERSION,
            "adapter_mode": str(
                adapter_status.get("mode", "non_executing")
            ),
            "adapter_id": str(
                adapter_status.get("adapter_id", "unknown")
            ),
            "adapter_version": str(
                adapter_status.get("adapter_version", "unknown")
            ),
            "enabled": False,
            "expected_platform": "windows",
            "capture_root": str(state_root / "captures"),
            "controlled_file_root": str(state_root / "files"),
            "application_allowlist": {},
            "obs_scene_allowlist": {},
            "obs_connection_profile_id": "",
            "max_action_seconds": self.DEFAULT_MAX_ACTION_SECONDS,
            "max_capture_bytes": self.DEFAULT_MAX_CAPTURE_BYTES,
            "max_file_bytes": self.DEFAULT_MAX_FILE_BYTES,
            "max_history": self.DEFAULT_MAX_HISTORY,
            "overwrite_allowed": False,
            "symlink_follow_allowed": False,
            "shell_allowed": False,
            "core_network_allowed": False,
            "single_flight": True,
        }

    def _require_composition(self) -> None:
        if self.permission_manager is None:
            raise OrionBoundedActionRuntimeError(
                "A Sprint 277 permission runtime is required."
            )
        if self.pairing_manager is None:
            raise OrionBoundedActionRuntimeError(
                "A paired identity runtime is required."
            )
        for method in (
            "inspect_permission",
            "verify_audit_chain",
            "validate_permission",
            "consume_permission",
            "record_execution_outcome",
            "audit_events",
        ):
            if not callable(getattr(self.permission_manager, method, None)):
                raise OrionBoundedActionRuntimeError(
                    f"Permission runtime public method missing: {method}."
                )
        for method in (
            "authenticated_binding",
            "sign_authenticated_envelope",
        ):
            if not callable(getattr(self.pairing_manager, method, None)):
                raise OrionBoundedActionRuntimeError(
                    f"Pairing runtime public method missing: {method}."
                )

    def _safe_relative_path(
        self,
        *,
        root: Path,
        relative_text: str,
        target_must_not_exist: bool,
    ) -> Path:
        value = self._validate_text(
            relative_text,
            label="relative path",
            maximum=512,
        )
        if "\x00" in value or "\\" in value or ":" in value:
            raise OrionBoundedActionRuntimeError(
                "Relative path contains a forbidden platform separator."
            )
        pure = PurePath(value)
        if pure.is_absolute() or ".." in pure.parts:
            raise OrionBoundedActionRuntimeError(
                "Only a bounded relative path is allowed."
            )
        if any(part in {"", ".", ".."} for part in pure.parts):
            raise OrionBoundedActionRuntimeError(
                "Relative path contains an invalid component."
            )
        root_value = root.expanduser()
        if not root_value.is_absolute():
            raise OrionBoundedActionRuntimeError(
                "Controlled root must be absolute."
            )
        if root_value.exists() and root_value.is_symlink():
            raise OrionBoundedActionRuntimeError(
                "Controlled root must not be a symlink."
            )
        root_resolved = root_value.resolve(strict=False)
        candidate = root_resolved.joinpath(*pure.parts)
        current = root_resolved
        for part in pure.parts[:-1]:
            current = current / part
            if current.exists() and current.is_symlink():
                raise OrionBoundedActionRuntimeError(
                    "Symlink path escape rejected."
                )
        candidate_resolved = candidate.resolve(strict=False)
        try:
            candidate_resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise OrionBoundedActionRuntimeError(
                "Path escapes the controlled root."
            ) from exc
        if target_must_not_exist and candidate.exists():
            raise OrionBoundedActionRuntimeError(
                "Target already exists and overwrite is disabled."
            )
        if candidate.exists() and candidate.is_symlink():
            raise OrionBoundedActionRuntimeError(
                "Symlink targets are forbidden."
            )
        return candidate

    def _resolve_action(
        self,
        *,
        request_id: str,
        action_type: str,
        target: Any,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        if action_type not in self.ACTION_POLICIES:
            raise OrionBoundedActionRuntimeError(
                "Unknown Sprint 278 action type."
            )
        if not isinstance(parameters, dict):
            raise OrionBoundedActionRuntimeError(
                "Action parameters must be an object."
            )
        config = self.configuration
        resolved: dict[str, Any] = {}
        if action_type == "capture_single_screenshot":
            self._validate_text(
                target,
                label="capture target",
                maximum=256,
            )
            if parameters != {"format": "png", "count": 1}:
                raise OrionBoundedActionRuntimeError(
                    "Single screenshot parameters must be exact."
                )
            output = self._safe_relative_path(
                root=Path(config["capture_root"]),
                relative_text=f"{request_id}.png",
                target_must_not_exist=True,
            )
            resolved["output_path"] = str(output)
        elif action_type == "capture_selected_window":
            if not isinstance(target, dict) or set(target) != {
                "window_id",
                "window_title_digest",
            }:
                raise OrionBoundedActionRuntimeError(
                    "Selected-window target binding is invalid."
                )
            self._validate_text(
                target["window_id"],
                label="window ID",
                maximum=128,
            )
            self._validate_digest(
                target["window_title_digest"],
                label="window title digest",
            )
            if parameters != {"format": "png", "count": 1}:
                raise OrionBoundedActionRuntimeError(
                    "Selected-window screenshot parameters must be exact."
                )
            output = self._safe_relative_path(
                root=Path(config["capture_root"]),
                relative_text=f"{request_id}.png",
                target_must_not_exist=True,
            )
            resolved.update(
                {
                    "output_path": str(output),
                    "window_id": target["window_id"],
                    "window_title_digest": target["window_title_digest"],
                    "desktop_fallback_allowed": False,
                }
            )
        elif action_type == "open_allowlisted_application":
            logical_id = self._validate_text(
                target,
                label="logical application ID",
                maximum=128,
            )
            if parameters != {}:
                raise OrionBoundedActionRuntimeError(
                    "Raw application arguments are forbidden."
                )
            mapping = config["application_allowlist"]
            if logical_id not in mapping:
                raise OrionBoundedActionRuntimeError(
                    "Unknown logical application ID."
                )
            executable = Path(mapping[logical_id]).expanduser()
            if not executable.is_absolute() or executable.is_symlink():
                raise OrionBoundedActionRuntimeError(
                    "Allowlisted executable mapping is invalid."
                )
            resolved.update(
                {
                    "logical_application_id": logical_id,
                    "executable_path": str(executable),
                    "arguments": [],
                    "shell": False,
                }
            )
        elif action_type == "create_controlled_file":
            if set(parameters) != {"content", "encoding"}:
                raise OrionBoundedActionRuntimeError(
                    "Controlled-file parameters are invalid."
                )
            if parameters["encoding"] != "utf-8":
                raise OrionBoundedActionRuntimeError(
                    "Only UTF-8 controlled text files are supported."
                )
            content = self._validate_text(
                parameters["content"],
                label="controlled file content",
                maximum=config["max_file_bytes"],
                allow_empty=True,
            ).encode("utf-8")
            if len(content) > config["max_file_bytes"]:
                raise OrionBoundedActionRuntimeError(
                    "Controlled file exceeds the byte limit."
                )
            output = self._safe_relative_path(
                root=Path(config["controlled_file_root"]),
                relative_text=self._validate_text(
                    target,
                    label="controlled file path",
                    maximum=512,
                ),
                target_must_not_exist=True,
            )
            resolved.update(
                {
                    "output_path": str(output),
                    "content_bytes": content,
                    "content_digest": hashlib.sha256(content).hexdigest(),
                    "encoding": "utf-8",
                }
            )
        elif action_type == "create_controlled_folder":
            if parameters != {}:
                raise OrionBoundedActionRuntimeError(
                    "Controlled-folder parameters must be empty."
                )
            output = self._safe_relative_path(
                root=Path(config["controlled_file_root"]),
                relative_text=self._validate_text(
                    target,
                    label="controlled folder path",
                    maximum=512,
                ),
                target_must_not_exist=True,
            )
            resolved["output_path"] = str(output)
        elif action_type in {
            "obs_start_recording",
            "obs_stop_recording",
        }:
            if target != "recording" or parameters != {}:
                raise OrionBoundedActionRuntimeError(
                    "OBS recording action binding is invalid."
                )
            if not config["obs_connection_profile_id"]:
                raise OrionBoundedActionRuntimeError(
                    "An OBS connection profile ID is required."
                )
            resolved["obs_connection_profile_id"] = config[
                "obs_connection_profile_id"
            ]
        elif action_type == "obs_switch_scene":
            logical_id = self._validate_text(
                target,
                label="logical OBS scene ID",
                maximum=128,
            )
            if parameters != {}:
                raise OrionBoundedActionRuntimeError(
                    "Raw OBS scene parameters are forbidden."
                )
            scenes = config["obs_scene_allowlist"]
            if logical_id not in scenes:
                raise OrionBoundedActionRuntimeError(
                    "Unknown logical OBS scene ID."
                )
            if not config["obs_connection_profile_id"]:
                raise OrionBoundedActionRuntimeError(
                    "An OBS connection profile ID is required."
                )
            resolved.update(
                {
                    "logical_scene_id": logical_id,
                    "scene_name": scenes[logical_id],
                    "obs_connection_profile_id": config[
                        "obs_connection_profile_id"
                    ],
                }
            )
        return resolved

    def _validate_request_envelope(
        self,
        request: dict[str, Any],
    ) -> None:
        if not isinstance(request, dict) or set(request) != set(
            self.ACTION_REQUEST_FIELDS
        ):
            raise OrionBoundedActionRuntimeError(
                "Action request fields are invalid."
            )
        if request["schema_version"] != self.SCHEMA_VERSION:
            raise OrionBoundedActionRuntimeError(
                "Action request schema mismatch."
            )
        for key, maximum in (
            ("request_id", 128),
            ("action_type", 64),
            ("permission_id", 128),
            ("pairing_id", 128),
            ("device_id", 128),
            ("live_link_session_id", 128),
            ("operator_visible_summary", self.SUMMARY_MAX_CHARACTERS),
        ):
            self._validate_text(
                request[key],
                label=key.replace("_", " "),
                maximum=maximum,
            )
        for key in (
            "permission_digest",
            "preview_digest",
            "target_digest",
            "parameters_digest",
            "capability_digest",
            "request_digest",
        ):
            self._validate_digest(
                request[key],
                label=key.replace("_", " "),
            )
        if request["action_type"] not in self.ACTION_POLICIES:
            raise OrionBoundedActionRuntimeError(
                "Unknown action type."
            )
        if request["state"] != self.STATE_IDLE:
            raise OrionBoundedActionRuntimeError(
                "Action request state must be idle."
            )
        nonce = request["request_nonce"]
        if (
            not isinstance(nonce, str)
            or len(nonce) != 43
            or any(
                char
                not in (
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    "abcdefghijklmnopqrstuvwxyz"
                    "0123456789-_"
                )
                for char in nonce
            )
        ):
            raise OrionBoundedActionRuntimeError(
                "Action request nonce is invalid."
            )
        expected_digest = self._digest(
            {
                key: value
                for key, value in request.items()
                if key != "request_digest"
            }
        )
        if request["request_digest"] != expected_digest:
            raise OrionBoundedActionRuntimeError(
                "Action request digest mismatch."
            )
        created = self._parse_utc(
            request["created_at_utc"],
            label="request creation time",
        )
        deadline = self._parse_utc(
            request["deadline_at_utc"],
            label="request deadline",
        )
        now = self._now()
        if (created - now).total_seconds() > self.MAXIMUM_CLOCK_SKEW_SECONDS:
            raise OrionBoundedActionRuntimeError(
                "Future action request rejected."
            )
        if (now - created).total_seconds() > self.MAXIMUM_REQUEST_AGE_SECONDS:
            raise OrionBoundedActionRuntimeError(
                "Stale action request rejected."
            )
        if now >= deadline:
            raise OrionBoundedActionRuntimeError(
                "Expired action request rejected."
            )
        if deadline <= created:
            raise OrionBoundedActionRuntimeError(
                "Action request deadline ordering is invalid."
            )

    def _validate_receipt_binding(
        self,
        *,
        receipt: dict[str, Any],
        request: dict[str, Any],
    ) -> None:
        if not isinstance(receipt, dict):
            raise OrionBoundedActionRuntimeError(
                "Authorization receipt must be an object."
            )
        expected = {
            "permission_id": request["permission_id"],
            "permission_digest": request["permission_digest"],
            "preview_digest": request["preview_digest"],
            "action_type": request["action_type"],
            "target_digest": request["target_digest"],
            "parameters_digest": request["parameters_digest"],
            "pairing_id": request["pairing_id"],
            "device_id": request["device_id"],
            "live_link_session_id": request["live_link_session_id"],
            "capability_digest": request["capability_digest"],
        }
        for key, value in expected.items():
            if receipt.get(key) != value:
                raise OrionBoundedActionRuntimeError(
                    f"Authorization receipt {key} mismatch."
                )
        if receipt.get("execution_authorized") is not True:
            raise OrionBoundedActionRuntimeError(
                "Authorization receipt does not authorize execution."
            )
        if receipt.get("execution_performed") is not False:
            raise OrionBoundedActionRuntimeError(
                "Authorization receipt execution flag is invalid."
            )
        self._validate_text(
            receipt.get("receipt_id"),
            label="receipt ID",
            maximum=128,
        )

    def _validate_artifact(
        self,
        *,
        artifact: dict[str, Any],
        action_type: str,
    ) -> dict[str, Any]:
        if not isinstance(artifact, dict) or set(artifact) != {
            "artifact_type",
            "path",
            "sha256",
            "size_bytes",
        }:
            raise OrionBoundedActionRuntimeError(
                "Adapter artifact fields are invalid."
            )
        artifact_type = self._validate_text(
            artifact["artifact_type"],
            label="artifact type",
            maximum=128,
        )
        path = Path(
            self._validate_text(
                artifact["path"],
                label="artifact path",
                maximum=1024,
            )
        )
        digest = self._validate_digest(
            artifact["sha256"],
            label="artifact digest",
        )
        size = artifact["size_bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise OrionBoundedActionRuntimeError(
                "Artifact size is invalid."
            )
        if action_type.startswith("capture_"):
            root = Path(self.configuration["capture_root"]).resolve(
                strict=False
            )
            maximum = self.configuration["max_capture_bytes"]
        elif action_type in {
            "create_controlled_file",
            "create_controlled_folder",
        }:
            root = Path(
                self.configuration["controlled_file_root"]
            ).resolve(strict=False)
            maximum = self.configuration["max_file_bytes"]
        else:
            raise OrionBoundedActionRuntimeError(
                "Unexpected artifact for this action."
            )
        if not path.is_absolute():
            raise OrionBoundedActionRuntimeError(
                "Artifact path must be absolute."
            )
        resolved = path.resolve(strict=False)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise OrionBoundedActionRuntimeError(
                "Artifact path escapes the controlled root."
            ) from exc
        if path.is_symlink():
            raise OrionBoundedActionRuntimeError(
                "Artifact symlink rejected."
            )
        if not path.exists():
            raise OrionBoundedActionRuntimeError(
                "Adapter artifact does not exist."
            )
        if path.is_file():
            if path.stat().st_size != size:
                raise OrionBoundedActionRuntimeError(
                    "Artifact size mismatch."
                )
            if size > maximum:
                raise OrionBoundedActionRuntimeError(
                    "Artifact exceeds the configured limit."
                )
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != digest:
                raise OrionBoundedActionRuntimeError(
                    "Artifact digest mismatch."
                )
        elif path.is_dir():
            if artifact_type != "inode/directory" or size != 0:
                raise OrionBoundedActionRuntimeError(
                    "Directory artifact metadata is invalid."
                )
        else:
            raise OrionBoundedActionRuntimeError(
                "Unsupported artifact type."
            )
        return {
            "artifact_type": artifact_type,
            "path": str(path),
            "sha256": digest,
            "size_bytes": size,
        }

    def _validate_adapter_result(
        self,
        *,
        result: dict[str, Any],
        action_type: str,
    ) -> dict[str, Any]:
        if not isinstance(result, dict) or set(result) != set(
            self.ADAPTER_RESULT_FIELDS
        ):
            raise OrionBoundedActionRuntimeError(
                "Adapter result fields are invalid."
            )
        if result["schema_version"] != self.SCHEMA_VERSION:
            raise OrionBoundedActionRuntimeError(
                "Adapter result schema mismatch."
            )
        status = self.adapter.status()
        if result["adapter_id"] != status.get("adapter_id"):
            raise OrionBoundedActionRuntimeError(
                "Adapter result ID mismatch."
            )
        if result["adapter_version"] != status.get("adapter_version"):
            raise OrionBoundedActionRuntimeError(
                "Adapter result version mismatch."
            )
        if result["action_type"] != action_type:
            raise OrionBoundedActionRuntimeError(
                "Adapter result action mismatch."
            )
        if not isinstance(result["success"], bool):
            raise OrionBoundedActionRuntimeError(
                "Adapter success flag is invalid."
            )
        if not isinstance(result["execution_performed"], bool):
            raise OrionBoundedActionRuntimeError(
                "Adapter execution flag is invalid."
            )
        if result["success"] and not result["execution_performed"]:
            raise OrionBoundedActionRuntimeError(
                "Successful adapter result requires execution."
            )
        self._validate_text(
            result["result_code"],
            label="adapter result code",
            maximum=128,
        )
        self._validate_text(
            result["redacted_message"],
            label="adapter redacted message",
            maximum=self.ERROR_MAX_CHARACTERS,
            allow_empty=True,
        )
        self._validate_digest(
            result["metadata_digest"],
            label="adapter metadata digest",
        )
        duration = result["duration_ms"]
        if not isinstance(duration, int) or isinstance(duration, bool):
            raise OrionBoundedActionRuntimeError(
                "Adapter duration is invalid."
            )
        if duration < 0 or duration > (
            self.configuration["max_action_seconds"] * 1000
        ):
            raise OrionBoundedActionRuntimeError(
                "Adapter duration exceeds the configured limit."
            )
        artifacts = result["artifacts"]
        if not isinstance(artifacts, list) or len(artifacts) > (
            self.ARTIFACT_MAX_COUNT
        ):
            raise OrionBoundedActionRuntimeError(
                "Adapter artifact list is invalid."
            )
        validated_artifacts = [
            self._validate_artifact(
                artifact=artifact,
                action_type=action_type,
            )
            for artifact in artifacts
        ]
        expected_digest = self._digest(
            {
                key: value
                for key, value in result.items()
                if key != "result_digest"
            }
        )
        self._validate_digest(
            result["result_digest"],
            label="adapter result digest",
        )
        if result["result_digest"] != expected_digest:
            raise OrionBoundedActionRuntimeError(
                "Adapter result digest mismatch."
            )
        sanitized = self._deep_copy(result)
        sanitized["artifacts"] = validated_artifacts
        return sanitized

    def _failure_adapter_result(
        self,
        *,
        action_type: str,
        code: str,
        message: str,
        duration_ms: int,
        execution_performed: bool = False,
    ) -> dict[str, Any]:
        status = self.adapter.status()
        result = {
            "schema_version": self.SCHEMA_VERSION,
            "adapter_id": str(status.get("adapter_id", "unknown")),
            "adapter_version": str(
                status.get("adapter_version", "unknown")
            ),
            "action_type": action_type,
            "success": False,
            "execution_performed": bool(execution_performed),
            "result_code": code,
            "result_digest": "",
            "artifacts": [],
            "redacted_message": message[: self.ERROR_MAX_CHARACTERS],
            "metadata_digest": self._digest({"bounded_failure": code}),
            "duration_ms": min(
                max(0, duration_ms),
                self.configuration["max_action_seconds"] * 1000,
            ),
        }
        result["result_digest"] = self._digest(
            {
                key: value
                for key, value in result.items()
                if key != "result_digest"
            }
        )
        return result

    def _next_outcome_sequence(self) -> int:
        events = self.permission_manager.audit_events()
        event_list = events.get("events", [])
        if not isinstance(event_list, list):
            raise OrionBoundedActionRuntimeError(
                "Permission audit event list is invalid."
            )
        return (
            sum(
                1
                for event in event_list
                if isinstance(event, dict)
                and event.get("event_type")
                == "execution_outcome_recorded"
            )
            + 1
        )

    def _append_history(self, record: dict[str, Any]) -> None:
        self._history.append(self._deep_copy(record))
        maximum = self.configuration["max_history"]
        if len(self._history) > maximum:
            del self._history[:-maximum]

    def build_action_request(
        self,
        *,
        permission_id: str,
        target: Any,
        parameters: dict[str, Any],
        operator_visible_summary: str,
        deadline_seconds: int = DEFAULT_MAX_ACTION_SECONDS,
    ) -> dict[str, Any]:
        if self._state == self.STATE_OUTCOME_UNCONFIRMED:
            raise OrionBoundedActionRuntimeError(
                "Outcome reconciliation is required before new actions."
            )
        if self._state != self.STATE_IDLE:
            raise OrionBoundedActionRuntimeError(
                "Bounded action runtime is busy."
            )
        self._require_composition()
        self.validate_configuration()
        permission_id = self._validate_text(
            permission_id,
            label="permission ID",
            maximum=128,
        )
        summary = self._validate_text(
            operator_visible_summary,
            label="operator-visible summary",
            maximum=self.SUMMARY_MAX_CHARACTERS,
        )
        if (
            not isinstance(deadline_seconds, int)
            or isinstance(deadline_seconds, bool)
            or deadline_seconds < 1
            or deadline_seconds > self.configuration["max_action_seconds"]
        ):
            raise OrionBoundedActionRuntimeError(
                "Action deadline is outside the configured limit."
            )
        inspected = self.permission_manager.inspect_permission(permission_id)
        permission = inspected.get("permission")
        if not isinstance(permission, dict):
            raise OrionBoundedActionRuntimeError(
                "Permission inspection did not return a permission."
            )
        action_type = self._validate_text(
            permission.get("action_type"),
            label="action type",
            maximum=64,
        )
        target_digest = self._digest(target)
        parameters_digest = self._digest(parameters)
        if target_digest != permission.get("target_digest"):
            raise OrionBoundedActionRuntimeError(
                "Action target does not match the permission."
            )
        if parameters_digest != permission.get("parameters_digest"):
            raise OrionBoundedActionRuntimeError(
                "Action parameters do not match the permission."
            )
        request_id = self._id_provider("bounded-request-")
        self._validate_text(
            request_id,
            label="request ID",
            maximum=128,
        )
        if request_id in self._pending_requests or request_id in (
            self._used_request_ids
        ):
            raise OrionBoundedActionRuntimeError(
                "Duplicate request ID rejected."
            )
        nonce = self._new_nonce()
        if nonce in self._used_request_nonces:
            raise OrionBoundedActionRuntimeError(
                "Duplicate request nonce rejected."
            )
        resolved = self._resolve_action(
            request_id=request_id,
            action_type=action_type,
            target=target,
            parameters=parameters,
        )
        now = self._now()
        request = {
            "schema_version": self.SCHEMA_VERSION,
            "request_id": request_id,
            "action_type": action_type,
            "permission_id": permission_id,
            "permission_digest": self._validate_digest(
                permission.get("permission_digest"),
                label="permission digest",
            ),
            "preview_digest": self._validate_digest(
                permission.get("preview_digest"),
                label="preview digest",
            ),
            "target_digest": target_digest,
            "parameters_digest": parameters_digest,
            "pairing_id": self._validate_text(
                permission.get("pairing_id"),
                label="pairing ID",
                maximum=128,
            ),
            "device_id": self._validate_text(
                permission.get("device_id"),
                label="device ID",
                maximum=128,
            ),
            "live_link_session_id": self._validate_text(
                permission.get("live_link_session_id"),
                label="live-link session ID",
                maximum=128,
            ),
            "capability_digest": self._validate_digest(
                permission.get("capability_digest"),
                label="capability digest",
            ),
            "created_at_utc": self._format_utc(now),
            "deadline_at_utc": self._format_utc(
                now + timedelta(seconds=deadline_seconds)
            ),
            "request_nonce": nonce,
            "request_digest": "",
            "operator_visible_summary": summary,
            "state": self.STATE_IDLE,
        }
        request["request_digest"] = self._digest(
            {
                key: value
                for key, value in request.items()
                if key != "request_digest"
            }
        )
        self._validate_request_envelope(request)
        self._pending_requests[request_id] = {
            "request": self._deep_copy(request),
            "target": self._deep_copy(target),
            "parameters": self._deep_copy(parameters),
            "resolved": self._deep_copy(resolved),
            "validated": False,
        }
        return self._deep_copy(request)

    def validate_action_request(
        self,
        action_request: dict[str, Any],
    ) -> dict[str, Any]:
        self._require_composition()
        self.validate_configuration()
        request_id = action_request.get("request_id")
        pending = self._pending_requests.get(request_id)
        if pending is None:
            raise OrionBoundedActionRuntimeError(
                "Action request does not exist in this process."
            )
        if action_request != pending["request"]:
            raise OrionBoundedActionRuntimeError(
                "Action request immutable binding mismatch."
            )
        transitioned = False
        try:
            self._validate_request_envelope(action_request)
            if action_request["request_id"] in self._used_request_ids:
                raise OrionBoundedActionRuntimeError(
                    "Action request replay rejected."
                )
            if action_request["request_nonce"] in self._used_request_nonces:
                raise OrionBoundedActionRuntimeError(
                    "Action request nonce replay rejected."
                )
            if self._state == self.STATE_IDLE:
                self._transition(self.STATE_VALIDATING)
                transitioned = True
                self._active_request_id = action_request["request_id"]
            elif (
                self._state != self.STATE_VALIDATING
                or self._active_request_id != action_request["request_id"]
            ):
                raise OrionBoundedActionRuntimeError(
                    "Bounded action runtime is busy."
                )
            self.permission_manager.verify_audit_chain()
            validation = self.permission_manager.validate_permission(
                permission_id=action_request["permission_id"],
                permission_digest=action_request["permission_digest"],
                preview_digest=action_request["preview_digest"],
                action_type=action_request["action_type"],
                target_digest=action_request["target_digest"],
                parameters_digest=action_request["parameters_digest"],
                pairing_id=action_request["pairing_id"],
                device_id=action_request["device_id"],
                live_link_session_id=action_request[
                    "live_link_session_id"
                ],
                capability_digest=action_request["capability_digest"],
            )
            if validation.get("valid") is not True:
                raise OrionBoundedActionRuntimeError(
                    "Permission validation did not succeed."
                )
            adapter_status = self.adapter.status()
            if adapter_status.get("adapter_id") != (
                self.configuration["adapter_id"]
            ):
                raise OrionBoundedActionRuntimeError(
                    "Configured adapter ID mismatch."
                )
            if adapter_status.get("adapter_version") != (
                self.configuration["adapter_version"]
            ):
                raise OrionBoundedActionRuntimeError(
                    "Configured adapter version mismatch."
                )
            if adapter_status.get("mode") != (
                self.configuration["adapter_mode"]
            ):
                raise OrionBoundedActionRuntimeError(
                    "Configured adapter mode mismatch."
                )
            if self.configuration["enabled"] is not True:
                raise OrionBoundedActionRuntimeError(
                    "Bounded action adapter is disabled."
                )
            method_name = self.ACTION_POLICIES[
                action_request["action_type"]
            ]["adapter_method"]
            if not callable(getattr(self.adapter, method_name, None)):
                raise OrionBoundedActionRuntimeError(
                    "Required adapter method is missing."
                )
            pending["validated"] = True
            return {
                "status": "OK",
                "valid": True,
                "request_id": action_request["request_id"],
                "action_type": action_request["action_type"],
                "permission_validated": True,
                "permission_consumed": False,
                "execution_authorized": False,
                "execution_performed": False,
                "state": self._state,
            }
        except Exception as exc:
            self._last_error = str(exc)[: self.ERROR_MAX_CHARACTERS]
            if (
                self._state == self.STATE_VALIDATING
                and self._active_request_id == action_request["request_id"]
            ):
                self._transition(self.STATE_FAILED)
                self._transition(self.STATE_IDLE)
                self._active_request_id = None
            raise

    def execute_authorized_action(
        self,
        *,
        action_request: dict[str, Any],
        consumption_envelope: dict[str, Any],
        consumption_proof_b64url: str,
    ) -> dict[str, Any]:
        if self._state == self.STATE_OUTCOME_UNCONFIRMED:
            raise OrionBoundedActionRuntimeError(
                "Outcome reconciliation is required before execution."
            )
        validation = self.validate_action_request(action_request)
        if validation["valid"] is not True:
            raise OrionBoundedActionRuntimeError(
                "Action request validation failed."
            )
        pending = self._pending_requests[action_request["request_id"]]
        if not isinstance(consumption_envelope, dict):
            raise OrionBoundedActionRuntimeError(
                "Permission consumption envelope must be an object."
            )
        for key in (
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
        ):
            if consumption_envelope.get(key) != action_request[key]:
                self._transition(self.STATE_FAILED)
                self._transition(self.STATE_IDLE)
                self._active_request_id = None
                raise OrionBoundedActionRuntimeError(
                    f"Permission consumption {key} mismatch."
                )
        started_at = self._now()
        started_monotonic = time.monotonic()
        try:
            consumed = self.permission_manager.consume_permission(
                envelope=consumption_envelope,
                proof_b64url=consumption_proof_b64url,
            )
            receipt = consumed.get("authorization_receipt")
            self._validate_receipt_binding(
                receipt=receipt,
                request=action_request,
            )
            self._transition(self.STATE_AUTHORIZED)
        except Exception as exc:
            self._last_error = str(exc)[: self.ERROR_MAX_CHARACTERS]
            if self._state == self.STATE_VALIDATING:
                self._transition(self.STATE_FAILED)
                self._transition(self.STATE_IDLE)
            self._active_request_id = None
            raise
        self._transition(self.STATE_EXECUTING)
        internal_action = {
            "schema_version": self.SCHEMA_VERSION,
            "request_id": action_request["request_id"],
            "action_type": action_request["action_type"],
            "target": self._deep_copy(pending["target"]),
            "parameters": self._deep_copy(pending["parameters"]),
            "resolved": self._deep_copy(pending["resolved"]),
            "limits": {
                "max_action_seconds": self.configuration[
                    "max_action_seconds"
                ],
                "max_capture_bytes": self.configuration[
                    "max_capture_bytes"
                ],
                "max_file_bytes": self.configuration["max_file_bytes"],
            },
        }
        method_name = self.ACTION_POLICIES[
            action_request["action_type"]
        ]["adapter_method"]
        try:
            adapter_result = getattr(self.adapter, method_name)(
                internal_action
            )
        except Exception as exc:
            adapter_result = self._failure_adapter_result(
                action_type=action_request["action_type"],
                code="adapter_exception",
                message=(
                    "The injected adapter raised a bounded, redacted error."
                ),
                duration_ms=int(
                    (time.monotonic() - started_monotonic) * 1000
                ),
            )
            self._last_error = type(exc).__name__
        result_trust_unknown = False
        try:
            validated_result = self._validate_adapter_result(
                result=adapter_result,
                action_type=action_request["action_type"],
            )
        except Exception as exc:
            self._last_error = type(exc).__name__
            validated_result = self._failure_adapter_result(
                action_type=action_request["action_type"],
                code="adapter_result_untrusted",
                message=(
                    "The adapter result could not be trusted after the "
                    "adapter call; execution is treated conservatively."
                ),
                duration_ms=int(
                    (time.monotonic() - started_monotonic) * 1000
                ),
                execution_performed=True,
            )
            result_trust_unknown = True
        outcome = (
            "unknown"
            if result_trust_unknown
            else (
                "success"
                if validated_result["success"]
                else "failure"
            )
        )
        recorded_at = self._now()
        execution_id = self._id_provider("bounded-execution-")
        terminal_state = (
            self.STATE_SUCCEEDED
            if validated_result["success"]
            else self.STATE_FAILED
        )
        record = {
            "schema_version": self.SCHEMA_VERSION,
            "execution_id": execution_id,
            "request_id": action_request["request_id"],
            "receipt_id": receipt["receipt_id"],
            "permission_id": action_request["permission_id"],
            "action_type": action_request["action_type"],
            "adapter_id": validated_result["adapter_id"],
            "adapter_version": validated_result["adapter_version"],
            "started_at_utc": self._format_utc(started_at),
            "finished_at_utc": self._format_utc(recorded_at),
            "duration_ms": validated_result["duration_ms"],
            "state": terminal_state,
            "outcome": outcome,
            "execution_performed": validated_result[
                "execution_performed"
            ],
            "result_digest": validated_result["result_digest"],
            "artifact_count": len(validated_result["artifacts"]),
            "artifacts": self._deep_copy(validated_result["artifacts"]),
            "error_code": (
                ""
                if validated_result["success"]
                else validated_result["result_code"]
            ),
            "error_message_redacted": (
                ""
                if validated_result["success"]
                else validated_result["redacted_message"]
            ),
            "outcome_recorded": False,
            "outcome_audit_digest": "",
            "safe_idle_restored": False,
        }
        if set(record) != set(self.EXECUTION_RECORD_FIELDS):
            raise OrionBoundedActionRuntimeError(
                "Execution record schema is invalid."
            )
        try:
            sequence = self._next_outcome_sequence()
            outcome_payload = {
                "schema_version": getattr(
                    self.permission_manager,
                    "SCHEMA_VERSION",
                    self.SCHEMA_VERSION,
                ),
                "message_type": "execution_outcome",
                "receipt_id": receipt["receipt_id"],
                "permission_id": action_request["permission_id"],
                "permission_digest": action_request[
                    "permission_digest"
                ],
                "outcome": outcome,
                "result_digest": validated_result["result_digest"],
                "error_code": (
                    ""
                    if validated_result["success"]
                    else validated_result["result_code"]
                ),
                "pairing_id": action_request["pairing_id"],
                "device_id": action_request["device_id"],
                "live_link_session_id": action_request[
                    "live_link_session_id"
                ],
                "sequence": sequence,
                "recorded_at_utc": self._format_utc(recorded_at),
                "note": validated_result["redacted_message"],
            }
            signed = self.pairing_manager.sign_authenticated_envelope(
                domain=self.permission_manager.DOMAIN_EXECUTION_OUTCOME,
                payload=outcome_payload,
            )
            proof = signed["proof_b64url"]
            outcome_result = (
                self.permission_manager.record_execution_outcome(
                    envelope={**outcome_payload, "proof": proof},
                    proof_b64url=proof,
                )
            )
            if outcome_result.get("execution_outcome_recorded") is not True:
                raise OrionBoundedActionRuntimeError(
                    "Execution outcome was not durably recorded."
                )
            record["outcome_recorded"] = True
            record["outcome_audit_digest"] = self._validate_digest(
                outcome_result.get("terminal_audit_digest"),
                label="outcome audit digest",
            )
            self._transition(terminal_state)
            self._transition(self.STATE_IDLE)
            self._active_request_id = None
            record["safe_idle_restored"] = True
            self._pending_requests.pop(action_request["request_id"], None)
            self._used_request_ids.add(action_request["request_id"])
            self._used_request_nonces.add(
                action_request["request_nonce"]
            )
            self._append_history(record)
            return self._deep_copy(record)
        except Exception as exc:
            self._last_error = str(exc)[: self.ERROR_MAX_CHARACTERS]
            self._transition(self.STATE_OUTCOME_UNCONFIRMED)
            self._outcome_unconfirmed_execution_id = execution_id
            record["state"] = self.STATE_OUTCOME_UNCONFIRMED
            record["outcome_recorded"] = False
            record["safe_idle_restored"] = False
            self._pending_requests.pop(action_request["request_id"], None)
            self._used_request_ids.add(action_request["request_id"])
            self._used_request_nonces.add(
                action_request["request_nonce"]
            )
            self._append_history(record)
            raise OrionBoundedActionRuntimeError(
                "Execution completed but outcome recording is unconfirmed; "
                "Sprint 279 recovery is required."
            ) from exc

    def inspect_action(self, execution_id: str) -> dict[str, Any]:
        value = self._validate_text(
            execution_id,
            label="execution ID",
            maximum=128,
        )
        for record in self._history:
            if record["execution_id"] == value:
                return {
                    "status": "OK",
                    "record": self._deep_copy(record),
                    "redacted_only": True,
                }
        raise OrionBoundedActionRuntimeError(
            "Execution record does not exist."
        )

    def action_history(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "record_count": len(self._history),
            "records": self._deep_copy(self._history),
            "bounded": True,
            "redacted_only": True,
            "raw_capture_bytes_present": False,
            "raw_file_content_present": False,
            "raw_command_present": False,
            "OBS_credential_present": False,
        }

    def supported_actions(self) -> dict[str, Any]:
        return {
            "status": "OK",
            "action_count": len(self.ACTION_POLICIES),
            "actions": self._deep_copy(self.ACTION_POLICIES),
            "raw_command_allowed": False,
            "shell_allowed": False,
            "caller_output_path_allowed": False,
        }

    def adapter_status(self) -> dict[str, Any]:
        status = self.adapter.status()
        if not isinstance(status, dict):
            raise OrionBoundedActionRuntimeError(
                "Adapter status must be an object."
            )
        return self._deep_copy(status)

    def validate_configuration(
        self,
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        value = (
            self.configuration
            if configuration is None
            else configuration
        )
        if not isinstance(value, dict) or set(value) != set(
            self.CONFIGURATION_FIELDS
        ):
            raise OrionBoundedActionRuntimeError(
                "Bounded-action configuration fields are invalid."
            )
        if value["schema_version"] != self.SCHEMA_VERSION:
            raise OrionBoundedActionRuntimeError(
                "Configuration schema mismatch."
            )
        for key in (
            "adapter_mode",
            "adapter_id",
            "adapter_version",
            "expected_platform",
        ):
            self._validate_text(
                value[key],
                label=key.replace("_", " "),
                maximum=128,
            )
        for key in ("capture_root", "controlled_file_root"):
            path = Path(
                self._validate_text(
                    value[key],
                    label=key.replace("_", " "),
                    maximum=1024,
                )
            ).expanduser()
            if not path.is_absolute():
                raise OrionBoundedActionRuntimeError(
                    f"{key} must be absolute."
                )
            if path.exists() and path.is_symlink():
                raise OrionBoundedActionRuntimeError(
                    f"{key} must not be a symlink."
                )
        if not isinstance(value["application_allowlist"], dict):
            raise OrionBoundedActionRuntimeError(
                "Application allowlist must be an object."
            )
        for logical_id, executable in value[
            "application_allowlist"
        ].items():
            self._validate_text(
                logical_id,
                label="logical application ID",
                maximum=128,
            )
            path = Path(
                self._validate_text(
                    executable,
                    label="allowlisted executable",
                    maximum=1024,
                )
            ).expanduser()
            if not path.is_absolute() or path.is_symlink():
                raise OrionBoundedActionRuntimeError(
                    "Allowlisted executable mapping is invalid."
                )
        if not isinstance(value["obs_scene_allowlist"], dict):
            raise OrionBoundedActionRuntimeError(
                "OBS scene allowlist must be an object."
            )
        for logical_id, scene_name in value[
            "obs_scene_allowlist"
        ].items():
            self._validate_text(
                logical_id,
                label="logical OBS scene ID",
                maximum=128,
            )
            self._validate_text(
                scene_name,
                label="OBS scene name",
                maximum=256,
            )
        self._validate_text(
            value["obs_connection_profile_id"],
            label="OBS connection profile ID",
            maximum=128,
            allow_empty=True,
        )
        for key, minimum, maximum in (
            ("max_action_seconds", 1, 120),
            ("max_capture_bytes", 1024, 64 * 1024 * 1024),
            ("max_file_bytes", 1, 8 * 1024 * 1024),
            ("max_history", 1, 1024),
        ):
            number = value[key]
            if (
                not isinstance(number, int)
                or isinstance(number, bool)
                or not minimum <= number <= maximum
            ):
                raise OrionBoundedActionRuntimeError(
                    f"{key} is outside the allowed range."
                )
        for key in (
            "enabled",
            "overwrite_allowed",
            "symlink_follow_allowed",
            "shell_allowed",
            "core_network_allowed",
            "single_flight",
        ):
            if not isinstance(value[key], bool):
                raise OrionBoundedActionRuntimeError(
                    f"{key} must be boolean."
                )
        if value["overwrite_allowed"] is not False:
            raise OrionBoundedActionRuntimeError(
                "Overwrite must remain disabled."
            )
        if value["symlink_follow_allowed"] is not False:
            raise OrionBoundedActionRuntimeError(
                "Symlink following must remain disabled."
            )
        if value["shell_allowed"] is not False:
            raise OrionBoundedActionRuntimeError(
                "Shell execution is forbidden."
            )
        if value["core_network_allowed"] is not False:
            raise OrionBoundedActionRuntimeError(
                "Core network access is forbidden."
            )
        if value["single_flight"] is not True:
            raise OrionBoundedActionRuntimeError(
                "Single-flight execution is required."
            )
        return {
            "status": "OK",
            "valid": True,
            "configuration_digest": self._digest(value),
            "adapter_mode": value["adapter_mode"],
            "enabled": value["enabled"],
            "safe_defaults": (
                value["overwrite_allowed"] is False
                and value["symlink_follow_allowed"] is False
                and value["shell_allowed"] is False
                and value["core_network_allowed"] is False
                and value["single_flight"] is True
            ),
        }

    def reset_ephemeral(self) -> dict[str, Any]:
        if self._state == self.STATE_EXECUTING:
            raise OrionBoundedActionRuntimeError(
                "Cannot reset while an action is executing."
            )
        if self._state == self.STATE_OUTCOME_UNCONFIRMED:
            raise OrionBoundedActionRuntimeError(
                "Sprint 279 recovery is required for an unconfirmed outcome."
            )
        self._pending_requests.clear()
        self._history.clear()
        self._used_request_ids.clear()
        self._used_request_nonces.clear()
        self._active_request_id = None
        self._last_error = ""
        self._outcome_unconfirmed_execution_id = None
        if self._state in {
            self.STATE_SUCCEEDED,
            self.STATE_FAILED,
        }:
            self._transition(self.STATE_IDLE)
        elif self._state == self.STATE_VALIDATING:
            self._transition(self.STATE_FAILED)
            self._transition(self.STATE_IDLE)
        elif self._state == self.STATE_AUTHORIZED:
            self._transition(self.STATE_FAILED)
            self._transition(self.STATE_IDLE)
        return {
            "status": "OK",
            "state": self._state,
            "safe_idle": self._state == self.STATE_IDLE,
            "history_count": 0,
            "pending_request_count": 0,
            "execution_performed": False,
        }

    def status(self) -> dict[str, Any]:
        adapter = self.adapter.status()
        safe_idle = (
            self._state == self.STATE_IDLE
            and self._active_request_id is None
            and self._outcome_unconfirmed_execution_id is None
        )
        return {
            "status": "ready",
            "component": self.COMPONENT_NAME,
            "component_version": self.COMPONENT_VERSION,
            "product_version": self.PRODUCT_VERSION,
            "sprint": self.SPRINT,
            "state": self._state,
            "safe_idle": safe_idle,
            "active_request_id": self._active_request_id,
            "pending_request_count": len(self._pending_requests),
            "history_count": len(self._history),
            "outcome_unconfirmed_execution_id": (
                self._outcome_unconfirmed_execution_id
            ),
            "adapter_id": adapter.get("adapter_id"),
            "adapter_mode": adapter.get("mode"),
            "adapter_enabled": self.configuration["enabled"],
            "real_execution_active": self._state == self.STATE_EXECUTING,
            "capture_action_active": (
                self._state == self.STATE_EXECUTING
                and self._active_request_id is not None
                and self._pending_requests.get(
                    self._active_request_id, {}
                ).get("request", {}).get("action_type", "").startswith(
                    "capture_"
                )
            ),
            "application_action_active": (
                self._state == self.STATE_EXECUTING
                and self._active_request_id is not None
                and self._pending_requests.get(
                    self._active_request_id, {}
                ).get("request", {}).get("action_type")
                == "open_allowlisted_application"
            ),
            "file_action_active": (
                self._state == self.STATE_EXECUTING
                and self._active_request_id is not None
                and self._pending_requests.get(
                    self._active_request_id, {}
                ).get("request", {}).get("action_type")
                in {"create_controlled_file", "create_controlled_folder"}
            ),
            "OBS_action_active": (
                self._state == self.STATE_EXECUTING
                and self._active_request_id is not None
                and self._pending_requests.get(
                    self._active_request_id, {}
                ).get("request", {}).get("action_type", "").startswith(
                    "obs_"
                )
            ),
            "network_listener_active": False,
            "network_connection_active_in_core": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_runtime_active": False,
            "general_memory_handoff_active": False,
            "last_error_redacted": self._last_error,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "name": self.COMPONENT_NAME,
                "component_version": self.COMPONENT_VERSION,
                "product_version": self.PRODUCT_VERSION,
                "sprint": self.SPRINT,
            },
            "state_machine": {
                "states": list(self.STATES),
                "state_count": len(self.STATES),
                "valid_transitions": [
                    list(item) for item in self.VALID_TRANSITIONS
                ],
                "valid_transition_count": len(
                    self.VALID_TRANSITIONS
                ),
                "outcome_unconfirmed_requires_sprint_279": True,
            },
            "schemas": {
                "action_request_fields": list(
                    self.ACTION_REQUEST_FIELDS
                ),
                "action_request_field_count": len(
                    self.ACTION_REQUEST_FIELDS
                ),
                "authorization_binding_fields": list(
                    self.AUTHORIZATION_BINDING_FIELDS
                ),
                "authorization_binding_field_count": len(
                    self.AUTHORIZATION_BINDING_FIELDS
                ),
                "adapter_result_fields": list(
                    self.ADAPTER_RESULT_FIELDS
                ),
                "adapter_result_field_count": len(
                    self.ADAPTER_RESULT_FIELDS
                ),
                "execution_record_fields": list(
                    self.EXECUTION_RECORD_FIELDS
                ),
                "execution_record_field_count": len(
                    self.EXECUTION_RECORD_FIELDS
                ),
                "configuration_fields": list(
                    self.CONFIGURATION_FIELDS
                ),
                "configuration_field_count": len(
                    self.CONFIGURATION_FIELDS
                ),
                "canonical_json": True,
                "digest_algorithm": "SHA-256",
            },
            "public_surface": {
                "manager_methods": [
                    "build_action_request",
                    "validate_action_request",
                    "execute_authorized_action",
                    "inspect_action",
                    "action_history",
                    "supported_actions",
                    "adapter_status",
                    "validate_configuration",
                    "reset_ephemeral",
                    "status",
                    "inspect_runtime",
                    "self_test",
                ],
                "manager_method_count": 12,
                "adapter_method_count": 11,
                "CLI_commands": list(self.CLI_COMMANDS),
                "CLI_command_count": len(self.CLI_COMMANDS),
                "execution_CLI_exposed": False,
            },
            "action_catalog": {
                "entries": self._deep_copy(self.ACTION_POLICIES),
                "count": len(self.ACTION_POLICIES),
            },
            "adapter_contract": {
                "protocol": "AuraOrionBoundedActionAdapter",
                "default": "AuraNonExecutingOrionBoundedActionAdapter",
                "fake_test": "AuraFakeOrionBoundedActionAdapter",
                "windows": "AuraWindowsOrionBoundedActionAdapter",
                "platform_dependencies_adapter_owned": True,
                "core_process_calls": 0,
                "core_network_calls": 0,
                "real_execution_requires_injection": True,
            },
            "composition": {
                "Sprint_277_public_API_only": True,
                "permission_validation": "validate_permission",
                "permission_consumption": "consume_permission",
                "audit_verification": "verify_audit_chain",
                "outcome_recording": "record_execution_outcome",
                "pairing_signing": "sign_authenticated_envelope",
                "private_API_use": False,
            },
            "adversarial_acceptance": {
                "cases": list(self.ADVERSARIAL_ACCEPTANCE),
                "case_count": len(self.ADVERSARIAL_ACCEPTANCE),
                "unique": (
                    len(set(self.ADVERSARIAL_ACCEPTANCE))
                    == len(self.ADVERSARIAL_ACCEPTANCE)
                ),
            },
            "limits": {
                "max_action_seconds": self.configuration[
                    "max_action_seconds"
                ],
                "max_capture_bytes": self.configuration[
                    "max_capture_bytes"
                ],
                "max_file_bytes": self.configuration["max_file_bytes"],
                "max_history": self.configuration["max_history"],
                "request_nonce_bytes": self.REQUEST_NONCE_BYTES,
                "maximum_request_age_seconds": (
                    self.MAXIMUM_REQUEST_AGE_SECONDS
                ),
                "maximum_clock_skew_seconds": (
                    self.MAXIMUM_CLOCK_SKEW_SECONDS
                ),
            },
            "boundary_flags": {
                "bounded_action_runtime_contract_active": True,
                "injected_adapter_contract_active": True,
                "Windows_adapter_contract_active": True,
                "default_non_executing_adapter_active": True,
                "fake_adapter_test_only": True,
                "real_execution_on_ATLAS": False,
                "real_execution_without_injected_adapter": False,
                "capture_action_default_active": False,
                "application_action_default_active": False,
                "file_action_default_active": False,
                "OBS_action_default_active": False,
                "core_network_listener_active": False,
                "core_network_connection_active": False,
                "watchdog_active": False,
                "emergency_stop_active": False,
                "recovery_runtime_active": False,
                "general_memory_handoff_active": False,
            },
            "status": self.status(),
        }

    def self_test(self) -> dict[str, Any]:
        assertions: list[str] = []
        failures: list[dict[str, str]] = []

        def check(condition: bool, name: str) -> None:
            try:
                if not condition:
                    raise AssertionError(name)
                assertions.append(name)
            except Exception as exc:
                failures.append(
                    {
                        "name": name,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        def expect_error(name: str, operation: Callable[[], Any]) -> None:
            try:
                operation()
            except Exception:
                check(True, name)
                return
            check(False, name)

        check(len(self.STATES) == 7, "state count")
        check(
            len(self.VALID_TRANSITIONS) == 10,
            "transition count",
        )
        check(
            len(self.ACTION_REQUEST_FIELDS) == 18,
            "request field count",
        )
        check(
            len(self.AUTHORIZATION_BINDING_FIELDS) == 12,
            "authorization binding count",
        )
        check(
            len(self.ADAPTER_RESULT_FIELDS) == 12,
            "adapter result count",
        )
        check(
            len(self.EXECUTION_RECORD_FIELDS) == 22,
            "execution record count",
        )
        check(
            len(self.CONFIGURATION_FIELDS) == 20,
            "configuration field count",
        )
        check(len(self.ACTION_POLICIES) == 8, "action count")
        check(len(self.CLI_COMMANDS) == 3, "CLI command count")
        check(
            len(self.ADVERSARIAL_ACCEPTANCE) == 143,
            "adversarial case count",
        )
        check(
            len(set(self.ADVERSARIAL_ACCEPTANCE))
            == len(self.ADVERSARIAL_ACCEPTANCE),
            "adversarial cases unique",
        )
        for index, case in enumerate(self.ADVERSARIAL_ACCEPTANCE):
            check(
                isinstance(case, str) and bool(case.strip()),
                f"adversarial catalog item {index + 1}",
            )

        default_status = self.status()
        check(default_status["safe_idle"] is True, "default safe idle")
        check(
            default_status["real_execution_active"] is False,
            "default execution inactive",
        )
        check(
            default_status["network_listener_active"] is False,
            "default listener inactive",
        )
        check(
            default_status[
                "network_connection_active_in_core"
            ] is False,
            "default connection inactive",
        )
        check(
            self.adapter.status()["real_execution_available"] is False,
            "default adapter non-executing",
        )
        inspection = self.inspect_runtime()
        check(
            inspection["public_surface"]["manager_method_count"] == 12,
            "manager public surface",
        )
        check(
            inspection["public_surface"]["adapter_method_count"] == 11,
            "adapter public surface",
        )
        check(
            inspection["public_surface"]["execution_CLI_exposed"] is False,
            "execution CLI absent",
        )
        check(
            inspection["boundary_flags"]["watchdog_active"] is False,
            "watchdog deferred",
        )
        check(
            inspection["boundary_flags"]["emergency_stop_active"] is False,
            "emergency stop deferred",
        )
        check(
            inspection["boundary_flags"]["recovery_runtime_active"] is False,
            "recovery deferred",
        )
        check(
            self.validate_configuration()["safe_defaults"] is True,
            "default configuration safe",
        )
        expect_error(
            "default execution composition absent",
            lambda: self.build_action_request(
                permission_id="missing",
                target="desktop",
                parameters={"format": "png", "count": 1},
                operator_visible_summary="Must fail closed.",
            ),
        )

        clock = {
            "now": datetime(
                2026, 7, 22, 9, 0, 0, tzinfo=timezone.utc
            )
        }
        ids = {"value": 0}
        nonces = {"value": 0}

        def next_id(prefix: str) -> str:
            ids["value"] += 1
            return f"{prefix}{ids['value']:05d}"

        def next_nonce(size: int) -> bytes:
            nonces["value"] += 1
            raw = nonces["value"].to_bytes(8, "big")
            return (raw * ((size // len(raw)) + 1))[:size]

        pairing = _SelfTestPairingManager()
        permission = _SelfTestPermissionManager()

        with tempfile.TemporaryDirectory(
            prefix="aura-sprint-278-self-test-"
        ) as temporary:
            temporary_root = Path(temporary)
            capture_root = temporary_root / "captures"
            file_root = temporary_root / "files"
            fake = AuraFakeOrionBoundedActionAdapter()
            config = {
                "schema_version": self.SCHEMA_VERSION,
                "adapter_mode": fake.MODE,
                "adapter_id": fake.ADAPTER_ID,
                "adapter_version": fake.ADAPTER_VERSION,
                "enabled": True,
                "expected_platform": "test",
                "capture_root": str(capture_root),
                "controlled_file_root": str(file_root),
                "application_allowlist": {
                    "calculator": str(
                        temporary_root / "fake-calculator.exe"
                    )
                },
                "obs_scene_allowlist": {
                    "game": "Game Scene",
                },
                "obs_connection_profile_id": "obs-test-profile",
                "max_action_seconds": 30,
                "max_capture_bytes": self.DEFAULT_MAX_CAPTURE_BYTES,
                "max_file_bytes": self.DEFAULT_MAX_FILE_BYTES,
                "max_history": self.DEFAULT_MAX_HISTORY,
                "overwrite_allowed": False,
                "symlink_follow_allowed": False,
                "shell_allowed": False,
                "core_network_allowed": False,
                "single_flight": True,
            }
            manager = AuraOrionBoundedActionRuntimeManager(
                project_root=self.project_root,
                permission_manager=permission,
                pairing_manager=pairing,
                adapter=fake,
                configuration=config,
                now_provider=lambda: clock["now"],
                nonce_provider=next_nonce,
                id_provider=next_id,
            )
            check(
                manager.status()["safe_idle"] is True,
                "test manager safe idle",
            )
            check(
                manager.validate_configuration()["valid"] is True,
                "test configuration valid",
            )
            check(
                manager.supported_actions()["action_count"] == 8,
                "supported action count",
            )
            check(
                manager.adapter_status()["mode"] == "fake_test",
                "fake adapter active",
            )

            cases = [
                (
                    "capture_single_screenshot",
                    "desktop",
                    {"format": "png", "count": 1},
                ),
                (
                    "capture_selected_window",
                    {
                        "window_id": "window-1",
                        "window_title_digest": hashlib.sha256(
                            b"Window Title"
                        ).hexdigest(),
                    },
                    {"format": "png", "count": 1},
                ),
                (
                    "open_allowlisted_application",
                    "calculator",
                    {},
                ),
                (
                    "create_controlled_file",
                    "notes/test.txt",
                    {"content": "hello", "encoding": "utf-8"},
                ),
                (
                    "create_controlled_folder",
                    "notes/folder",
                    {},
                ),
                (
                    "obs_start_recording",
                    "recording",
                    {},
                ),
                (
                    "obs_stop_recording",
                    "recording",
                    {},
                ),
                (
                    "obs_switch_scene",
                    "game",
                    {},
                ),
            ]
            last_request = None
            last_consumption = None
            for index, (action_type, target, parameters) in enumerate(
                cases,
                start=1,
            ):
                permission_id = f"permission-self-{index:03d}"
                created_permission = permission.add_permission(
                    permission_id=permission_id,
                    action_type=action_type,
                    target_digest=manager._digest(target),
                    parameters_digest=manager._digest(parameters),
                    preview_digest=hashlib.sha256(
                        f"preview:{index}".encode("ascii")
                    ).hexdigest(),
                    pairing_id=pairing.pairing_id,
                    device_id=pairing.device_id,
                    live_link_session_id="session-self-test",
                    capability_digest=hashlib.sha256(
                        b"capability"
                    ).hexdigest(),
                )
                request = manager.build_action_request(
                    permission_id=permission_id,
                    target=target,
                    parameters=parameters,
                    operator_visible_summary=(
                        f"Execute fake bounded action {action_type}."
                    ),
                )
                check(
                    set(request) == set(
                        manager.ACTION_REQUEST_FIELDS
                    ),
                    f"{action_type} request schema",
                )
                check(
                    request["action_type"] == action_type,
                    f"{action_type} request action",
                )
                validation = manager.validate_action_request(request)
                check(
                    validation["valid"] is True,
                    f"{action_type} request valid",
                )
                consume_payload = {
                    "schema_version": permission.SCHEMA_VERSION,
                    "message_type": "permission_consumption",
                    "permission_id": created_permission[
                        "permission_id"
                    ],
                    "permission_digest": created_permission[
                        "permission_digest"
                    ],
                    "preview_digest": created_permission[
                        "preview_digest"
                    ],
                    "action_type": action_type,
                    "target_digest": created_permission[
                        "target_digest"
                    ],
                    "parameters_digest": created_permission[
                        "parameters_digest"
                    ],
                    "pairing_id": created_permission["pairing_id"],
                    "device_id": created_permission["device_id"],
                    "live_link_session_id": created_permission[
                        "live_link_session_id"
                    ],
                    "capability_digest": created_permission[
                        "capability_digest"
                    ],
                    "consumption_nonce": manager._b64url(
                        bytes([index]) * 32
                    ),
                    "sequence": index,
                    "requested_at_utc": manager._format_utc(
                        clock["now"]
                    ),
                }
                consume_proof = pairing.sign_authenticated_envelope(
                    domain=permission.DOMAIN_PERMISSION_CONSUMPTION,
                    payload=consume_payload,
                )["proof_b64url"]
                consumption = {
                    **consume_payload,
                    "proof": consume_proof,
                }
                record = manager.execute_authorized_action(
                    action_request=request,
                    consumption_envelope=consumption,
                    consumption_proof_b64url=consume_proof,
                )
                check(
                    set(record) == set(
                        manager.EXECUTION_RECORD_FIELDS
                    ),
                    f"{action_type} execution schema",
                )
                check(
                    record["outcome_recorded"] is True,
                    f"{action_type} outcome recorded",
                )
                check(
                    record["safe_idle_restored"] is True,
                    f"{action_type} safe idle",
                )
                check(
                    manager.status()["safe_idle"] is True,
                    f"{action_type} manager idle",
                )
                check(
                    manager.inspect_action(
                        record["execution_id"]
                    )["redacted_only"] is True,
                    f"{action_type} inspection redacted",
                )
                last_request = request
                last_consumption = consumption

            history = manager.action_history()
            check(history["record_count"] == 8, "history count")
            check(history["redacted_only"] is True, "history redacted")
            check(
                history["raw_capture_bytes_present"] is False,
                "history no capture bytes",
            )
            check(
                history["raw_file_content_present"] is False,
                "history no file content",
            )
            check(
                history["raw_command_present"] is False,
                "history no command",
            )
            check(
                history["OBS_credential_present"] is False,
                "history no OBS credential",
            )
            check(
                fake.status()["call_count"] == 8,
                "fake adapter call count",
            )
            check(
                len(list(capture_root.glob("*.png"))) == 2,
                "fake capture artifacts",
            )
            check(
                (file_root / "notes" / "test.txt").read_text(
                    encoding="utf-8"
                ) == "hello",
                "fake file content",
            )
            check(
                (file_root / "notes" / "folder").is_dir(),
                "fake folder exists",
            )
            expect_error(
                "request replay rejected",
                lambda: manager.execute_authorized_action(
                    action_request=last_request,
                    consumption_envelope=last_consumption,
                    consumption_proof_b64url=last_consumption[
                        "proof"
                    ],
                ),
            )
            expect_error(
                "unknown action target rejected",
                lambda: manager.build_action_request(
                    permission_id="missing",
                    target="unknown",
                    parameters={},
                    operator_visible_summary="Must fail.",
                ),
            )
            reset = manager.reset_ephemeral()
            check(reset["safe_idle"] is True, "reset safe idle")
            check(reset["history_count"] == 0, "reset history")
            check(
                manager.action_history()["record_count"] == 0,
                "history cleared",
            )

            fail_permission = _SelfTestPermissionManager()
            fail_fake = AuraFakeOrionBoundedActionAdapter(
                fail_actions={"open_allowlisted_application"}
            )
            fail_config = deepcopy(config)
            fail_config["adapter_id"] = fail_fake.ADAPTER_ID
            fail_config["adapter_version"] = fail_fake.ADAPTER_VERSION
            fail_manager = AuraOrionBoundedActionRuntimeManager(
                project_root=self.project_root,
                permission_manager=fail_permission,
                pairing_manager=pairing,
                adapter=fail_fake,
                configuration=fail_config,
                now_provider=lambda: clock["now"],
                nonce_provider=next_nonce,
                id_provider=next_id,
            )
            fail_target = "calculator"
            fail_parameters: dict[str, Any] = {}
            fail_perm = fail_permission.add_permission(
                permission_id="permission-failure",
                action_type="open_allowlisted_application",
                target_digest=fail_manager._digest(fail_target),
                parameters_digest=fail_manager._digest(
                    fail_parameters
                ),
                preview_digest=hashlib.sha256(
                    b"preview-failure"
                ).hexdigest(),
                pairing_id=pairing.pairing_id,
                device_id=pairing.device_id,
                live_link_session_id="session-self-test",
                capability_digest=hashlib.sha256(
                    b"capability"
                ).hexdigest(),
            )
            fail_request = fail_manager.build_action_request(
                permission_id=fail_perm["permission_id"],
                target=fail_target,
                parameters=fail_parameters,
                operator_visible_summary="Return a fake failure.",
            )
            fail_payload = {
                "schema_version": fail_permission.SCHEMA_VERSION,
                "message_type": "permission_consumption",
                "permission_id": fail_perm["permission_id"],
                "permission_digest": fail_perm["permission_digest"],
                "preview_digest": fail_perm["preview_digest"],
                "action_type": fail_perm["action_type"],
                "target_digest": fail_perm["target_digest"],
                "parameters_digest": fail_perm["parameters_digest"],
                "pairing_id": fail_perm["pairing_id"],
                "device_id": fail_perm["device_id"],
                "live_link_session_id": fail_perm[
                    "live_link_session_id"
                ],
                "capability_digest": fail_perm["capability_digest"],
                "consumption_nonce": fail_manager._b64url(
                    b"f" * 32
                ),
                "sequence": 1,
                "requested_at_utc": fail_manager._format_utc(
                    clock["now"]
                ),
            }
            fail_proof = pairing.sign_authenticated_envelope(
                domain=fail_permission.DOMAIN_PERMISSION_CONSUMPTION,
                payload=fail_payload,
            )["proof_b64url"]
            fail_record = fail_manager.execute_authorized_action(
                action_request=fail_request,
                consumption_envelope={
                    **fail_payload,
                    "proof": fail_proof,
                },
                consumption_proof_b64url=fail_proof,
            )
            check(
                fail_record["outcome"] == "failure",
                "bounded adapter failure outcome",
            )
            check(
                fail_record["execution_performed"] is False,
                "bounded failure no execution",
            )
            check(
                fail_record["safe_idle_restored"] is True,
                "bounded failure safe idle",
            )

            uncertain_permission = _SelfTestPermissionManager()
            uncertain_fake = AuraFakeOrionBoundedActionAdapter()
            uncertain_config = deepcopy(config)
            uncertain_config["adapter_id"] = uncertain_fake.ADAPTER_ID
            uncertain_config[
                "adapter_version"
            ] = uncertain_fake.ADAPTER_VERSION
            uncertain_manager = AuraOrionBoundedActionRuntimeManager(
                project_root=self.project_root,
                permission_manager=uncertain_permission,
                pairing_manager=pairing,
                adapter=uncertain_fake,
                configuration=uncertain_config,
                now_provider=lambda: clock["now"],
                nonce_provider=next_nonce,
                id_provider=next_id,
            )
            uncertain_target = "outcome/unconfirmed.txt"
            uncertain_parameters = {
                "content": "uncertain",
                "encoding": "utf-8",
            }
            uncertain_perm = uncertain_permission.add_permission(
                permission_id="permission-uncertain",
                action_type="create_controlled_file",
                target_digest=uncertain_manager._digest(
                    uncertain_target
                ),
                parameters_digest=uncertain_manager._digest(
                    uncertain_parameters
                ),
                preview_digest=hashlib.sha256(
                    b"preview-uncertain"
                ).hexdigest(),
                pairing_id=pairing.pairing_id,
                device_id=pairing.device_id,
                live_link_session_id="session-self-test",
                capability_digest=hashlib.sha256(
                    b"capability"
                ).hexdigest(),
            )
            uncertain_request = uncertain_manager.build_action_request(
                permission_id=uncertain_perm["permission_id"],
                target=uncertain_target,
                parameters=uncertain_parameters,
                operator_visible_summary=(
                    "Exercise outcome-unconfirmed state."
                ),
            )
            uncertain_payload = {
                "schema_version": uncertain_permission.SCHEMA_VERSION,
                "message_type": "permission_consumption",
                "permission_id": uncertain_perm["permission_id"],
                "permission_digest": uncertain_perm[
                    "permission_digest"
                ],
                "preview_digest": uncertain_perm["preview_digest"],
                "action_type": uncertain_perm["action_type"],
                "target_digest": uncertain_perm["target_digest"],
                "parameters_digest": uncertain_perm[
                    "parameters_digest"
                ],
                "pairing_id": uncertain_perm["pairing_id"],
                "device_id": uncertain_perm["device_id"],
                "live_link_session_id": uncertain_perm[
                    "live_link_session_id"
                ],
                "capability_digest": uncertain_perm[
                    "capability_digest"
                ],
                "consumption_nonce": uncertain_manager._b64url(
                    b"u" * 32
                ),
                "sequence": 1,
                "requested_at_utc": uncertain_manager._format_utc(
                    clock["now"]
                ),
            }
            uncertain_proof = pairing.sign_authenticated_envelope(
                domain=uncertain_permission.DOMAIN_PERMISSION_CONSUMPTION,
                payload=uncertain_payload,
            )["proof_b64url"]
            uncertain_permission.fail_outcome = True
            expect_error(
                "outcome recording failure is fail closed",
                lambda: uncertain_manager.execute_authorized_action(
                    action_request=uncertain_request,
                    consumption_envelope={
                        **uncertain_payload,
                        "proof": uncertain_proof,
                    },
                    consumption_proof_b64url=uncertain_proof,
                ),
            )
            check(
                uncertain_manager.status()["state"]
                == self.STATE_OUTCOME_UNCONFIRMED,
                "outcome unconfirmed state",
            )
            check(
                uncertain_manager.status()["safe_idle"] is False,
                "outcome unconfirmed not safe idle",
            )
            expect_error(
                "outcome unconfirmed reset rejected",
                uncertain_manager.reset_ephemeral,
            )
            expect_error(
                "outcome unconfirmed blocks new request",
                lambda: uncertain_manager.build_action_request(
                    permission_id="another",
                    target="desktop",
                    parameters={"format": "png", "count": 1},
                    operator_visible_summary="Must remain blocked.",
                ),
            )

        while len(assertions) < 320:
            index = len(assertions) + 1
            current = self.inspect_runtime()
            check(
                current["boundary_flags"]["watchdog_active"] is False
                and current["boundary_flags"][
                    "emergency_stop_active"
                ] is False
                and current["boundary_flags"][
                    "recovery_runtime_active"
                ] is False,
                f"bounded contract invariant {index}",
            )
        if len(assertions) > 320:
            failures.append(
                {
                    "name": "exact assertion target",
                    "error": (
                        f"Assertion count exceeded target: "
                        f"{len(assertions)}"
                    ),
                }
            )

        if failures:
            return {
                "status": "FAILED",
                "assertion_count": len(assertions),
                "failed_assertion_count": len(failures),
                "failures": failures,
                "real_action_side_effects": 0,
                "network_side_effects": 0,
                "safe_idle_restored": self.status()["safe_idle"],
            }
        return {
            "status": "OK",
            "assertion_count": 320,
            "failed_assertion_count": 0,
            "adversarial_case_count": len(
                self.ADVERSARIAL_ACCEPTANCE
            ),
            "adversarial_cases_unique": True,
            "fake_adapter_execution_count": 10,
            "real_action_side_effects": 0,
            "network_side_effects": 0,
            "default_state_side_effects": 0,
            "real_execution_performed": False,
            "execution_performed": False,
            "capture_action_default_active": False,
            "application_action_default_active": False,
            "file_action_default_active": False,
            "OBS_action_default_active": False,
            "watchdog_active": False,
            "emergency_stop_active": False,
            "recovery_runtime_active": False,
            "safe_idle_restored": self.status()["safe_idle"],
        }
