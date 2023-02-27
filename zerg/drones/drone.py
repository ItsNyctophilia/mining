"""Parent class for all drone zerg units."""


from zerg.zerg import Zerg


class Drone(Zerg):
    """Parent class for all drone zerg units."""

    def __init__(self, health: int, capacity: int, moves: int) -> None:
        """Initialize a Drone.

        Args:
            health (int): The max health of the drone.
            capacity (int): the max mineral capacity of the drone.
            moves (int): the max moves per tick for the drone.
        """
        super().__init__(health)
        self._capacity = capacity
        self._moves = moves
