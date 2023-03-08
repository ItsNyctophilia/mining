"""Overlord, who oversees zerg drones and assigns tasks to them."""

import itertools
from typing import Dict, List, Optional, Set, Tuple

from mining.utils import Context, Coordinate, Map, Tile, Icon

from .drones import Drone, MinerDrone, ScoutDrone
from .zerg import Zerg


class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them."""

    def __init__(
        self, total_ticks: int, refined_minerals: int, dashboard=None
    ):
        # TODO: Add docstring
        self.dashboard = dashboard
        # a map id as key and summary as value
        self.maps: Dict[int, float] = {}
        # a drone id as key and drone as value
        self.drones: Dict[int, Drone] = {}
        # a set of the coords of minerals and maps
        self._minerals: Set[Tuple[Coordinate, int]] = set()
        # a drone id as key and map id as value
        self._deployed: Dict[int, Optional[int]] = {}
        # a list of map updates from zerg drones
        self._update_queue: List[Tuple[int, Drone, Context]] = []
        # a map id as key and Map as value
        self._tile_maps: Dict[int, Map] = {}

        for _ in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone("Miner")
            self._create_drone("Scout")
        for drone_id in self.drones:
            # Set 'map deployed to' for all drones to None
            self._deployed[drone_id] = None

    def _create_drone(self, type: str) -> None:
        """Create a new zerg drone of the specified drone type."""
        # TODO: create custom drones based on available resources
        drone_types = {
            "Drone": Drone,
            "Miner": MinerDrone,
            "Scout": ScoutDrone,
        }
        new_drone = drone_types[type](self)
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id: int, summary: float) -> None:
        """Register ID for map and summary of mineral density."""
        self.maps[map_id] = summary
        self._tile_maps.update({map_id: None})

    def add_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Add a mineral to the set of known minerals."""
        map_id = self._deployed[drone_id]
        self._minerals.add((coord, map_id))

    def del_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Remove a mineral from the set of known minerals."""
        map_id = self._deployed[drone_id]
        self._minerals.remove((coord, map_id))

    def _select_map(self) -> int:
        """Select the map with the least number of zerg on it.

        Returns:
            int: The id of the chosen map
        """
        # TODO: Only count DroneScouts to avoid conflicts with miners
        zerg_per_map = {map_id: 0 for map_id in self.maps}
        for drone_id in self._deployed:
            if (current_map_id := self._deployed[drone_id]) is not None:
                zerg_per_map[current_map_id] += 1
        return min(zerg_per_map, key=zerg_per_map.get)

    def enqueue_map_update(self, drone: Drone, context: Context) -> None:
        """Enqueue a map update of the drone's location and its context.

        This method will register the update information to a queue that will
        be processed at a later time.
        Args:
            drone (Drone): The drone giving updates.
            context (Context): The update information.
        """
        map_id = self._deployed[id(drone)]
        self._update_queue.append((map_id, drone, context))

    def _spiral(
            self,
            ring: int,
            map: Map,
            start: Coordinate
            ) -> List[Coordinate]:
        """Implement the spiral search for a given radius around start

        Args:
            ring (int): The radius around the start value in which
                to check for valid tiles
            map (Map): Map object to search on
            start (Coordinate): Coordinate to start search from
        Returns:
            list(Coordinate)
        """
        adjacent_coords = []
        # TODO: Use itertools.product(range(*), repeat=2)?
        # TODO: Only take the outermost ring of coords to avoid repeating
        for coord_x, coord_y in itertools.product(
            range(-ring, 1 + ring),
            range(-ring, 1 + ring),
        ):
            current_coord = Coordinate(start.x + coord_x, start.y + coord_y)
            if current_coord != start:
                adjacent_coords.append(current_coord)
        for coord in adjacent_coords:
            tile = map.get(coord, None)
            if tile is not None:
                continue
            path = None
            default_tile = Tile(Coordinate(0, 0), Icon.UNREACHABLE)
            neighbor_icons = [map.get(coord, default_tile).icon for coord in coord.cardinals()]
            if not any(True for icon in neighbor_icons if icon in [Icon.MINERAL, Icon.EMPTY,
                                                                   Icon.DEPLOY_ZONE, Icon.ACID]):
                continue
            print(neighbor_icons)
            print(f"call for {coord}")
            path = map.dijkstra(start, coord)
            if not len(path):
                #print(f"{coord} marked unreachable")
                #map.add_tile(coord, Tile(coord, Icon.UNREACHABLE))
                continue
            return path

        return None

    def _spiral_search(
            self,
            start: Coordinate,
            map_id: int
            ) -> List[Coordinate]:
        """Attempt to give a ScoutDrone a new path

        This method searches for the first unexplored tile in a ring
        around a given start tile, incrementally expanding the ring
        in the case that a valid tile is not found, stopping after
        all tiles within a 10-tile radius have been checked.

        Args:
            start (Coordinate): Start position of the search
            map_id (int): map_id of the map to search on
        Returns:
            list(Coordinate): The path for the ScoutDrone to explore
                to next
        """
        current_map = self._tile_maps[map_id]
        for current_ring in range(1, 5):
            print(current_ring)
            path = self._spiral(current_ring, current_map, start)
            if path is not None:
                break

        return path

    def _set_drone_path(self, drone_id: int, context: Context) -> None:
        """Give a drone a path based on their role and context."""
        map_id = self._deployed[drone_id]
        start = Coordinate(context.x, context.y)
        dest = self._spiral_search(start, map_id)
        if dest is None:
            return
        self.drones[drone_id].path = dest

    def action(self, context=None) -> str:
        """Perform some action, based on the context of the situation.

        Args:
            context (Context): Context surrounding the overlord;
                               currently unused

        Returns:
            str: The action for the overlord to perform
        """
        action = "None"
        # Deploy all scouts at start
        for drone in self.drones.values():
            if isinstance(drone, ScoutDrone):
                if self._deployed[id(drone)] is not None:
                    continue
                selected_map = self._select_map()
                action = f"DEPLOY {id(drone)} {selected_map}"
                self._deployed[id(drone)] = selected_map
                break

        # Drone map updates
        # TODO: iterating over _update_queue twice. maybe combine loops?
        # seen_drones = [drone for _, drone, _ in self._update_queue]
        # for drone in self.drones.values():
        #     if drone not in seen_drones:
        #         self._deployed[id(drone)] = None
        for map_id, drone, drone_context in self._update_queue:
            if not self._tile_maps.get(map_id):
                self._tile_maps[map_id] = Map(drone_context)
                # Map initialize already calls update_context()
                # self._tile_maps[map_id].update_context(drone_context, True)
                continue
            current_map = self._tile_maps[map_id]
            current_map.update_context(drone_context)
            if not len(drone.path):
                self._set_drone_path(id(drone), drone_context)
        self._update_queue.clear()

        return action
