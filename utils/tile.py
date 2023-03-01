"""A single tile on the map."""


from dataclasses import InitVar, dataclass
from typing import Optional

from utils import Coordinate, Icon


@dataclass
class Tile:
    location: InitVar[Coordinate]
    icon: Optional[Icon] = None
    discovered: bool = False

    def __post_init__(self, location):
        if self.discovered and not self.icon:
            raise ValueError("A discovered tile must have an icon")
        if not self.discovered and self.icon:
            raise ValueError("An undiscovered tile cannot have an icon")
        self._coordinate = location

    @property
    def coordinate(self) -> Coordinate:
        """The coordinates of this tile on the map."""
        return self._coordinate
