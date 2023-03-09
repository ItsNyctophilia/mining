"""Overlord, who oversees zerg drones and assigns tasks to them."""

from queue import SimpleQueue
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Type

from mining.utils import Context, Coordinate, Icon, Map, Tile

from .drones import Drone, MinerDrone, ScoutDrone, State
from .zerg import Zerg

if TYPE_CHECKING:
    from mining.GUI.dashboard import Dashboard


class Overlord(Zerg):
    """Overlord, who oversees zerg drones and assigns tasks to them."""

    DEFAULT_TILE = Tile(Coordinate(0, 0), Icon.UNREACHABLE)

    DEPLOY = "DEPLOY"
    RETURN = "RETURN"

    def __init__(
        self,
        total_ticks: int,
        refined_minerals: int,
        dashboard: "Dashboard",
    ) -> None:
        """Initialize the Overlord.

        Args:
            total_ticks (int): Total ticks allowed for mining.
            refined_minerals (int): Total given minerals.
            dashboard (_type_, optional): The GUI dashboard. Defaults to None.
        """
        self.dashboard = dashboard
        # a map id as key and summary as value
        self._drones: Dict[Type[Drone], Dict[int, Drone]] = {
            ScoutDrone: {},
            MinerDrone: {},
        }
        self.drones: Dict[int, Drone] = {}
        # a drone id as key and drone as value
        self._deployed: Dict[int, Optional[int]] = {}
        # a drone id as key and map id as value
        self._idle_miners: Set[Drone] = set()
        self._update_queue: SimpleQueue[
            Tuple[int, Drone, Context]
        ] = SimpleQueue()
        # a queue of map updates from zerg drones
        self._pickup_queue: SimpleQueue[Tuple[int, int]] = SimpleQueue()
        # a queue of pick up requests from drones
        self._maps: Dict[int, Map] = {}
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
        # TODO: if miner dies, untask a mineral it may have been working on

    def add_map(self, map_id: int, summary: float) -> None:
        """Register ID for map and summary of mineral density.

        Args:
            map_id (int): The id of the map.
            summary (float): The density of minerals in the map.
        """
        physical_map = Map(summary)
        self._maps[map_id] = physical_map
        self.dashboard.create_map_gui(physical_map)
        self.dashboard.update_drone_table(self.drones.values())

    def del_mineral(self, coord: Coordinate, drone_id: int) -> None:
        """Remove a mineral from the set of known minerals.

        Args:
            coord (Coordinate): The coordinate of the mineral to delete.
            drone_id (int): The id of the drone who found the removed mineral.
        """
        # TODO: maybe pass in map id instead of drone id
        if map_id := self._deployed[drone_id]:
            del self._maps[map_id].minerals[coord]

    def _select_map(self) -> int:
        """Select the map with the least number of scouts on it.

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
        if map_id := self._deployed[id(drone)]:
            self._update_queue.put((map_id, drone, context))

    def request_pickup(self, drone_id: int) -> None:
        """Enqueue a drone pickup requests.

        This method will register the drone's request to be picked up to a
        queue that will be processed at a later time. If a drone is not on the
        deployment zone when its request is handled, it will not be picked up.

        Args:
            drone (Drone): The drone requesting pickup.
            coordinate (Coordinate): The location of the drone.
        """
        if map_id := self._deployed[drone_id]:
            self._pickup_queue.put((map_id, drone_id))

    def _distance_sort(self, start: Coordinate, end: Coordinate):
        start_x, start_y = start
        end_x, end_y = end
        return (start_x - end_x) + (start_y - end_y)

    def _assign_scout_target(
        self, map_id: int, start: Coordinate
    ) -> List[Coordinate]:
        current_map = self._maps[map_id]
        tiles = current_map.get_unexplored_tiles()
        tiles.sort(
            key=lambda tile: self._distance_sort(start, tile.coordinate),
            reverse=True,
        )
        path = []
        for tile in tiles:
            coord = tile.coordinate
            neighbor_icons = [
                current_map.get(coord, self.DEFAULT_TILE).icon
                for coord in coord.cardinals()
            ]
            if not any(
                True
                for icon in neighbor_icons
                if icon
                in [Icon.MINERAL, Icon.EMPTY, Icon.DEPLOY_ZONE, Icon.ACID]
            ):
                continue
            print(f"Finding path from {start} to {coord}")
            if path := current_map.dijkstra(start, tile.coordinate):
                break

        return path

    def _set_drone_path(self, drone: Drone, context: Context) -> None:
        """Give a drone a path based on their role and context."""
        if map_id := self._deployed[id(drone)]:
            start = Coordinate(context.x, context.y)
            # dest = self._spiral_search(start, map_id)
            dest = self._assign_scout_target(map_id, start)
            drone.path = dest

    def action(self, context=None) -> str:
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
        while not self._update_queue.empty():
            map_id, drone, drone_context = self._update_queue.get()
            current_map = self._maps[map_id]
            current_map.update_context(drone_context)
            if drone.state == State.WAITING and isinstance(drone, ScoutDrone):
                print(current_map.get_unexplored_tiles())
                self._set_drone_path(drone, drone_context)
        self.dashboard.update_maps()

    def _recall_drones(self) -> str:
        if not self._pickup_queue.empty():
            map_id, drone_id = self._pickup_queue.get()
            return self._build_action(self.RETURN, drone_id, map_id)
        return ""

    def _deploy_miners(self) -> str:
        for map_id, map_ in self._maps.items():
            if map_.untasked_minerals and self._idle_miners:
                miner = self._idle_miners.pop()
                map_.task_miner(miner)
                return self._build_action(self.DEPLOY, id(miner), map_id)
        return ""

    def _deploy_scouts(self) -> str:
        for drone in self._drones[ScoutDrone].values():
            if not self._deployed[id(drone)]:
                map_id = self._select_map()
                self._deployed[id(drone)] = map_id
                return self._build_action(self.DEPLOY, id(drone), map_id)
        return ""

    def _build_action(self, action: str, drone_id: int, map_id: int) -> str:
        return f"{action} {drone_id} {map_id}"
