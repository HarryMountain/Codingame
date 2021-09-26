from unittest import TestCase
from MarsLander.lander import solve_lander

# [x, y, hs, vs, r, p, fuel, land_x, land_y]
TEST_CASES = [
    [2500, 2700, 0, 0, 0, 0, 1, [0, 1000, 1500, 3000, 4000, 5500, 6999], [100, 500, 1500, 1000, 150, 150, 800]],
    [6500, 2800, -100, 0, 90, 0, 1, [0, 1000, 1500, 3000, 3500, 3700, 5000, 5800, 6000, 6999], [100, 500, 100, 100, 500, 200, 1500, 300, 1000, 2000]],
    [500, 2700, 100, 0, -90, 0, 800, [0, 300, 350, 500, 800, 1000, 1200, 1500, 2000, 2200, 2500, 2900, 3000, 3200, 3500, 3800, 4000, 5000, 5500, 6999], [1000, 1500, 1400, 2000, 1800, 2500, 2100, 2400, 1000, 500, 100, 800, 500, 1000, 2000, 800, 200, 200, 1500, 2800]]
]


class Test(TestCase):
    def test_lander0(self):
        solve_lander(*TEST_CASES[0])

    def test_lander1(self):
        solve_lander(*TEST_CASES[1])

    def test_lander2(self):
        solve_lander(*TEST_CASES[2])

    def test_all_landers(self):
        for i in range(len(TEST_CASES)):
            solve_lander(*TEST_CASES[i])
