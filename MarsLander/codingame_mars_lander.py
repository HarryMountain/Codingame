import math
from random import randint
from enum import Enum
import numpy as np

GRAVITY = -3.711


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


# Save the Planet.
# Use less Fossil Fuel.

n = int(input())  # the number of points used to draw the surface of Mars.
land_x = []
land_y = []
for i in range(n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    coords = [int(j) for j in input().split()]
    land_x.append(coords[0])
    land_y.append(coords[1])
print(land_x, file=sys.stderr, flush=True)
print(land_y, file=sys.stderr, flush=True)

current_r = 0
current_p = 0
sim_x = -1
sim_y = -1
sim_hs = 0
sim_vs = 0
sim_state = State.Flying

# game loop
while True:
    # hs: the horizontal speed (in m/s), can be negative.
    # vs: the vertical speed (in m/s), can be negative.
    # f: the quantity of remaining fuel in liters.
    # r: the rotation angle in degrees (-90 to 90).
    # p: the thrust power (0 to 4).
    x, y, hs, vs, f, r, p = [int(i) for i in input().split()]
    if sim_x == -1:
        sim_x = x
        sim_y = y
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    current_r = min(max(current_r + randint(-15, 15), -90), 90)
    current_p = min(max(current_p + randint(-1, 1), 0), 4)
    radians_r = math.radians(current_r)

    print(hs, round(sim_hs), file=sys.stderr, flush=True)
    print(vs, round(sim_vs), file=sys.stderr, flush=True)
    print(x, round(sim_x), file=sys.stderr, flush=True)
    print(y, round(sim_y), file=sys.stderr, flush=True)
    print(sim_state, file=sys.stderr, flush=True)
    ha = -current_p * math.sin(radians_r)
    va = current_p * math.cos(radians_r) + GRAVITY
    sim_x += sim_hs + ha / 2
    sim_y += sim_vs + va / 2
    sim_hs += ha
    sim_vs += va
    land_height = np.interp(sim_x, land_x, land_y, left=None, right=None, period=None)
    if sim_y < land_height:
        sim_state = State.Crashed  # TODO - always crasheds
    print(sim_state, file=sys.stderr, flush=True)

    # R P. R is the desired rotation angle. P is the desired thrust power.
    print(current_r, current_p)