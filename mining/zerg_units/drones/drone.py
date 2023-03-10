"""Parent class for all drone zerg units."""

from __future__ import annotations

import logging
from enum import Enum, auto
from typing import TYPE_CHECKING, TypeVar

from mining.utils import Coordinate, Directions, Icon, Map, Tile
from mining.zerg_units.zerg import Zerg

if TYPE_CHECKING:
    from typing import List, Optional, Type

    from mining.utils import Context
    from mining.zerg_units import Overlord


class Drone(Zerg):
    """Parent class for all drone zerg units."""

    max_health = 40
    max_capacity = 10
    max_moves = 1

    def __init__(self, overlord: Overlord) -> None:
        """Initialize a Drone."""
        super().__init__(self.max_health)
        self._overlord = overlord
        self._capacity = 0
        self._path_to_goal: List["Coordinate"] = []
        self._path_traveled: List["Coordinate"] = []
        self._steps = 0
        self.state = State.WAITING
        self.map: Optional[Map]
        self._previous_tile: Optional[Tile] = None

    @property
    def capacity(self) -> int:
        """The max mineral capacity for this drone.

        Returns:
            int: The max capacity.
        """
        return self.max_capacity

    def reset_minerals(self) -> None:
        """Reset all minerals this drone may be carrying.

        This should only be called by the overlord after the drone has be
        retrieved from the map.
        """
        self._capacity = 0

    @property
    def moves(self) -> int:
        """The max moves this drone can take in 1 tick.

        Returns:
            int: The drone's max moves.
        """
        return self.max_moves

    @property
    def path(self) -> List["Coordinate"]:
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
        self.state = State.TRAVELING if len(new_path) > 2 else State.WAITING

    @property
    def dest(self) -> Optional[Coordinate]:
        """The coordinates of the current intended destination of this drone.

        This value will automatically be set when the path is updated.
        """
        return self._path_to_goal[-1] if self._path_to_goal else None

    def take_damage(self, damage) -> bool:
        """Take damage.

        If the drone died, the Overlord will be notified.

        Args:
            damage (int): The damage to take.

        Returns:
            bool: False if taking damage caused the drone to die.
        """
        self._health -= damage
        if not (alive := self._health > 0):
            # If the drone times out before the action can be returned, this
            # may cause an issue
            self._overlord.mark_drone_dead(self)
        return alive

    @property
    def icon(self) -> Icon:
        """The icon of this drone type."""
        raise NotImplementedError("Drone subtypes must implement icon")

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
        # TODO: Remove test print
        print(
            f"Acting!ID: {id(self)} context: {context} path: {self.path} "
            f" traveled:{self._path_traveled}"
        )
        self._overlord.enqueue_map_update(self, context)
        result = Directions.CENTER.name
        # do not move if no path set
        if self.path:
            result = self._travel(context)
        else:
            self._finish_traveling()
        return result

    def _travel(self, context: Context):
        curr_tile = self.map[Coordinate(context.x, context.y)]
        dest = self._update_path(curr_tile)
        return self._choose_direction(curr_tile.coordinate, dest, context)

    def _update_path(self, curr_tile: Tile) -> Coordinate:
        """Check if the current location is on the path, and remove if so.

        Args:
            curr (Coordinate): The drone's current location.

        Returns:
            Coordinate: The intended next destination of the drone.
        """
        next_step = self.path[0]
        # only pop if last action caused movement
        if curr_tile.coordinate == next_step:
            self._handle_occupation(curr_tile)
            self._path_traveled.insert(0, self.path.pop(0))
            # if false, currently at destination
            if self.path:
                next_step = self.path[0]

        return next_step

    def _handle_occupation(self, curr_tile: Tile) -> None:
        curr_tile.occupied_drone = self
        if self._previous_tile:
            self._previous_tile.occupied_drone = None
        self._previous_tile = curr_tile

    def _choose_direction(
        self, curr: Coordinate, dest: Coordinate, context: Context
    ) -> str:
        """Choose which cardinal direction the drone should head.

        Health calculations will be made during this call. If the drone dies,
        the Overlord will be notified.

        Args:
            curr (Coordinate): The drone's current location.
            dest (Coordinate): The destination of the drone.
            context (Context): The context surrounding the drone.

        Returns:
            str: The direction the drone should head to reach the destination.
        """
        direction = curr.direction(dest).upper()
        if direction == Directions.CENTER.name:
            self._finish_traveling()
        else:
            target = Icon(getattr(context, direction.lower()))
            self._handle_moving(target)
        # TODO: Remove test print
        print(f"Moving {direction}!")
        return direction

    def _handle_moving(self, target: Icon) -> None:
        """Perform any necessary tasks that come with moving the drone.

        Args:
            target (Icon): The icon of the targeted tile.
        """
        self.take_damage(target.health_cost())
        self._hit_mineral(target)
        if target.traversable():
            self._steps += 1

    def _hit_mineral(self, target: Icon) -> bool:
        # TODO: Remove test print
        print(f"Checking Tile {target} capacity: {self._capacity}...")
        if (
            is_mineral := (target == Icon.MINERAL.value)
        ) and self._capacity <= self.max_capacity:
            # TODO: Remove test print
            print("Target is a mineral!")
            self._capacity += 1
        return is_mineral

    def _finish_traveling(self) -> None:
        """Perform some operations to signify traveling is done.

        This method is mostly for subtypes to create a hook and modify behavior
        during travel. The drone base class will call this method whenever it
        reaches it's intended destination.
        """
        self.state = State.WAITING

    def steps(self) -> int:
        """Accumulated number of steps since the drone was created.

        Returns:
            int: The total number of steps.
        """
        return self._steps

    def __str__(self):
        """Return the string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        # TODO: Finish pretty printing
        base = super().__str__()
        return (
            f"{base} current health = {self.health}, "
            f"max capacity = {self.capacity}, moves per turn = {self.moves}, "
            f"current destination = {self.dest}, "
            f"Drone is {'' if self.state else 'not '}traveling"
        )

    def __repr__(self) -> str:
        """Return a representation of this object.

        The string returned by this method is not valid for a call to eval.

        Returns:
            str: The string representation of this object.
        """
        # TODO: Finish string representation
        return (
            f"Drone({self.health=}, {self.capacity=}, {self.moves=}, "
            f"{self.path=})"
        )

    def log_creation(self, message: str) -> None:
        """Log the creation of a drone.

        Logging is stored in a special file in the current directory.
        https://www.geeksforgeeks.org/logging-in-python/
        arguments:
            message (str) : message that will display in the log.
        """
        # Create and configure logger
        logging.basicConfig(
            filename="drone.log",
            format="%(asctime)s %(message)s",
            filemode="w",
        )

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        drone_id = id(self)
        drone_type = type(self).__name__
        # Scoutdrone id has been created
        logger.info(f"{drone_type} {drone_id} {message}")


class State(Enum):
    """Drone states."""

    TRAVELING = auto()
    WORKING = auto()
    WAITING = auto()


T = TypeVar("T", bound=Drone)
