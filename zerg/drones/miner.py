"""Miner drone, whose primary purpose is to mine minerals."""
from zerg.drones.drone import Drone


class MinerDrone(Drone):
    """Miner drone, whose primary purpose is to mine minerals."""

    max_health = 30
    max_capacity = 10
    max_moves = 2

    def __init__(self) -> None:
        """Initialize a MinerDrone."""
        super().__init__()
