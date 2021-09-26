from unittest import TestCase
from MarsLander.lander import solve_lander

TEST_CASES = [
    [2500, 2700, 0, 0, 0, 0, [0, 1000, 1500, 3000, 4000, 5500, 6999], [100, 500, 1500, 1000, 150, 150, 800]],
    [6500, 2800, -100, 0, 90, 0, [0, 1000, 1500, 3000, 3500, 3700, 5000, 5800, 6000, 6999],
     [100, 500, 100, 100, 500, 200, 1500, 300, 1000, 2000]],
]


class Test(TestCase):
    def adder(self, x, y):
        return x+y

    def test_lander0(self):
        solve_lander(*TEST_CASES[0])

    def test_lander1(self):
        solve_lander(*TEST_CASES[1])

    def test_all_landers(self):
        for i in range(len(TEST_CASES)):
            solve_lander(*TEST_CASES[i])

    def test_add(self):
        aaa = self.adder(*[2, 3])
        print(aaa)
