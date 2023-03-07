"""Test class for coordinates"""
import unittest

from mining.utils import Coordinate


class TestCoordinate(unittest.TestCase):
    def test_compare_points(self):
        x = 3
        y = 7
        c_1 = Coordinate(1, 5)
        c_2 = Coordinate(x, y)
        x_check = x - c_1.x
        y_check = y - c_1.y

        x_diff, y_diff = c_1.difference(c_2)
        self.assertEqual(x_diff, x_check)
        self.assertEqual(y_diff, y_check)

        x_diff, y_diff = c_1.difference(x, y)
        self.assertEqual(x_diff, x_check)
        self.assertEqual(y_diff, y_check)
