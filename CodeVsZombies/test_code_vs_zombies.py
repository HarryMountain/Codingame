import unittest

import numpy as np
from CodeVsZombies.code_vs_zombies import GameState, genetic_algorithm


class TestCodeVsZombies(unittest.TestCase):
    def test_case1_single_zombie_single_human(self):
        ash_position = np.array((0, 0))
        zombie_positions = [np.array((8250, 8999))]
        human_positions = [np.array((8250, 4500))]

        expected_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10]

        state = GameState(ash_position, zombie_positions, human_positions)
        steps = genetic_algorithm(None, state)
        for i in range(10):
            score = state.update(steps[i])
            self.assertEqual(expected_scores[i], score)

    def test_case2_two_zombies_two_humans(self):
        ash_position = np.array((5000, 0))
        zombie_positions = [np.array((3100, 7000)), np.array((11500, 7100))]
        human_positions = [np.array((950, 6000)), np.array((8000, 6100))]

        expected_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10]

        state = GameState(ash_position, zombie_positions, human_positions)
        steps = genetic_algorithm(None, state)
        for i in range(10):
            score = state.update(steps[i])
            self.assertEqual(expected_scores[i], score)


if __name__ == '__main__':
    unittest.main()
