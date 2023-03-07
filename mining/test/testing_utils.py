"""Various methods that multiple test classes may use."""
import random
from typing import Optional, Tuple

from mining.utils import Coordinate


class TestingUtils:
    """Various methods that multiple test classes may use."""

    @staticmethod
    def random_number_pair(min: int, max) -> Tuple[int, int]:
        """Return a tuple of random numbers, bound to min/man inclusive.

        Args:
            min (int): Minimum number.
            max (_type_): Maximum number.

        Returns:
            Tuple[int, int]: The returned random numbers.
        """
        return random.randint(min, max), random.randint(min, max)

    @staticmethod
    def randomize_coordinate(
        min: int = -10,
        max=10,
        avoid: Optional[Coordinate] = None,
    ) -> Coordinate:
        """Create a randomized coordinate with given min/max.

        The avoid parameter can be used to set a coordinate to never return.
        If None is given (the default) any coordinate within the given range is
        valid.

        Args:
            min (int, optional): Minimum number. Defaults to -10.
            max (int, optional): Maximum number. Defaults to 10.
            avoid (Optional[Coordinate], optional): Coordinate to avoid.
                Defaults to None.

        Returns:
            Coordinate: The random coordinate.
        """
        x, y = TestingUtils.random_number_pair(min, max)
        if not avoid:
            return Coordinate(x, y)
        while (coord := Coordinate(x, y)) == avoid:
            x, y = TestingUtils.random_number_pair(min, max)
        return coord
