"""Test class for drone zerg units."""
import random
import unittest
from typing import List, NamedTuple, Type

from utils import Context
from utils.coordinate import Coordinate
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


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

    def setUp(self) -> None:
        self.phony_context_ = Context(0, 0, "", "", "", "")
        self.base_drone_ = Drone()
        self.base_scout_ = ScoutDrone()
        self.base_miner_ = MinerDrone()
        self.custom_drone_count_ = self.RANDOM_TEST_RUNS
        self.custom_drones_: List[Drone] = []
        self.custom_drone_stats_: List[TestDrone.CustomDroneStat] = []
        for _ in range(self.custom_drone_count_):
            health = random.randrange(10, 101, 10)
            capacity = random.randrange(5, 51, 5)
            moves = random.randrange(1, 11, 5)
            Blueprint = Drone.drone_blueprint(health, capacity, moves)
            self.custom_drone_stats_.append(
                self.CustomDroneStat(health, capacity, moves, Blueprint)
            )
            self.custom_drones_.append(Blueprint())

    def test_drone_init(self):
        self.assertIsInstance(self.base_drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.base_scout_, ScoutDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.base_miner_, MinerDrone)

    def test_drones_action(self):
        directions = ["NORTH", "SOUTH", "EAST", "WEST", "CENTER"]
        for _ in range(self.RANDOM_TEST_RUNS):
            result_drone = self.base_drone_.action(self.phony_context_)
            self.assertTrue(result_drone in directions, f"{result_drone}")
            result_scout = self.base_drone_.action(self.phony_context_)
            self.assertTrue(result_scout in directions, f"{result_scout}")
            result_miner = self.base_drone_.action(self.phony_context_)
            self.assertTrue(result_miner in directions, f"{result_miner}")

    def test_dynamic_drone(self):
        for drone_n in range(self.custom_drone_count_):
            self.assertIsInstance(self.custom_drone_stats_[drone_n].init, type)
            self.assertIsInstance(self.custom_drones_[drone_n], Drone)

    def test_drone_cost(self):
        for drone_n in range(self.custom_drone_count_):
            check_cost = self.custom_drones_[drone_n].get_init_cost()
            health = self.custom_drone_stats_[drone_n].health
            capacity = self.custom_drone_stats_[drone_n].capacity
            moves = self.custom_drone_stats_[drone_n].moves
            total_cost = (health / 10) + (capacity / 5) + (moves * 3)
            self.assertEqual(check_cost, total_cost)

    def test_drone_steps_taken(self):
        ticks = random.randint(0, 100)
        for _ in range(ticks):
            self.base_scout_.action(self.phony_context_)
        self.assertEqual(self.base_scout_.steps(), ticks)

    def test_drone_reach_dest(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            path = self.generate_path()
            dest = path[-1]
            curr = Coordinate(0, 0)
            self.base_scout_.path = path
            ticks = 0
            while True:
                context = Context(*curr, " ", " ", " ", " ")
                result = self.base_scout_.action(context)
                ticks += 1
                x = curr.x
                y = curr.y
                if result == "NORTH":
                    y += 1
                elif result == "SOUTH":
                    y -= 1
                elif result == "EAST":
                    x += 1
                elif result == "WEST":
                    x -= 1
                else:
                    break
                # handle infinite loops
                if ticks >= len(path) * 2:
                    break
                curr = Coordinate(x, y)
            self.assertEqual(ticks, len(path))
            self.assertEqual(curr, dest)

    def generate_path(self) -> List[Coordinate]:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        dest = Coordinate(x, y)
        path: List[Coordinate] = []
        x, y = 0, 0
        while x != dest.x or y != dest.y:
            if x < dest.x:
                x += 1
                path.append(Coordinate(x, y))
                continue
            elif x > dest.x:
                x -= 1
                path.append(Coordinate(x, y))
                continue
            elif y < dest.y:
                y += 1
                path.append(Coordinate(x, y))
                continue
            elif y > dest.y:
                y -= 1
                path.append(Coordinate(x, y))
                continue
        path.append(dest)
        return path
