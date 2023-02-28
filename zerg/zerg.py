"""Abstract base class for all zerg units"""
from abc import ABC
from enum import Enum
from typing import NamedTuple

from utils.context import Context


class Zerg(ABC):
    """Abstract base class for all zerg units"""

    class Directions(Enum):
        NORTH = "NORTH"
        SOUTH = "SOUTH"
        EAST = "EAST"
        WEST = "WEST"

    class Coordinate(NamedTuple):
        x: int
        y: int

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
        return self.Directions.NORTH.value
