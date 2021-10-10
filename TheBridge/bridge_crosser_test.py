from unittest import TestCase
from TheBridge.bridge_crosser import solve_bridge

# [number of motorbikes, number required to finish, [lane 0, lane 1, lane 2, lane 3], speed, [bike0 data[x, y, alive/dead = 1/0]]
TEST_CASES = [
    [1, 1, ['..............................', '..............................', '...........0..................',
     '..............................'], 0, [[0, 2, 1]]],
]


class Test(TestCase):
    def test_one_lonely_hole(self):
        solve_bridge(*TEST_CASES[0])
