"""A map made up of tiles."""

from queue import PriorityQueue as Queue
from typing import Dict, List, Optional, Tuple, Union, overload

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
        Icon.DEPLOY_ZONE: 2,
        Icon.ACID: 10,
        Icon.MINERAL: NON_TRAVERSABLE,
        Icon.WALL: NON_TRAVERSABLE,
        Icon.UNREACHABLE: NON_TRAVERSABLE,
        None: NON_TRAVERSABLE,  # catch-all case for undiscovered tiles
    }

    def __init__(self, context: Optional[Context] = None):
        """Initialize a Map.

        If a starting context is given, it will be treated as the origin of the
        map and the map will updates itself accordingly.

        Args:
            context (Optional[Context], optional): The origin of the map.
                Defaults to None.
        """
        # dict{Tile: [Tile, Tile, Tile, Tile]}
        self.adjacency_list: Dict[Tile, List[Tile]] = {}
        self._stored_tiles_: Dict[Coordinate, Tile] = {}
        if context:
            # TODO: Use of self.origin?
            self.origin = Coordinate(context.x, context.y)
            self.update_context(context, True)

    def dijkstra(self, start: Coordinate, end: Coordinate) -> List[Coordinate]:
        """Apply Dijkstra's Algorithm to find path between points

        Args:
            start (Coordinate): The start point for the search
            end (Coordinate): The end point for the search
        Returns:
            list(Coordinate): Path in the form of a Coordinate list
        """

        # TODO: dynamically assign acid weight
        visited: List[Coordinate] = set()  # TODO: should this be a set?
        parents_map: Dict[Coordinate, Coordinate] = {}
        final_path: List[Coordinate] = []
        path_found = False
        pqueue: Queue[Tuple[int, Coordinate]] = Queue()
        pqueue.put((0, start))
        while not pqueue.empty():
            _, node = pqueue.get()
            if node == end:
                path_found = True
                break
            visited.add(node)
            tile_neighbors = self.adjacency_list[Tile(node)]
            if not tile_neighbors:
                continue
            for neighbor in tile_neighbors:
                neigh_coord = neighbor.coordinate
                if neigh_coord in visited:
                    continue
                parents_map[neigh_coord] = node
                pqueue.put((self.NODE_WEIGHTS[neighbor.icon], neigh_coord))
        if not path_found:
            return []

        curr = end
        while curr != start:
            coord = parents_map[curr]
            final_path.append(coord)
            curr = coord
        return final_path[::-1]

    def update_context(self, context: Context, origin: bool = False) -> None:
        """Update the adjacency list for the Map with a context object.

        Arguments:
            context (Context): The context object to use to update
                the Map.
            origin (bool): Whether or not the passed context object
                is the origin of the map.
        """
        x = context.x
        y = context.y
        symbols = []
        symbols.append(context.north)
        symbols.append(context.south)
        symbols.append(context.east)
        symbols.append(context.west)

        zerg_position = Coordinate(x, y)

        if origin:
            start_tile = Tile(zerg_position, Icon.DEPLOY_ZONE)
            self.adjacency_list.update({start_tile: []})
        else:
            start_tile = Tile(zerg_position)

        neighbors = []

        # TODO: use zerg_position.cardinals() instead of static offsets
        # TODO: Fix the 'overlapping coordinates' bug
        for symbol, offset in zip(symbols, self.COORDINATE_OFFSETS):
            x_offset, y_offset = offset
            current_coord = Coordinate(x + x_offset, y + y_offset)
            current_tile = Tile(current_coord, Icon(symbol))
            neighbors.append(current_tile)
            if current_tile not in self.adjacency_list:
                neighbors_nbrs = []
                self._stored_tiles_[current_coord] = current_tile
                for offset in self.COORDINATE_OFFSETS:
                    x_offset2, y_offset2 = offset
                    neighbor_coord = Coordinate(
                        current_coord.x + x_offset2,
                        current_coord.y + y_offset2,
                    )
                    neighbor_tile = Tile(neighbor_coord)
                    neighbors_nbrs.append(neighbor_tile)
                    if self.adjacency_list.get(neighbor_tile) is None:
                        self._stored_tiles_[neighbor_coord] = neighbor_tile
                        self.adjacency_list.update({neighbor_tile: None})
                self.adjacency_list.update({current_tile: neighbors_nbrs})

        self.adjacency_list.update({start_tile: neighbors})

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
        yield from self.adjacency_list

    def __repr__(self) -> str:
        """Return a representation of this object.

        The string returned by this method is not valid for a call to eval.

        Returns:
            str: The string representation of this object.
        """
        return f"Map({list(self.adjacency_list)})"
