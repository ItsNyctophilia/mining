"""Scout drone, whose primary purpose is revealing the map."""
from zerg.drones.drone import Drone


class ScoutDrone(Drone):
    """Scout drone, whose primary purpose is revealing the map."""

    max_health = 40
    max_capacity = 5
    max_moves = 1

    def __init__(self) -> None:
        """Initialize a ScoutDrone.

        Args:
            health (int): The max health of the scout.
            capacity (int): the max mineral capacity of the scout.
            moves (int): the max moves per tick for the scout.
        """
        super().__init__()
