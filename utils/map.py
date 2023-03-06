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
                if (node.x == end.x
                    or node.x + 1 == end.x
                    or node.x - 1 == end.x) and (node.y == end.y
                                                 or node.y + 1 == end.y
                                                 or node.y - 1 == end.y):
                    # TODO: is_adjacent() method in coordinate?
                    parents_map[Tile(end)] = node
                    break

            for neighbor in tile_neighbors:
                if neighbor in visited:
                    continue
                parents_map[neighbor] = node
                pqueue.put((node_weights[neighbor.icon.value],
                            neighbor.coordinate))

        tile = end
        while tile != start:
            coord = parents_map[Tile(tile)]
            final_path.append(coord)
            tile = coord
        print(final_path)
        return final_path

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
                self.adjacency_list.update({current_tile: None})

        self.adjacency_list.update({start_tile: neighbors})
