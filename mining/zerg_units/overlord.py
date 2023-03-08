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
    
    def _distance_sort(self, start: Coordinate, end: Coordinate):
        start_x, start_y = start
        end_x, end_y = end
        return (start_x - end_x) + (start_y - end_y)
    
    def _assign_scout_target(
            self,
            map_id: int,
            start: Coordinate
            ) -> Coordinate:
        current_map = self._tile_maps[map_id]
        tiles = current_map.get_unexplored_tiles()
        tiles = sorted(tiles, key=lambda x:
                       self._distance_sort(start, x.coordinate), reverse=True)
        for tile in tiles:
            coord = tile.coordinate
            default_tile = Tile(Coordinate(0, 0), Icon.UNREACHABLE)
            neighbor_icons = [current_map.get(coord, default_tile).icon for coord in coord.cardinals()]
            if not any(True for icon in neighbor_icons if icon in [Icon.MINERAL, Icon.EMPTY,
                                                                   Icon.DEPLOY_ZONE, Icon.ACID]):
                continue
            print(f"Finding path from {start} to {coord}")
            path = current_map.dijkstra(start, tile.coordinate)
            if not path:
                #print("I gave up. c:")
                #path = current_map.dijkstra(start, current_map.origin)
                continue
            else:
                break

        return(path)

    def _set_drone_path(self, drone_id: int, context: Context) -> None:
        """Give a drone a path based on their role and context."""
        map_id = self._deployed[drone_id]
        start = Coordinate(context.x, context.y)
        #dest = self._spiral_search(start, map_id)
        dest = self._assign_scout_target(map_id, start)
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
                continue
            current_map = self._tile_maps[map_id]
            current_map.update_context(drone_context)
            if not len(drone.path):
                print(current_map.get_unexplored_tiles())
                self._set_drone_path(id(drone), drone_context)
        self._update_queue.clear()

        return action
