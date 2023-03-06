"""(X, Y) coordinates for a grid system."""
from __future__ import annotations

from functools import singledispatchmethod
from typing import NamedTuple, Tuple


class Coordinate(NamedTuple):
    """(X, Y) coordinates for a grid system."""

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
            Tuple[int, int]: The distance difference, as (x, y) tuple.
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
            Tuple[int, int]: The distance difference, as (x, y) tuple.
        """
        return (x - self.x, y - self.y)

    @singledispatchmethod
    def direction(self, other_coord: Coordinate) -> str:
        """Get the direction of the other coordinate in relation to this one.

        Note that this only works if this coordinate and the other are on the
        same axis as each other. Otherwise an empty string will be returned.
        If the 2 coordinates are the same, 'center' will be returned.

        Args:
            other_coord (Coordinate): The other coordinate.

        Returns:
            str: The direction of the other coordinate.
        """
        return self.direction(*other_coord)

    @direction.register
    def _(self, x: int, y: int) -> str:
        """Get the direction of the other coordinate in relation to this one.

        This method allows for the other point to be given as 2 ints for x, y.
        Note that this only works if this coordinate and the other are on the
        same axis as each other. Otherwise an empty string will be returned.
        If the 2 coordinates are the same, 'center' will be returned.

        Args:
            x (int): The x value of the other coordinate.
            y (int): The y value of the other coordinate.

        Returns:
            str: The direction of the other coordinate.
        """
        x_offset, y_offset = self.difference(x, y)
        if x_offset and y_offset:
            return ""  # can't determine direction
        if x_offset > 0:
            return "east"
        elif x_offset < 0:
            return "west"
        elif y_offset > 0:
            return "north"
        elif y_offset < 0:
            return "south"
        else:  # x_offset == 0 and y_offset == 0
            return "center"
