"""Test class for drone zerg units."""
import random
import unittest
from typing import Dict, List, NamedTuple, Optional, Tuple, Type

from utils import Context, Coordinate, Directions, Icon
from zerg.drones import Drone, MinerDrone, ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    RANDOM_TEST_RUNS = 50

    CustomDroneStat = NamedTuple(
        "CustomDroneStat",
        [
            ("health", int),
            ("capacity", int),
            ("moves", int),
            ("init", Type[Drone]),
        ],
    )

    DRONE_TYPES = [Drone, MinerDrone, ScoutDrone]
    DIRECTIONS = [d.name for d in Directions]

    def setUp(self) -> None:
        self.phony_context_ = Context()
        self.base_drone_ = Drone()
        self.base_scout_ = ScoutDrone()
        self.base_miner_ = MinerDrone()
        self.custom_drones_: List[Drone] = []
        self.custom_drone_stats_: List[TestDrone.CustomDroneStat] = []
        for _ in range(self.RANDOM_TEST_RUNS):
            health = random.randrange(10, 101, 10)
            capacity = random.randrange(5, 51, 5)
            moves = random.randrange(1, 11, 5)
            Blueprint: Type[Drone] = Drone.drone_blueprint(
                health, capacity, moves, random.choice(self.DRONE_TYPES)
            )
            self.custom_drones_.append(Blueprint())
            self.custom_drone_stats_.append(
                self.CustomDroneStat(health, capacity, moves, Blueprint)
            )

    def test_drone_init(self):
        self.assertIsInstance(self.base_drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.base_scout_, ScoutDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.base_miner_, MinerDrone)

    def test_drones_action(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            result_drone = self.base_drone_.action(self.phony_context_)
            self.assertTrue(result_drone in self.DIRECTIONS, f"{result_drone}")
            result_scout = self.base_scout_.action(self.phony_context_)
            self.assertTrue(result_scout in self.DIRECTIONS, f"{result_scout}")
            result_miner = self.base_miner_.action(self.phony_context_)
            self.assertTrue(result_miner in self.DIRECTIONS, f"{result_miner}")

    def test_dynamic_drone(self):
        for drone_n in range(len(self.custom_drones_)):
            self.assertIsInstance(self.custom_drone_stats_[drone_n].init, type)
            self.assertIsInstance(self.custom_drones_[drone_n], Drone)

    def test_drone_cost(self):
        for drone_n in range(len(self.custom_drones_)):
            health, capacity, moves, _ = self.custom_drone_stats_[drone_n]
            check_cost = self.custom_drones_[drone_n].get_init_cost()
            total_cost = (health / 10) + (capacity / 5) + (moves * 3)
            self.assertEqual(check_cost, total_cost)

    def test_drone_steps_taken(self):
        steps = 0
        for _ in range(self.RANDOM_TEST_RUNS):
            _, curr_steps, _, _, _, _ = self.travel(self.base_scout_)
            steps += curr_steps
        self.assertEqual(self.base_scout_.steps(), steps)

    def test_drone_reach_dest(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            ticks, _, _, dest, curr, path = self.travel(self.base_scout_)
            path_len = len(path)
            msg = (
                f"It took {'more' if ticks > path_len else 'less'} time "
                "to get to the goal than expected"
            )
            self.assertEqual(curr, dest)
            self.assertEqual(ticks, path_len, msg)

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

    def generate_path(
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

    def travel(
        self,
        drone: Drone,
        start: Optional[Coordinate] = None,
        dest: Optional[Coordinate] = None,
    ) -> Tuple[int, int, Coordinate, Coordinate, Coordinate, List[Coordinate]]:
        path = self.generate_path(start=start, dest=dest)
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
