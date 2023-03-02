"""Abstract base class for all zerg units"""
from abc import ABC

from utils import Context, Directions


class Zerg(ABC):
    """Abstract base class for all zerg units"""

    def __init__(self, health: int) -> None:
        self._health = health

    @property
    def health(self) -> int:
        """The current health of this zerg.

        Returns:
            int: The current health.
        """
        return self._health

    def action(self, context: Context) -> str:
        return Directions.NORTH.name
