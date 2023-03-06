"""Overlord, who oversees zerg drones and assigns tasks to them."""
from typing import Dict, List, Set, Tuple

from utils import Context, Coordinate, Map
from zerg.drones import Drone, MinerDrone, ScoutDrone

from .zerg import Zerg


class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them."""

    def __init__(
        self, total_ticks: int, refined_minerals: int, dashboard=None
    ):
        self.dashboard = dashboard
        # a map id as key and summary as value
        self.maps: Dict[int, float] = {}
        # a drone id as key and drone as value
        self.drones: Dict[int, Drone] = {}
        # a set of the coords of minerals and maps
        self._minerals: Set[Tuple[Coordinate, int]] = set()
        # a drone id as key and map id as value
        self._deployed: Dict[int, int] = {}
        self._update_queue: List[Tuple[int, Context]] = []  # a
        # a map id as key and Map as value
        self._tile_maps: Dict[int, Map] = {}

        for _ in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone("Miner")
            self._create_drone("Scout")
        for drone in self.drones:
            # Set 'map deployed to' for all drones to 0
            self._deployed[id(self.drones[drone])] = 0

    def _create_drone(self, type: str) -> None:
        """Create a new zerg drone of the specified drone type."""
        # TODO: create custom drones based on available resources
        drone_types = {
            "Drone": Drone(self),
            "Miner": MinerDrone(self),
            "Scout": ScoutDrone(self),
        }
        new_drone = drone_types[type]
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id: int, summary: float) -> None:
        """Register ID for map and summary of mineral density."""
        self.maps[map_id] = summary
        # TODO: allow maps to be initialized with no context
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
            if current_map_id := self._deployed[drone_id]:
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
        self._update_queue.append((map_id, context))

    def _set_drone_path(self, drone_id: int):
        """Give a drone a path based on their role and context."""
        # TODO: find path using Dijkstra's
        pass

    def action(self, context=None) -> str:
        """Perform some action, based on the context of the situation.

        Args:
            context (Context): Context surrounding the overlord;
                               currently unused

        Returns:
            str: The action for the overlord to perform
        """
        action = None
        # Deploy all scouts at start
        for drone in self.drones.values():
            if isinstance(drone, ScoutDrone):
                if not self._deployed[id(drone)]:
                    continue
                action = f"DEPLOY {id(drone)} {self._select_map()}"
                break

        # Drone map updates
        for map_id, drone_context in self._update_queue:
            if not self._tile_maps[map_id]:
                self._tile_maps[map_id] = Map(drone_context)
                self._tile_maps[map_id].update_context(drone_context, True)

            self._tile_maps[map_id].update_context(drone_context)

        for drone in self.drones.values():
            if not self._deployed[id(drone)] or drone.path:
                continue
            self.set_drone_path()
        return action
