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
            box_x[0] = math.floor(divide) + 1
        elif (bomb_dir == 'WARMER') == (x < old_x):
            box_x[1] = math.ceil(divide) - 1
    elif last_move == 'vertical':
        divide = (old_y + y) / 2
        if bomb_dir == 'SAME':
            box_y = [int(divide), int(divide)]
            y = int(divide)
        elif (bomb_dir == 'WARMER') == (y > old_y):
            box_y[0] = math.floor(divide) + 1
        elif (bomb_dir == 'WARMER') == (y < old_y):
            box_y[1] = math.ceil(divide) - 1
    print(box_x, file=sys.stderr, flush=True)
    print(box_y, file=sys.stderr, flush=True)
    old_x = x
    old_y = y
    if box_x[0] != box_x[1]:
        if box_x[0] <= x <= box_x[1]:
            x = sum(box_x) - old_x
            if x == box_x[1] and x > 0:
                x -= 1
            elif x == box_x[0] and x < w - 1:
                x += 1
            if x == old_x:
                x += 1
        else:
            x = max(0, min(w - 1, sum(box_x) - old_x))
            if x == old_x:
                x += 1
            # x = int(0.75 * box_x[1] + 0.25 * box_x[0])
            # x = ((old_x + box_x[0]) // 2) if old_x > box_x[1] else (old_x + box_x[1]) // 2
            # x = int(box_x[0] * 1 / 3 + box_x[1] * 2 / 3) if old_x < box_x[0] else int(box_x[1] * 1 / 3 + box_x[0] * 2 / 3)

        last_move = 'horizontal'
    else:
        changed = x != box_x[0]
        x = box_x[0]
        if not changed:
            if box_y[0] != box_y[1]:
                if box_y[0] <= y <= box_y[1]:
                    y = sum(box_y) - old_y
                    if y == box_y[1] and y > 0:
                        y -= 1
                    elif y == box_y[0] and y < h - 1:
                        y += 1
                    if y == old_y:
                        y += 1
                else:
                    # y = int(0.75 * box_y[1] + 0.25 * box_y[0])
                    # y = ((old_y + box_y[0]) // 2) if old_y > box_y[1] else (old_y + box_y[1]) // 2
                    # y = int(box_y[0] * 1 / 3 + box_y[1] * 2 / 3) if old_y < box_y[0] else int(box_y[1] * 1 / 3 + box_y[0] * 2 / 3)
                    y = max(0, min(h - 1, sum(box_y) - old_y))
                    if y == old_y:
                        y += 1
                last_move = 'vertical'
            else:
                y = box_y[0]
    print('0 1')
    #print(*[x, y])
