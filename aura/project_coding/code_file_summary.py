from dataclasses import dataclass, field
from typing import Any


@dataclass
class CodeFileSummary:
    """
    Safe code file summary for Project Coding Assistant v2.
    """

    path: str
    language: str
    size_bytes: int
    line_count: int
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    parse_ok: bool = True
    parse_error: str | None = None
    safety_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "language": self.language,
            "size_bytes": self.size_bytes,
            "line_count": self.line_count,
            "imports": self.imports,
            "classes": self.classes,
            "functions": self.functions,
            "methods": self.methods,
            "import_count": len(self.imports),
            "class_count": len(self.classes),
            "function_count": len(self.functions),
            "method_count": len(self.methods),
            "parse_ok": self.parse_ok,
            "parse_error": self.parse_error,
            "safety_notes": self.safety_notes,
            "metadata": self.metadata,
        }
