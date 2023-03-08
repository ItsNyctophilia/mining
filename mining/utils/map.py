"""A map made up of tiles."""

from queue import PriorityQueue as Queue
from typing import Dict, List, Optional, Set, Tuple, Union, overload

from .context import Context
from .coordinate import Coordinate
from .icon import Icon
from .tile import Tile


class Map:
    """A map object, used to describe the tile layout of an area."""

    COORDINATE_OFFSETS = Coordinate(0, 0).cardinals()

    NON_TRAVERSABLE = 9999
    NODE_WEIGHTS = {
        Icon.EMPTY: 1,
        Icon.ZERG: 1,
        Icon.DEPLOY_ZONE: 1,
        Icon.ACID: 10,
        Icon.MINERAL: 20,
    }
    DEFAULT_TILE = Tile(Coordinate(0, 0), Icon.UNREACHABLE)

    def __init__(self, context: Context):
        """Initialize a Map with a context object

        Args:
            context (Context): The origin of the map.
        """
        self._stored_tiles_: Dict[Coordinate, Tile] = {}
        if context:
            self.origin = Coordinate(context.x, context.y)
            self.add_tile(self.origin, Tile(self.origin, Icon.DEPLOY_ZONE))
            self.update_context(context)

    def dijkstra(self, start: Coordinate, end: Coordinate) -> List[Coordinate]:
        """Apply Dijkstra's Algorithm to find path between points.

        Args:
            start (Coordinate): The start point for the search
            end (Coordinate): The end point for the search
        Returns:
            list(Coordinate): Path in the form of a Coordinate list
        """

        # TODO: dynamically assign acid weight
        visited: Set[Coordinate] = set()
        parents_map: Dict[Coordinate, Coordinate] = {}
        final_path: List[Coordinate] = []
        path_found = False
        pqueue: Queue[Tuple[int, Tile]] = Queue()
        pqueue.put((0, Tile(start)))
        counter = 1000
        while not pqueue.empty() and counter:
            _, node = pqueue.get()
            if node.icon == Icon.WALL:
                continue
            node = node.coordinate
            if node == end:
                path_found = True
                break
            node_neighbors = node.cardinals()

            tile_icons = [
                self.get(neighbor, self.DEFAULT_TILE).icon
                for neighbor in node_neighbors
            ]
            are_tiles_valid = any(i in tile_icons for i in self.NODE_WEIGHTS)
            if not are_tiles_valid:
                continue

            if end in node_neighbors:
                path_found = True
                parents_map[end] = node
                break
            visited.add(node)
            for neighbor in node_neighbors:
                neighbor = self.get(neighbor, None)
                if (
                    neighbor is None
                    or neighbor in visited
                    or neighbor.icon not in self.NODE_WEIGHTS
                ):
                    continue
                parents_map[neighbor.coordinate] = node
                pqueue.put((self.NODE_WEIGHTS[neighbor.icon], neighbor))
            counter -= 1
        if not path_found:
            return []

        curr = end
        final_path.append(curr)
        while curr != start:
            coord = parents_map[curr]
            final_path.append(coord)
            curr = coord
            if start in coord.cardinals():
                break
        final_path.append(start)
        print(final_path)
        return final_path[::-1]

    def update_context(self, context: Context) -> None:
        """Update the adjacency list for the Map with a context object.

        Arguments:
            context (Context): The context object to use to update
                the Map.
            origin (bool): Whether or not the passed context object
                is the origin of the map.
        """
        x = context.x
        y = context.y
        symbols = [context.north, context.south, context.east, context.west]
        zerg_position = Coordinate(x, y)

        for symbol, coordinate in zip(symbols, zerg_position.cardinals()):
            current_tile = Tile(coordinate, Icon(symbol))
            self._stored_tiles_[coordinate] = current_tile

    def add_tile(self, coord: Coordinate, tile: Tile) -> None:
        self._stored_tiles_[coord] = tile

    @overload
    def get(
        self, key: Union[Tile, Coordinate], default: None
    ) -> Optional[Tile]:
        pass

    @overload
    def get(self, key: Union[Tile, Coordinate], default: Tile) -> Tile:
        pass

    def get(self, key, default):
        """Get the tile with the specified coordinates from the map.

        A Tile or Coordinate object may be passed in as the key; if a Tile is
        given, only it's coordinate attribute will be used in look up.

        Args:
            key (Union[Tile, Coordinate]): The key to look up.
            default (Optional[Tile], optional): A value to return if the
                key is not found. Defaults to None.

        Returns:
            Optional[Tile]: The Tile within this map.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key: Union[Tile, Coordinate]) -> Tile:
        """Get the tile with the specified coordinates from the map.

        A Tile or Coordinate object may be passed in as the key; if a Tile is
        given, only it's coordinate attribute will be used in look up.

        Args:
            key (Union[Tile, Coordinate]): The key to look up.

        Raises:
            KeyError: If no Tile with the given coordinates exists in this map.

        Returns:
            Tile: The Tile within this map.
        """
        if isinstance(key, Tile):
            key = key.coordinate
        return self._stored_tiles_[key]

    def __iter__(self):
        """Iterate over this map.

        Yields:
            _type_: The iterator.
        """
        yield from self._stored_tiles_

    # def __repr__(self) -> str:
    #     """Return a representation of this object.

    #     The string returned by this method is not valid for a call to eval.

    #     Returns:
    #         str: The string representation of this object.
    #     """
    #     return f"Map({list(self.adjacency_list)})"
