"""Parent class for all drone zerg units."""


from zerg.zerg import Zerg


class Drone(Zerg):
    """Parent class for all drone zerg units."""

    def __init__(self, health: int, capacity: int, moves: int) -> None:
        super().__init__(health)
        self._capacity = capacity
        self._moves = moves
