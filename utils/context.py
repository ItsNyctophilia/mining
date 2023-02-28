"""A context object, used to describe the surrounding's of a drone."""


class Context:
    """A context object, used to describe the surrounding's of a drone."""

    def __init__(
        self, x: int, y: int, north: str, south: str, east: str, west: str
    ) -> None:
        """Initialize a context object.

        Args:
            x (int): The X coordinate of the drone.
            y (int): The Y coordinate of the drone.
            north (str): The tile to the north of the drone.
            south (str): The tile to the south of the drone.
            east (str): The tile to the east of the drone.
            west (str): The tile to the west of the drone.
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
