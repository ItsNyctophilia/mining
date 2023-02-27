"""Test class for drone zerg units."""
import unittest

from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    def setUp(self) -> None:
        health = 40
        capacity = 5
        moves = 1
        self.drone_ = Drone(health, capacity, moves)
        self.scout_ = ScoutDrone(health, capacity, moves)
        self.miner_ = MinerDrone(health, capacity, moves)

    def test_drone_init(self):
        self.assertIsInstance(self.drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.scout_, ScoutDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.miner_, MinerDrone)

    def test_drones_action(self):
        context = None
        directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        for _ in range(50):
            result_drone = self.drone_.action(context)
            self.assertTrue(result_drone in directions, f"{result_drone}")
            result_scout = self.drone_.action(context)
            self.assertTrue(result_scout in directions, f"{result_scout}")
            result_miner = self.drone_.action(context)
            self.assertTrue(result_miner in directions, f"{result_miner}")
