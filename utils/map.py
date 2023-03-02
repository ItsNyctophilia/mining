"""A map made up of tiles"""

from typing import Dict, List, Optional

from .context import Context
from .coordinate import Coordinate
from .icon import Icon
from .tile import Tile


class Map:
    """A map object, used to describe the tile layout of an area"""

    def __init__(self, context: Context):
        self.origin = Coordinate(context.x, context.y)
        self.adjacency_list: Dict[Tile, Optional[List[Tile]]] = {}

        # dict{Tile: [Tile, Tile, Tile, Tile]}

    def update_context(self, context: Context, origin: bool = False):
        """Updates the adjacency list for the Map with a context object

        Arguments:
            context (Context): The context object to use to update
                the Map.
            origin (bool): Whether or not the passed context object
                is the origin of the map."""
        x = context.x
        y = context.y
        zerg_position = Coordinate(x, y)

        if origin:
            start_tile = Tile(zerg_position, Icon.DEPLOY_ZONE)
            self.adjacency_list.update({start_tile: None})
        else:
            start_tile = Tile(zerg_position)

        symbols = (context.north, context.south, context.east, context.west)
        coordinate_offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))
        neighbors = []

        for symbol, offset in zip(symbols, coordinate_offsets):
            x_offset, y_offset = offset
            current_coord = Coordinate(x + x_offset, y + y_offset)
            current_tile = Tile(current_coord, Icon[symbol])
            neighbors.append(current_tile)
            if current_tile not in self.adjacency_list:
                self.adjacency_list.update({current_tile: None})

        self.adjacency_list.update({start_tile: neighbors})
