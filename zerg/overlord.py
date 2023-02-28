"""Overlord, who oversees zerg drones and assigns tasks to them"""
from utils import Coordinate

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
        # TODO: Implement terrain map dict with map id as key
        # TODO: Implement function to create default map objects

        for value in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone("Miner")
            self._create_drone("Scout")
        for drone in self.drones:
            # Set 'map deployed to' for all drones to 0
            self._deployed[id(self.drones[drone])] = 0

    def _create_drone(self, type: str) -> None:
        """Creates a new zerg drone of the specified drone type"""
        drone_types = {"Drone": Drone(),
                       "Miner": MinerDrone(),
                       "Scout": ScoutDrone()}
        new_drone = drone_types[type]
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id: int, summary: float) -> None:
        """Registers ID for map and summary of mineral density"""
        self.maps[map_id] = summary

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
        for map in self.maps.keys():
            zerg_per_map.update({map: 0})
        for drone in self._deployed.keys():
            current_map = self._deployed[drone]
            if not current_map:
                continue
            zerg_per_map[current_map] += 1
        return min(zerg_per_map, key=zerg_per_map.get)

    def _set_drone_path(self, drone_id: int):
        """Gives a drone a path based on their role and context"""
        # TODO: find path using Dijkstra's
        pass

    def action(self, context=None) -> str:
        """Performs some action, based on the context of the situation

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

        for drone in self.drones.values():
            if not self._deployed[id(drone)] or drone.path:
                continue
            self.set_drone_path()
        return action
