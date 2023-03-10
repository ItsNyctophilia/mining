"""Overlord, who oversees zerg drones and assigns tasks to them."""

from __future__ import annotations

from queue import SimpleQueue
from typing import TYPE_CHECKING

from mining.utils import DEFAULT_TILE, Coordinate, Icon, Map

import random
from .drones import Drone, MinerDrone, ScoutDrone, State
from .zerg import Zerg

if TYPE_CHECKING:
    from typing import Dict, List, Optional, Set, Tuple, Type

    from mining.GUI.dashboard import Dashboard
    from mining.utils import Context




class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them."""

    DEPLOY = "DEPLOY"
    RETURN = "RETURN"

    def __init__(
        self,
        total_ticks: int,
        refined_minerals: int,
        dashboard: Dashboard,
    ) -> None:
        """Initialize the Overlord.

        Args:
            total_ticks (int): Total ticks allowed for mining.
            refined_minerals (int): Total given minerals.
            dashboard (_type_, optional): The GUI dashboard. Defaults to None.
        """
        self.dashboard = dashboard
        self.drones: Dict[int, Drone] = {}
        # a drone id as key and drone as value
        self._deployed: Dict[int, Optional[int]] = {}
        # a drone id as key and map id as value
        self._idle_drones: Dict[Type[Drone], Set[Drone]] = {}
        self._update_queue: SimpleQueue[
            Tuple[int, Drone, Context]
        ] = SimpleQueue()
        # a queue of map updates from zerg drones
        self._pickup_queue: SimpleQueue[Tuple[Map, Drone]] = SimpleQueue()
        # a queue of pick up requests from drones
        self._maps: Dict[int, Map] = {}
        # a map id as key and Map as value
        num_scouts, num_miners, classes = self._create_drone_classes(refined_minerals)
        print (num_scouts, num_miners)
        for _ in range(num_scouts):
            self._create_drone(classes["Scout"])
        for _ in range(num_miners):   
            self._create_drone(classes["Miner"])
    
    def _purchase_part(self, minerals: int, cost: int, drones: int):
        cost = drones * cost
        if (minerals := minerals - cost) < 0:
            return None
        return minerals 

    def _create_drone_classes(self, minerals: int) -> Dict(Drone):
        """Create custom drone classes based on number of minerals
        
        Args:
            minerals (int): Number of allotted minerals for drone
                creation

        Returns:
            List(Drone): List of drone classes containing a custom
            ScoutDrone and MinerDrone
        """
        # Maximum desired drones to create at instantiation,
        # leaving leftover minerals for drone stat upgrades
        MAX_ALLOWABLE_DRONES = 12
        # Minimum drone: 10HP, 5 Capacity, 1 Move = 5 Minerals
        MIN_DRONE_DEFAULTS = (10, 5, 1)
        MIN_MINERALS = 5
        # +10HP = 1 Mineral,
        HP_COST = 1
        # +5 Capacity = 1 Mineral,
        CAP_COST = 1
        # +1 Move = 3 Minerals
        MOVE_COST = 3

        max_drones = int(minerals / 5)
        if max_drones > MAX_ALLOWABLE_DRONES:
            max_drones = MAX_ALLOWABLE_DRONES
        num_scouts = int(max_drones / 2)
        if num_scouts < 1:
            num_scouts = 1
        num_miners = max_drones - num_scouts

        leftover = minerals - (MAX_ALLOWABLE_DRONES * MIN_MINERALS)

        scout_hp, scout_cap, scout_moves = MIN_DRONE_DEFAULTS
        miner_hp, miner_cap, miner_moves = MIN_DRONE_DEFAULTS

        drone_classes = {}
        while leftover > 0:
            if scout_hp < 40:
                leftover = self._purchase_part(leftover, HP_COST, num_scouts)
                if leftover is None:
                    break
                scout_hp += 10
            elif miner_cap < 10:
                leftover = self._purchase_part(leftover, CAP_COST, num_miners)
                if leftover is None:
                    break
                miner_cap += 5
            elif miner_hp < 40:
                leftover = self._purchase_part(leftover, HP_COST, num_miners)
                if leftover is None:
                    break
                miner_hp += 10
            elif miner_moves < 2:
                leftover = self._purchase_part(leftover, MOVE_COST, num_miners)
                if leftover is None:
                    break
                miner_moves += 1
            else:
                leftover = self._purchase_part(leftover, HP_COST, num_scouts)
                if leftover is None:
                    break
                scout_hp += 10
        custom_scout = Drone.drone_blueprint(scout_hp, scout_cap, scout_moves,
                                      "Custom Scout", ScoutDrone)
        custom_miner = Drone.drone_blueprint(miner_hp, miner_cap, miner_moves,
                                      "Custom Miner", MinerDrone)       
        drone_classes.update({"Scout": custom_scout})
        drone_classes.update({"Miner": custom_miner})

        return (num_scouts, num_miners, drone_classes)

    def _create_drone(self, drone_type: Type[Drone]) -> None:
        """Create a new zerg drone of the specified drone type."""
        new_drone = drone_type(self)
        drone_id = id(new_drone)
        # self._drones[drone_type][drone_id] = new_drone
        self.drones[drone_id] = new_drone
        self._deployed[drone_id] = None
        print(f"{drone_type} : {drone_type.__bases__[0]}")
        self._idle_drones.setdefault(drone_type.__bases__[0],
                                     set()).add(new_drone)

    def mark_drone_dead(self, drone: Drone) -> None:
        """Mark a drone as dead.

        Args:
            drone (int): The drone to mark as dead.
        """
        drone_id = id(drone)
        if (map_id := self._deployed[drone_id]) is not None:
            del self._deployed[drone_id]
            del self.drones[drone_id]
            if isinstance(drone, ScoutDrone):
                self._maps[map_id].scout_count -= 1
            # TODO: if miner dies, untask a mineral it may have been working on

    def add_map(self, map_id: int, summary: float) -> None:
        """Register ID for map and summary of mineral density.

        Args:
            map_id (int): The id of the map.
            summary (float): The density of minerals in the map.
        """
        physical_map = Map(map_id, summary)
        self._maps[map_id] = physical_map
        self.dashboard.create_map_gui(physical_map)
        # TODO: Is this overwriting the drone table every time a map is added?
        self.dashboard.update_drone_table(self.drones.values())

    def del_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Remove a mineral from the set of known minerals.

        Args:
            coord (Coordinate): The coordinate of the mineral to delete.
            drone_id (int): The id of the drone who found the removed mineral.
        """
        # TODO: maybe pass in map id instead of drone id
        if (map_id := self._deployed[drone_id]) is not None:
            self._maps[map_id].tasked_minerals.remove(coord)

    def _select_map(self) -> int:
        """Select the map to deploy a scout to.

        Returns:
            int: The id of the chosen map
        """
        map_id, map_ = min(
            self._maps.items(),
            key=lambda map_pair: map_pair[1].scout_count,
        )
        map_.scout_count += 1
        return map_id

    def enqueue_map_update(self, drone: Drone, context: Context) -> None:
        """Enqueue a map update of the drone's location and its context.

        This method will register the update information to a queue that will
        be processed at a later time.
        Args:
            drone (Drone): The drone giving updates.
            context (Context): The update information.
        """
        if (map_id := self._deployed.get(id(drone))) is not None:
            self._update_queue.put((map_id, drone, context))

    def request_pickup(self, drone: Drone) -> None:
        """Enqueue a drone pickup request.

        This method will register the drone's request to be picked up to a
        queue that will be processed at a later time. If a drone is not on the
        deployment zone when its request is handled, it will not be picked up.

        Args:
            drone (Drone): The drone requesting pickup.
            coordinate (Coordinate): The location of the drone.
        """
        if (map_id := self._deployed[id(drone)]) is not None:
            self._pickup_queue.put((self._maps[map_id], drone))

    def _distance_sort(self, start: Coordinate, end: Coordinate):
        start_x, start_y = start
        end_x, end_y = end
        return (start_x - end_x) + (start_y - end_y)

    def _assign_scout_target(
        self, map_id: int, start: Coordinate
    ) -> List[Coordinate]:
        current_map = self._maps[map_id]
        unexplored_tiles = current_map.get_unexplored_tiles()
        unexplored_tiles.sort(
            key=lambda tile: self._distance_sort(start, tile.coordinate),
            reverse=True,
        )
        random.seed()
        for tile in unexplored_tiles:
            if random.randint(1, 2) == 2:
                continue
            coord = tile.coordinate
            neighbor_icons = (
                current_map.get(coord, DEFAULT_TILE).icon
                for coord in coord.cardinals()
            )
            if not any(
                True
                for icon in neighbor_icons
                if icon
                in [Icon.MINERAL, Icon.EMPTY, Icon.DEPLOY_ZONE, Icon.ACID]
            ):
                continue
            # TODO: Remove test print
            print(f"Finding path from {start} to {tile.coordinate}")
            if path := current_map.dijkstra(start, tile.coordinate):
                return path

        return []

    def _set_drone_path(self, drone: "Drone", context: "Context") -> None:
        """Give a drone a path based on their role and context.

        Args:
            drone (Drone): The drone whose path will be set.
            context (Context): The context of the drone.
        """
        if (map_id := self._deployed[id(drone)]) is not None:
            start = Coordinate(context.x, context.y)
            dest = self._assign_scout_target(map_id, start)
            drone.path = dest

    def action(self, context=None) -> str:
        # sourcery skip: assign-if-exp, reintroduce-else
        """Perform some action, based on the context of the situation.

        Args:
            context (Context): Context surrounding the overlord;
                currently unused

        Returns:
            str: The action for the overlord to perform
        """
        self._update_map()

        if action := self._recall_drones():
            return action

        if action := self._deploy_miners():
            return action

        return self._deploy_scouts()

    def _update_map(self) -> None:
        drone_positions = []
        while not self._update_queue.empty():
            map_id, drone, drone_context = self._update_queue.get()
            zerg_coord = Coordinate(drone_context.x, drone_context.y)
            drone_positions.append(
                {"map_id": map_id, "coord": zerg_coord, "icon": drone.icon}
            )
            self._maps[map_id].update_context(drone_context)
            if drone.state == State.WAITING and isinstance(drone, ScoutDrone):
                self._set_drone_path(drone, drone_context)
        self.dashboard.update_maps(drone_positions)

    def _recall_drones(self) -> str:
        if self._pickup_queue.empty():
            return ""

        map_, drone = self._pickup_queue.get()
        # TODO: have map track all drones, make this a generic counter
        if isinstance(drone, ScoutDrone):
            map_.scout_count -= 1
        self._idle_drones[type(drone).__bases__[0]].add(drone)
        drone.reset_minerals()
        action = f"{self.RETURN} {id(drone)}"
        # TODO: Remove test print
        print(action)
        return action

    def _deploy_miners(self) -> str:
        for map_id, map_ in self._maps.items():
            if map_.untasked_minerals and self._idle_drones[MinerDrone]:
                miner = self._idle_drones[MinerDrone].pop()
                map_.task_miner(miner)
                # TODO: Remove test print
                print("IDLE MINERS", self._idle_drones[MinerDrone])
                return self._deploy_drone(map_id, miner)
        return ""

    def _deploy_scouts(self) -> str:
        if not self._idle_drones[ScoutDrone]:
            return ""

        scout = self._idle_drones[ScoutDrone].pop()
        map_id = self._select_map()
        return self._deploy_drone(map_id, scout)

    def _deploy_drone(self, map_id: int, drone: "Drone") -> str:
        drone_id = id(drone)
        self._deployed[drone_id] = map_id
        action = f"{self.DEPLOY} {drone_id} {map_id}"
        # TODO: Remove test print
        print(drone.__class__.__name__, action)
        return action
