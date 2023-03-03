"""Abstract base class for all zerg units"""
from abc import ABC, abstractmethod

from utils import Context


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

    @abstractmethod
    def action(self, context: Context) -> str:
        raise NotImplementedError("Zerg subtypes must implement action")
