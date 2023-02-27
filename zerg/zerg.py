"""Abstract base class for all zerg units"""


from abc import ABC


class Zerg(ABC):
    """Abstract base class for all zerg units"""

    def __init__(self, health: int) -> None:
        self._health = health
