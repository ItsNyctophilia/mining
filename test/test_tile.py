"""Test class for map tiles."""
import random
import unittest
from typing import Optional, Tuple

from utils import Coordinate, Icon, Tile


class TestTile(unittest.TestCase):
    def setUp(self) -> None:
        self.default_coord_ = self._randomize_coordinate()
        self.tile_ = Tile(self.default_coord_, Icon.EMPTY)
        self.tile_acid_ = Tile(self.default_coord_, Icon.ACID)
        self.tile_wall_ = Tile(self.default_coord_, Icon.WALL)
        self.tile_undiscovered_ = Tile(self.default_coord_, None)

    def test_tile_init(self):
        self.assertIsInstance(self.tile_, Tile)

    def test_tile_immutable_coordinate(self):
        self.assertEqual(self.tile_.coordinate, self.default_coord_)
        with self.assertRaises(AttributeError):
            self.tile_.coordinate = self.default_coord_  # type: ignore

    def test_tile_icon_value(self):
        self.assertEqual(self.tile_wall_.icon, Icon.WALL)
        self.assertTrue(self.tile_wall_.discovered)
        self.assertIsNone(self.tile_undiscovered_.icon)
        self.assertFalse(self.tile_undiscovered_.discovered)

    def test_tile_occupation(self):
        self.assertFalse(self.tile_acid_.unoccupy())
        self.assertEqual(self.tile_acid_.icon, Icon.ACID)
        self.assertNotEqual(self.tile_acid_.icon, Icon.ZERG)

        self.assertTrue(self.tile_acid_.occupy())
        self.assertNotEqual(self.tile_acid_.icon, Icon.ACID)
        self.assertEqual(self.tile_acid_.icon, Icon.ZERG)
        self.assertFalse(self.tile_acid_.occupy())

        self.assertTrue(self.tile_acid_.unoccupy())
        self.assertNotEqual(self.tile_acid_.icon, Icon.ZERG)
        self.assertEqual(self.tile_acid_.icon, Icon.ACID)
        self.assertFalse(self.tile_acid_.unoccupy())

        with self.assertRaises(RuntimeError):
            self.tile_undiscovered_.occupy()
        with self.assertRaises(RuntimeError):
            self.tile_undiscovered_.unoccupy()

    def test_tile_comparison(self):
        diff_tile = Tile(self._randomize_coordinate())
        self.assertTrue(self.tile_ == self.tile_acid_)
        self.assertFalse(self.tile_ == diff_tile)
        self.assertFalse(self.tile_ != self.tile_acid_)
        self.assertTrue(self.tile_ != diff_tile)

    def _random_numbers(self) -> Tuple[int, int]:
        return random.randint(-10, 10), random.randint(-10, 10)

    def _randomize_coordinate(
        self, avoid: Optional[Coordinate] = None
    ) -> Coordinate:
        x, y = self._random_numbers()
        if not avoid:
            return Coordinate(x, y)
        while (coord := Coordinate(x, y)) == avoid:
            x, y = self._random_numbers()
        return coord
