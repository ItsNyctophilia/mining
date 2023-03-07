"""Base class for all zerg drone testing."""
import random
import unittest
from test.testing_utils import TestingUtils
from typing import Dict, List, NamedTuple, Optional, Tuple, Type, TypeVar

from utils import Context, Coordinate, Directions, Icon, Map, Tile
from zerg import Overlord
from zerg.drones import Drone

T = TypeVar("T", bound=Drone)


class BaseDroneTester(unittest.TestCase):
    """Base class for all zerg drone testing."""

    total_ticks = random.randint(10, 100)
    refined_minerals = random.randint(100, 1000)
    overlord = Overlord(total_ticks, refined_minerals)
    CustomDroneStat = NamedTuple(
        "CustomDroneStat",
        [
            ("health", int),
            ("capacity", int),
            ("moves", int),
            ("init", Type[T]),
        ],
    )

    RANDOM_TEST_RUNS = 50
    DIRECTIONS = [d.name for d in Directions]
    phony_context_ = Context()
    map_ = Map()
    minerals_: Dict[Tile, int] = {}

    def _randomize_stats(self) -> Tuple[int, int, int]:
        health = random.randrange(10, 101, 10)
        capacity = random.randrange(5, 51, 5)
        moves = random.randrange(1, 11, 5)
        return health, capacity, moves

    def _build_dynamic_units(
        self, drone_type: Type[T]
    ) -> Tuple[List[T], List[CustomDroneStat]]:
        custom_drones_: List[T] = []
        custom_drone_stats_: List[BaseDroneTester.CustomDroneStat] = []
        for _ in range(self.RANDOM_TEST_RUNS):
            health, capacity, moves = self._randomize_stats()
            blueprint: Type[T] = Drone.drone_blueprint(
                health, capacity, moves, drone_type
            )
            custom_drones_.append(blueprint(self.overlord))
            custom_drone_stats_.append(
                self.CustomDroneStat(health, capacity, moves, blueprint)
            )
        return custom_drones_, custom_drone_stats_

    def _init_start_dest(
        self,
        start: Optional[Tile] = None,
        dest: Optional[Tile] = None,
    ) -> Tuple[Tile, Tile]:
        if not start:
            start = Tile(Coordinate(0, 0), Icon.EMPTY)
        if not dest:
            coord = TestingUtils._randomize_coordinate(
                -100, 100, avoid=start.coordinate
            )
            dest = Tile(coord, Icon.EMPTY)
        return start, dest

    def _update_axis(self, curr_axis: int, dest_axis: int) -> int:
        if curr_axis < dest_axis:
            return 1
        elif curr_axis > dest_axis:
            return -1
        else:
            return 0

    def _generate_path(
        self,
        *,
        start: Optional[Tile] = None,
        dest: Optional[Tile] = None,
    ) -> List[Tile]:
        start, dest = self._init_start_dest(start, dest)
        path = [dest]
        x, y = dest.coordinate
        start_x, start_y = start.coordinate
        while x != start_x or y != start_y:
            if update := self._update_axis(x, start_x):
                x += update
            else:
                y += self._update_axis(y, start_y)
            new_tile = Tile(Coordinate(x, y), Icon.EMPTY)
            self._register_tile(new_tile)
            path.insert(0, new_tile)
        return path

    def _drone_act(self, travel_info: Dict[str, int], drone: Drone) -> bool:
        """Allow the drone to act.

        Return True if the drone requests to continue moving, else False.

        Args:
            travel_info (Dict[str, int]): Information on the drone's travel.
            drone (Drone): The drone traveling.
            context (Context): The context surrounding the drone.

        Returns:
            bool: True if the drones wants to move, else False.
        """
        context = self._get_context_from_map(
            Coordinate(travel_info["x"], travel_info["y"])
        )
        direction = drone.action(context)
        if direction == Directions.EAST.name:
            return self._move_up_or_right(travel_info, "x")
        elif direction == Directions.NORTH.name:
            return self._move_up_or_right(travel_info, "y")
        elif direction == Directions.SOUTH.name:
            return self._move_down_or_left(travel_info, "y")
        elif direction == Directions.WEST.name:
            return self._move_down_or_left(travel_info, "x")
        else:
            return False

    def _get_context_from_map(self, coord: Coordinate) -> Context:
        cardinals = dict(
            zip(["north", "south", "east", "west"], coord.cardinals())
        )
        icons: Dict[str, str] = {
            "north": self.map_.get(
                cardinals["north"], Tile(cardinals["north"], Icon.EMPTY)
            ).icon.value,
            "south": self.map_.get(
                cardinals["south"], Tile(cardinals["south"], Icon.EMPTY)
            ).icon.value,
            "east": self.map_.get(
                cardinals["east"], Tile(cardinals["east"], Icon.EMPTY)
            ).icon.value,
            "west": self.map_.get(
                cardinals["west"], Tile(cardinals["west"], Icon.EMPTY)
            ).icon.value,
        }
        return Context(*coord, **icons)

    def _register_tile(self, tile: Tile) -> None:
        context = self._get_context_from_map(tile.coordinate)
        self.map_.update_context(context)
        if tile.icon == Icon.MINERAL:
            self.minerals_[tile] = random.randint(1, 9)

    def _update_tile(self, coord: Coordinate) -> bool:
        """Update the tile if the testing class is tracking it.

        If the tile at the coordinate is tracked and is a mineral, decrement
        its health and possibly remove it. Will also return whether a drone
        can move into this tile on the tick it was possibly updated.

        Args:
            coord (Coordinate): The coordinate of the tile to update.

        Returns:
            bool: True if a drone can move into this tile, else False.
        """
        if tile := self.map_.get(coord, None):
            if tile in self.minerals_:
                self.minerals_[tile] -= 1
                if self.minerals_[tile] == 0:
                    del self.minerals_[tile]
                    tile.icon = Icon.EMPTY
                return False
        return True

    def _move_down_or_left(
        self, travel_info: Dict[str, int], axis: str
    ) -> bool:
        coord = Coordinate(travel_info["x"], travel_info["y"])
        dest = coord._replace(**{axis: travel_info[axis] - 1})
        if self._update_tile(dest):
            travel_info[axis] -= 1
            travel_info["steps"] += 1
        return True

    def _move_up_or_right(
        self, travel_info: Dict[str, int], axis: str
    ) -> bool:
        coord = Coordinate(travel_info["x"], travel_info["y"])
        dest = coord._replace(**{axis: travel_info[axis] + 1})
        if self._update_tile(dest):
            travel_info[axis] += 1
            travel_info["steps"] += 1
        return True

    def _travel(
        self,
        drone: Drone,
        *,
        start: Optional[Tile] = None,
        dest: Optional[Tile] = None,
    ) -> Tuple[int, int, Tile, Tile, Coordinate, List[Tile]]:
        path = self._generate_path(start=start, dest=dest)
        start = path[0]
        dest = path[-1]
        travel_info = {
            "x": start.coordinate.x,
            "y": start.coordinate.y,
            "steps": 0,
        }
        # duplicate path, drone will modify its internal copy
        drone.path = [cur.coordinate for cur in path]
        ticks = 1
        mineral_offset = self.minerals_.get(dest, 0)
        max_ticks = len(path) * 2 + mineral_offset

        # handle infinite loops
        while ticks < max_ticks and self._drone_act(travel_info, drone):
            ticks += 1
        return (
            ticks,
            travel_info["steps"],
            start,
            dest,
            Coordinate(
                travel_info["x"], travel_info["y"]
            ),  # drone's current locations
            path,
        )
