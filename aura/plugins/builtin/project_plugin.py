from pathlib import Path


class ProjectPlugin:
    """
    Safe project inspection plugin for AURA.

    Current phase:
    - metadata and read-only project inspection
    - no file writing
    - no command execution
    """

    name = "project"
    version = "0.1.0"
    description = "Safe project file and structure inspection plugin for AURA."

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        "logs",
        "data",
    }

    IGNORED_SUFFIXES = {
        ".pyc",
        ".pyo",
        ".log",
        ".sqlite",
        ".db",
    }

    SENSITIVE_FILENAMES = {
        ".env",
        ".env.local",
        ".env.production",
        "id_rsa",
        "id_ed25519",
        "known_hosts",
    }

    MAX_READ_BYTES = 50_000

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()

    def is_ignored_path(self, path: Path) -> bool:
        parts = set(path.parts)

        if parts & self.IGNORED_DIRS:
            return True

        if path.name in self.SENSITIVE_FILENAMES:
            return True

        if path.suffix in self.IGNORED_SUFFIXES:
            return True

        return False

    def resolve_safe_path(self, relative_path: str) -> Path:
        target = (self.project_root / relative_path).resolve()

        if self.project_root not in target.parents and target != self.project_root:
            raise ValueError("Path is outside project root.")

        if self.is_ignored_path(target):
            raise ValueError("Path is ignored or sensitive.")

        return target

    def list_files(self, limit: int = 50) -> list[str]:
        files: list[str] = []

        for path in sorted(self.project_root.rglob("*")):
            if len(files) >= limit:
                break

            if not path.is_file():
                continue

            relative = path.relative_to(self.project_root)

            if self.is_ignored_path(relative):
                continue

            files.append(str(relative))

        return files

    def summary(self) -> dict:
        files = self.list_files(limit=500)

        python_files = [
            file
            for file in files
            if file.endswith(".py")
        ]

        markdown_files = [
            file
            for file in files
            if file.endswith(".md")
        ]

        yaml_files = [
            file
            for file in files
            if file.endswith((".yaml", ".yml"))
        ]

        return {
            "project_root": str(self.project_root),
            "visible_files": len(files),
            "python_files": len(python_files),
            "markdown_files": len(markdown_files),
            "yaml_files": len(yaml_files),
            "top_files": files[:20],
        }

    def project_map(self, depth: int = 2, limit: int = 80) -> dict:
        """
        Build a safe high-level project map.

        This is read-only and ignores sensitive/runtime paths.
        """
        depth = max(1, min(depth, 5))
        entries: list[dict] = []

        for path in sorted(self.project_root.rglob("*")):
            if len(entries) >= limit:
                break

            relative = path.relative_to(self.project_root)

            if self.is_ignored_path(relative):
                continue

            if len(relative.parts) > depth:
                continue

            entry_type = "directory" if path.is_dir() else "file"

            entries.append(
                {
                    "path": str(relative),
                    "type": entry_type,
                    "suffix": path.suffix if path.is_file() else "",
                }
            )

        directories = [
            entry
            for entry in entries
            if entry["type"] == "directory"
        ]

        files = [
            entry
            for entry in entries
            if entry["type"] == "file"
        ]

        return {
            "project_root": str(self.project_root),
            "depth": depth,
            "limit": limit,
            "entries": entries,
            "directories": len(directories),
            "files": len(files),
        }

    def inspect_path(self, relative_path: str, child_limit: int = 40) -> dict:
        """
        Safely inspect a file or directory inside the project.
        """
        target = self.resolve_safe_path(relative_path)

        if not target.exists():
            raise FileNotFoundError(f"Path not found: {relative_path}")

        relative = target.relative_to(self.project_root)

        if target.is_dir():
            children: list[dict] = []

            for child in sorted(target.iterdir()):
                child_relative = child.relative_to(self.project_root)

                if self.is_ignored_path(child_relative):
                    continue

                children.append(
                    {
                        "path": str(child_relative),
                        "name": child.name,
                        "type": "directory" if child.is_dir() else "file",
                        "suffix": child.suffix if child.is_file() else "",
                    }
                )

                if len(children) >= child_limit:
                    break

            return {
                "path": str(relative),
                "type": "directory",
                "children": children,
                "children_shown": len(children),
                "child_limit": child_limit,
            }

        if target.is_file():
            size = target.stat().st_size

            preview_lines: list[str] = []

            if size <= self.MAX_READ_BYTES:
                content = target.read_text(encoding="utf-8", errors="replace")
                preview_lines = content.splitlines()[:30]

            return {
                "path": str(relative),
                "type": "file",
                "suffix": target.suffix,
                "size_bytes": size,
                "safe_to_read": size <= self.MAX_READ_BYTES,
                "preview_lines": preview_lines,
                "preview_line_count": len(preview_lines),
            }

        return {
            "path": str(relative),
            "type": "unknown",
        }

    def find_text(self, keyword: str, limit: int = 30) -> dict:
        """
        Search for a keyword in safe project text files.

        This is read-only and capped by limit.
        """
        normalized_keyword = keyword.strip()

        if not normalized_keyword:
            raise ValueError("Keyword cannot be empty.")

        matches: list[dict] = []

        for relative_file in self.list_files(limit=1000):
            if len(matches) >= limit:
                break

            target = self.resolve_safe_path(relative_file)

            if not target.is_file():
                continue

            if target.stat().st_size > self.MAX_READ_BYTES:
                continue

            try:
                content = target.read_text(encoding="utf-8", errors="replace")
            except UnicodeDecodeError:
                continue

            for line_number, line in enumerate(content.splitlines(), start=1):
                if normalized_keyword.lower() not in line.lower():
                    continue

                matches.append(
                    {
                        "file": relative_file,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )

                if len(matches) >= limit:
                    break

        return {
            "keyword": normalized_keyword,
            "limit": limit,
            "matches": matches,
            "match_count": len(matches),
        }

    def read_file(self, relative_path: str) -> str:
        target = self.resolve_safe_path(relative_path)

        if not target.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if not target.is_file():
            raise ValueError(f"Path is not a file: {relative_path}")

        size = target.stat().st_size
        if size > self.MAX_READ_BYTES:
            raise ValueError(
                f"File too large to read safely: {relative_path} ({size} bytes)"
            )

        return target.read_text(encoding="utf-8", errors="replace")
