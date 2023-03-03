"""A context object, used to describe the surrounding's of a drone."""
from .icon import Icon


class Context:
    """A context object, used to describe the surrounding's of a drone."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        *,
        north: str = Icon.EMPTY.value,
        south: str = Icon.EMPTY.value,
        east: str = Icon.EMPTY.value,
        west: str = Icon.EMPTY.value,
    ) -> None:
        """Initialize a context object.

        Args:
            x (int, optional): The X coordinate of the drone. Defaults to 0.
            y (int, optional): The Y coordinate of the drone. Defaults to 0.
            north (str, optional): The tile to the north of the drone.
                Defaults to Icon.EMPTY.value.
            south (str, optional): The tile to the south of the drone.
                Defaults to Icon.EMPTY.value.
            east (str, optional): The tile to the east of the drone.
                Defaults to Icon.EMPTY.value.
            west (str, optional): The tile to the west of the drone.
                Defaults to Icon.EMPTY.value.
        """
        self._x = x
        self._y = y
        self._north = north
        self._south = south
        self._east = east
        self._west = west

    @property
    def x(self) -> int:
        """The current x coordinate of the zerg in the current map.

        Will be a positive or negative integer.

        Returns:
            int: The x coordinate.
        """
        return self._x

    @property
    def y(self) -> int:
        """The current y coordinate of the zerg in the current map.

        Will be a positive or negative integer.

        Returns:
            int: The y coordinate.
        """
        return self._y

    @property
    def north(self) -> str:
        """The tile to the north of the drone's position, as a string

        Returns:
            int: The tile to the north.
        """
        return self._north

    @property
    def south(self) -> str:
        """The tile to the south of the drone's position, as a string

        Returns:
            int: The tile to the south.
        """
        return self._south

    @property
    def east(self) -> str:
        """The tile to the east of the drone's position, as a string

        Returns:
            int: The tile to the east.
        """
        return self._east

    @property
    def west(self) -> str:
        """The tile to the westof the drone's position, as a string

        Returns:
            int: The tile to the west.
        """
        return self._west
