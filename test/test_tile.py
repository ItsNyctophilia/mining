"""Test class for map tiles."""
import unittest

from utils import Coordinate, Icon, Tile


class TestTile(unittest.TestCase):
    def setUp(self) -> None:
        coord = Coordinate(5, 9)
        icon = Icon["EMPTY"]
        discovered = True
        self.tile_ = Tile(coord, icon, discovered)

    def test_tile_init(self):
        self.assertIsInstance(self.tile_, Tile)
