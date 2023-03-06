"""Parent class for all drone zerg units."""
from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Type

from utils import Context, Coordinate, Directions
from zerg import Zerg


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
        self._path_to_goal: List[Coordinate] = []
        self._path_traveled: List[Coordinate] = []
        self._steps = 0
        self._state = State.WAITING

    @property
    def capacity(self) -> int:
        """The max mineral capacity for this drone.

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
    def path(self) -> List[Coordinate]:
        """The path this drone will take to its destination.

        The destination of this drone will always be the final element of this
        list. Setting the path implicitly sets the destination.
        """
        return self._path_to_goal

    @path.setter
    def path(self, new_path: List[Coordinate]) -> None:
        self._path_to_goal = new_path
        self._path_traveled = []
        # traveling if path length is greater than 2 (start, dest)
        self._state = State.TRAVELING if len(new_path) > 2 else State.WAITING

    @property
    def dest(self) -> Optional[Coordinate]:
        """The coordinates of the current intended destination of this drone.

        This value will automatically be set when the path is updated.
        """
        return self._path_to_goal[-1] if self._path_to_goal else None

    @classmethod
    def drone_blueprint(
        cls,
        health: int,
        capacity: int,
        moves: int,
        drone_class: Optional[Type[T]] = None,
    ) -> Type[T]:
        """Create a custom drone class, with given stats.

        This method can be used to dynamically create a class with arbitrary
        stats, and is ready to be instantiated.

        Args:
            health (int): The drone's maximum health.
            capacity (int): The drone's maximum mineral capacity.
            moves (int): The drone's maximum move's per tick.
            drone_class (Type[Drone]): The type the custom class will
                extend from.

        Returns:
            Type[Drone]: A custom drone class.
        """
        # TODO: type hints still not working perfectly
        if not drone_class:
            drone_class = cls  # type: ignore
        new_drone_type: Type[T] = type(
            "CustomDrone",
            (drone_class,),  # type: ignore
            {
                "max_health": health,
                "max_capacity": capacity,
                "max_moves": moves,
            },
        )
        cost = new_drone_type.get_init_cost()
        msg = (
            "Invalid parameters; "
            "total drone cost must result in a whole number: "
            f"{health=}, {capacity=}, {moves=}, {cost=}"
        )
        # check if cost is a whole number
        if cost != int(cost):
            raise ValueError(msg)
        return new_drone_type

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
        result = Directions.CENTER.name
        # do not move if no path set
        if self.path:
            current_location = Coordinate(context.x, context.y)
            dest = self._update_path(current_location, self.path)
            result = self._choose_direction(current_location, dest)
        else:
            self._finish_traveling()
        return result

    def _update_path(
        self, curr: Coordinate, path: List[Coordinate]
    ) -> Coordinate:
        """Check if the current location is on the path, and remove if so.

        Args:
            curr (Coordinate): The drone's current location.
            path (List[Coordinate]): The path the drone should follow.

        Returns:
            Coordinate: The intended next destination of the drone.
        """
        # only pop if last action caused movement
        if curr == path[0] and len(path) > 1:
            path.pop(0)
        return path[0]

    def _choose_direction(self, curr: Coordinate, dest: Coordinate) -> str:
        """Choose which cardinal direction the drone should head.

        Args:
            curr (Coordinate): The drone's current location.
            dest (Coordinate): The destination of the drone.

        Returns:
            str: The direction the drone should head to reach the destination.
        """
        # choose direction to move in
        direction = curr.direction(dest).upper()
        if direction == Directions.CENTER.name:
            self._finish_traveling()
        else:
            self._steps += 1
        return direction

    def _finish_traveling(self):
        """Perform some operations to signify traveling is done.

        This method is mostly for subtypes to create a hook and modify behavior
        during travel. The drone base class will call this method whenever it
        reaches it's intended destination.
        """
        self._state = State.WAITING

    def steps(self) -> int:
        """Accumulated number of steps since the drone was created.

        Returns:
            int: The total number of steps.
        """
        return self._steps

class State(Enum):
    """Drone states."""

    TRAVELING = auto()
    WORKING = auto()
    WAITING = auto()


T = TypeVar("T", bound=Drone)
