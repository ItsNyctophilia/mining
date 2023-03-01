"""A single tile on the map."""


from dataclasses import dataclass
from typing import Optional

from utils import Coordinate, Icon


@dataclass
class Tile:
    coordinate: Coordinate
    icon: Optional[Icon] = None
    discovered: bool = False
