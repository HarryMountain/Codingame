from unittest import TestCase
from TheBridge.bridge_crosser import solve_bridge

# [number of motorbikes, number required to finish, speed, [bike0 data[x, y, alive/dead = 1/0], [lane 0, lane 1, lane 2, lane 3]]
TEST_CASES = [
    [1, 1, 0, [[0, 2, 1]], ['..............................', '..............................', '...........0..................',
     '..............................']],
    [4, 4, 2, [[7, 0, 1], [7, 1, 1], [7, 2, 1], [7, 3, 1]], '..........000......0000..............000000.............', '..........000......0000..............000000.............', '..........000......0000..............000000.............', '..........000......0000..............000000.............'],
    [4, 4, 8, [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1]], '..............00000......0000.....00......', '..............00000......0000.....00......', '..............00000......0000.....00......', '..............00000......0000.....00......'],
    [4, 4, 1, [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1]], '..............00..00..00............', '..............00..00..00............', '..............00..00..00............', '..............00..00..00............'],
    [4, 3, 6, [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1]], '.............0.............0........', '..............0.............0.......', '...............0.............0......', '................0..........000......'],
    [2, 2, 2, [[0, 1, 1], [0, 2, 1]], '...0......0....0........0..0..0..0.....', '....0............000........0...0......', '.....0..........000..........0.0.......', '...0......0....0........0..0..0..0.....'],
    [3, 2, 7, [[0, 0, 1], [0, 1, 1], [0, 2, 1]], '.........0000000............................0.0.0.0.0.0.0.0.....', '.................0..........................0.0.0.0.0.0.0.0.....', '.........0000000............................0.0.0.0.0.0.0.0.....', '............................................0.0.0.0.0.0.0.0.....'],
]


class Test(TestCase):
    def test_one_lonely_hole(self):
        solve_bridge(*TEST_CASES[0])

    def jumps_increasing_length(self):
        solve_bridge(*TEST_CASES[1])

    def jumps_decreasing_length(self):
        solve_bridge(*TEST_CASES[2])

    def jumps_equal_length(self):
        solve_bridge(*TEST_CASES[3])

    def diagonal_holes(self):
        solve_bridge(*TEST_CASES[4])

    def scattered_pits(self):
        solve_bridge(*TEST_CASES[5])

    def big_jump_hole_columns(self):
        solve_bridge(*TEST_CASES[6])