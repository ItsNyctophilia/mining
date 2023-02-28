"""Abstract base class for all zerg units"""
from abc import ABC
from enum import Enum

from utils.context import Context


class Zerg(ABC):
    """Abstract base class for all zerg units"""

    class Directions(Enum):
        NORTH = "NORTH"
        SOUTH = "SOUTH"
        EAST = "EAST"
        WEST = "WEST"

    def __init__(self, health: int) -> None:
        self._health = health

    def action(self, context: Context) -> str:
        return Zerg.Directions.NORTH.value
