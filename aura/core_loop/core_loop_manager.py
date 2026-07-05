from pathlib import Path
from typing import Any

from aura.actions.action_request import ActionRequest
from aura.actions.action_request_manager import ActionRequestManager
from aura.context.context_manager import ContextManager
from aura.core.chat import AuraChat
from aura.status.system_status_manager import SystemStatusManager


class CoreLoopManager:
    """
    AURA Alpha Core Loop.

    Current phase:
    - connects input, context, reasoning, planning, safety, response, and journal context
    - prepares safe flow traces
    - never executes external actions
    """

    name = "alpha_core_loop"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.context_manager = ContextManager(project_root=project_root)
        self.chat = AuraChat(project_root=project_root)
        self.action_request_manager = ActionRequestManager()
        self.system_status_manager = SystemStatusManager(project_root=project_root)

    def steps(self) -> list[dict[str, Any]]:
        return [
            {
                "index": 1,
                "name": "input",
                "status": "online",
                "component": "user_message",
                "description": "Receive the user's message.",
            },
            {
                "index": 2,
                "name": "context",
                "status": "online",
                "component": "ContextManager",
                "description": "Build pinned memory, important memory, relevant memory, and recent project journal context.",
            },
            {
                "index": 3,
                "name": "reasoning",
                "status": "online",
                "component": "ReasoningProvider",
                "description": "Generate a text response through the configured reasoning provider.",
            },
            {
                "index": 4,
                "name": "plan",
                "status": "alpha",
                "component": "CoreLoopManager",
                "description": "Infer a safe high-level intent and prepare a non-executing action proposal.",
            },
            {
                "index": 5,
                "name": "safety",
                "status": "online",
                "component": "ActionRequestManager + PermissionManager",
                "description": "Check permission state and confirmation requirement without executing actions.",
            },
            {
                "index": 6,
                "name": "response",
                "status": "online",
                "component": "AuraChat",
                "description": "Return AURA's response to the user.",
            },
            {
                "index": 7,
                "name": "journal",
                "status": "foundation",
                "component": "ProjectJournal",
                "description": "Use recent project journal as context. Writing still requires explicit journal commands.",
            },
        ]

    def status(self) -> dict[str, Any]:
        system_status = self.system_status_manager.build_status()

        return {
            "name": self.name,
            "version": self.version,
            "status": "alpha",
            "loop_ready": True,
            "execution_ready": False,
            "safe_action_execution": False,
            "steps": len(self.steps()),
            "flow": "Input -> Context -> Reasoning -> Plan -> Safety -> Response -> Journal",
            "systems": {
                "memory": system_status["systems"]["memory"],
                "context": system_status["systems"]["context"],
                "permissions": system_status["systems"]["permissions"],
                "plugin_actions": system_status["systems"]["plugin_actions"],
                "desktop_bridge": system_status["systems"]["desktop_bridge"],
                "voice_runtime": system_status["systems"]["voice_runtime"],
                "vision_runtime": system_status["systems"]["vision_runtime"],
                "avatar": system_status["systems"]["avatar"],
            },
            "runtime": {
                "real_voice_runtime": system_status["runtime"]["real_voice_runtime"],
                "real_vision_runtime": system_status["runtime"]["real_vision_runtime"],
                "avatar_runtime": system_status["runtime"]["avatar_runtime"],
                "safe_action_execution": system_status["runtime"]["safe_action_execution"],
            },
            "note": "AURA Alpha Core Loop is online, but external action execution remains disabled.",
        }

    def infer_action_name(self, message: str) -> str:
        normalized = message.strip().lower()

        if any(keyword in normalized for keyword in {"status", "keadaan", "sistem"}):
            return "system.status"

        if "avatar" in normalized:
            return "avatar.status"

        if "vision" in normalized or "lihat" in normalized or "screen" in normalized or "camera" in normalized:
            return "vision.runtime_status"

        if "voice" in normalized or "suara" in normalized or "bicara" in normalized:
            return "voice.runtime_status"

        if "desktop" in normalized:
            return "desktop.status"

        if "project" in normalized or "proyek" in normalized:
            return "project.summary"

        return "think"

    def action_request_to_dict(self, request: ActionRequest) -> dict[str, Any]:
        return {
            "requested_action": request.requested_action,
            "resolved_action": request.resolved_action,
            "plugin_action_found": request.plugin_action_found,
            "plugin": request.plugin,
            "skill": request.skill,
            "plugin_action_status": request.plugin_action_status,
            "permission_action": request.permission_action,
            "permission_level": request.permission_level,
            "permission_level_name": request.permission_level_name,
            "permission_level_label": request.permission_level_label,
            "allowed": request.allowed,
            "requires_confirmation": request.requires_confirmation,
            "request_state": request.request_state,
            "description": request.description,
            "reason": request.reason,
            "note": request.note,
            "metadata": request.metadata or {},
        }

    def context_summary(self, message: str) -> dict[str, Any]:
        packet = self.context_manager.build(user_message=message)
        latest_journal = packet.recent_journal_entries[-1].content if packet.recent_journal_entries else ""

        return {
            "pinned_memories": len(packet.pinned_memories),
            "important_memories": len(packet.important_memories),
            "relevant_memories": len(packet.relevant_memories),
            "recent_journal_entries": len(packet.recent_journal_entries),
            "latest_journal": latest_journal,
        }

    def run(self, message: str, *, save_response: bool = True) -> dict[str, Any]:
        action_name = self.infer_action_name(message)
        action_request = self.action_request_manager.build(action_name=action_name)

        response = (
            self.chat.respond(message, source="AuraCoreLoop")
            if save_response
            else self.chat.generate_response(message)
        )

        return {
            "input": {
                "message": message,
                "received": True,
            },
            "context": self.context_summary(message=message),
            "reasoning": {
                "provider": self.chat.provider_info(),
                "response_generated": True,
            },
            "plan": {
                "inferred_action": action_name,
                "mode": "proposal_only",
            },
            "safety": self.action_request_to_dict(action_request),
            "response": {
                "text": response,
            },
            "journal": {
                "mode": "context_only",
                "write_performed": False,
                "note": "Project journal was used as context only. No journal entry was written by the core loop.",
            },
            "execution": {
                "executed": False,
                "external_action_executed": False,
                "safe_action_execution": False,
            },
        }

    def trace(self, message: str) -> dict[str, Any]:
        result = self.run(message=message, save_response=False)
        result["loop"] = {
            "name": self.name,
            "version": self.version,
            "status": "alpha",
            "steps": self.steps(),
        }
        return result
