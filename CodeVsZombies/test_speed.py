import time
import numpy as np


class Zombie:
    def __init__(self):
        self.x = 10
        self.y = 20
        self.vx = 140
        self.vy = -260


zombie = Zombie()
ms = int(time.time() * 1000.0)
for i in range(1000000):
    zombie.x += zombie.vx
    zombie.y += zombie.vy
print(int(time.time() * 1000.0) - ms)

zombie = [np.array((10, 20)), np.array((140, -260))]
ms = int(time.time() * 1000.0)
for i in range(1000000):
    zombie[0][0] += zombie[1][0]
    zombie[0][1] += zombie[1][1]
print(int(time.time() * 1000.0) - ms)