"""Test class for drone zerg units."""
import random
import unittest
from typing import List, Tuple, Type

from utils.context import Context
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    # index for health in custom_drons_stats
    HEALTH = 0
    # index for capacity in custom_drons_stats
    CAPACITY = 1
    # index for moves in custom_drons_stats
    MOVES = 2
    # index for initializer in custom_drons_stats
    INIT = 3

    def setUp(self) -> None:
        self.base_drone_ = Drone()
        self.base_scout_ = ScoutDrone()
        self.base_miner_ = MinerDrone()
        self.custom_drone_count_ = 50
        self.custom_drones_: List[Drone] = []
        self.custom_drone_stats_: List[Tuple[int, int, int, Type[Drone]]] = []
        for _ in range(self.custom_drone_count_):
            health = random.randrange(10, 101, 10)
            capacity = random.randrange(5, 51, 5)
            moves = random.randrange(1, 11, 5)
            Blueprint = Drone.drone_blueprint(health, capacity, moves)
            self.custom_drone_stats_.append(
                (health, capacity, moves, Blueprint)
            )
            self.custom_drones_.append(Blueprint())

    def test_drone_init(self):
        self.assertIsInstance(self.base_drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.base_scout_, ScoutDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.base_miner_, MinerDrone)

    def test_drones_action(self):
        context = Context()
        directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        for _ in range(50):
            result_drone = self.base_drone_.action(context)
            self.assertTrue(result_drone in directions, f"{result_drone}")
            result_scout = self.base_drone_.action(context)
            self.assertTrue(result_scout in directions, f"{result_scout}")
            result_miner = self.base_drone_.action(context)
            self.assertTrue(result_miner in directions, f"{result_miner}")

    def test_dynamic_drone(self):
        for drone_n in range(self.custom_drone_count_):
            self.assertIsInstance(
                self.custom_drone_stats_[drone_n][self.INIT], type
            )
            self.assertIsInstance(self.custom_drones_[drone_n], Drone)
