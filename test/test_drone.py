"""Test class for drone zerg units."""
import random
import unittest
from typing import List, NamedTuple, Type

from utils import Context
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

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
        self.custom_drone_count_ = 50
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
        for _ in range(50):
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
