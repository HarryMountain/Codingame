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

    def test_mass_zombie_attack(self):
        ash_position = np.array((7992, 8304))
        zombie_positions = [np.array((3996, 4152)), np.array((3996, 4844)), np.array((3996, 7612)), np.array((5328, 1384)),
                            np.array((7992, 3460)), np.array((11322, 5536)), np.array((11322, 8304))]
        human_positions = [np.array((757, 3545)), np.array((510, 8170)), np.array((1119, 733)), np.array((1416, 7409)), np.array((1110, 8488)),
                           np.array((2118, 1983)), np.array((3167, 480)), np.array((6576, 664)), np.array((8704, 1276)), np.array((13340, 5663)),
                           np.array((13808, 4731)), np.array((15355, 3528)), np.array((15495, 5035)), np.array((15182, 6184)), np.array((15564, 7640))]

        for i in range(10):
            state = GameState(ash_position, zombie_positions, human_positions)
            steps = genetic_algorithm(None, state)
            #self.assertEqual(expected_scores[i], score)


if __name__ == '__main__':
    unittest.main()