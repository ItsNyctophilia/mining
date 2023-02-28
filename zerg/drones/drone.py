"""Parent class for all drone zerg units."""


from zerg.zerg import Zerg


class Drone(Zerg):
    """Parent class for all drone zerg units."""

    max_health = 40
    max_capacity = 10
    max_moves = 1

    def __init__(self) -> None:
        """Initialize a Drone.

        Args:
            health (int): The max health of the drone.
            capacity (int): the max mineral capacity of the drone.
            moves (int): the max moves per tick for the drone.
        """
        super().__init__(self.max_health)
        self._capacity = self.max_capacity
        self._moves = self.max_moves
