from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib import error, parse, request
import json
import os
import socket
import time

from aura.atlas_resource_monitoring.aura_atlas_resource_monitoring_planner import (
    AuraAtlasResourceMonitoringPlanner,
)
from aura.local_model_router_activation.local_model_router_activation_contract import (
    LocalModelRouterActivationContract,
)
from aura.local_model_service_discovery_health.local_model_service_discovery_health_contract import (
    LocalModelServiceDiscoveryHealthContract,
)
from aura.resource_baseline_metrics.aura_resource_baseline_metrics_planner import (
    AuraResourceBaselineMetricsPlanner,
)


@dataclass(frozen=True)
class LifecycleTransportResponse:
    status_code: int
    headers: Mapping[str, str]
    body: bytes


LifecycleTransport = Callable[
    [str, str, bytes | None, Mapping[str, str], float],
    LifecycleTransportResponse,
]


class ModelLifecycleQueueBudgetError(RuntimeError):
    "Base Sprint 259 runtime error."


class ModelLifecyclePermissionError(ModelLifecycleQueueBudgetError):
    "Missing explicit lifecycle or queue permission."


class ModelLifecycleHealthError(ModelLifecycleQueueBudgetError):
    "Provider health is unverified."


class ModelResourceBudgetError(ModelLifecycleQueueBudgetError):
    "Read-only resource budget denied work."


class ModelQueueFullError(ModelLifecycleQueueBudgetError):
    "Bounded queue is full."


class ModelQueueTimeoutError(ModelLifecycleQueueBudgetError):
    "Queue item expired."


class ModelQueueBusyError(ModelLifecycleQueueBudgetError):
    "Single in-flight slot is occupied."


class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


class UrllibLifecycleTransport:
    MAX_RESPONSE_BYTES = 1024 * 1024

    @staticmethod
    def validate_loopback(url: str) -> None:
        parsed = parse.urlsplit(url)
        if parsed.scheme != "http":
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle transport requires HTTP loopback."
            )
        if (
            parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or parsed.port is None
        ):
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle endpoint contains forbidden URL fields."
            )
        if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle endpoint must be loopback."
            )
        records = socket.getaddrinfo(
            parsed.hostname,
            parsed.port,
            type=socket.SOCK_STREAM,
        )
        if not records:
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle endpoint did not resolve."
            )
        for record in records:
            address = record[4][0]
            if not (address.startswith("127.") or address == "::1"):
                raise ModelLifecycleQueueBudgetError(
                    "Lifecycle endpoint resolved outside loopback."
                )

    def __call__(
        self,
        method: str,
        url: str,
        body: bytes | None,
        headers: Mapping[str, str],
        timeout_seconds: float,
    ) -> LifecycleTransportResponse:
        self.validate_loopback(url)
        if method not in {"GET", "POST"}:
            raise ModelLifecycleQueueBudgetError(
                "Unsupported lifecycle HTTP method."
            )
        opener = request.build_opener(
            request.ProxyHandler({}),
            _NoRedirect(),
        )
        req = request.Request(
            url=url,
            data=body,
            headers=dict(headers),
            method=method,
        )
        try:
            with opener.open(req, timeout=timeout_seconds) as response:
                payload = response.read(self.MAX_RESPONSE_BYTES + 1)
                if len(payload) > self.MAX_RESPONSE_BYTES:
                    raise ModelLifecycleQueueBudgetError(
                        "Lifecycle response exceeds limit."
                    )
                return LifecycleTransportResponse(
                    status_code=int(response.status),
                    headers=dict(response.headers.items()),
                    body=payload,
                )
        except error.HTTPError as exc:
            payload = exc.read(self.MAX_RESPONSE_BYTES + 1)
            return LifecycleTransportResponse(
                status_code=int(exc.code),
                headers=dict(exc.headers.items()),
                body=payload[: self.MAX_RESPONSE_BYTES],
            )
        except (error.URLError, TimeoutError, OSError) as exc:
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle transport failed."
            ) from exc


class BoundedModelLifecycleQueue:
    MAX_DEPTH = 4
    MAX_INFLIGHT = 1
    TIMEOUT_SECONDS = 120.0

    def __init__(self) -> None:
        self._items: deque[dict[str, Any]] = deque()
        self._inflight = 0

    def status(self) -> dict[str, Any]:
        return {
            "mode": "bounded_in_memory_single_process",
            "enabled_by_default": False,
            "depth": len(self._items),
            "max_depth": self.MAX_DEPTH,
            "inflight": self._inflight,
            "max_inflight": self.MAX_INFLIGHT,
            "timeout_seconds": self.TIMEOUT_SECONDS,
            "persistent": False,
            "background_worker": False,
            "cross_process_queue": False,
        }

    def enqueue(
        self,
        item: Mapping[str, Any],
        *,
        now: float | None = None,
    ) -> dict[str, Any]:
        if len(self._items) >= self.MAX_DEPTH:
            raise ModelQueueFullError("Model lifecycle queue is full.")
        created = time.monotonic() if now is None else float(now)
        packet = {
            "queue_id": str(item["queue_id"]),
            "action": str(item["action"]),
            "created_at": created,
            "expires_at": created + self.TIMEOUT_SECONDS,
        }
        self._items.append(packet)
        return {
            "accepted": True,
            "queue_id": packet["queue_id"],
            "depth": len(self._items),
            "persistent": False,
        }

    def process_next(
        self,
        handler: Callable[[dict[str, Any]], dict[str, Any]],
        *,
        now: float | None = None,
    ) -> dict[str, Any]:
        if self._inflight >= self.MAX_INFLIGHT:
            raise ModelQueueBusyError(
                "Model lifecycle in-flight slot is busy."
            )
        if not self._items:
            raise ModelLifecycleQueueBudgetError(
                "Model lifecycle queue is empty."
            )
        current = time.monotonic() if now is None else float(now)
        item = self._items.popleft()
        if current > item["expires_at"]:
            raise ModelQueueTimeoutError(
                "Model lifecycle queue item expired."
            )
        self._inflight += 1
        try:
            result = handler(item)
        finally:
            self._inflight -= 1
        return {
            "queue_id": item["queue_id"],
            "status": "completed",
            "result": result,
            "persistent": False,
        }


class ModelLifecycleQueueBudgetContract:
    VERSION = "1.1.9"
    SPRINT = 259
    LIFECYCLE_CONFIRMATION_TOKEN = "MANAGE_LOCAL_MODEL_LIFECYCLE"
    QUEUE_CONFIRMATION_TOKEN = "QUEUE_LOCAL_MODEL_LIFECYCLE"
    DEFAULT_KEEP_ALIVE = "5m"
    MEMORY_RESERVE_RATIO = 0.20
    MAX_SWAP_USED_RATIO = 0.50
    MAX_NORMALIZED_LOAD_1M = 1.0

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.router = LocalModelRouterActivationContract(
            project_root=self.project_root
        )
        self.health = LocalModelServiceDiscoveryHealthContract(
            project_root=self.project_root
        )

    def provider_profile(self) -> dict[str, Any]:
        profile = self.router.profile_mapping()
        return {
            "provider": profile["provider"],
            "base_url": profile["base_url"],
            "model": profile["model"],
            "timeout_seconds": min(
                float(profile["timeout_seconds"]),
                120.0,
            ),
            "loopback_only": True,
            "credentials_read": False,
            "persistent_configuration_write": False,
        }

    @staticmethod
    def _meminfo() -> dict[str, int]:
        packet: dict[str, int] = {}
        for line in Path("/proc/meminfo").read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines():
            if ":" not in line:
                continue
            key, raw = line.split(":", 1)
            fields = raw.strip().split()
            if not fields:
                continue
            try:
                value = int(fields[0])
            except ValueError:
                continue
            if len(fields) > 1 and fields[1].lower() == "kb":
                value *= 1024
            packet[key] = value
        return packet

    def resource_budget_preview(self) -> dict[str, Any]:
        info = self._meminfo()
        total = info.get("MemTotal", 0)
        available = info.get("MemAvailable", 0)
        swap_total = info.get("SwapTotal", 0)
        swap_free = info.get("SwapFree", 0)
        cpu_count = max(int(os.cpu_count() or 1), 1)
        load_1m, load_5m, load_15m = os.getloadavg()
        memory_ratio = available / total if total else 0.0
        swap_used_ratio = (
            (swap_total - swap_free) / swap_total
            if swap_total
            else 0.0
        )
        normalized_load = load_1m / cpu_count
        baseline_status = AuraResourceBaselineMetricsPlanner(
            self.project_root
        ).status()
        monitor_status = AuraAtlasResourceMonitoringPlanner(
            self.project_root
        ).status()
        denials = []
        if memory_ratio < self.MEMORY_RESERVE_RATIO:
            denials.append("memory_reserve_below_policy")
        if swap_used_ratio > self.MAX_SWAP_USED_RATIO:
            denials.append("swap_guard_exceeded")
        if normalized_load > self.MAX_NORMALIZED_LOAD_1M:
            denials.append("load_average_guard_exceeded")
        if baseline_status.get("status_valid") is not True:
            denials.append("resource_baseline_invalid")
        if monitor_status.get("status_valid") is not True:
            denials.append("atlas_monitor_invalid")
        return {
            "approved": not denials,
            "denial_reasons": denials,
            "cpu_count": cpu_count,
            "load_1m": round(load_1m, 4),
            "load_5m": round(load_5m, 4),
            "load_15m": round(load_15m, 4),
            "normalized_load_1m": round(normalized_load, 6),
            "max_normalized_load_1m": self.MAX_NORMALIZED_LOAD_1M,
            "memory_total_bytes": total,
            "memory_available_bytes": available,
            "memory_available_ratio": round(memory_ratio, 6),
            "memory_reserve_ratio": self.MEMORY_RESERVE_RATIO,
            "swap_total_bytes": swap_total,
            "swap_free_bytes": swap_free,
            "swap_used_ratio": round(swap_used_ratio, 6),
            "max_swap_used_ratio": self.MAX_SWAP_USED_RATIO,
            "gpu_optional": True,
            "gpu_required": False,
            "vram_guard_when_available": True,
            "baseline_owner": "AuraResourceBaselineMetricsPlanner",
            "baseline_status_valid": (
                baseline_status.get("status_valid") is True
            ),
            "monitor_owner": "AuraAtlasResourceMonitoringPlanner",
            "monitor_status_valid": (
                monitor_status.get("status_valid") is True
            ),
            "threshold_mutated": False,
            "budget_persisted": False,
        }

    def lifecycle_preview(self, action: str) -> dict[str, Any]:
        normalized = action.strip().lower()
        if normalized not in {"load", "status", "release"}:
            raise ModelLifecycleQueueBudgetError(
                "Lifecycle action must be load, status, or release."
            )
        profile = self.provider_profile()
        budget = self.resource_budget_preview()
        host = self.health.host_posture()
        return {
            "action": normalized,
            "provider": profile["provider"],
            "base_url": profile["base_url"],
            "model": profile["model"],
            "provider_state": host["state"],
            "resource_budget_approved": budget["approved"],
            "permission_required": True,
            "confirmation_token": self.LIFECYCLE_CONFIRMATION_TOKEN,
            "health_verification_required": True,
            "load_semantics": "provider_managed_keep_alive",
            "release_semantics": "explicit_provider_release",
            "keep_alive": (
                self.DEFAULT_KEEP_ALIVE
                if normalized == "load"
                else (0 if normalized == "release" else None)
            ),
            "execution_ready": False,
            "network_connection_opened": False,
            "model_lifecycle_executed": False,
            "model_downloaded": False,
            "model_pulled": False,
            "service_mutated": False,
        }

    def queue_preview(self) -> dict[str, Any]:
        return {
            **BoundedModelLifecycleQueue().status(),
            "confirmation_required": True,
            "confirmation_token": self.QUEUE_CONFIRMATION_TOKEN,
            "queue_mutated": False,
            "queue_item_created": False,
        }

    def _endpoint(self, path: str) -> str:
        url = self.provider_profile()["base_url"].rstrip("/") + path
        UrllibLifecycleTransport.validate_loopback(url)
        return url

    @staticmethod
    def _decode(response: LifecycleTransportResponse) -> dict[str, Any]:
        if not 200 <= response.status_code < 300:
            raise ModelLifecycleQueueBudgetError(
                "Provider lifecycle request failed."
            )
        try:
            packet = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelLifecycleQueueBudgetError(
                "Provider lifecycle response is invalid."
            ) from exc
        if not isinstance(packet, dict):
            raise ModelLifecycleQueueBudgetError(
                "Provider lifecycle response must be an object."
            )
        return packet

    def execute_lifecycle(
        self,
        *,
        action: str,
        provider_health_verified: bool,
        resource_budget_approved: bool,
        confirm_lifecycle: bool,
        confirmation_token: str,
        transport: LifecycleTransport | None = None,
    ) -> dict[str, Any]:
        if (
            confirm_lifecycle is not True
            or confirmation_token != self.LIFECYCLE_CONFIRMATION_TOKEN
        ):
            raise ModelLifecyclePermissionError(
                "Lifecycle execution requires exact confirmation."
            )
        if provider_health_verified is not True:
            raise ModelLifecycleHealthError(
                "Provider health must be verified."
            )
        budget = self.resource_budget_preview()
        if (
            resource_budget_approved is not True
            or budget["approved"] is not True
        ):
            raise ModelResourceBudgetError(
                "Resource budget denied lifecycle execution."
            )
        preview = self.lifecycle_preview(action)
        profile = self.provider_profile()
        normalized = preview["action"]
        active_transport = transport or UrllibLifecycleTransport()
        if normalized == "status":
            method = "GET"
            url = self._endpoint("/api/ps")
            body = None
        else:
            method = "POST"
            url = self._endpoint("/api/generate")
            body = json.dumps(
                {
                    "model": profile["model"],
                    "prompt": "",
                    "stream": False,
                    "keep_alive": (
                        self.DEFAULT_KEEP_ALIVE
                        if normalized == "load"
                        else 0
                    ),
                },
                separators=(",", ":"),
            ).encode("utf-8")
        packet = self._decode(
            active_transport(
                method,
                url,
                body,
                {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                profile["timeout_seconds"],
            )
        )
        model_count = None
        configured_reported = None
        if normalized == "status":
            models = packet.get("models")
            if not isinstance(models, list):
                raise ModelLifecycleQueueBudgetError(
                    "Provider status response lacks models list."
                )
            model_count = len(models)
            configured_reported = any(
                isinstance(item, dict)
                and item.get("name") == profile["model"]
                for item in models
            )
        return {
            "status": "completed",
            "version": self.VERSION,
            "sprint": self.SPRINT,
            "action": normalized,
            "provider": profile["provider"],
            "model": profile["model"],
            "provider_health_verified": True,
            "resource_budget_verified": True,
            "lifecycle_permission_verified": True,
            "network_connection_opened": True,
            "loopback_only": True,
            "provider_model_count": model_count,
            "configured_model_reported": configured_reported,
            "provider_model_names_exposed": False,
            "model_downloaded": False,
            "model_pulled": False,
            "service_started": False,
            "service_stopped": False,
            "queue_persisted": False,
            "resource_budget_mutated": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }

    def execute_queued_lifecycle(
        self,
        *,
        action: str,
        provider_health_verified: bool,
        resource_budget_approved: bool,
        confirm_queue: bool,
        queue_confirmation_token: str,
        confirm_lifecycle: bool,
        lifecycle_confirmation_token: str,
        transport: LifecycleTransport,
    ) -> dict[str, Any]:
        if (
            confirm_queue is not True
            or queue_confirmation_token != self.QUEUE_CONFIRMATION_TOKEN
        ):
            raise ModelLifecyclePermissionError(
                "Queue submission requires exact confirmation."
            )
        queue = BoundedModelLifecycleQueue()
        queue.enqueue(
            {
                "queue_id": "modelqueue_sprint259",
                "action": action,
            }
        )
        return queue.process_next(
            lambda item: self.execute_lifecycle(
                action=item["action"],
                provider_health_verified=provider_health_verified,
                resource_budget_approved=resource_budget_approved,
                confirm_lifecycle=confirm_lifecycle,
                confirmation_token=lifecycle_confirmation_token,
                transport=transport,
            )
        )

    def isolated_rehearsal(self) -> dict[str, Any]:
        class FakeTransport:
            def __init__(self) -> None:
                self.responses: deque[LifecycleTransportResponse] = deque()
                self.calls: list[dict[str, Any]] = []

            def queue(self, payload: Mapping[str, Any]) -> None:
                self.responses.append(
                    LifecycleTransportResponse(
                        status_code=200,
                        headers={"Content-Type": "application/json"},
                        body=json.dumps(dict(payload)).encode("utf-8"),
                    )
                )

            def __call__(
                self,
                method: str,
                url: str,
                body: bytes | None,
                headers: Mapping[str, str],
                timeout_seconds: float,
            ) -> LifecycleTransportResponse:
                self.calls.append(
                    {
                        "method": method,
                        "url": url,
                        "payload": (
                            json.loads(body.decode("utf-8"))
                            if body is not None
                            else None
                        ),
                    }
                )
                if not self.responses:
                    raise RuntimeError(
                        "Fake lifecycle response queue is empty."
                    )
                return self.responses.popleft()

        denied_permission = denied_health = denied_budget = False
        fake = FakeTransport()
        fake.queue({"done": True})
        try:
            self.execute_lifecycle(
                action="load",
                provider_health_verified=True,
                resource_budget_approved=True,
                confirm_lifecycle=False,
                confirmation_token="",
                transport=fake,
            )
        except ModelLifecyclePermissionError:
            denied_permission = True
        try:
            self.execute_lifecycle(
                action="load",
                provider_health_verified=False,
                resource_budget_approved=True,
                confirm_lifecycle=True,
                confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
                transport=fake,
            )
        except ModelLifecycleHealthError:
            denied_health = True
        try:
            self.execute_lifecycle(
                action="load",
                provider_health_verified=True,
                resource_budget_approved=False,
                confirm_lifecycle=True,
                confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
                transport=fake,
            )
        except ModelResourceBudgetError:
            denied_budget = True

        load = self.execute_lifecycle(
            action="load",
            provider_health_verified=True,
            resource_budget_approved=True,
            confirm_lifecycle=True,
            confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
            transport=fake,
        )
        fake.queue(
            {"models": [{"name": self.provider_profile()["model"]}]}
        )
        status = self.execute_lifecycle(
            action="status",
            provider_health_verified=True,
            resource_budget_approved=True,
            confirm_lifecycle=True,
            confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
            transport=fake,
        )
        fake.queue({"done": True})
        release = self.execute_lifecycle(
            action="release",
            provider_health_verified=True,
            resource_budget_approved=True,
            confirm_lifecycle=True,
            confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
            transport=fake,
        )

        full = timeout = busy = False
        queue = BoundedModelLifecycleQueue()
        for index in range(4):
            queue.enqueue(
                {"queue_id": f"q{index}", "action": "status"},
                now=10.0,
            )
        try:
            queue.enqueue(
                {"queue_id": "overflow", "action": "status"},
                now=10.0,
            )
        except ModelQueueFullError:
            full = True
        timeout_queue = BoundedModelLifecycleQueue()
        timeout_queue.enqueue(
            {"queue_id": "timeout", "action": "status"},
            now=10.0,
        )
        try:
            timeout_queue.process_next(
                lambda item: {"ok": True},
                now=131.0,
            )
        except ModelQueueTimeoutError:
            timeout = True
        busy_queue = BoundedModelLifecycleQueue()
        busy_queue.enqueue(
            {"queue_id": "busy", "action": "status"}
        )
        busy_queue._inflight = 1
        try:
            busy_queue.process_next(lambda item: {"ok": True})
        except ModelQueueBusyError:
            busy = True
        finally:
            busy_queue._inflight = 0

        queue_fake = FakeTransport()
        queue_fake.queue({"done": True})
        queued = self.execute_queued_lifecycle(
            action="load",
            provider_health_verified=True,
            resource_budget_approved=True,
            confirm_queue=True,
            queue_confirmation_token=self.QUEUE_CONFIRMATION_TOKEN,
            confirm_lifecycle=True,
            lifecycle_confirmation_token=self.LIFECYCLE_CONFIRMATION_TOKEN,
            transport=queue_fake,
        )

        load_call, status_call, release_call = fake.calls
        return {
            "denied_without_permission": denied_permission,
            "denied_without_health": denied_health,
            "denied_without_budget": denied_budget,
            "load_completed": load["action"] == "load",
            "status_completed": status["action"] == "status",
            "release_completed": release["action"] == "release",
            "load_method": load_call["method"],
            "load_path": load_call["url"].split(":11434", 1)[-1],
            "load_keep_alive": load_call["payload"]["keep_alive"],
            "status_method": status_call["method"],
            "status_path": status_call["url"].split(":11434", 1)[-1],
            "release_method": release_call["method"],
            "release_path": release_call["url"].split(":11434", 1)[-1],
            "release_keep_alive": release_call["payload"]["keep_alive"],
            "provider_model_count": status["provider_model_count"],
            "configured_model_reported": status[
                "configured_model_reported"
            ],
            "provider_model_names_exposed": False,
            "queue_full_denied": full,
            "queue_timeout_denied": timeout,
            "queue_busy_denied": busy,
            "queued_lifecycle_completed": queued["status"] == "completed",
            "queue_persisted": False,
            "background_worker_started": False,
            "canonical_network_opened": False,
            "canonical_data_mutated": False,
            "canonical_session_mutated": False,
            "model_downloaded": False,
            "model_pulled": False,
            "service_mutated": False,
            "resource_budget_mutated": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }
