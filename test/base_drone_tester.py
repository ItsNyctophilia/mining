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
    stored_tiles_: Dict[Coordinate, Tile] = {}
    minerals_: Dict[Tile, int] = {}

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

    def _construct_context(self, drone_loc: Coordinate, dest: Tile):
        direction = drone_loc.direction(dest.coordinate)
        new_mapping = {direction: dest.icon.value if dest.icon else " "}
        return Context(*drone_loc)._replace(**new_mapping)  # type: ignore

    def _safely_construct_context(
        self,
        path: List[Tile],
        cur_step: int,
    ) -> Tuple[Context, int]:
        drone_loc = path[cur_step].coordinate
        if cur_step + 1 >= len(path):
            dest = Tile(Coordinate(drone_loc.x, drone_loc.y + 1))
        else:
            dest = path[cur_step + 1]
            cur_step += 1
        return (
            self._construct_context(drone_loc, dest),
            cur_step,
        )

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

    def _drone_act(
        self, travel_info: Dict[str, int], drone: Drone, context: Context
    ) -> bool:
        """Allow the drone to act.

        Return True if the drone requests to continue moving, else False.

        Args:
            travel_info (Dict[str, int]): Information on the drone's travel.
            drone (Drone): The drone traveling.
            context (Context): The context surrounding the drone.

        Returns:
            bool: True if the drones wants to move, else False.
        """
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

    def _register_tile(self, tile: Tile) -> None:
        self.stored_tiles_[tile.coordinate] = tile
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
        if tile := self.stored_tiles_.get(coord, None):
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
        context, step_idx = self._safely_construct_context(path, 0)

        # handle infinite loops
        while ticks < max_ticks and self._drone_act(
            travel_info, drone, context
        ):
            ticks += 1
            context, step_idx = self._safely_construct_context(
                path, travel_info["steps"]
            )
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
