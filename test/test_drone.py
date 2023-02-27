"""Test class for drone zerg units."""
import unittest

from zerg.drones.drone import Drone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    def setUp(self) -> None:
        health = 1
        capacity = 5
        moves = 1
        self.drone_ = Drone(health, capacity, moves)
        return

    def test_drone_init(self):
        self.assertIsInstance(self.drone_, Drone)
