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
    # TODO:
    #  Art : I think the problem is this:
    # When the range is near the centre it makers sense to try to cut out half the range each time
    # As the range gets close to the side it's harder to clsoe the range on the edge of the range next to the
    # edge of the grid
    # So need to put the next point close to the edge than the middle of the range


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
        if (abs(x - old_x) > 2 and abs(x - old_x) % 2 == 1) or x == old_x:
            x += -1 if x > 0 else 1
        x = max(0, min(w - 1, x))
        last_move = 'horizontal'
    else:
        changed = x != box_x[0] # todo : should this be above and x != old_x?
        x = box_x[0]
        if not changed:
            if box_y[0] == box_y[1]:
                y = box_y[0]
            else:
                y = sum(box_y) - old_y
                if (abs(y - old_y) > 2 and abs(y - old_y) % 2 == 1) or y == old_y:
                    y += -1 if y > 0 else 1
                y = max(0, min(h - 1, y))
                last_move = 'vertical'

    print(*[x, y])
