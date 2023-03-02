"""An icon on the map."""

from enum import Enum


class Icon(Enum):
    ZERG = "Z"
    WALL = "#"
    DEPLOY_ZONE = "_"
    MINERAL = "*"
    ACID = "~"
    EMPTY = " "

    def traversable(self) -> bool:
        """Whether a tile with this icon is traversable by a drone.

        Returns:
            bool: True if traversable, else False.
        """
        return self in [Icon.DEPLOY_ZONE, Icon.ACID, Icon.EMPTY]

    def health_cost(self) -> int:
        """Return the health cost for traversing over this tile.

        If the tile is not traversable, a value of -1 will be returned.

        Returns:
            int: A non-negative number representing the health cost, or -1.
        """
        if self is Icon.WALL:
            return 1
        elif self is Icon.ACID:
            return 3
        else:
            return 0
