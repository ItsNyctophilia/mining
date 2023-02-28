"""Parent class for all drone zerg units."""
from __future__ import annotations

from typing import Type

from utils import Context, Coordinate, Directions
from zerg.zerg import Zerg


class Drone(Zerg):
    """Parent class for all drone zerg units."""

    max_health = 40
    max_capacity = 10
    max_moves = 1

    def __init__(self) -> None:
        """Initialize a Drone."""
        super().__init__(self.max_health)
        self._capacity = self.max_capacity
        self._moves = self.max_moves
        # TODO: temp attribute, will eventually keep a list of path travelled
        self._steps = 0

    @property
    def capacity(self) -> int:
        """The max mineral capacitry for this drone.

        Returns:
            int: The max capacity.
        """
        return self._capacity

    @property
    def moves(self) -> int:
        """The max moves this drone can take in 1 tick.

        Returns:
            int: The drone's max moves.
        """
        return self._moves

    @classmethod
    def drone_blueprint(
        cls, health: int, capacity: int, moves: int
    ) -> Type[Drone]:
        return type(
            "CustomDrone",
            (Drone,),
            {
                "max_health": health,
                "max_capacity": capacity,
                "max_moves": moves,
            },
        )

    @classmethod
    def get_init_cost(cls) -> float:
        return (
            (cls.max_health / 10)
            + (cls.max_capacity / 5)
            + (cls.max_moves * 3)
        )

    def action(self, context: Context) -> str:
        self._steps += 1
        return Directions.NORTH.value

    def steps(self) -> int:
        return self._steps
