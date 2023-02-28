"""(X, Y) coordinates for a grid system."""
from __future__ import annotations

from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int

    def difference(self, other_coord: Coordinate):
        return (other_coord.x - self.x, other_coord.y - self.y)
