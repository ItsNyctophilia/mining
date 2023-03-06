"""Test class for scout drone zerg units."""
from test.base_drone_tester import BaseDroneTester

from zerg.drones import ScoutDrone


class TestDrone(BaseDroneTester):
    def setUp(self) -> None:
        self.base_scout_ = ScoutDrone(self.overlord)
        (
            self.custom_drones_,
            self.custom_drone_stats_,
        ) = self._build_dynamic_units(
            ScoutDrone  # type: ignore
        )

    def test_scout_init(self):
        self.assertIsInstance(self.base_scout_, ScoutDrone)

    def test_scout_action(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            result = self.base_scout_.action(self.phony_context_)
            self.assertTrue(result in self.DIRECTIONS, f"{result}")

    def test_dynamic_scout(self):
        for drone_n in range(len(self.custom_drones_)):
            self.assertIsInstance(self.custom_drone_stats_[drone_n].init, type)
            self.assertIsInstance(self.custom_drones_[drone_n], ScoutDrone)
