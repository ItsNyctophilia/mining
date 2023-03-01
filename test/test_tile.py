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

    def test_tile_immutable_coordinate(self):
        coord = Coordinate(5, 9)
        self.assertEqual(self.tile_.coordinate, coord)
        with self.assertRaises(AttributeError):
            self.tile_.coordinate = coord  # type: ignore

    def test_tile_discoverability(self):
        coord = Coordinate(5, 9)
        icon = Icon["WALL"]
        discovered = True
        with self.assertRaises(ValueError):
            Tile(coord, icon, not discovered)
        with self.assertRaises(ValueError):
            Tile(coord, None, discovered)
