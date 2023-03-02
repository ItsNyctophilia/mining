"""Test class for basic drone zerg units."""
import random
from test.base_drone_tester import BaseDroneTester

from zerg.drones import Drone, MinerDrone, ScoutDrone


class TestDrone(BaseDroneTester):
    """Test class for basic drone zerg units."""

    DRONE_TYPES = [Drone, MinerDrone, ScoutDrone]

    def setUp(self) -> None:
        self.base_drone_ = Drone()
        self.base_miner_ = MinerDrone()
        (
            self.custom_drones_,
            self.custom_drone_stats_,
        ) = self._build_dynamic_units(
            random.choice(self.DRONE_TYPES)  # type: ignore
        )

    def test_drone_init(self):
        self.assertIsInstance(self.base_drone_, Drone)

    def test_miner_init(self):
        self.assertIsInstance(self.base_miner_, MinerDrone)

    def test_drones_action(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            result_drone = self.base_drone_.action(self.phony_context_)
            self.assertTrue(result_drone in self.DIRECTIONS, f"{result_drone}")
            result_miner = self.base_miner_.action(self.phony_context_)
            self.assertTrue(result_miner in self.DIRECTIONS, f"{result_miner}")

    def test_dynamic_drone(self):
        for drone_n in range(len(self.custom_drones_)):
            self.assertIsInstance(self.custom_drone_stats_[drone_n].init, type)
            self.assertIsInstance(self.custom_drones_[drone_n], Drone)

    def test_drone_cost(self):
        for drone_n in range(len(self.custom_drones_)):
            health, capacity, moves, _ = self.custom_drone_stats_[drone_n]
            check_cost = self.custom_drones_[drone_n].get_init_cost()
            total_cost = (health / 10) + (capacity / 5) + (moves * 3)
            self.assertEqual(check_cost, total_cost)

    def test_drone_steps_taken(self):
        steps = 0
        for _ in range(self.RANDOM_TEST_RUNS):
            _, curr_steps, _, _, _, _ = self._travel(self.base_drone_)
            steps += curr_steps
        self.assertEqual(self.base_drone_.steps(), steps)

    def test_drone_reach_dest(self):
        for _ in range(self.RANDOM_TEST_RUNS):
            ticks, _, _, dest, curr, path = self._travel(self.base_drone_)
            path_len = len(path)
            msg = (
                f"It took {'more' if ticks > path_len else 'less'} time "
                "to get to the goal than expected"
            )
            self.assertEqual(curr, dest)
            self.assertEqual(ticks, path_len, msg)
