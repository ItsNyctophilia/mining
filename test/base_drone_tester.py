"""Base class for all zerg drone testing."""
import random
import unittest
from typing import Dict, List, Optional, Tuple

from utils import Context, Coordinate, Directions, Icon
from zerg.drones import Drone


class BaseDroneTester(unittest.TestCase):
    """Base class for all zerg drone testing."""

    RANDOM_TEST_RUNS = 50
    DIRECTIONS = [d.name for d in Directions]
    phony_context_ = Context()

    def _init_start_dest(
        self,
        start: Optional[Coordinate] = None,
        dest: Optional[Coordinate] = None,
    ) -> Tuple[Coordinate, Coordinate]:
        if not dest:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            dest = Coordinate(x, y)
        if not start:
            start = Coordinate(0, 0)
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
        start: Optional[Coordinate] = None,
        dest: Optional[Coordinate] = None,
    ) -> List[Coordinate]:
        start, dest = self._init_start_dest(start, dest)
        path: List[Coordinate] = [dest]
        x, y = dest
        while x != start.x or y != start.y:
            if update := self._update_axis(x, start.x):
                x += update
            else:
                y += self._update_axis(y, start.y)
            path.insert(0, Coordinate(x, y))
        return path

    def _drone_act(self, travel_info: Dict[str, int], drone: Drone) -> bool:
        space = Icon.EMPTY.value
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
        start: Optional[Coordinate] = None,
        dest: Optional[Coordinate] = None,
    ) -> Tuple[int, int, Coordinate, Coordinate, Coordinate, List[Coordinate]]:
        path = self._generate_path(start=start, dest=dest)
        start = path[0]
        travel_info = {"x": start.x, "y": start.y, "steps": 0}
        # duplicate path, drone will modify its internal copy
        drone.path = list(path)
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
