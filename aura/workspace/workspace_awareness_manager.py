from pathlib import Path
from typing import Any

import yaml

from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager


class WorkspaceAwarenessManager:
    """
    AURA Workspace Awareness Foundation.

    Current phase:
    - read project identity
    - read safe workspace structure
    - identify important project files
    - identify ignored/runtime directories
    - infer current sprint from journal
    - prepare workspace map and workspace context
    - no file writes
    - no memory writes
    - no journal writes
    - no command execution
    """

    name = "workspace_awareness"
    version = "0.1.0"
    status_name = "online"

    DEFAULT_IGNORED_DIRS = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "data",
        "logs",
    }

    IMPORTANT_FILE_CANDIDATES = [
        "README.md",
        "main.py",
        "requirements.txt",
        ".gitignore",
        "aura/personality/identity.yaml",
        "aura/config/settings.yaml",
        "aura/core/cli.py",
        "aura/core/shell.py",
        "aura/status/system_status_manager.py",
        "aura/partner/partner_alpha_manager.py",
        "aura/project_coding/project_coding_manager.py",
        "aura/plugins/builtin/plugin_actions.py",
        "aura/skills/builtin_skills.py",
        "docs/AURA_MASTER_ROADMAP.md",
        "docs/AURA_PRODUCT_VISION.md",
    ]

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.gitignore_path = self.project_root / ".gitignore"

        self.memory_store = MemoryStore(project_root=self.project_root)
        self.project_journal = ProjectJournal(project_root=self.project_root)
        self.memory_reflection = MemoryReflectionManager(project_root=self.project_root)
        self.project_coding = ProjectCodingManager(project_root=self.project_root)
        self.project_plugin = ProjectPlugin(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def read_gitignore_entries(self) -> list[str]:
        if not self.gitignore_path.exists():
            return []

        entries: list[str] = []

        for line in self.gitignore_path.read_text(encoding="utf-8", errors="replace").splitlines():
            item = line.strip()

            if not item or item.startswith("#"):
                continue

            entries.append(item)

        return entries

    def ignored_dirs(self) -> list[str]:
        entries = set(self.DEFAULT_IGNORED_DIRS)

        for item in self.read_gitignore_entries():
            normalized = item.strip().rstrip("/")

            if not normalized:
                continue

            if "/" not in normalized and not normalized.startswith("*"):
                entries.add(normalized)

        return sorted(entries)

    def should_ignore_path(self, path: Path) -> bool:
        relative = path.relative_to(self.project_root)
        ignored = set(self.ignored_dirs())

        for part in relative.parts:
            if part in ignored:
                return True

        return False

    def workspace_entries(self, depth: int = 2, limit: int = 120) -> list[dict[str, Any]]:
        depth = max(1, min(depth, 5))
        limit = max(1, min(limit, 500))

        entries: list[dict[str, Any]] = []

        for path in sorted(self.project_root.rglob("*")):
            if len(entries) >= limit:
                break

            if self.should_ignore_path(path):
                continue

            relative = path.relative_to(self.project_root)
            relative_parts = relative.parts

            if len(relative_parts) > depth:
                continue

            entries.append(
                {
                    "path": str(relative),
                    "type": "directory" if path.is_dir() else "file",
                    "depth": len(relative_parts),
                    "size_bytes": path.stat().st_size if path.is_file() else 0,
                }
            )

        return entries

    def top_level_directories(self) -> list[str]:
        directories: list[str] = []

        for path in sorted(self.project_root.iterdir()):
            if not path.is_dir():
                continue

            if self.should_ignore_path(path):
                continue

            directories.append(path.name)

        return directories

    def top_level_files(self) -> list[str]:
        files: list[str] = []

        for path in sorted(self.project_root.iterdir()):
            if not path.is_file():
                continue

            if self.should_ignore_path(path):
                continue

            files.append(path.name)

        return files

    def important_files(self) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []

        for relative_path in self.IMPORTANT_FILE_CANDIDATES:
            path = self.project_root / relative_path

            files.append(
                {
                    "path": relative_path,
                    "exists": path.exists(),
                    "type": "file" if path.is_file() else "missing",
                    "size_bytes": path.stat().st_size if path.is_file() else 0,
                    "reason": self.reason_for_important_file(relative_path),
                }
            )

        return files

    def reason_for_important_file(self, relative_path: str) -> str:
        reason_map = {
            "README.md": "Project overview and public project status.",
            "main.py": "Main entry point for AURA CLI and boot.",
            "requirements.txt": "Python dependency list.",
            ".gitignore": "Runtime and local file exclusion rules.",
            "aura/personality/identity.yaml": "AURA identity, version, creator, codename, and motto.",
            "aura/config/settings.yaml": "Local configuration for app, server, paths, and reasoning provider.",
            "aura/core/cli.py": "Command-line interface surface.",
            "aura/core/shell.py": "Interactive shell surface.",
            "aura/status/system_status_manager.py": "Unified system status dashboard.",
            "aura/partner/partner_alpha_manager.py": "Unified safe partner layer.",
            "aura/project_coding/project_coding_manager.py": "Read-only project coding assistant.",
            "aura/plugins/builtin/plugin_actions.py": "Builtin plugin action registry.",
            "aura/skills/builtin_skills.py": "Builtin skill registry.",
            "docs/AURA_MASTER_ROADMAP.md": "Master roadmap.",
            "docs/AURA_PRODUCT_VISION.md": "Long-range product vision.",
        }

        return reason_map.get(relative_path, "Important project file.")

    def current_branch(self) -> str:
        head = self.project_root / ".git" / "HEAD"

        if not head.exists():
            return "unknown"

        content = head.read_text(encoding="utf-8", errors="replace").strip()

        if content.startswith("ref:"):
            return content.split("/")[-1]

        if content:
            return "detached"

        return "unknown"

    def latest_commit_hint(self) -> str:
        head = self.project_root / ".git" / "HEAD"

        if not head.exists():
            return ""

        content = head.read_text(encoding="utf-8", errors="replace").strip()

        if content.startswith("ref:"):
            ref_path = content.replace("ref:", "").strip()
            target = self.project_root / ".git" / ref_path

            if target.exists():
                return target.read_text(encoding="utf-8", errors="replace").strip()[:12]

            return ""

        return content[:12]

    def latest_milestone(self) -> dict[str, Any] | None:
        milestones = self.memory_reflection.extract_milestones(journal_limit=500)

        if not milestones:
            return None

        return milestones[-1]

    def current_sprint(self) -> str:
        milestone = self.latest_milestone()

        if not milestone:
            return ""

        return milestone.get("name", "")

    def workspace_map(self, depth: int = 2, limit: int = 120) -> dict[str, Any]:
        entries = self.workspace_entries(depth=depth, limit=limit)
        directories = [item for item in entries if item["type"] == "directory"]
        files = [item for item in entries if item["type"] == "file"]

        return {
            "status": self.status_name,
            "workspace_map_ready": True,
            "project_root": str(self.project_root),
            "depth": max(1, min(depth, 5)),
            "limit": max(1, min(limit, 500)),
            "directories": len(directories),
            "files": len(files),
            "entries": entries,
            "ignored_dirs": self.ignored_dirs(),
            "read_only": True,
            "write_performed": False,
            "command_execution_performed": False,
            "note": "Workspace map is read-only and skips ignored/runtime directories.",
        }

    def current_state(self) -> dict[str, Any]:
        identity = self.load_identity()
        project_coding_status = self.project_coding.status()
        latest_milestone = self.latest_milestone()

        return {
            "status": self.status_name,
            "current_state_ready": True,
            "project_root": str(self.project_root),
            "version": identity.get("version", "unknown"),
            "codename": identity.get("codename", "Genesis"),
            "creator": identity.get("creator", "Kiput"),
            "motto": identity.get("motto", "Grow Together"),
            "current_sprint": self.current_sprint(),
            "latest_milestone": latest_milestone,
            "git_repository_detected": (self.project_root / ".git").exists(),
            "git_branch": self.current_branch(),
            "latest_commit_hint": self.latest_commit_hint(),
            "git_status_checked": False,
            "git_status_note": "Git working-tree status is not checked here because Workspace Awareness does not execute git commands.",
            "python_files": project_coding_status["python_files"],
            "memory_records": self.memory_store.count(),
            "journal_entries": self.project_journal.count(),
            "read_only": True,
            "write_performed": False,
            "command_execution_performed": False,
        }

    def context(self) -> dict[str, Any]:
        state = self.current_state()
        workspace_map = self.workspace_map(depth=2, limit=120)
        important_files = self.important_files()

        return {
            "status": self.status_name,
            "context_ready": True,
            "workspace_summary": self.summary_text(state=state, workspace_map=workspace_map),
            "current_state": state,
            "top_level_directories": self.top_level_directories(),
            "top_level_files": self.top_level_files(),
            "important_files": important_files,
            "workspace_map": workspace_map,
            "ignored_dirs": self.ignored_dirs(),
            "disabled_capabilities": [
                "automatic_file_write",
                "automatic_memory_write",
                "automatic_journal_write",
                "command_execution",
                "desktop_action_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Workspace context is read-only and safe for future reasoning.",
        }

    def summary_text(self, state: dict[str, Any], workspace_map: dict[str, Any]) -> str:
        sprint = state["current_sprint"] or "unknown sprint"

        return (
            f"AURA workspace is at version {state['version']} in {state['codename']} phase. "
            f"Current milestone context is {sprint}. "
            f"The visible workspace map contains {workspace_map['directories']} directories and "
            f"{workspace_map['files']} files at depth {workspace_map['depth']}, with "
            f"{state['python_files']} Python files tracked by Project Coding Assistant."
        )

    def status(self) -> dict[str, Any]:
        identity = self.load_identity()
        workspace_map = self.workspace_map(depth=2, limit=120)
        important_files = self.important_files()
        existing_important_files = [
            item
            for item in important_files
            if item["exists"]
        ]

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "awareness_ready": True,
            "workspace_map_ready": True,
            "workspace_context_ready": True,
            "current_state_ready": True,
            "important_files_ready": True,
            "project_root_detected": self.project_root.exists(),
            "git_repository_detected": (self.project_root / ".git").exists(),
            "git_branch": self.current_branch(),
            "latest_commit_hint": self.latest_commit_hint(),
            "aura_version": identity.get("version", "unknown"),
            "current_sprint": self.current_sprint(),
            "top_level_directories": len(self.top_level_directories()),
            "top_level_files": len(self.top_level_files()),
            "workspace_directories": workspace_map["directories"],
            "workspace_files": workspace_map["files"],
            "important_file_count": len(important_files),
            "existing_important_file_count": len(existing_important_files),
            "ignored_dir_count": len(self.ignored_dirs()),
            "python_files": self.project_coding.status()["python_files"],
            "read_only": True,
            "file_write": False,
            "memory_write": False,
            "journal_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "sections": 5,
            "project_root": str(self.project_root),
            "note": "Workspace Awareness Foundation is online for read-only workspace understanding. It does not write files, write memory, write journal entries, execute commands, or perform desktop actions.",
        }
