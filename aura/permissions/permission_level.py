from enum import IntEnum


class PermissionLevel(IntEnum):
    """
    Permission levels for AURA actions.
    """

    THINK_ONLY = 0
    SUGGEST = 1
    READ = 2
    PREPARE = 3
    ACT_WITH_CONFIRMATION = 4
    RESTRICTED = 5

    @property
    def label(self) -> str:
        labels = {
            PermissionLevel.THINK_ONLY: "Think Only",
            PermissionLevel.SUGGEST: "Suggest",
            PermissionLevel.READ: "Read",
            PermissionLevel.PREPARE: "Prepare",
            PermissionLevel.ACT_WITH_CONFIRMATION: "Act With Confirmation",
            PermissionLevel.RESTRICTED: "Restricted",
        }
        return labels[self]

    @property
    def description(self) -> str:
        descriptions = {
            PermissionLevel.THINK_ONLY: "AURA only thinks and responds with text.",
            PermissionLevel.SUGGEST: "AURA may suggest something when context is clear.",
            PermissionLevel.READ: "AURA may read permitted files, logs, screen, or project state.",
            PermissionLevel.PREPARE: "AURA may prepare drafts, plans, commands, or files.",
            PermissionLevel.ACT_WITH_CONFIRMATION: "AURA may act only after explicit confirmation.",
            PermissionLevel.RESTRICTED: "AURA must not do this without explicit approval or special handling.",
        }
        return descriptions[self]
