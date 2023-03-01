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
        self._coordinate = location

    @property
    def coordinate(self) -> Coordinate:
        """The coordinates of this tile on the map."""
        return self._coordinate
