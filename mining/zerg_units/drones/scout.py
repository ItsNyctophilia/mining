"""Scout drone, whose primary purpose is revealing the map."""
from typing import List, Optional

from mining.utils import Coordinate

from .drone import Drone


class ScoutDrone(Drone):
    """Scout drone, whose primary purpose is revealing the map."""

    max_health = 40
    max_capacity = 5
    max_moves = 1

    def __init__(self, overlord) -> None:
        """Initialize a ScoutDrone."""
        super().__init__(overlord)
        self._unexplored_land: Optional[Coordinate] = None
