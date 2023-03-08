"""Miner drone, whose primary purpose is to mine minerals."""
from typing import List, Optional

from mining.utils import Context, Coordinate, Icon

from .drone import Drone, State


class MinerDrone(Drone):
    """Miner drone, whose primary purpose is to mine minerals."""

    max_health = 30
    max_capacity = 10
    max_moves = 2

    def __init__(self, overlord) -> None:
        """Initialize a Miner."""
        super().__init__(overlord)
        self._mineral_location: Optional[Coordinate] = None

    @Drone.path.setter
    def path(self, new_path: List[Coordinate]) -> None:
        """Set the path this drone will take towards the tasked mineral."""
        # separate mineral tile as new attribute
        self._mineral_location = new_path.pop()
        self._mineral_direction = new_path[-1].direction(
            self._mineral_location
        )
        super(type(self), type(self)).path.fset(self, new_path)

    def action(self, context: Context) -> str:
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
        result = super().action(context)
        if self._state == State.WORKING:
            return self._mine(context)
        else:
            return result

    def _mine(self, context: Context) -> str:
        """Mine the miner's tasked mineral until it is depleted.

        Args:
            context (Context): The surrounding context of the miner.

        Returns:
            str: The direction the miner wants to move.
        """
        dest_icon = getattr(context, self._mineral_direction)
        if dest_icon == Icon.MINERAL.value:
            return self._mineral_direction.upper()
        super(type(self), type(self)).path.fset(self, self._path_traveled)
        self._state = State.TRAVELING
        return super().action(context)

    def _finish_traveling(self):
        # set state to working if miner tasked with a mineral
        # else assume at loading zone and wait for pickup
        self._state = (
            State.WORKING if self._mineral_location else State.WAITING
        )