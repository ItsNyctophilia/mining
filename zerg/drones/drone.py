"""Parent class for all drone zerg units."""
from __future__ import annotations

from typing import List, Optional, Type

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
        self._path: Optional[List[Coordinate]] = None
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

    @property
    def path(self) -> Optional[List[Coordinate]]:
        """The path this drone will take to its destination.

        The destination of this drone will always be the final element of this
        list. Setting the path implicitly sets the destination.
        """
        return self._path

    @path.setter
    def path(self, new_path: List[Coordinate]) -> None:
        self._path = new_path

    @property
    def dest(self) -> Optional[Coordinate]:
        """The coordinates of the current intended destination of this drone.

        This value will automatically be set when the path is updated.
        """
        if self._path:
            return self._path[-1]
        return None

    @classmethod
    def drone_blueprint(
        cls, health: int, capacity: int, moves: int
    ) -> Type[Drone]:
        """Create a custom drone class, with given stats.

        This method can be used to dynamically create a class with arbitrary
        stats, and is ready to be instantiated.

        Args:
            health (int): The drone's maximum health.
            capacity (int): The drone's maximum mineral capacity.
            moves (int): The drone's maximum move's per tick.

        Returns:
            Type[Drone]: A custome drone class.
        """
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
        """Return the refined mineral cost to create a drone of this type.

        Returns:
            float: The refined mineral cost.
        """
        return (
            (cls.max_health / 10)
            + (cls.max_capacity / 5)
            + (cls.max_moves * 3)
        )

    def action(self, context: Context) -> str:
        """Perform some action, based on the type of drone.

        Args:
            context (Context): The context surrounding the drone.

        Returns:
            str: The direction the drone would like to move.
        """
        result = Directions.CENTER.value
        # do not move if no destination set
        if self.dest:
            current_location = Coordinate(context.x, context.y)
            result = self._choose_direction(current_location, self.dest)
        return result

    def _choose_direction(
        self, location: Coordinate, destination: Coordinate
    ) -> str:
        x_diff, y_diff = location.difference(destination)

        # choose direction to move in
        if x_diff > 0:
            self._steps += 1
            direction = Directions.EAST.value
        elif x_diff < 0:
            self._steps += 1
            direction = Directions.WEST.value
        elif y_diff > 0:
            self._steps += 1
            direction = Directions.NORTH.value
        elif y_diff < 0:
            self._steps += 1
            direction = Directions.SOUTH.value
        else:  # x_diff == 0 and y_diff == 0
            # do not move if at current destination
            direction = Directions.CENTER.value
        return direction

    def steps(self) -> int:
        """Accumulated number of steps since the drone was created.

        Returns:
            int: The total number of steps.
        """
        return self._steps
