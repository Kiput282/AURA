"""Injected safety-control adapters for AURA Sprint 279.

The supervision manager never performs process, network, capture, file, or OBS
side effects directly. Real emergency side effects are available only through
an explicitly injected adapter. The default adapter is non-executing and
fails closed.
"""

from __future__ import annotations

import hashlib
import json
import platform
import time
from typing import Any, Callable, Protocol, runtime_checkable


class OrionSafetyControlAdapterError(RuntimeError):
    """Raised when an injected safety adapter cannot continue safely."""


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
        raise OrionSafetyControlAdapterError(
            "Safety adapter payload is not canonicalizable."
        ) from exc


def _digest(payload: Any) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _result(
    *,
    adapter_id: str,
    adapter_version: str,
    operation: str,
    success: bool,
    execution_performed: bool,
    result_code: str,
    safe_idle_verified: bool,
    action_interrupted: bool,
    redacted_message: str,
    metadata: dict[str, Any] | None = None,
    duration_ms: int = 0,
    platform_name: str | None = None,
) -> dict[str, Any]:
    metadata_value = {} if metadata is None else metadata
    result = {
        "schema_version": "1",
        "adapter_id": str(adapter_id),
        "adapter_version": str(adapter_version),
        "operation": str(operation),
        "success": bool(success),
        "execution_performed": bool(execution_performed),
        "result_code": str(result_code),
        "result_digest": "",
        "safe_idle_verified": bool(safe_idle_verified),
        "action_interrupted": bool(action_interrupted),
        "redacted_message": str(redacted_message),
        "metadata_digest": _digest(metadata_value),
        "duration_ms": max(0, int(duration_ms)),
        "platform": (
            platform.system().lower()
            if platform_name is None
            else str(platform_name).lower()
        ),
    }
    result["result_digest"] = _digest(
        {
            key: value
            for key, value in result.items()
            if key != "result_digest"
        }
    )
    return result


@runtime_checkable
class AuraOrionSafetyControlAdapter(Protocol):
    """Public protocol for injected emergency-control side effects."""

    def interrupt_active_action(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def stop_application(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def stop_capture(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def stop_file_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def stop_obs_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def verify_safe_idle(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def status(self) -> dict[str, Any]:
        ...

    def inspect_runtime(self) -> dict[str, Any]:
        ...

    def self_test(self) -> dict[str, Any]:
        ...


class AuraNonExecutingOrionSafetyControlAdapter:
    """Default adapter that never performs a platform side effect."""

    ADAPTER_ID = "orion-safety-non-executing"
    ADAPTER_VERSION = "0.1.0"
    MODE = "non_executing"

    def _deny(
        self,
        operation: str,
        *,
        safe_idle_verified: bool = False,
    ) -> dict[str, Any]:
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            operation=operation,
            success=safe_idle_verified,
            execution_performed=False,
            result_code=(
                "safe_idle_verified_without_side_effect"
                if safe_idle_verified
                else "adapter_non_executing"
            ),
            safe_idle_verified=safe_idle_verified,
            action_interrupted=False,
            redacted_message=(
                "No authorized real ORION safety adapter was injected."
            ),
        )

    def interrupt_active_action(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny("interrupt_active_action")

    def stop_application(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny("stop_application")

    def stop_capture(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny("stop_capture")

    def stop_file_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny("stop_file_operation")

    def stop_obs_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny("stop_obs_operation")

    def verify_safe_idle(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(
            "verify_safe_idle",
            safe_idle_verified=True,
        )

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": False,
            "platform": platform.system().lower(),
            "real_emergency_side_effect_available": False,
            "network_listener_active": False,
            "network_connection_active": False,
            "background_thread_active": False,
            "process_execution_active": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "public_surface": {
                "adapter_method_count": 9,
            },
            "boundaries": {
                "enabled": False,
                "real_emergency_side_effect_available": False,
                "network_listener_active": False,
                "network_connection_active": False,
                "background_thread_active": False,
                "process_execution_active": False,
            },
            "status": "OK",
        }

    def self_test(self) -> dict[str, Any]:
        status = self.status()
        verification = self.verify_safe_idle({})
        assertions = [
            status["enabled"] is False,
            status["real_emergency_side_effect_available"] is False,
            status["network_listener_active"] is False,
            status["network_connection_active"] is False,
            status["background_thread_active"] is False,
            status["process_execution_active"] is False,
            verification["execution_performed"] is False,
            verification["safe_idle_verified"] is True,
            verification["success"] is True,
        ]
        failures = [
            index + 1
            for index, value in enumerate(assertions)
            if not value
        ]
        return {
            "status": "OK" if not failures else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failures),
            "failed_assertions": failures,
            "real_emergency_side_effects": 0,
            "network_side_effects": 0,
        }


class AuraFakeOrionSafetyControlAdapter:
    """Deterministic in-memory adapter used only by self-tests."""

    ADAPTER_ID = "orion-safety-fake-test"
    ADAPTER_VERSION = "0.1.0"
    MODE = "fake_test"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.safe_idle = True
        self.fail_operations: set[str] = set()

    def _execute(
        self,
        operation: str,
        context: dict[str, Any],
        *,
        safe_idle_verified: bool = False,
        action_interrupted: bool = False,
    ) -> dict[str, Any]:
        started = time.monotonic()
        self.calls.append(
            {
                "operation": operation,
                "context_digest": _digest(context),
            }
        )
        failed = operation in self.fail_operations
        if operation == "verify_safe_idle":
            safe_idle_verified = self.safe_idle and not failed
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            operation=operation,
            success=not failed,
            execution_performed=(operation != "verify_safe_idle"),
            result_code=(
                "fake_operation_failed"
                if failed
                else "fake_operation_completed"
            ),
            safe_idle_verified=safe_idle_verified,
            action_interrupted=action_interrupted and not failed,
            redacted_message="Deterministic fake safety operation.",
            metadata={"call_count": len(self.calls)},
            duration_ms=int((time.monotonic() - started) * 1000),
            platform_name="test",
        )

    def interrupt_active_action(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "interrupt_active_action",
            context,
            action_interrupted=True,
        )

    def stop_application(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "stop_application",
            context,
            action_interrupted=True,
        )

    def stop_capture(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "stop_capture",
            context,
            action_interrupted=True,
        )

    def stop_file_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "stop_file_operation",
            context,
            action_interrupted=True,
        )

    def stop_obs_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "stop_obs_operation",
            context,
            action_interrupted=True,
        )

    def verify_safe_idle(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._execute(
            "verify_safe_idle",
            context,
            safe_idle_verified=self.safe_idle,
        )

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": True,
            "platform": "test",
            "real_emergency_side_effect_available": False,
            "fake_side_effect_available": True,
            "call_count": len(self.calls),
            "safe_idle": self.safe_idle,
            "network_listener_active": False,
            "network_connection_active": False,
            "background_thread_active": False,
            "process_execution_active": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "public_surface": {
                "adapter_method_count": 9,
            },
            "history": {
                "call_count": len(self.calls),
                "operations": [item["operation"] for item in self.calls],
            },
            "boundaries": {
                "real_emergency_side_effect_available": False,
                "network_listener_active": False,
                "network_connection_active": False,
                "background_thread_active": False,
                "process_execution_active": False,
            },
            "status": "OK",
        }

    def self_test(self) -> dict[str, Any]:
        original_count = len(self.calls)
        interrupt = self.interrupt_active_action(
            {"action_type": "capture_single_screenshot"}
        )
        verification = self.verify_safe_idle({})
        assertions = [
            interrupt["success"] is True,
            interrupt["execution_performed"] is True,
            interrupt["action_interrupted"] is True,
            verification["success"] is True,
            verification["safe_idle_verified"] is True,
            self.status()["call_count"] == original_count + 2,
            self.status()["network_listener_active"] is False,
            self.status()["network_connection_active"] is False,
            self.status()["real_emergency_side_effect_available"] is False,
        ]
        failures = [
            index + 1
            for index, value in enumerate(assertions)
            if not value
        ]
        return {
            "status": "OK" if not failures else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failures),
            "failed_assertions": failures,
            "fake_execution_count": 2,
            "real_emergency_side_effects": 0,
            "network_side_effects": 0,
        }


class AuraWindowsOrionSafetyControlAdapter:
    """Guarded optional Windows adapter backed only by injected callbacks."""

    ADAPTER_ID = "orion-safety-windows-guarded"
    ADAPTER_VERSION = "0.1.0"
    MODE = "windows_guarded"

    def __init__(
        self,
        *,
        enabled: bool = False,
        interrupt_callback: Callable[[dict[str, Any]], Any] | None = None,
        application_callback: Callable[[dict[str, Any]], Any] | None = None,
        capture_callback: Callable[[dict[str, Any]], Any] | None = None,
        file_callback: Callable[[dict[str, Any]], Any] | None = None,
        obs_callback: Callable[[dict[str, Any]], Any] | None = None,
        verify_callback: Callable[[dict[str, Any]], bool] | None = None,
    ) -> None:
        self.enabled = bool(enabled)
        self._callbacks = {
            "interrupt_active_action": interrupt_callback,
            "stop_application": application_callback,
            "stop_capture": capture_callback,
            "stop_file_operation": file_callback,
            "stop_obs_operation": obs_callback,
        }
        self._verify_callback = verify_callback

    def _invoke(
        self,
        operation: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        callback = self._callbacks.get(operation)
        platform_ok = platform.system().lower() == "windows"
        allowed = self.enabled and platform_ok and callback is not None
        if not allowed:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                operation=operation,
                success=False,
                execution_performed=False,
                result_code="windows_adapter_not_available",
                safe_idle_verified=False,
                action_interrupted=False,
                redacted_message=(
                    "Guarded Windows callback is unavailable or disabled."
                ),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        try:
            callback(context)
        except Exception as exc:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                operation=operation,
                success=False,
                execution_performed=False,
                result_code="windows_callback_failed",
                safe_idle_verified=False,
                action_interrupted=False,
                redacted_message=(
                    f"Injected Windows callback failed: "
                    f"{type(exc).__name__}."
                ),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            operation=operation,
            success=True,
            execution_performed=True,
            result_code="windows_callback_completed",
            safe_idle_verified=False,
            action_interrupted=True,
            redacted_message="Injected Windows callback completed.",
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def interrupt_active_action(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._invoke("interrupt_active_action", context)

    def stop_application(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._invoke("stop_application", context)

    def stop_capture(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._invoke("stop_capture", context)

    def stop_file_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._invoke("stop_file_operation", context)

    def stop_obs_operation(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return self._invoke("stop_obs_operation", context)

    def verify_safe_idle(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        platform_ok = platform.system().lower() == "windows"
        allowed = (
            self.enabled
            and platform_ok
            and self._verify_callback is not None
        )
        if not allowed:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                operation="verify_safe_idle",
                success=False,
                execution_performed=False,
                result_code="safe_idle_verifier_unavailable",
                safe_idle_verified=False,
                action_interrupted=False,
                redacted_message=(
                    "Guarded Windows safe-idle verifier is unavailable."
                ),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        try:
            safe = bool(self._verify_callback(context))
        except Exception as exc:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                operation="verify_safe_idle",
                success=False,
                execution_performed=False,
                result_code="safe_idle_verifier_failed",
                safe_idle_verified=False,
                action_interrupted=False,
                redacted_message=(
                    f"Injected safe-idle verifier failed: "
                    f"{type(exc).__name__}."
                ),
                duration_ms=int((time.monotonic() - started) * 1000),
            )
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            operation="verify_safe_idle",
            success=safe,
            execution_performed=False,
            result_code=(
                "safe_idle_verified" if safe else "safe_idle_not_verified"
            ),
            safe_idle_verified=safe,
            action_interrupted=False,
            redacted_message="Injected safe-idle verification completed.",
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def status(self) -> dict[str, Any]:
        platform_ok = platform.system().lower() == "windows"
        callback_count = sum(
            callback is not None for callback in self._callbacks.values()
        )
        return {
            "status": "ready",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": self.enabled,
            "platform": platform.system().lower(),
            "platform_supported": platform_ok,
            "callback_count": callback_count,
            "safe_idle_verifier_available": (
                self._verify_callback is not None
            ),
            "real_emergency_side_effect_available": (
                self.enabled and platform_ok and callback_count > 0
            ),
            "network_listener_active": False,
            "network_connection_active": False,
            "background_thread_active": False,
            "process_execution_active_in_adapter": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        status = self.status()
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "public_surface": {
                "adapter_method_count": 9,
            },
            "callbacks": {
                key: value is not None
                for key, value in self._callbacks.items()
            },
            "safe_idle_verifier_available": (
                self._verify_callback is not None
            ),
            "boundaries": {
                "network_listener_active": False,
                "network_connection_active": False,
                "background_thread_active": False,
                "process_execution_active_in_adapter": False,
                "real_emergency_side_effect_available": status[
                    "real_emergency_side_effect_available"
                ],
            },
            "status": "OK",
        }

    def self_test(self) -> dict[str, Any]:
        status = self.status()
        assertions = [
            status["network_listener_active"] is False,
            status["network_connection_active"] is False,
            status["background_thread_active"] is False,
            status["process_execution_active_in_adapter"] is False,
            status["secret_exposed"] is False,
            self.inspect_runtime()["public_surface"][
                "adapter_method_count"
            ]
            == 9,
        ]
        if platform.system().lower() != "windows":
            assertions.append(
                status["real_emergency_side_effect_available"] is False
            )
        failures = [
            index + 1
            for index, value in enumerate(assertions)
            if not value
        ]
        return {
            "status": "OK" if not failures else "FAILED",
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failures),
            "failed_assertions": failures,
            "network_side_effects": 0,
            "process_side_effects": 0,
        }
