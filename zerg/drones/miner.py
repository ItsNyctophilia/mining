"""Miner drone, whose primary purpose is to mine minerals."""
from zerg.drones.drone import Drone


class MinerDrone(Drone):
    """Miner drone, whose primary purpose is to mine minerals."""

    max_health = 30
    max_capacity = 10
    max_moves = 2

    def __init__(self) -> None:
        """Initialize a MinerDrone.

        Args:
            health (int): The max health of the miner.
            capacity (int): the max mineral capacity of the miner.
            moves (int): the max moves per tick for the miner.
        """
        super().__init__()
