from __future__ import annotations

from pathlib import Path
from typing import Sequence
import json
import sys

from .session_list_resume_rename_archive_restore_planner import (
    SessionListResumeRenameArchiveRestorePlanner,
)


COMMANDS = {
    "session-list-resume-rename-archive-restore-status",
    "session-list-resume-rename-archive-restore-context",
    "session-list-resume-rename-archive-restore-check",
    "session-list-resume-rename-archive-restore-review",
    "session-list-resume-rename-archive-restore-preview",
    "session-list-resume-rename-archive-restore-runtime-status",
    "session-list-resume-rename-archive-restore-routes",
    "session-list-resume-rename-archive-restore-web-surface",
    "session-list-resume-rename-archive-restore-isolated-rehearsal",
}


def _safe_error(
    command: str,
    detail: str,
) -> dict[str, object]:
    return {
        "status": "error",
        "command": command,
        "detail": detail,
        "runtime_mutated": False,
    }


def handle_session_list_resume_rename_archive_restore_command(
    args: Sequence[str],
) -> bool:
    if not args:
        return False

    command = str(args[0])
    if command not in COMMANDS:
        return False

    if len(args) != 1:
        print(
            json.dumps(
                _safe_error(
                    command,
                    "This command does not accept arguments.",
                ),
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    planner = SessionListResumeRenameArchiveRestorePlanner(
        project_root=Path.cwd()
    )
    handlers = {
        "session-list-resume-rename-archive-restore-status":
            planner.status,
        "session-list-resume-rename-archive-restore-context":
            planner.context,
        "session-list-resume-rename-archive-restore-check":
            planner.check,
        "session-list-resume-rename-archive-restore-review":
            planner.review,
        "session-list-resume-rename-archive-restore-preview":
            planner.preview,
        "session-list-resume-rename-archive-restore-runtime-status":
            planner.runtime_status,
        "session-list-resume-rename-archive-restore-routes":
            planner.route_status,
        "session-list-resume-rename-archive-restore-web-surface":
            planner.web_surface_status,
        "session-list-resume-rename-archive-restore-isolated-rehearsal":
            planner.isolated_rehearsal,
    }

    print(
        json.dumps(
            handlers[command](),
            indent=2,
            sort_keys=True,
        )
    )
    return True
