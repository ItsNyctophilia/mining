"""Test class for drone zerg units."""
import unittest

from zerg.drones.drone import Drone


class TestDrone(unittest.TestCase):
    """Test class for drone zerg units."""

    def test_drone_init(self):
        health = 1
        capacity = 5
        moves = 1
        drone = Drone(health, capacity, moves)
        self.assertIsInstance(drone, Drone)
