from aura.roles.role import AuraRole


class RoleRegistry:
    """
    Registry for AURA internal roles.
    """

    def __init__(self):
        self.roles: dict[str, AuraRole] = {}

    def register(self, role: AuraRole) -> None:
        self.roles[role.name] = role

    def get(self, name: str) -> AuraRole | None:
        return self.roles.get(name)

    def list_roles(self) -> list[AuraRole]:
        return list(self.roles.values())

    def count(self) -> int:
        return len(self.roles)
