"""(X, Y) coordinates for a grid system."""
from __future__ import annotations

from functools import singledispatchmethod
from typing import NamedTuple, Tuple


class Coordinate(NamedTuple):
    x: int
    y: int

    @singledispatchmethod
    def difference(self, other_coord: Coordinate) -> Tuple[int, int]:
        """Get the difference in distance between 2 coordinates.

        In relation to this coordinate, a positive/negative return value will
        indicate direction; a positive  x means the other coordinate is to the
        right of this one, while a positive y means the other coordinate is
        above this one, and reversed for negative values.

        Args:
            other_coord (Coordinate): The other coordinate.

        Returns:
            Tuple[int, int]: The distance differnce, as (x, y) tuple.
        """
        return (other_coord.x - self.x, other_coord.y - self.y)

    @difference.register
    def _(self, x: int, y: int) -> Tuple[int, int]:
        """Get the difference in distance between 2 coordinates.

        This method allows for the other point to be given as 2 ints for x, y.
        In relation to this coordinate, a positive/negative return value will
        indicate direction; a positive  x means the other coordinate is to the
        right of this one, while a positive y means the other coordinate is
        above this one, and reversed for negative values.

        Args:
            x (int): The x value of the other coordinate.
            y (int): The y value of the other coordinate.

        Returns:
            Tuple[int, int]: The distance differnce, as (x, y) tuple.
        """
        return (x - self.x, y - self.y)
