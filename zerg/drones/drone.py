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
        self._path_to_goal: Optional[List[Coordinate]] = None
        self._path_traveled: Optional[List[Coordinate]] = None
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
        return self._path_to_goal

    @path.setter
    def path(self, new_path: List[Coordinate]) -> None:
        self._path_to_goal = new_path
        self._path_traveled = []

    @property
    def dest(self) -> Optional[Coordinate]:
        """The coordinates of the current intended destination of this drone.

        This value will automatically be set when the path is updated.
        """
        return self._path_to_goal[-1] if self._path_to_goal else None

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
        # do not move if no path set
        if self.path:
            current_location = Coordinate(context.x, context.y)
            dest = self._update_path(current_location, self.path)
            result = self._choose_direction(current_location, dest)
        return result

    def _update_path(
        self, curr: Coordinate, path: List[Coordinate]
    ) -> Coordinate:
        """Check if the currecnt location is on the path, and remove if so.

        Args:
            curr (Coordinate): The drone's current location.
            path (List[Coordinate]): The path the drone should follow.

        Returns:
            Coordinate: The intended next destination of the drone.
        """
        dest = path[0]
        if curr.x == path[0].x and curr.y == path[0].y:
            path.pop(0)
            # may have popped off the last item in the path, which is the
            # final destination
            if path:
                dest = path[0]
        return dest

    def _choose_direction(self, curr: Coordinate, dest: Coordinate) -> str:
        """Choose which cardinal direction the drone should head.

        Args:
            curr (Coordinate): The drone's current location.
            dest (Coordinate): The destination of the drone.

        Returns:
            str: The direction the drone should head to reach the destination.
        """
        x_diff, y_diff = curr.difference(dest)

        # choose direction to move in
        if x_diff > 0:
            self._steps += 1
            return Directions.EAST.value
        elif x_diff < 0:
            self._steps += 1
            return Directions.WEST.value
        elif y_diff > 0:
            self._steps += 1
            return Directions.NORTH.value
        elif y_diff < 0:
            self._steps += 1
            return Directions.SOUTH.value
        else:  # x_diff == 0 and y_diff == 0
            # do not move if at current destination
            return Directions.CENTER.value

    def steps(self) -> int:
        """Accumulated number of steps since the drone was created.

        Returns:
            int: The total number of steps.
        """
        return self._steps
