"""Scout drone, whose primary purpose is revealing the map."""


from zerg.drones.drone import Drone


class ScoutDrone(Drone):
    """Scout drone, whose primary purpose is revealing the map."""

    def __init__(self, health: int, capacity: int, moves: int) -> None:
        """Initialize a ScoutDrone.

        Args:
            health (int): The max health of the scout.
            capacity (int): the max mineral capacity of the scout.
            moves (int): the max moves per tick for the scout.
        """
        super().__init__(health, capacity, moves)
