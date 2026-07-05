from pathlib import Path
from shlex import split
from typing import Any

from aura.tool_sandbox.sandbox_policy import SandboxPolicy


class ToolSandboxManager:
    """
    Tool Execution Sandbox Foundation for AURA.

    Current phase:
    - classify shell command safety
    - provide dry-run proposals
    - block dangerous commands/patterns
    - does not execute shell commands
    """

    name = "tool_execution_sandbox"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.policy = self.build_policy()

    def build_policy(self) -> SandboxPolicy:
        return SandboxPolicy(
            name="default_tool_sandbox_policy",
            status="foundation",
            description="Default local-first sandbox policy for checking and dry-running tool commands.",
            allowed_commands=[
                "pwd",
                "ls",
                "echo",
                "cat",
                "sed",
                "grep",
                "find",
                "head",
                "tail",
                "wc",
                "python3",
                "git status",
                "git diff",
                "git log",
            ],
            blocked_commands=[
                "rm",
                "rmdir",
                "mv",
                "cp",
                "chmod",
                "chown",
                "sudo",
                "su",
                "apt",
                "apt-get",
                "pip install",
                "curl",
                "wget",
                "ssh",
                "scp",
                "rsync",
                "dd",
                "mkfs",
                "mount",
                "umount",
                "systemctl",
                "service",
                "reboot",
                "shutdown",
                "poweroff",
            ],
            blocked_patterns=[
                "rm -rf",
                "rm -fr",
                "sudo ",
                ">/dev/",
                " /dev/",
                ":(){",
                "chmod -R",
                "chown -R",
                "mkfs",
                "dd if=",
                "dd of=",
                "curl | sh",
                "wget | sh",
                "| sh",
                "| bash",
                "| zsh",
                "| fish",
                " sh <",
                " bash <",
                "wget ",
                "curl ",
                "bash -c",
                "sh -c",
                "python -c",
                "python3 -c",
                "> /",
                ">> /",
                "wipe",
                "format",
            ],
            dry_run_supported=True,
            real_execution_supported=False,
            requires_confirmation_for_execution=True,
            metadata={
                "local_first": True,
                "proposal_only": True,
                "execution_default": "disabled",
            },
        )

    def status(self) -> dict[str, Any]:
        policy = self.policy

        return {
            "name": self.name,
            "version": self.version,
            "status": "foundation",
            "sandbox_ready": True,
            "policy_ready": True,
            "dry_run_ready": policy.dry_run_supported,
            "real_execution_ready": policy.real_execution_supported,
            "requires_confirmation_for_execution": policy.requires_confirmation_for_execution,
            "allowed_command_count": len(policy.allowed_commands),
            "blocked_command_count": len(policy.blocked_commands),
            "blocked_pattern_count": len(policy.blocked_patterns),
            "project_root": str(self.project_root),
            "note": "Tool sandbox foundation is online. Commands can be checked and dry-run, but real execution is disabled.",
        }

    def policy_dict(self) -> dict[str, Any]:
        return self.policy.to_dict()

    def tokenize(self, command: str) -> list[str]:
        try:
            return split(command)
        except ValueError:
            return command.strip().split()

    def base_command(self, command: str) -> str:
        tokens = self.tokenize(command)

        if not tokens:
            return ""

        if len(tokens) >= 2:
            pair = f"{tokens[0]} {tokens[1]}".lower()

            for blocked in self.policy.blocked_commands:
                if pair == blocked.lower():
                    return pair

            for allowed in self.policy.allowed_commands:
                if pair == allowed.lower():
                    return pair

        return tokens[0].lower()

    def pattern_hits(self, command: str) -> list[str]:
        normalized = command.strip().lower()

        return [
            pattern
            for pattern in self.policy.blocked_patterns
            if pattern.lower() in normalized
        ]

    def is_allowed_base(self, command: str) -> bool:
        base = self.base_command(command)

        if not base:
            return False

        allowed = {item.lower() for item in self.policy.allowed_commands}
        blocked = {item.lower() for item in self.policy.blocked_commands}

        if base in blocked:
            return False

        if base in allowed:
            return True

        if " " in base:
            first = base.split()[0]
            return first in allowed and base not in blocked

        return False

    def check_command(self, command: str) -> dict[str, Any]:
        original = command
        normalized = command.strip()
        tokens = self.tokenize(normalized)
        base = self.base_command(normalized)
        hits = self.pattern_hits(normalized)

        if not normalized:
            state = "empty"
            allowed = False
            reason = "No command was provided."
        elif hits:
            state = "blocked"
            allowed = False
            reason = "Command contains blocked dangerous pattern."
        elif not self.is_allowed_base(normalized):
            state = "not_allowlisted"
            allowed = False
            reason = "Command is not in the sandbox allowlist."
        else:
            state = "allowed_for_dry_run"
            allowed = True
            reason = "Command is allowlisted for dry-run proposal only."

        return {
            "command": original,
            "normalized_command": normalized,
            "tokens": tokens,
            "base_command": base,
            "allowed": allowed,
            "state": state,
            "blocked_patterns_found": hits,
            "dry_run_supported": self.policy.dry_run_supported and allowed,
            "real_execution_supported": False,
            "requires_confirmation_for_execution": True,
            "executed": False,
            "reason": reason,
            "note": "Sandbox check only. No command was executed.",
        }

    def dry_run(self, command: str) -> dict[str, Any]:
        check = self.check_command(command)

        if not check["allowed"]:
            return {
                "command": command,
                "dry_run_ready": False,
                "would_execute": False,
                "executed": False,
                "check": check,
                "plan": [],
                "note": "Dry-run refused because the command failed sandbox safety checks.",
            }

        return {
            "command": command,
            "dry_run_ready": True,
            "would_execute": False,
            "executed": False,
            "check": check,
            "plan": [
                "Validate command against sandbox policy.",
                "Confirm the command is allowlisted.",
                "Prepare command execution request.",
                "Require explicit confirmation before any future real execution.",
            ],
            "note": "Dry-run prepared only. Real command execution is disabled in this sprint.",
        }
