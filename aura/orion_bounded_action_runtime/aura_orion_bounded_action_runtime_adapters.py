"""Injected platform adapters for Sprint 278 bounded ORION actions.

The core manager never imports Windows, capture, OBS, or process-launch
dependencies. Real side effects exist only behind an explicitly injected
adapter. The default adapter is non-executing and fails closed.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable


class OrionBoundedActionAdapterError(RuntimeError):
    """Raised when a bounded platform adapter cannot safely continue."""


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
        raise OrionBoundedActionAdapterError(
            "Adapter payload is not canonicalizable."
        ) from exc


def _digest(payload: Any) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            value.update(chunk)
    return value.hexdigest()


def _result(
    *,
    adapter_id: str,
    adapter_version: str,
    action_type: str,
    success: bool,
    execution_performed: bool,
    result_code: str,
    artifacts: list[dict[str, Any]] | None = None,
    redacted_message: str = "",
    metadata: dict[str, Any] | None = None,
    duration_ms: int = 0,
) -> dict[str, Any]:
    artifact_list = [] if artifacts is None else artifacts
    metadata_value = {} if metadata is None else metadata
    result = {
        "schema_version": "1",
        "adapter_id": adapter_id,
        "adapter_version": adapter_version,
        "action_type": action_type,
        "success": bool(success),
        "execution_performed": bool(execution_performed),
        "result_code": str(result_code),
        "result_digest": "",
        "artifacts": artifact_list,
        "redacted_message": str(redacted_message),
        "metadata_digest": _digest(metadata_value),
        "duration_ms": max(0, int(duration_ms)),
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
class AuraOrionBoundedActionAdapter(Protocol):
    """Public adapter protocol. Every action receives sanitized internal data."""

    def capture_single_screenshot(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def capture_selected_window(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def open_allowlisted_application(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def create_controlled_file(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def create_controlled_folder(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def obs_start_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def obs_stop_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def obs_switch_scene(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def status(self) -> dict[str, Any]:
        ...

    def inspect_runtime(self) -> dict[str, Any]:
        ...

    def self_test(self) -> dict[str, Any]:
        ...


class AuraNonExecutingOrionBoundedActionAdapter:
    """Default adapter that never performs an operating-system action."""

    ADAPTER_ID = "orion-non-executing"
    ADAPTER_VERSION = "0.1.0"
    MODE = "non_executing"

    def _deny(self, action: dict[str, Any]) -> dict[str, Any]:
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action.get("action_type", "unknown")),
            success=False,
            execution_performed=False,
            result_code="adapter_non_executing",
            redacted_message=(
                "No authorized real ORION adapter was injected."
            ),
        )

    def capture_single_screenshot(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def capture_selected_window(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def open_allowlisted_application(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def create_controlled_file(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def create_controlled_folder(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def obs_start_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def obs_stop_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def obs_switch_scene(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._deny(action)

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": False,
            "platform": platform.system().lower(),
            "real_execution_available": False,
            "network_listener_active": False,
            "network_connection_active": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "supported_actions": [],
            "real_execution_available": False,
            "default_adapter": True,
            "fail_closed": True,
            "network_listener_active": False,
            "network_connection_active": False,
        }

    def self_test(self) -> dict[str, Any]:
        sample = {
            "action_type": "capture_single_screenshot",
        }
        result = self.capture_single_screenshot(sample)
        assert result["success"] is False
        assert result["execution_performed"] is False
        return {
            "status": "OK",
            "assertion_count": 2,
            "failed_assertion_count": 0,
            "real_execution_performed": False,
            "network_side_effects": 0,
        }


class AuraFakeOrionBoundedActionAdapter:
    """Deterministic fake adapter used only by isolated tests and acceptance."""

    ADAPTER_ID = "orion-fake-test"
    ADAPTER_VERSION = "0.1.0"
    MODE = "fake_test"
    PNG_BYTES = (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\rIHDR"
        b"\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDAT\x08\xd7c\xf8\xcf\xc0\xf0\x1f\x00"
        b"\x05\x00\x01\xff\x89\x99=\x1d"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    def __init__(
        self,
        *,
        fail_actions: set[str] | None = None,
    ) -> None:
        self._fail_actions = set() if fail_actions is None else set(
            fail_actions
        )
        self._recording = False
        self._scene = "default"
        self._calls: list[str] = []

    def _maybe_fail(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any] | None:
        action_type = str(action["action_type"])
        self._calls.append(action_type)
        if action_type not in self._fail_actions:
            return None
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=action_type,
            success=False,
            execution_performed=False,
            result_code="fake_requested_failure",
            redacted_message="The fake adapter returned a bounded failure.",
            duration_ms=1,
        )

    def _write_capture(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        output_path = Path(action["resolved"]["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("xb") as stream:
            stream.write(self.PNG_BYTES)
            stream.flush()
            os.fsync(stream.fileno())
        artifact = {
            "artifact_type": "image/png",
            "path": str(output_path),
            "sha256": _file_digest(output_path),
            "size_bytes": output_path.stat().st_size,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_capture_created",
            artifacts=[artifact],
            redacted_message="A fake bounded PNG artifact was created.",
            metadata={"fake": True},
            duration_ms=1,
        )

    def capture_single_screenshot(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._write_capture(action)

    def capture_selected_window(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._write_capture(action)

    def open_allowlisted_application(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        logical_id = str(action["resolved"]["logical_application_id"])
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_application_opened",
            redacted_message="A fake allowlisted application was opened.",
            metadata={
                "logical_application_id": logical_id,
                "process_identity": f"fake-process:{logical_id}",
            },
            duration_ms=1,
        )

    def create_controlled_file(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        output_path = Path(action["resolved"]["output_path"])
        content = action["resolved"]["content_bytes"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        artifact = {
            "artifact_type": "application/octet-stream",
            "path": str(output_path),
            "sha256": _file_digest(output_path),
            "size_bytes": output_path.stat().st_size,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_file_created",
            artifacts=[artifact],
            redacted_message="A fake controlled file was created.",
            metadata={"fake": True},
            duration_ms=1,
        )

    def create_controlled_folder(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        output_path = Path(action["resolved"]["output_path"])
        output_path.mkdir(parents=True, exist_ok=False)
        artifact = {
            "artifact_type": "inode/directory",
            "path": str(output_path),
            "sha256": _digest({"directory": str(output_path)}),
            "size_bytes": 0,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_folder_created",
            artifacts=[artifact],
            redacted_message="A fake controlled folder was created.",
            metadata={"fake": True},
            duration_ms=1,
        )

    def obs_start_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        if self._recording:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                action_type=str(action["action_type"]),
                success=False,
                execution_performed=False,
                result_code="already_recording",
                redacted_message="OBS recording is already active.",
                duration_ms=1,
            )
        self._recording = True
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_obs_recording_started",
            redacted_message="Fake OBS recording state is active.",
            metadata={"recording": True},
            duration_ms=1,
        )

    def obs_stop_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        if not self._recording:
            return _result(
                adapter_id=self.ADAPTER_ID,
                adapter_version=self.ADAPTER_VERSION,
                action_type=str(action["action_type"]),
                success=False,
                execution_performed=False,
                result_code="not_recording",
                redacted_message="OBS recording is not active.",
                duration_ms=1,
            )
        self._recording = False
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_obs_recording_stopped",
            redacted_message="Fake OBS recording state is inactive.",
            metadata={"recording": False},
            duration_ms=1,
        )

    def obs_switch_scene(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        failed = self._maybe_fail(action)
        if failed is not None:
            return failed
        self._scene = str(action["resolved"]["scene_name"])
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="fake_obs_scene_switched",
            redacted_message="The fake OBS scene was switched.",
            metadata={"scene_digest": _digest(self._scene)},
            duration_ms=1,
        )

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": True,
            "platform": "test",
            "real_execution_available": False,
            "fake_execution_available": True,
            "recording": self._recording,
            "scene_digest": _digest(self._scene),
            "call_count": len(self._calls),
            "network_listener_active": False,
            "network_connection_active": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "supported_actions": [
                "capture_single_screenshot",
                "capture_selected_window",
                "open_allowlisted_application",
                "create_controlled_file",
                "create_controlled_folder",
                "obs_start_recording",
                "obs_stop_recording",
                "obs_switch_scene",
            ],
            "fake_only": True,
            "call_count": len(self._calls),
            "fail_actions": sorted(self._fail_actions),
            "network_listener_active": False,
            "network_connection_active": False,
        }

    def self_test(self) -> dict[str, Any]:
        status = self.status()
        assert status["mode"] == self.MODE
        assert status["real_execution_available"] is False
        return {
            "status": "OK",
            "assertion_count": 2,
            "failed_assertion_count": 0,
            "real_execution_performed": False,
            "fake_execution_only": True,
            "network_side_effects": 0,
        }


class AuraWindowsOrionBoundedActionAdapter:
    """Guarded Windows adapter for explicitly authorized ORION use.

    Capture callbacks and the OBS controller are injected. Application launch
    uses ``subprocess.Popen`` with ``shell=False`` and an absolute executable
    path that was resolved by the core manager from a logical allowlist ID.
    """

    ADAPTER_ID = "orion-windows-authorized"
    ADAPTER_VERSION = "0.1.0"
    MODE = "windows_authorized"

    def __init__(
        self,
        *,
        enabled: bool,
        screen_capture_callback: Callable[[dict[str, Any]], bytes] | None = None,
        window_capture_callback: Callable[[dict[str, Any]], bytes] | None = None,
        obs_controller: Any = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._screen_capture_callback = screen_capture_callback
        self._window_capture_callback = window_capture_callback
        self._obs_controller = obs_controller

    def _guard(self) -> None:
        if not self._enabled:
            raise OrionBoundedActionAdapterError(
                "The Windows adapter is disabled."
            )
        if platform.system().lower() != "windows":
            raise OrionBoundedActionAdapterError(
                "The Windows adapter can only run on Windows."
            )

    def _write_png(
        self,
        action: dict[str, Any],
        callback: Callable[[dict[str, Any]], bytes] | None,
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        if callback is None:
            raise OrionBoundedActionAdapterError(
                "An explicit capture callback is required."
            )
        raw = callback(action)
        if not isinstance(raw, bytes) or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            raise OrionBoundedActionAdapterError(
                "Capture callback must return PNG bytes."
            )
        maximum = int(action["limits"]["max_capture_bytes"])
        if len(raw) > maximum:
            raise OrionBoundedActionAdapterError(
                "Capture output exceeds the configured byte limit."
            )
        output_path = Path(action["resolved"]["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        artifact = {
            "artifact_type": "image/png",
            "path": str(output_path),
            "sha256": _file_digest(output_path),
            "size_bytes": output_path.stat().st_size,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="capture_created",
            artifacts=[artifact],
            redacted_message="A bounded PNG capture was created.",
            metadata={"capture_mode": action["action_type"]},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def capture_single_screenshot(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._write_png(action, self._screen_capture_callback)

    def capture_selected_window(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        return self._write_png(action, self._window_capture_callback)

    def open_allowlisted_application(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        executable = Path(action["resolved"]["executable_path"])
        if not executable.is_absolute() or executable.is_symlink():
            raise OrionBoundedActionAdapterError(
                "Allowlisted executable must be an absolute non-symlink path."
            )
        if not executable.is_file():
            raise OrionBoundedActionAdapterError(
                "Allowlisted executable does not exist."
            )
        process = subprocess.Popen(
            [str(executable)],
            shell=False,
            close_fds=True,
        )
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="application_opened",
            redacted_message="An allowlisted application was opened.",
            metadata={
                "logical_application_id": action["resolved"][
                    "logical_application_id"
                ],
                "process_id": int(process.pid),
            },
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def create_controlled_file(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        output_path = Path(action["resolved"]["output_path"])
        content = action["resolved"]["content_bytes"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        artifact = {
            "artifact_type": "application/octet-stream",
            "path": str(output_path),
            "sha256": _file_digest(output_path),
            "size_bytes": output_path.stat().st_size,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="controlled_file_created",
            artifacts=[artifact],
            redacted_message="A controlled file was created.",
            metadata={"bounded": True},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def create_controlled_folder(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        output_path = Path(action["resolved"]["output_path"])
        output_path.mkdir(parents=True, exist_ok=False)
        artifact = {
            "artifact_type": "inode/directory",
            "path": str(output_path),
            "sha256": _digest({"directory": str(output_path)}),
            "size_bytes": 0,
        }
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="controlled_folder_created",
            artifacts=[artifact],
            redacted_message="A controlled folder was created.",
            metadata={"bounded": True},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def obs_start_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        if self._obs_controller is None:
            raise OrionBoundedActionAdapterError(
                "A dedicated OBS controller is required."
            )
        value = self._obs_controller.start_recording()
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="obs_recording_started",
            redacted_message="OBS recording was started.",
            metadata={"controller_result_digest": _digest(value)},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def obs_stop_recording(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        if self._obs_controller is None:
            raise OrionBoundedActionAdapterError(
                "A dedicated OBS controller is required."
            )
        value = self._obs_controller.stop_recording()
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="obs_recording_stopped",
            redacted_message="OBS recording was stopped.",
            metadata={"controller_result_digest": _digest(value)},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def obs_switch_scene(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()
        self._guard()
        if self._obs_controller is None:
            raise OrionBoundedActionAdapterError(
                "A dedicated OBS controller is required."
            )
        value = self._obs_controller.switch_scene(
            str(action["resolved"]["scene_name"])
        )
        return _result(
            adapter_id=self.ADAPTER_ID,
            adapter_version=self.ADAPTER_VERSION,
            action_type=str(action["action_type"]),
            success=True,
            execution_performed=True,
            result_code="obs_scene_switched",
            redacted_message="The allowlisted OBS scene was switched.",
            metadata={"controller_result_digest": _digest(value)},
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    def status(self) -> dict[str, Any]:
        is_windows = platform.system().lower() == "windows"
        return {
            "status": "ready" if self._enabled and is_windows else "guarded",
            "adapter_id": self.ADAPTER_ID,
            "adapter_version": self.ADAPTER_VERSION,
            "mode": self.MODE,
            "enabled": self._enabled,
            "platform": platform.system().lower(),
            "real_execution_available": self._enabled and is_windows,
            "screen_capture_callback": (
                self._screen_capture_callback is not None
            ),
            "window_capture_callback": (
                self._window_capture_callback is not None
            ),
            "obs_controller": self._obs_controller is not None,
            "network_listener_active": False,
            "network_connection_active": False,
            "secret_exposed": False,
        }

    def inspect_runtime(self) -> dict[str, Any]:
        return {
            "component": {
                "adapter_id": self.ADAPTER_ID,
                "adapter_version": self.ADAPTER_VERSION,
                "mode": self.MODE,
            },
            "guarded": True,
            "expected_platform": "windows",
            "shell_allowed": False,
            "raw_commands_allowed": False,
            "capture_callback_required": True,
            "OBS_controller_required": True,
            "network_listener_active": False,
            "network_connection_owned_by_core": False,
        }

    def self_test(self) -> dict[str, Any]:
        status = self.status()
        assert status["mode"] == self.MODE
        assert status["network_listener_active"] is False
        assert status["network_connection_active"] is False
        return {
            "status": "OK",
            "assertion_count": 3,
            "failed_assertion_count": 0,
            "real_execution_performed": False,
            "network_side_effects": 0,
        }
