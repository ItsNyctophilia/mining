"""Test class for map tiles."""
import unittest

from utils import Coordinate, Icon


class TestTile(unittest.TestCase):
    def test_tile_init(self):
        coord = Coordinate(5, 9)
        icon = Icon["EMPTY"]
        discovered = False
        tile = Tile(coord, icon, discovered)
        self.assertIsInstance(tile, Tile)
