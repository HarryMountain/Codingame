import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x, y = [int(i) for i in input().split()]
box_x = [0, w - 1]
box_y = [0, h - 1]
# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    bomb_dirs = list(bomb_dir)
    for direction in bomb_dirs:
        if direction == 'U':
            box_y[1] = y - 1
        elif direction == 'R':
            box_x[0] = x + 1
        elif direction == 'D':
            box_y[0] = y + 1
        elif direction == 'L':
            box_x[1] = x - 1
    x = sum(box_x) // 2
    y = sum(box_y) // 2
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # the location of the next window Batman should jump to.
    print(*[x, y])