"""Overlord, who oversees zerg drones and assigns tasks to them."""

import itertools
from queue import SimpleQueue
from typing import Dict, List, Optional, Set, Tuple, Type

from mining.utils import Context, Coordinate, Icon, Map, Tile

from .drones import Drone, MinerDrone, ScoutDrone
from .zerg import Zerg


class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them."""

    def __init__(
        self, total_ticks: int, refined_minerals: int, dashboard=None
    ) -> None:
        """Initialize the Overlord.

        Args:
            total_ticks (int): Total ticks allowed for mining.
            refined_minerals (int): Total given minerals.
            dashboard (_type_, optional): The GUI dashboard. Defaults to None.
        """
        self.dashboard = dashboard
        self._maps: Dict[int, float] = {}
        # a map id as key and summary as value
        self._drones: Dict[Type[Drone], Dict[int, Drone]] = {
            ScoutDrone: {},
            MinerDrone: {},
        }
        self.drones: Dict[int, Drone] = {}
        # a drone id as key and drone as value
        self._minerals: Set[Tuple[Coordinate, int]] = set()
        # a set of the coords of minerals and maps
        self._deployed: Dict[int, Optional[int]] = {}
        # a drone id as key and map id as value
        self._update_queue: SimpleQueue[
            Tuple[int, Drone, Context]
        ] = SimpleQueue()
        # a list of map updates from zerg drones
        self._tile_maps: Dict[int, Map] = {}
        # a map id as key and Map as value

        for _ in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone(MinerDrone)
            self._create_drone(ScoutDrone)

    def _create_drone(self, drone_type: Type[Drone]) -> None:
        """Create a new zerg drone of the specified drone type."""
        # TODO: create custom drones based on available resources
        new_drone = drone_type(self)
        drone_id = id(new_drone)
        self._drones[drone_type][drone_id] = new_drone
        self.drones[drone_id] = new_drone
        # Set 'map deployed to' for all drones to None
        self._deployed[drone_id] = None

    def mark_drone_dead(self, drone: Drone) -> None:
        """Mark a drone as dead.

        Args:
            drone (int): The drone to mark as dead.
        """
        drone_id = id(drone)
        del self._drones[type(drone)][drone_id]
        del self._deployed[drone_id]
        del self.drones[drone_id]

    def add_map(self, map_id: int, summary: float) -> None:
        """Register ID for map and summary of mineral density.

        Args:
            map_id (int): The id of the map.
            summary (float): The density of minerals in the map.
        """
        self._maps[map_id] = summary
        self._tile_maps[map_id] = Map()

    def add_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Add a mineral to the set of known minerals."""
        if map_id := self._deployed[drone_id]:
            self._minerals.add((coord, map_id))

    def del_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Remove a mineral from the set of known minerals.

        Args:
            coord (Coordinate): The coordinate of the mineral to delete.
            drone_id (int): The id of the drone who found the removed mineral.
        """
        # TODO: maybe pass in map id instead of drone id
        if map_id := self._deployed[drone_id]:
            self._minerals.remove((coord, map_id))

    def _select_map(self) -> int:
        """Select the map with the least number of zerg on it.

        Returns:
            int: The id of the chosen map
        """
        # TODO: Only count DroneScouts to avoid conflicts with miners
        zerg_per_map = {map_id: 0 for map_id in self._maps}
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
        if map_id := self._deployed[id(drone)]:
            self._update_queue.put((map_id, drone, context))

    def _spiral(
        self, ring: int, map: Map, start: Coordinate
    ) -> List[Coordinate]:
        """Implement the spiral search for a given radius around start.

        Args:
            ring (int): The radius around the start value in which
                to check for valid tiles
            map (Map): Map object to search on
            start (Coordinate): Coordinate to start search from
        Returns:
            list(Coordinate)
        """
        adjacent_coords: List[Coordinate] = []
        # TODO: Only take the outermost ring of coords to avoid repeating
        for x_offset, y_offset in itertools.product(
            range(-ring, 1 + ring), repeat=2
        ):
            current_coord = start.translate(x_offset, y_offset)
            if current_coord != start:
                adjacent_coords.append(current_coord)
        for coord in adjacent_coords:
            tile = map.get(coord, None)
            if tile is not None:
                continue
            path = None
            default_tile = Tile(Coordinate(0, 0), Icon.UNREACHABLE)
            neighbor_icons = [
                map.get(coord, default_tile).icon
                for coord in coord.cardinals()
            ]
            if not any(
                True
                for icon in neighbor_icons
                if icon
                in [Icon.MINERAL, Icon.EMPTY, Icon.DEPLOY_ZONE, Icon.ACID]
            ):
                continue
            print(neighbor_icons)
            print(f"call for {coord}")
            path = map.dijkstra(start, coord)
            if not len(path):
                # print(f"{coord} marked unreachable")
                # map.add_tile(coord, Tile(coord, Icon.UNREACHABLE))
                continue
            return path

        return []

    def _spiral_search(
        self, start: Coordinate, map_id: int
    ) -> Optional[List[Coordinate]]:
        """Attempt to give a ScoutDrone a new path.

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
        path = None
        current_map = self._tile_maps[map_id]
        for current_ring in range(1, 5):
            print(current_ring)
            path = self._spiral(current_ring, current_map, start)
            if path:
                break
        return path

    def _set_drone_path(self, drone: Drone, context: Context) -> None:
        """Give a drone a path based on their role and context."""
        drone_id = id(drone)
        if map_id := self._deployed[drone_id]:
            start = Coordinate(context.x, context.y)
            dest = self._spiral_search(start, map_id)
            if not dest:
                return
            print(f"Setting path for drone {drone_id} to {dest}")
            self._drones[type(drone)][drone_id].path = dest

    def action(self, context=None) -> str:
        """Perform some action, based on the context of the situation.

        Args:
            context (Context): Context surrounding the overlord;
                currently unused

        Returns:
            str: The action for the overlord to perform
        """
        # Deploy all scouts at start
        action = self._deploy_scouts()

        # Drone map updates
        self._update_map()

        return action

    def _deploy_scouts(self) -> str:
        action = "None"
        for drone in self._drones[ScoutDrone].values():
            if not self._deployed[id(drone)]:
                selected_map = self._select_map()
                action = f"DEPLOY {id(drone)} {selected_map}"
                self._deployed[id(drone)] = selected_map
                break
        return action

    def _update_map(self) -> None:
        # TODO: iterating over _update_queue twice. maybe combine loops?
        # seen_drones = [drone for _, drone, _ in self._update_queue]
        # for drone in self.drones.values():
        #     if drone not in seen_drones:
        #         self._deployed[id(drone)] = None
        while not self._update_queue.empty():
            map_id, drone, drone_context = self._update_queue.get()
            if not self._tile_maps.get(map_id):
                self._tile_maps[map_id] = Map(drone_context)
                # Map initialize already calls update_context()
                # self._tile_maps[map_id].update_context(drone_context, True)
                continue
            current_map = self._tile_maps[map_id]
            current_map.update_context(drone_context)
            if not len(drone.path):
                self._set_drone_path(drone, drone_context)
