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

    def occupy(self) -> bool:
        """Occupy this tile with a zerg drone.

        An occupied tile will return a zerg icon for the icon property. An
        occupied tile will remember the icon that was on it before the zerg
        occupied it. Trying to occupy a tile that is already occupied, or has
        a wall or mineral icon will fail. An undiscovered tile cannot be
        occupied. Trying to occupy an undiscovered tile will raise an exception

        Raises:
            RuntimeError: If the tile is undiscovered, and therefore cannot
                be occupied.

        Returns:
            bool: Whether occupation of the tile succeeded.
        """
        return False

    def unoccupy(self) -> bool:
        """Unoccupy this tile with a zerg drone.

        Unoccupying a tile will cause the original icon on the tile to returned
        by the icon property. Trying to unoccupy a tile that was not unoccupied
        will fail with no operation happening. Trying to unoccupy an
        undiscovered tile will raise an exception.

        Raised:
            RuntimeError: If the tile is undiscovered, and therefor cannot be
                unoccupied.

        Returns:
            bool: Whether the tile was able to be unoccupied.
        """
        return False
