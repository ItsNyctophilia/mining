"""Test class for miner drone zerg units."""
from test.base_drone_tester import BaseDroneTester
from test.testing_utils import TestingUtils

from utils import Icon, Tile
from zerg.drones import MinerDrone


class TestMiner(BaseDroneTester):
    def setUp(self) -> None:
        self.base_miner_ = MinerDrone(self.overlord)
        (
            self.custom_drones_,
            self.custom_drone_stats_,
        ) = self._build_dynamic_units(MinerDrone)

    def test_miner_init(self):
        self.assertIsInstance(self.base_miner_, MinerDrone)

    def test_miner_action(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            result = self.base_miner_.action(self.phony_context_)
            self.assertTrue(result in self.DIRECTIONS, f"{result}")

    def test_dynamic_miner(self):
        for drone_n in range(len(self.custom_drones_)):
            self.assertIsInstance(self.custom_drone_stats_[drone_n].init, type)
            self.assertIsInstance(self.custom_drones_[drone_n], MinerDrone)

    def test_miner_mine_mineral(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            mineral_tile = Tile(
                TestingUtils._randomize_coordinate(), Icon.MINERAL
            )
            self._register_tile(mineral_tile)
            mineral_health_max = self.minerals_[mineral_tile]
            self._travel(self.base_miner_, dest=mineral_tile)
            mineral_health_left = self.minerals_[mineral_tile]
            self.assertEqual(
                mineral_tile.icon,
                Icon.EMPTY,
                f"Mineral at {mineral_tile} with health "
                f"{mineral_health_left}/{mineral_health_max}"
                f"{self.map_}",
            )

    def test_miner_return_home(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            mineral_tile = Tile(
                TestingUtils._randomize_coordinate(), Icon.MINERAL
            )
            self._register_tile(mineral_tile)
            mineral_health = self.minerals_[mineral_tile]
            ticks, steps, start, _, curr, path = self._travel(
                self.base_miner_, dest=mineral_tile
            )
            expected_steps = len(path) * 2
            expected_ticks = expected_steps + mineral_health
            self.assertEqual(start, curr)
            self.assertEqual(ticks, expected_ticks)
            self.assertEqual(steps, expected_steps)
