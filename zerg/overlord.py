from utils import Coordinate

from zerg.zerg import Zerg
from zerg.drones.drone import Drone
from zerg.drones.miner import MinerDrone
from zerg.drones.scout import ScoutDrone


class Overlord(Zerg):
    # There are components missing from this class that are
    # required to be added in order to meet the project requirements.
    #
    # There are no restrictions on what you as the developer might want
    # to add to this class definition in addition to the minimal requirements

    def __init__(self, total_ticks: int,
                 refined_minerals: int, dashboard=None):
        self.dashboard = dashboard
        self.maps = {}    # a map id as key and summary as value
        self.drones = {}  # a drone id as key and drone as value
        self._minerals = []  # a list of the coordinates of minerals
        self._deployed = {}  # a drone id as key and map id as value
        for value in range(3):
            # Create three MinerDrones and three ScoutDrones
            self._create_drone("Miner")
            self._create_drone("Scout")
        for drone in self.drones:
            self._deployed[id(self.drones[drone])] = 0

    def _create_drone(self, type: str):
        drone_types = {"Drone": Drone(),
                       "Miner": MinerDrone(),
                       "Scout": ScoutDrone()}
        new_drone = drone_types[type]
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id: int, summary: float):
        self.maps[map_id] = summary

    def _select_map(self):
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
        # TODO: find path using Dijkstra's
        pass

    def action(self, context=None):
        action = None
        # Deploy all scouts at start
        for drone in self.drones.values():
            if isinstance(drone, ScoutDrone):
                if not self._deployed[id(drone)]:
                    continue
                action = f"DEPLOY {id(drone)} {self._select_map()}"
                break

        for drone in self.drones.values():
            if drone not in self._deployed or drone.path:
                continue
            self.set_drone_path()
        return action
