import sys
import math

FRACTION_FROM_EDGE = 2/3

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x, y = [int(i) for i in input().split()]
box_x = [0, w - 1]
box_y = [0, h - 1]
print(str(w) + str(h), file=sys.stderr, flush=True)


def distance(x_dif, y_dif):
    return math.sqrt(x_dif**2 + y_dif**2)


last_move = None
while True:
    bomb_dir = input()

    # Process last move
    if last_move == 'horizontal':
        divide = (old_x + x) / 2
        if bomb_dir == 'SAME':
            box_x = [int(divide), int(divide)]
        elif (bomb_dir == 'WARMER') == (x > old_x):
            box_x[0] = max(box_x[0], math.floor(divide) + 1)
        elif (bomb_dir == 'WARMER') == (x < old_x):
            box_x[1] = min(box_x[1], math.ceil(divide) - 1)
    elif last_move == 'vertical':
        divide = (old_y + y) / 2
        if bomb_dir == 'SAME':
            box_y = [int(divide), int(divide)]
            y = int(divide)
        elif (bomb_dir == 'WARMER') == (y > old_y):
            box_y[0] = max(box_y[0], math.floor(divide) + 1)
        elif (bomb_dir == 'WARMER') == (y < old_y):
            box_y[1] = min(box_y[1], math.ceil(divide) - 1)
    print(box_x, file=sys.stderr, flush=True)
    print(box_y, file=sys.stderr, flush=True)
    old_x = x
    old_y = y
    if box_x[0] != box_x[1]:
        x = sum(box_x) - old_x
        if not (0 <= x < w):
            a = box_x[0] / (w - (box_x[1] - box_x[0]))
            fraction = FRACTION_FROM_EDGE + a * (1 - 2 * FRACTION_FROM_EDGE)
            x = math.floor(box_x[0] * (1 - fraction) + box_x[1] * fraction) if x < 0 else \
                math.ceil(box_x[0] * fraction + box_x[1] * (1 - fraction))

        if (abs(x - old_x) > 2 and abs(x - old_x) % 2 == 1) or x == old_x:
            x += 1 if x < w // 2 else -1
        last_move = 'horizontal'
    else:
        changed = x != box_x[0]
        x = box_x[0]
        if not changed:
            if box_y[0] == box_y[1]:
                y = box_y[0]
            else:
                y = sum(box_y) - old_y
                if not (0 <= y < h):
                    a = box_y[0] / (h - (box_y[1] - box_y[0]))
                    fraction = FRACTION_FROM_EDGE + a * (1 - 2 * FRACTION_FROM_EDGE)
                    y = math.floor(box_y[0] * (1 - fraction) + box_y[1] * fraction) if y < 0 else \
                        math.ceil(box_y[0] * fraction + box_y[1] * (1 - fraction))
                if (abs(y - old_y) > 2 and abs(y - old_y) % 2 == 1) or y == old_y:
                    y += 1 if y < h // 2 else -1
                last_move = 'vertical'

    print(*[x, y])
