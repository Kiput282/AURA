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
