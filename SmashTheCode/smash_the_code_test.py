from unittest import TestCase

import time
from copy import deepcopy

import numpy as np
from SmashTheCode.smash_the_code import place_block, merge


class Test(TestCase):
    def test_smash_the_code_timing_no_merge(self):
        grid = np.zeros((6, 12), dtype=int)
        grid_fill = [
            [1, 1, 2, 3, 0, 4],
            [3, 4, 5, 0, 0, 3],
            [2, 1, 1, 0, 0, 2],
            [2, 2, 1, 0, 0, 2],
        ]
        row_index = 0
        for row in grid_fill:
            for i in range(6):
                grid[row_index, i] = row[i]
            row_index += 1
        start_time = time.time()
        for i in range(10000):
            temp_grid = deepcopy(grid)
            block = [5, 4]
            place_block(block, 1, temp_grid, 0)
            merge(temp_grid, 0)
        end_time = time.time()
        print('Time taken : ' + str(end_time - start_time))
        self.assertEqual(True, True)

    def test_smash_the_code_timing_with_merge(self):
        grid = np.zeros((6, 12), dtype=int)
        grid_fill = [
            [1, 1, 2, 3, 0, 4],
            [3, 4, 5, 0, 0, 3],
            [2, 1, 1, 0, 0, 2],
            [2, 2, 1, 0, 0, 2],
        ]
        row_index = 0
        for row in grid_fill:
            for i in range(6):
                grid[row_index, i] = row[i]
            row_index += 1
        start_time = time.time()
        for i in range(10000):
            temp_grid = deepcopy(grid)
            block = [2, 1]
            place_block(block, 1, temp_grid, 1)
            merge(temp_grid, 0)
        end_time = time.time()
        print('Time taken : ' + str(end_time - start_time))
        self.assertEqual(True, True)

#
#if __name__ == '__main__':
#    unittest.main()
