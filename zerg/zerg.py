"""Abstract base class for all zerg units"""


from abc import ABC

from utils.context import Context


class Zerg(ABC):
    """Abstract base class for all zerg units"""

    def __init__(self, health: int) -> None:
        self._health = health

    def action(self, context: Context) -> str:
        return ""
