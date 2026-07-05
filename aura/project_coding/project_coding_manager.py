import ast
from pathlib import Path
from typing import Any

from aura.model_router.model_router import ModelRouter
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.project_coding.code_file_summary import CodeFileSummary
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager


class ProjectCodingManager:
    """
    Project Coding Assistant v2.

    Current phase:
    - read-only project coding analysis
    - Python AST inspection
    - safe patch planning
    - sandbox-aware command safety checks
    - no automatic file writing
    - no command execution
    """

    name = "project_coding_assistant_v2"
    version = "0.1.0"

    PYTHON_SUFFIXES = {".py"}
    MAX_CODE_READ_BYTES = 300_000

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.project_plugin = ProjectPlugin(project_root=self.project_root)
        self.model_router = ModelRouter(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)

    def python_files(self, limit: int = 200) -> list[str]:
        files = self.project_plugin.list_files(limit=1000)
        python_files = [
            file
            for file in files
            if Path(file).suffix in self.PYTHON_SUFFIXES
        ]

        return python_files[: max(1, min(limit, 500))]

    def status(self) -> dict[str, Any]:
        python_files = self.python_files(limit=500)
        route = self.model_router.select("coding")["route"]
        sandbox_status = self.tool_sandbox.status()

        return {
            "name": self.name,
            "version": self.version,
            "status": "online",
            "analysis_ready": True,
            "ast_inspection_ready": True,
            "patch_planning_ready": True,
            "file_write_ready": False,
            "command_execution_ready": False,
            "sandbox_check_ready": sandbox_status["sandbox_ready"],
            "real_tool_execution": sandbox_status["real_execution_ready"],
            "coding_route": route,
            "python_files": len(python_files),
            "project_root": str(self.project_root),
            "note": "Project Coding Assistant v2 is online for read-only analysis and patch planning. It does not write files or execute commands.",
        }

    def language_for_path(self, path: str) -> str:
        suffix = Path(path).suffix.lower()

        if suffix == ".py":
            return "python"

        if suffix in {".md", ".txt"}:
            return "text"

        if suffix in {".yaml", ".yml"}:
            return "yaml"

        return "unknown"

    def read_code_file(self, relative_path: str) -> tuple[str, int]:
        """
        Read a safe project code file for coding analysis.

        This uses ProjectPlugin path safety, but allows larger source files
        than ProjectPlugin.read_file because AST inspection often needs
        complete Python modules.
        """
        target = self.project_plugin.resolve_safe_path(relative_path)

        if not target.exists():
            raise FileNotFoundError(f"Path not found: {relative_path}")

        if not target.is_file():
            raise ValueError(f"Path is not a file: {relative_path}")

        size = target.stat().st_size

        if size > self.MAX_CODE_READ_BYTES:
            raise ValueError(
                f"Code file too large to analyze safely: {relative_path} ({size} bytes)"
            )

        content = target.read_text(encoding="utf-8", errors="replace")
        return content, size

    def summarize_python(self, relative_path: str, content: str, size_bytes: int) -> CodeFileSummary:
        line_count = len(content.splitlines())
        imports: list[str] = []
        classes: list[str] = []
        functions: list[str] = []
        methods: list[str] = []

        try:
            tree = ast.parse(content)
        except SyntaxError as error:
            return CodeFileSummary(
                path=relative_path,
                language="python",
                size_bytes=size_bytes,
                line_count=line_count,
                parse_ok=False,
                parse_error=f"{error.msg} at line {error.lineno}",
                safety_notes=[
                    "File could not be parsed as valid Python.",
                    "Patch planning should inspect syntax errors before editing.",
                ],
            )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append(module)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(f"{node.name}.{child.name}")

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)

        unique_imports = sorted({item for item in imports if item})
        unique_classes = sorted(set(classes))
        unique_functions = sorted(set(functions))
        unique_methods = sorted(set(methods))

        return CodeFileSummary(
            path=relative_path,
            language="python",
            size_bytes=size_bytes,
            line_count=line_count,
            imports=unique_imports,
            classes=unique_classes,
            functions=unique_functions,
            methods=unique_methods,
            parse_ok=True,
            parse_error=None,
            safety_notes=[
                "Read-only AST summary.",
                "No file modification was performed.",
            ],
        )

    def summarize_file(self, relative_path: str) -> dict[str, Any]:
        target = self.project_plugin.resolve_safe_path(relative_path)

        if not target.exists():
            raise FileNotFoundError(f"Path not found: {relative_path}")

        if not target.is_file():
            raise ValueError(f"Path is not a file: {relative_path}")

        content, size_bytes = self.read_code_file(relative_path)
        language = self.language_for_path(relative_path)

        if language == "python":
            return self.summarize_python(
                relative_path=relative_path,
                content=content,
                size_bytes=size_bytes,
            ).to_dict()

        lines = content.splitlines()

        return CodeFileSummary(
            path=relative_path,
            language=language,
            size_bytes=size_bytes,
            line_count=len(lines),
            parse_ok=True,
            safety_notes=[
                "Read-only text summary.",
                "No file modification was performed.",
            ],
        ).to_dict()

    def code_map(self, limit: int = 80) -> dict[str, Any]:
        limit = max(1, min(limit, 200))
        files = self.python_files(limit=limit)

        summaries: list[dict[str, Any]] = []

        for file in files:
            try:
                summary = self.summarize_file(file)
            except Exception as error:
                summary = {
                    "path": file,
                    "language": "python",
                    "parse_ok": False,
                    "parse_error": str(error),
                    "imports": [],
                    "classes": [],
                    "functions": [],
                    "methods": [],
                    "import_count": 0,
                    "class_count": 0,
                    "function_count": 0,
                    "method_count": 0,
                }

            summaries.append(summary)

        totals = {
            "files": len(summaries),
            "imports": sum(item.get("import_count", 0) for item in summaries),
            "classes": sum(item.get("class_count", 0) for item in summaries),
            "functions": sum(item.get("function_count", 0) for item in summaries),
            "methods": sum(item.get("method_count", 0) for item in summaries),
        }

        return {
            "project_root": str(self.project_root),
            "limit": limit,
            "totals": totals,
            "files": summaries,
            "note": "Code map is read-only and based on safe project files.",
        }

    def related_files_for_request(self, request: str, limit: int = 12) -> list[str]:
        normalized = request.lower()
        candidates = self.python_files(limit=500)
        matches: list[str] = []

        keyword_map = {
            "cli": ["aura/core/cli.py"],
            "shell": ["aura/core/shell.py"],
            "command": ["aura/core/cli.py", "aura/core/shell.py"],
            "status": ["aura/status/system_status_manager.py"],
            "skill": ["aura/skills/builtin_skills.py"],
            "plugin": ["aura/plugins/builtin/plugin_actions.py"],
            "permission": ["aura/permissions/permission_manager.py"],
            "sandbox": ["aura/tool_sandbox/tool_sandbox_manager.py"],
            "model": ["aura/model_router/model_router.py"],
            "router": ["aura/model_router/model_router.py"],
            "project": ["aura/plugins/builtin/project_plugin.py"],
            "memory": ["aura/memory/memory_store.py"],
            "journal": ["aura/journal/project_journal.py"],
        }

        for keyword, files in keyword_map.items():
            if keyword not in normalized:
                continue

            for file in files:
                if file in candidates and file not in matches:
                    matches.append(file)

        if not matches:
            for file in candidates:
                if file.startswith("aura/core/") or file.startswith("aura/plugins/"):
                    matches.append(file)

                if len(matches) >= limit:
                    break

        return matches[:limit]

    def patch_plan(self, request: str) -> dict[str, Any]:
        normalized = request.strip()

        if not normalized:
            raise ValueError("Patch request cannot be empty.")

        route_selection = self.model_router.select("coding")
        related_files = self.related_files_for_request(normalized)

        sandbox_checks = [
            self.tool_sandbox.check_command("git status"),
            self.tool_sandbox.check_command("python3 -m py_compile aura/core/cli.py"),
        ]

        return {
            "request": normalized,
            "mode": "patch_plan_only",
            "file_write_performed": False,
            "command_execution_performed": False,
            "coding_route": route_selection["route"],
            "related_files": related_files,
            "recommended_steps": [
                "Inspect the related files.",
                "Identify the smallest safe change.",
                "Prepare a patch plan.",
                "Run syntax checks after user-approved changes.",
                "Use tool sandbox checks before any future command execution.",
                "Commit only after validation and user approval.",
            ],
            "sandbox_checks": sandbox_checks,
            "safety": {
                "writes_allowed_without_confirmation": False,
                "real_tool_execution": False,
                "dangerous_commands_blocked": True,
                "note": "This is only a coding plan. No file was modified and no command was executed.",
            },
        }

    def command_safety(self, command: str) -> dict[str, Any]:
        check = self.tool_sandbox.check_command(command)
        dry_run = self.tool_sandbox.dry_run(command)

        return {
            "command": command,
            "check": check,
            "dry_run": dry_run,
            "project_coding_note": "Project Coding Assistant v2 uses tool sandbox checks before recommending command workflows.",
        }
