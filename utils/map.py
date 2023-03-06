"""A map made up of tiles."""

import heapq as heap
from typing import Dict, List, Optional, Set, Tuple, Union

from .context import Context
from .coordinate import Coordinate
from .icon import Icon
from .tile import Tile


class Map:
    """A map object, used to describe the tile layout of an area."""

    def __init__(self, context: Optional[Context] = None):
        """Initialize a Map.

        If a starting context is given, it will be treated as the origin of the
        map and the map will updates itself accordingly.

        Args:
            context (Optional[Context], optional): The origin of the map.
                Defaults to None.
        """
        self.adjacency_list: Dict[Tile, List[Tile]] = {}
        self._stored_tiles_: Dict[Coordinate, Tile] = {}
        if context:
            self.origin = Coordinate(context.x, context.y)
            self.update_context(context, True)

        # dict{Tile: [Tile, Tile, Tile, Tile]}

    def dijkstra(
        self, start: Coordinate, end: Coordinate
    ) -> Dict[Coordinate, Coordinate]:
        node_weights = {
            Icon.EMPTY.value: 1,
            Icon.ACID.value: 10,
            Icon.MINERAL.value: 9999,
            Icon.WALL.value: 9999,
        }
        # TODO: dynamically assign acid weight
        visited: Set[Coordinate] = set()
        parents_map: Dict[Coordinate, Coordinate] = {}
        pq: List[Tuple[int, Coordinate]] = []
        heap.heappush(pq, (0, start))

        while pq:
            _, node = heap.heappop(pq)
            visited.add(node)

            for neighbor in self.adjacency_list[Tile(node)]:
                if neighbor in visited:
                    continue
                parents_map[neighbor.coordinate] = node
                # TODO: handle when neighbor has no icon
                heap.heappush(
                    pq,
                    (node_weights[neighbor.icon.value], neighbor.coordinate),
                )
        return parents_map

    def update_context(self, context: Context, origin: bool = False):
        """Update the adjacency list for the Map with a context object.

        Arguments:
            context (Context): The context object to use to update
                the Map.
            origin (bool): Whether or not the passed context object
                is the origin of the map.
        """
        x, y, *symbols = context
        zerg_position = Coordinate(x, y)

        if origin:
            start_tile = Tile(zerg_position, Icon.DEPLOY_ZONE)
            self.adjacency_list.update({start_tile: []})
        else:
            start_tile = Tile(zerg_position)

        coordinate_offsets = ((0, 1), (0, -1), (1, 0), (-1, 0))
        neighbors = []

        for symbol, offset in zip(symbols, coordinate_offsets):
            x_offset, y_offset = offset
            current_coord = Coordinate(x + x_offset, y + y_offset)
            current_tile = Tile(current_coord, Icon(symbol))
            neighbors.append(current_tile)
            if current_tile not in self.adjacency_list:
                # TODO: update this new tile neighbor to reference start tile
                self.adjacency_list.update({current_tile: []})
                self._stored_tiles_[current_coord] = current_tile

        self.adjacency_list.update({start_tile: neighbors})

    def get(
        self, key: Union[Tile, Coordinate], default: Optional[Tile] = None
    ) -> Optional[Tile]:
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
        if not (tile := self._stored_tiles_.get(key, None)):
            raise KeyError(repr(key))
        return tile

    def __iter__(self):
        yield from self.adjacency_list

    def __repr__(self) -> str:
        """Return a representation of this object.

        The string returned by this method is not valid for a call to eval.

        Returns:
            str: The string representation of this object.
        """
        return f"Map({list(self.adjacency_list)})"
