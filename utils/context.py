"""A context object, used to describe the surrounding's of a drone."""


class Context:
    """A context object, used to describe the surrounding's of a drone."""

    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        self._north = " "
        self._south = " "
        self._east = " "
        self._west = " "

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
