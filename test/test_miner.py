"""Test class for miner drone zerg units."""
from test.base_drone_tester import BaseDroneTester

from zerg.drones import MinerDrone


class TestMiner(BaseDroneTester):
    def setUp(self) -> None:
        self.base_miner_ = MinerDrone()
        (
            self.custom_drones_,
            self.custom_drone_stats_,
        ) = self._build_dynamic_units(
            MinerDrone  # type: ignore
        )

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
