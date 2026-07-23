"""CLI for Sprint 282 supported-game detection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .aura_supported_game_detection_orion_adapter import (
    AuraWindowsSupportedGameDetectionAdapter,
)
from .aura_supported_game_detection_runtime_manager import (
    AuraSupportedGameDetectionRuntimeManager,
    SupportedGameDetectionRuntimeError,
)


def _emit(payload: object) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aura-supported-game-detection",
        description=(
            "Inspect or explicitly invoke the read-only Sprint 282 "
            "supported-game detection boundary."
        ),
    )
    parser.add_argument(
        "--project-root",
        default=str(Path.cwd()),
        help="AURA project root.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")
    subparsers.add_parser("inspect")
    subparsers.add_parser("capability")
    subparsers.add_parser("self-test")

    fixture = subparsers.add_parser("review-fixture")
    fixture.add_argument("--agent-id", default="orion-agent")
    fixture.add_argument("--device-id", default="orion-device")

    scan = subparsers.add_parser("windows-scan")
    scan.add_argument("--agent-id", required=True)
    scan.add_argument("--device-id", required=True)
    scan.add_argument("--sequence", required=True, type=int)
    scan.add_argument(
        "--enable-read-only-scan",
        action="store_true",
        help="Required explicit gate for one Windows scan.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = AuraSupportedGameDetectionRuntimeManager(
        project_root=Path(args.project_root)
    )
    try:
        if args.command == "status":
            _emit(manager.status())
        elif args.command == "inspect":
            _emit(manager.inspect_runtime())
        elif args.command == "capability":
            _emit(manager.capability_declaration())
        elif args.command == "self-test":
            _emit(manager.self_test())
        elif args.command == "review-fixture":
            import hashlib
            from datetime import datetime, timezone

            now = datetime.now(timezone.utc)
            match = {
                "game_id": "osu_offline",
                "profile_version": "1",
                "executable_basename": "osu!.exe",
                "process_id": 4242,
                "visible_top_level_window": True,
                "window_title_sha256": hashlib.sha256(
                    b"osu! fixture"
                ).hexdigest(),
                "process_name_exact": True,
            }
            packet = manager.build_observation_packet(
                agent_id=args.agent_id,
                device_id=args.device_id,
                sequence=1,
                observed_at_utc=manager._format_utc(now),
                monotonic_ms=1,
                matches=[match],
            )
            _emit(
                manager.review_observation(
                    packet,
                    expected_agent_id=args.agent_id,
                    expected_device_id=args.device_id,
                )
            )
        elif args.command == "windows-scan":
            if not args.enable_read_only_scan:
                raise SupportedGameDetectionRuntimeError(
                    "--enable-read-only-scan is required."
                )
            adapter = AuraWindowsSupportedGameDetectionAdapter(
                manager=manager,
                enabled=True,
            )
            _emit(
                adapter.scan_once(
                    agent_id=args.agent_id,
                    device_id=args.device_id,
                    sequence=args.sequence,
                )
            )
        else:
            raise SupportedGameDetectionRuntimeError(
                f"unsupported command: {args.command}"
            )
    except SupportedGameDetectionRuntimeError as exc:
        _emit(
            {
                "status": "FAILED",
                "error": str(exc),
                "safe_idle": True,
                "capture_started": False,
                "recording_started": False,
                "game_input_control_started": False,
            }
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
