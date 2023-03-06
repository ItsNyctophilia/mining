"""(X, Y) coordinates for a grid system."""
from __future__ import annotations

from functools import singledispatchmethod
from typing import NamedTuple, Tuple, Union

from .directions import Directions


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

    def cardinals(
        self
    ) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
        """Return translated coordinate objects in the 4 cardinal directions.

        The order returned is North, South, East, West.

        Returns:
            Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
                The translated coordinates.
        """
        return (
            self.translate(Directions.NORTH),
            self.translate(Directions.SOUTH),
            self.translate(Directions.EAST),
            self.translate(Directions.WEST)
            )

    def translate(self, direction: Union[str, Directions]) -> Coordinate:
        """Translate this coordinate in the given direction.

        Translation moves the coordinate by 1 space in the given direction.
        This method will always return a new object. If Directions.CENTER is
        given, this coordinate is copied and returned.

        Args:
            direction (Directions): The direction to translate.

        Returns:
            Coordinate: The translated coordinate object.
        """
        if isinstance(direction, str):
            try:
                direction = Directions[direction.upper()]
            except KeyError:
                raise ValueError(f"Unknown  direction: {direction}") from None
        if direction == Directions.NORTH:
            return self._replace(y=self.y+1)
        elif direction == Directions.SOUTH:
            return self._replace(y=self.y-1)
        elif direction == Directions.EAST:
            return self._replace(x=self.x+1)
        elif direction == Directions.WEST:
            return self._replace(x=self.x-1)
        else:
            return Coordinate(*self)
