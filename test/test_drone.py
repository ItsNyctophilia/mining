"""Test class for drone zerg units."""
import random
import unittest

from utils.context import Context
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    def setUp(self) -> None:
        self.drone_ = Drone()
        self.scout_ = ScoutDrone()
        self.miner_ = MinerDrone()

    def test_drone_init(self):
        self.assertIsInstance(self.drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.scout_, ScoutDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.miner_, MinerDrone)

    def test_drones_action(self):
        context = Context()
        directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        for _ in range(50):
            result_drone = self.drone_.action(context)
            self.assertTrue(result_drone in directions, f"{result_drone}")
            result_scout = self.drone_.action(context)
            self.assertTrue(result_scout in directions, f"{result_scout}")
            result_miner = self.drone_.action(context)
            self.assertTrue(result_miner in directions, f"{result_miner}")

    def test_dynamic_drone(self):
        for _ in range(50):
            health = random.randrange(10, 101, 10)
            capacity = random.randrange(5, 51, 5)
            moves = random.randrange(1, 11, 5)
            Blueprint = Drone.drone_blueprint(health, capacity, moves)
            self.assertIsInstance(Blueprint, type)
            drone = Blueprint()
            self.assertIsInstance(drone, Drone)
