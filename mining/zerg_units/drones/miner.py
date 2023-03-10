"""Miner drone, whose primary purpose is to mine minerals."""
from __future__ import annotations

from typing import TYPE_CHECKING

from mining.utils import Icon

from .drone import Drone, State

if TYPE_CHECKING:
    from typing import List, Optional

    from mining.utils import Context, Coordinate
    from mining.zerg_units import Overlord


class MinerDrone(Drone):
    """Miner drone, whose primary purpose is to mine minerals."""

    max_health = 30
    max_capacity = 10
    max_moves = 2

    def __init__(self, overlord: "Overlord") -> None:
        """Initialize a Miner.

        Args:
            overlord (Overlord): The Overlord owning this drone.
        """
        super().__init__(overlord)
        self._mineral_location: Optional["Coordinate"] = None

    @property
    def icon(self) -> Icon:
        """The icon of this drone type."""
        return Icon.MINER

    @Drone.path.setter
    def path(self, new_path: List["Coordinate"]) -> None:
        """Set the path this drone will take towards the tasked mineral."""
        # separate mineral tile as new attribute
        self._mineral_location = new_path.pop()
        self._mineral_direction = new_path[-1].direction(
            self._mineral_location
        )
        super(type(self), type(self)).path.fset(self, new_path)

    def action(self, context: "Context") -> str:
        # sourcery skip: assign-if-exp, reintroduce-else
        """Perform some action.

        A miner will move towards an assigned mineral, and mine it until the
        mineral is depleted. After done mining, the miner will return to the
        landing zone and await retrieval from the overlord.The miner will
        return early if its capacity is maxed out or if continued mining will
        cause it to die.

        Args:
            context (Context): The drone's current location.

        Returns:
            str: The intended next destination of the drone.
        """
        # TODO: Remove test print
        print(f"Looking for mineral at {self._mineral_location}")
        result = super().action(context)
        if self.state == State.WORKING:
            return self._mine(context)
        else:
            return result

    def _mine(self, context: "Context") -> str:
        """Mine the miner's tasked mineral until it is depleted.

        Args:
            context (Context): The surrounding context of the miner.

        Returns:
            str: The direction the miner wants to move.
        """
        dest_icon = getattr(context, self._mineral_direction)
        if self._hit_mineral(dest_icon):
            # TODO: Remove test print
            print(f"Mining mineral at {self._mineral_location}")
            return self._mineral_direction.upper()
        self._deplete_mineral()
        return super().action(context)

    def _deplete_mineral(self):
        if self.map and self._mineral_location:
            self.map.tasked_minerals.remove(self._mineral_location)
            self._mineral_location = None
            super(type(self), type(self)).path.fset(self, self._path_traveled)
            self.state = State.TRAVELING

    def _finish_traveling(self):
        # set state to working if miner tasked with a mineral
        # else assume at loading zone and wait for pickup
        if self._mineral_location:
            self.state = State.WORKING
        else:
            self._overlord.request_pickup(self)
            self.state = State.WAITING
