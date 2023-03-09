"""Scout drone, whose primary purpose is revealing the map."""

from typing import TYPE_CHECKING

from .drone import Drone

if TYPE_CHECKING:
    from typing import Optional

    from mining.utils import Coordinate
    from mining.zerg_units import Overlord


class ScoutDrone(Drone):
    """Scout drone, whose primary purpose is revealing the map."""

    max_health = 40
    max_capacity = 5
    max_moves = 1

    def __init__(self, overlord: "Overlord") -> None:
        """Initialize a ScoutDrone.

        Args:
            overlord (Overlord): The Overlord owning this drone.
        """
        super().__init__(overlord)
        self._unexplored_land: Optional["Coordinate"] = None
