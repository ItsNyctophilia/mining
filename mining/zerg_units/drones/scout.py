"""Scout drone, whose primary purpose is revealing the map."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mining.utils import Directions, Icon

from .drone import Drone

if TYPE_CHECKING:
    from mining.utils import Context, Coordinate, Tile
    from mining.zerg_units import Overlord


class ScoutDrone(Drone):
    """Scout drone, whose primary purpose is revealing the map."""

    max_health = 40
    max_capacity = 5
    max_moves = 1

    def __init__(self, overlord: Overlord) -> None:
        """Initialize a ScoutDrone.

        Args:
            overlord (Overlord): The Overlord owning this drone.
        """
        super().__init__(overlord)

    @property
    def icon(self) -> Icon:
        """The icon of this drone type."""
        return Icon.SCOUT

    def action(self, context: Context) -> str:
        """Perform some action, based on the type of drone.

        The scout will check if its current location is the deployment zone and
        if it is blocked by non-traversable tiles on all side. If so, it will
        request to be recalled, otherwise continue on its path.

        Args:
            context (Context): The context surrounding the scout.

        Returns:
            str: The direction the scout would like to move.
        """
        cardinals = [
            Icon(context.north),
            Icon(context.south),
            Icon(context.east),
            Icon(context.west),
        ]
        if all(not icon.traversable() for icon in cardinals):
            self._overlord.enqueue_map_update(self, context)
            self._finish_traveling()
            self._overlord.request_pickup(self)
            return Directions.CENTER.name
        return super().action(context)

    def _update_path(self, curr_tile: Tile) -> Coordinate:
        if self.path[0] == self.dest:
            # next step is an undiscovered tile, stop here
            # TODO: Remove test print
            print(f"Scout reached destination at {self.dest}, stopping here")
            self.path.pop(0)
            return curr_tile.coordinate
        return super()._update_path(curr_tile)
