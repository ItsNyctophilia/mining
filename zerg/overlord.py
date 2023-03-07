"""Overlord, who oversees zerg drones and assigns tasks to them"""
from utils import Coordinate, Context, Map, Tile

from zerg.zerg import Zerg
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them"""
    def __init__(self, total_ticks: int,
                 refined_minerals: int, dashboard=None):
        self.dashboard = dashboard
        self.maps = {}    # a map id as key and summary as value
        self.drones = {}  # a drone id as key and drone as value
        self._minerals = {}  # a set of the coords of minerals and maps
        self._deployed = {}  # a drone id as key and map id as value
        self._update_queue = []  # a list of map updates from zerg drones
        self._tile_maps = {}  # a map id as key and Map as value

        for value in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone("Miner")
            self._create_drone("Scout")
        for drone in self.drones:
            # Set 'map deployed to' for all drones to None
            self._deployed[id(self.drones[drone])] = None

    def _create_drone(self, type: str) -> None:
        """Creates a new zerg drone of the specified drone type"""
        drone_types = {"Drone": Drone(),
                       "Miner": MinerDrone(),
                       "Scout": ScoutDrone()}
        new_drone = drone_types[type]
        new_drone.overlord = self
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id: int, summary: float) -> None:
        """Registers ID for map and summary of mineral density"""
        self.maps[map_id] = summary
        self._tile_maps.update({map_id: None})

    def add_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Adds a mineral to the set of known minerals"""
        map_id = self._deployed[drone_id]
        self._minerals.add((coord, map_id))

    def del_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Removes a mineral from the set of known minerals"""
        map_id = self._deployed[drone_id]
        self._minerals.remove((coord, map_id))

    def _select_map(self) -> int:
        """Selects the map with the least number of zerg on it

        Returns:
            int: The id of the chosen map
            """
        # TODO: Only count DroneScouts to avoid conflicts with miners
        zerg_per_map = {}
        for map in self.maps:
            zerg_per_map.update({map: 0})
        for drone in self._deployed:
            current_map = self._deployed[drone]
            if current_map is None:
                continue
            zerg_per_map[current_map] += 1
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

    def _spiral_algorithm(self, start: Coordinate, map_id: int) -> Coordinate:
        current_map = self._tile_maps[map_id]
        current_ring = 1
        while current_ring < 10:
            adjacent_coords = []
            for coord_x in range(0 - current_ring, 1 + current_ring):
                for coord_y in range(0 - current_ring, 1 + current_ring):
                    current_coord = Coordinate(coord_x, coord_y)
                    if current_coord != start:
                        adjacent_coords.append(current_coord)
            for coord in adjacent_coords:
                try:
                    neighbors = current_map.adjacency_list[Tile(coord)]
                    if neighbors is None:
                        return coord

                except KeyError:
                    continue
            current_ring += 1

    def _set_drone_path(self, drone_id: int, context: Context) -> None:
        """Gives a drone a path based on their role and context"""
        map_id = self._deployed[drone_id]
        start = Coordinate(context.x, context.y)
        dest = self._spiral_algorithm(Coordinate(context.x, context.y),
                                      map_id)
        print("Start/Dest:", start, dest)
        self.drones[drone_id].path = self._tile_maps[map_id].dijkstra(start,
                                                                      dest)

    def action(self, context=None) -> str:
        """Performs some action, based on the context of the situation

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
        seen_drones = []
        for _, drone, _ in self._update_queue:
            seen_drones.append(drone)
        for drone in self.drones:
            if drone not in seen_drones:
                self._deployed[id(drone)] = None
        for map_id, drone, drone_context in self._update_queue:
            if self._tile_maps.get(map_id) is None:
                self._tile_maps[map_id] = Map(drone_context)
                self._tile_maps[map_id].update_context(drone_context, True)
                continue
            self._tile_maps[map_id].update_context(drone_context)
            if drone.path is None:
                self._set_drone_path(id(drone), drone_context)
        self._update_queue = []

        return action
