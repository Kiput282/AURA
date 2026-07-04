from aura.permissions.permission_manager import PermissionManager
from aura.permissions.permission_request import PermissionCheckResult
from aura.skills.skill import AuraSkill


class SkillRegistry:
    """
    Registry for AURA skills.

    Skills describe what AURA can do.
    Each skill belongs to a role and maps to a permission action.
    """

    def __init__(self):
        self.skills: dict[str, AuraSkill] = {}

    def register(self, skill: AuraSkill) -> None:
        self.skills[skill.name] = skill

    def get(self, name: str) -> AuraSkill | None:
        return self.skills.get(name)

    def list_skills(self) -> list[AuraSkill]:
        return list(self.skills.values())

    def list_by_role(self, role: str) -> list[AuraSkill]:
        return [
            skill
            for skill in self.list_skills()
            if skill.role == role
        ]

    def count(self) -> int:
        return len(self.skills)

    def check_permission(self, skill: AuraSkill) -> PermissionCheckResult:
        permission_manager = PermissionManager()
        return permission_manager.check(action=skill.permission_action)
