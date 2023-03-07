"""A map made up of tiles"""

from typing import Dict, List, Optional

from .context import Context
from .coordinate import Coordinate
from .icon import Icon
from .tile import Tile

from queue import PriorityQueue as Queue


class Map:
    """A map object, used to describe the tile layout of an area"""

    def __init__(self, context: Context):
        self.origin = Coordinate(context.x, context.y)
        self.adjacency_list: Dict[Tile, Optional[List[Tile]]] = {}

        # dict{Tile: [Tile, Tile, Tile, Tile]}

    def dijkstra(self, start: Coordinate, end: Coordinate) -> None:
        node_weights = {
                        " ": 1,
                        "_": 2,
                        "~": 10,
                        "*": 9998,
                        "#": 9999
                        }
        # TODO: dynamically assign acid weight
        visited = []
        parents_map = {}
        final_path = []
        pqueue = Queue()
        pqueue.put((0, start))
        while pqueue.empty() is False:
            _, node = pqueue.get()
            visited.append(node)
            tile_neighbors = self.adjacency_list[Tile(node)]
            if tile_neighbors is None:
                continue
            for neighbor in tile_neighbors:
                if neighbor.coordinate in visited:
                    continue
                parents_map[neighbor] = node
                try:
                    pqueue.put((node_weights[neighbor.icon.value],
                                neighbor.coordinate))
                except AttributeError:
                    pqueue.put((1, neighbor.coordinate))

        tile = end
        while tile != start:
            coord = parents_map[Tile(tile)]
            final_path.append(coord)
            tile = coord
        return final_path[::-1]

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
            current_tile = Tile(current_coord, Icon(symbol))
            neighbors.append(current_tile)
            if current_tile not in self.adjacency_list:
                neighbors_nbrs = []
                for offset in coordinate_offsets:
                    x_offset2, y_offset2 = offset
                    neighbor_coord = Coordinate(current_coord.x + x_offset2,
                                                current_coord.y + y_offset2)
                    neighbor_tile = Tile(neighbor_coord)
                    neighbors_nbrs.append(neighbor_tile)
                    if self.adjacency_list.get(neighbor_tile) is None:
                        self.adjacency_list.update({neighbor_tile: None})
                self.adjacency_list.update({current_tile: neighbors_nbrs})

        self.adjacency_list.update({start_tile: neighbors})
