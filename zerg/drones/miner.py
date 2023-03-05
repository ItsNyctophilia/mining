"""Miner drone, whose primary purpose is to mine minerals."""
from utils.context import Context
from utils.directions import Directions

from .drone import Drone


class MinerDrone(Drone):
    """Miner drone, whose primary purpose is to mine minerals."""

    max_health = 30
    max_capacity = 10
    max_moves = 2

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
        if self._traveling:
            return super().action(context)
        return self._mine(context)

    def _mine(self, context: Context) -> str:
        # TODO: Actually mine the mineral
        return Directions.CENTER.name
