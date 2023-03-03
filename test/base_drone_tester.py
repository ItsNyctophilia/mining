"""Base class for all zerg drone testing."""
import random
import unittest
from test.testing_utils import TestingUtils
from typing import Dict, List, NamedTuple, Optional, Tuple, Type

from utils import Context, Coordinate, Directions, Icon, Tile
from zerg.drones import Drone


class BaseDroneTester(unittest.TestCase):
    """Base class for all zerg drone testing."""

    CustomDroneStat = NamedTuple(
        "CustomDroneStat",
        [
            ("health", int),
            ("capacity", int),
            ("moves", int),
            ("init", Type[Drone]),
        ],
    )

    RANDOM_TEST_RUNS = 50
    DIRECTIONS = [d.name for d in Directions]
    phony_context_ = Context()

    offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))
    directions = Context._fields[2:]
    OFFSET_TO_DIRECTION = dict(zip(offsets, directions))

    def _randomize_stats(self) -> Tuple[int, int, int]:
        health = random.randrange(10, 101, 10)
        capacity = random.randrange(5, 51, 5)
        moves = random.randrange(1, 11, 5)
        return health, capacity, moves

    def _build_dynamic_units(
        self, drone_type: Drone
    ) -> Tuple[List[Drone], List[CustomDroneStat]]:
        custom_drones_: List[Drone] = []
        custom_drone_stats_: List[BaseDroneTester.CustomDroneStat] = []
        for _ in range(self.RANDOM_TEST_RUNS):
            health, capacity, moves = self._randomize_stats()
            Blueprint: Type[Drone] = drone_type.drone_blueprint(
                health, capacity, moves, drone_type  # type: ignore
            )
            custom_drones_.append(Blueprint())
            custom_drone_stats_.append(
                self.CustomDroneStat(health, capacity, moves, Blueprint)
            )
        return custom_drones_, custom_drone_stats_

    def _init_start_dest(
        self,
        start: Optional[Tile] = None,
        dest: Optional[Tile] = None,
    ) -> Tuple[Tile, Tile]:
        if not dest:
            coord = TestingUtils._randomize_coordinate(-100, 100)
            dest = Tile(coord, Icon.EMPTY)
        if not start:
            start = Tile(Coordinate(0, 0), Icon.EMPTY)
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
            path.insert(0, Tile(Coordinate(x, y), Icon.EMPTY))
        return path

    def _drone_act(self, travel_info: Dict[str, int], drone: Drone) -> bool:
        context = Context(travel_info["x"], travel_info["y"])
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

    def _move_down_or_left(
        self, travel_info: Dict[str, int], axis: str
    ) -> bool:
        travel_info[axis] -= 1
        travel_info["steps"] += 1
        return True

    def _move_up_or_right(
        self, travel_info: Dict[str, int], axis: str
    ) -> bool:
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
        travel_info = {
            "x": start.coordinate.x,
            "y": start.coordinate.y,
            "steps": 0,
        }
        # duplicate path, drone will modify its internal copy
        drone.path = [cur.coordinate for cur in path]
        ticks = 1
        max_ticks = len(path) * 2

        # handle infinite loops
        while ticks < max_ticks and self._drone_act(travel_info, drone):
            ticks += 1
        return (
            ticks,
            travel_info["steps"],
            start,
            path[-1],  # drone's intended destination
            Coordinate(
                travel_info["x"], travel_info["y"]
            ),  # drone's current locations
            path,
        )