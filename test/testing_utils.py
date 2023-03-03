"""Various methods that multiple test classes may use."""


import random
from typing import Optional, Tuple

from utils import Coordinate


class TestingUtils:
    @staticmethod
    def _random_numbers(min: int, max) -> Tuple[int, int]:
        return random.randint(min, max), random.randint(min, max)

    @staticmethod
    def _randomize_coordinate(
        min: int = -10,
        max=10,
        avoid: Optional[Coordinate] = None,
    ) -> Coordinate:
        x, y = TestingUtils._random_numbers(min, max)
        if not avoid:
            return Coordinate(x, y)
        while (coord := Coordinate(x, y)) == avoid:
            x, y = TestingUtils._random_numbers(min, max)
        return coord
