"""A single tile on the map."""
from typing import Optional

from .coordinate import Coordinate
from .icon import Icon


class Tile:
    def __init__(self, coordinate: Coordinate, icon: Optional[Icon] = None):
        self._coordinate = coordinate
        self._icon = icon

    @property
    def coordinate(self) -> Coordinate:
        """The coordinates of this tile on the map."""
        return self._coordinate

    @property
    def icon(self) -> Optional[Icon]:
        """The icon for this tile.

        Setting the icon for a tile implicitly makes it discovered. If a tile
        is not discovered, the icon will always be None."""
        return self._icon or None

    @icon.setter
    def icon(self, icon: Icon) -> None:
        if not icon:
            raise ValueError("Cannot set icon to None")
        self._icon = icon

    @property
    def discovered(self) -> bool:
        """True if the tile has been discovered and has an icon, else False."""
        return bool(self.icon)
