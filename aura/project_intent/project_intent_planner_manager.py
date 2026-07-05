from pathlib import Path
from typing import Any

import yaml

from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class ProjectIntentPlannerManager:
    """
    AURA Project Intent Planner.

    Current phase:
    - summarize project intent safely
    - prepare project goal plans
    - prepare sprint intent plans
    - prepare next action candidates
    - prepare safety-aware implementation plans
    - integrate workspace memory link, workspace awareness, project coding, daily briefing, and reflection
    - never writes files automatically
    - never writes memory automatically
    - never writes journal automatically
    - never executes commands
    """

    name = "project_intent_planner"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
        self.project_coding = ProjectCodingManager(project_root=self.project_root)
        self.daily_briefing = DailyBriefingManager(project_root=self.project_root)
        self.memory_reflection = MemoryReflectionManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())

        if len(normalized) > 500:
            return normalized[:500].rstrip() + "..."

        return normalized

    def intent_categories(self) -> list[str]:
        return [
            "project_goal",
            "sprint_intent",
            "next_action",
            "implementation_plan",
            "safety_boundary",
            "context_alignment",
        ]

    def latest_milestone(self) -> dict[str, Any] | None:
        milestones = self.memory_reflection.extract_milestones(journal_limit=500)

        if not milestones:
            return None

        return milestones[-1]

    def classify_intent(self, text: str) -> dict[str, Any]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "sprint": "sprint",
            "roadmap": "roadmap",
            "goal": "goal",
            "autonomous": "autonomy",
            "automation": "automation",
            "safe": "safety",
            "safety": "safety",
            "memory": "memory",
            "workspace": "workspace",
            "project": "project",
            "coding": "coding",
            "planner": "planner",
            "intent": "intent",
            "next": "next_action",
            "implementation": "implementation",
            "runtime": "runtime",
            "voice": "runtime",
            "vision": "runtime",
            "avatar": "runtime",
            "desktop": "runtime",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["project", "intent"])

        if "safety" in tags or "autonomy" in tags or "automation" in tags:
            priority = "safety_first_planning"
        elif "sprint" in tags:
            priority = "sprint_execution_planning"
        elif "coding" in tags or "implementation" in tags:
            priority = "implementation_planning"
        elif "roadmap" in tags or "next_action" in tags:
            priority = "roadmap_continuity"
        else:
            priority = "project_alignment"

        return {
            "tags": tags[:8],
            "priority": priority,
            "safety_related": "safety" in tags or "autonomy" in tags or "automation" in tags,
            "sprint_related": "sprint" in tags,
            "implementation_related": "implementation" in tags or "coding" in tags,
            "memory_related": "memory" in tags or "workspace" in tags,
        }

    def integration_context(self) -> dict[str, Any]:
        workspace_memory_summary = self.workspace_memory_link.summary()
        workspace_context = self.workspace_awareness.context()
        project_coding_status = self.project_coding.status()
        daily_compact = self.daily_briefing.compact(limit=4)
        reflection_context = self.memory_reflection.reflection_context(limit=6)

        return {
            "workspace_memory_summary": workspace_memory_summary,
            "workspace_context": workspace_context,
            "project_coding_status": project_coding_status,
            "daily_briefing_compact": daily_compact,
            "reflection_context": reflection_context,
            "latest_milestone": self.latest_milestone(),
        }

    def base_plan(
        self,
        plan_type: str,
        target: str,
        recommended_steps: list[str],
        action_candidates: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        cleaned_target = self.normalize_text(target) or "<unspecified>"
        intent = self.classify_intent(cleaned_target)
        context = self.integration_context()

        patch_plan = self.project_coding.patch_plan(cleaned_target)

        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "intent": intent,
            "intent_priority": intent["priority"],
            "intent_tags": intent["tags"],
            "latest_milestone": context["latest_milestone"],
            "workspace_summary": context["workspace_context"]["workspace_summary"],
            "workspace_memory_summary": context["workspace_memory_summary"]["summary"],
            "daily_project_summary": context["daily_briefing_compact"]["project_summary"],
            "project_coding_route": context["project_coding_status"]["coding_route"],
            "project_python_files": context["project_coding_status"]["python_files"],
            "patch_plan": patch_plan,
            "recommended_steps": recommended_steps,
            "action_candidates": action_candidates or [],
            "action_candidate_count": len(action_candidates or []),
            "permissions": {
                "read_project": read_project_permission.to_dict(),
                "read_memory": read_memory_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "read_only": True,
            "file_write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Project intent plan is proposal-only.",
                "No file was written.",
                "No memory was written.",
                "No journal entry was written.",
                "No command was executed.",
                "Future implementation must go through explicit review, validation, and confirmation.",
            ],
        }

    def summary(self, topic: str) -> dict[str, Any]:
        cleaned_topic = self.normalize_text(topic) or "AURA next sprint planning"
        context = self.integration_context()
        latest = context["latest_milestone"]
        identity = self.load_identity()

        return {
            "status": self.status_name,
            "summary_ready": True,
            "topic": cleaned_topic,
            "intent": self.classify_intent(cleaned_topic),
            "summary": (
                f"AURA {identity.get('version', 'unknown')} is in Genesis phase. "
                f"The latest milestone is {latest['title'] if latest else 'unknown'}. "
                f"The current project direction is to continue safe, layered planning toward stronger local partner autonomy."
            ),
            "workspace_memory_summary": context["workspace_memory_summary"]["summary"],
            "workspace_summary": context["workspace_context"]["workspace_summary"],
            "daily_project_summary": context["daily_briefing_compact"]["project_summary"],
            "top_insights": context["daily_briefing_compact"]["top_insights"],
            "recommended_next_steps": context["daily_briefing_compact"]["next_steps"],
            "read_only": True,
            "write_performed": False,
            "file_write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Project intent summary is read-only and planning-only.",
        }

    def goal_plan(self, goal: str) -> dict[str, Any]:
        cleaned_goal = self.normalize_text(goal) or "make AURA more autonomous safely"

        candidates = [
            self.build_action_candidate(
                "clarify_goal",
                "Clarify durable project goal and safety boundary before implementation.",
                "Keeps AURA aligned with long-term Genesis roadmap.",
            ),
            self.build_action_candidate(
                "map_dependencies",
                "Identify managers, CLI commands, shell commands, plugin actions, skills, and system-status fields needed.",
                "Keeps implementation modular and predictable.",
            ),
            self.build_action_candidate(
                "validate_safety",
                "Confirm file writing, memory writing, journal writing, and command execution remain disabled by default.",
                "Preserves AURA safety-first architecture.",
            ),
        ]

        return self.base_plan(
            plan_type="project_goal_plan",
            target=cleaned_goal,
            recommended_steps=[
                "Define the goal in one durable sentence.",
                "Split the goal into safe read-only planning capabilities first.",
                "Connect the goal to existing workspace, memory, briefing, and project coding context.",
                "Prepare implementation only after status, CLI, shell, plugin, skill, and system-status fields are clear.",
                "Keep all real writes and commands behind explicit user confirmation.",
            ],
            action_candidates=candidates,
        )

    def sprint_intent_plan(self, sprint_goal: str) -> dict[str, Any]:
        cleaned_goal = self.normalize_text(sprint_goal) or "Sprint 58 project intent planner"

        candidates = [
            self.build_action_candidate(
                "create_manager",
                "Create a manager that produces intent summaries, goal plans, sprint plans, next-action candidates, and context.",
                "Centralizes Sprint intent logic safely.",
            ),
            self.build_action_candidate(
                "register_interfaces",
                "Register skill, plugin actions, CLI commands, shell commands, and system-status fields.",
                "Makes the feature visible across AURA surfaces.",
            ),
            self.build_action_candidate(
                "final_validation",
                "Validate py_compile, CLI, shell, action-request, system-status, boot, journal, commit, and push.",
                "Keeps sprint closure consistent.",
            ),
        ]

        return self.base_plan(
            plan_type="sprint_intent_plan",
            target=cleaned_goal,
            recommended_steps=[
                "Inspect current project state and latest sprint milestone.",
                "Implement the smallest manager layer that stays proposal-only.",
                "Add skill and plugin actions before CLI/shell surfaces.",
                "Expose runtime readiness and disabled write/command flags in system-status.",
                "Close the sprint only after validation and clean git state.",
            ],
            action_candidates=candidates,
        )

    def next_action_candidates(self, topic: str) -> dict[str, Any]:
        cleaned_topic = self.normalize_text(topic) or "continue Genesis roadmap"

        candidates = [
            self.build_action_candidate(
                "continue_next_roadmap_sprint",
                "Continue with the next roadmap sprint after validating current repo state.",
                "Keeps Genesis progress linear and auditable.",
                importance=4,
            ),
            self.build_action_candidate(
                "review_memory_candidates",
                "Review workspace memory candidates and decide whether any durable facts should be saved later.",
                "Improves long-context continuity without automatic memory writes.",
                importance=3,
            ),
            self.build_action_candidate(
                "stabilize_planning_layers",
                "Keep planning modules consistent before enabling any real runtime execution.",
                "Reduces risk before future autonomy layers.",
                importance=4,
            ),
            self.build_action_candidate(
                "prepare_safety_review",
                "Track disabled capabilities across file writing, memory writing, journal writing, and command execution.",
                "Maintains safety guarantees across new modules.",
                importance=5,
            ),
        ]

        return self.base_plan(
            plan_type="project_next_action_candidates",
            target=cleaned_topic,
            recommended_steps=[
                "Review the candidate list.",
                "Choose only one small next step for implementation.",
                "Keep the next step aligned with the roadmap and current safety boundaries.",
                "Use project coding assistant for patch planning only.",
                "Do not write files, memory, journal, or commands automatically.",
            ],
            action_candidates=candidates,
        )

    def build_action_candidate(
        self,
        name: str,
        description: str,
        reason: str,
        importance: int = 3,
    ) -> dict[str, Any]:
        return {
            "name": name,
            "description": description,
            "reason": reason,
            "importance": max(1, min(importance, 5)),
            "candidate_only": True,
            "execution_ready": False,
            "executed": False,
            "file_write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
        }

    def context(self) -> dict[str, Any]:
        status = self.status()
        context = self.integration_context()

        return {
            "status": self.status_name,
            "context_ready": True,
            "planner_status": status,
            "identity": self.load_identity(),
            "workspace_memory_context": self.workspace_memory_link.context(),
            "workspace_context": context["workspace_context"],
            "daily_briefing_context": self.daily_briefing.context(limit=5),
            "reflection_context": context["reflection_context"],
            "project_coding_status": context["project_coding_status"],
            "safe_current_capabilities": [
                "project_intent_status",
                "project_intent_summary",
                "project_goal_plan",
                "sprint_intent_plan",
                "project_next_action_candidates",
                "project_intent_context",
            ],
            "disabled_capabilities": [
                "automatic_file_write",
                "automatic_memory_write",
                "automatic_journal_write",
                "command_execution",
                "external_action_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "file_write_performed": False,
            "memory_write_performed": False,
            "journal_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Project Intent Planner context is read-only and proposal-only.",
        }

    def status(self) -> dict[str, Any]:
        workspace_memory_status = self.workspace_memory_link.status()
        workspace_status = self.workspace_awareness.status()
        project_coding_status = self.project_coding.status()
        briefing_status = self.daily_briefing.status()
        reflection_status = self.memory_reflection.status()

        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "intent_ready": True,
            "summary_ready": True,
            "goal_plan_ready": True,
            "sprint_intent_plan_ready": True,
            "next_action_candidates_ready": True,
            "context_ready": True,
            "workspace_memory_link_integration_ready": workspace_memory_status["link_ready"],
            "workspace_awareness_integration_ready": workspace_status["awareness_ready"],
            "project_coding_integration_ready": project_coding_status["analysis_ready"],
            "daily_briefing_integration_ready": briefing_status["briefing_ready"],
            "memory_reflection_integration_ready": reflection_status["reflection_ready"],
            "intent_categories": len(self.intent_categories()),
            "project_python_files": project_coding_status["python_files"],
            "memory_count": reflection_status["memory_count"],
            "journal_count": reflection_status["journal_count"],
            "milestone_count": reflection_status["milestone_count"],
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_read_memory_confirmation": read_memory_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "proposal_only": True,
            "file_write": False,
            "memory_write": False,
            "journal_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Project Intent Planner is online for safe project intent planning. It does not write files, write memory, write journal entries, execute commands, or perform external actions automatically.",
        }
