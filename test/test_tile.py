"""Test class for map tiles."""
import unittest

from utils import Coordinate, Icon, Tile


class TestTile(unittest.TestCase):
    def setUp(self) -> None:
        self.default_coord_ = Coordinate(5, 9)
        self.tile_ = Tile(self.default_coord_, Icon.EMPTY)

    def test_tile_init(self):
        self.assertIsInstance(self.tile_, Tile)

    def test_tile_immutable_coordinate(self):
        self.assertEqual(self.tile_.coordinate, self.default_coord_)
        with self.assertRaises(AttributeError):
            self.tile_.coordinate = self.default_coord_  # type: ignore

    def test_tile_discoverability(self):
        coord = Coordinate(5, 9)
        icon = Icon["WALL"]
        discovered = True
        with self.assertRaises(ValueError):
            Tile(coord, icon, not discovered)
        with self.assertRaises(ValueError):
            Tile(coord, None, discovered)
