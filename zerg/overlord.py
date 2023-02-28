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
        self._minerals = {}  # a list of the coordinates of minerals
        for value in range(3):
            self._create_drone("Miner")
            self._create_drone("Scout")

    def _create_drone(self, type: str):
        drone_types = {"Drone": Drone(),
                       "Miner": MinerDrone(),
                       "Scout": ScoutDrone()}
        new_drone = drone_types[type]
        self.drones[id(new_drone)] = new_drone

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self, context=None):
        return None
