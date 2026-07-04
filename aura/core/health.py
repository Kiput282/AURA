from dataclasses import dataclass
from typing import Literal


HealthState = Literal["OK", "NOT_READY", "WARNING", "ERROR"]


@dataclass
class HealthItem:
    name: str
    status: HealthState
    detail: str = ""


class HealthCheck:
    """
    Basic health check system for AURA.

    This will eventually check:
    - core
    - config
    - identity
    - events
    - memory
    - plugins
    - voice
    - vision
    """

    def __init__(self):
        self.items: list[HealthItem] = []

    def add(self, name: str, status: HealthState, detail: str = "") -> None:
        self.items.append(HealthItem(name=name, status=status, detail=detail))

    def summary(self) -> list[HealthItem]:
        return self.items

    def print_summary(self) -> None:
        print()
        print("AURA Health Check")
        print("=================")

        for item in self.items:
            detail = f" - {item.detail}" if item.detail else ""
            print(f"{item.name:<10}: {item.status}{detail}")
