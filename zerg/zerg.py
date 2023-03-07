"""Abstract base class for all zerg units."""
from abc import ABC, abstractmethod

from utils import Context


class Zerg(ABC):
    """Abstract base class for all zerg units."""

    def __init__(self, health: int) -> None:
        """Initialize a zerg unit.

        The zerg's health must be at least 1.

        Raises:
            ValueError: if the passed in health is less than 1

        Args:
            health (int): The zerg's maximum health.
        """
        if health <= 0:
            raise ValueError("Zerg health must be 1 or greater")
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
        """Perform some action, based on the type of zerg.

        Args:
            context (Context): The context surrounding the zerg.

        Returns:
            str: The action the zerg wants to take.
        """
        raise NotImplementedError("Zerg subtypes must implement action")

    def __str__(self):
        """Return the string representation of this object.

        Returns:
            _type_: The string representation of this object.
        """
        # TODO: Finish pretty printing
        return f"{self.__class__}"
