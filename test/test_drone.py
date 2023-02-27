"""Test class for drone zerg units."""
import unittest

from zerg.drones.drone import Drone
from zerg.drones.scout import ScoutDrone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    def setUp(self) -> None:
        health = 1
        capacity = 5
        moves = 1
        self.drone_ = Drone(health, capacity, moves)
        self.scout_ = ScoutDrone(health, capacity, moves)

    def test_drone_init(self):
        self.assertIsInstance(self.drone_, Drone)

    def test_scout_init(self):
        self.assertIsInstance(self.scout_, ScoutDrone)
