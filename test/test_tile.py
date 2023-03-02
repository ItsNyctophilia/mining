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

    def test_tile_icon_value(self):
        discovered_tile = Tile(self.default_coord_, Icon.WALL)
        undiscovered_tile = Tile(self.default_coord_, None)
        self.assertEqual(discovered_tile.icon, Icon.WALL)
        self.assertTrue(discovered_tile.discovered)
        self.assertIsNone(undiscovered_tile.icon)
        self.assertFalse(undiscovered_tile.discovered)
