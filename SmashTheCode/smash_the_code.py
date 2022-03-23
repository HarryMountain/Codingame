import sys
import math
from copy import deepcopy

import numpy as np

SCORE_THRESHOLD_MULTIPLIER = 4
HEIGHT_PENALTY = 100

grid = np.zeros((6, 12), dtype=int)


def find_blocks(grid):
    blocks = []
    number_sorted = 0
    visited = []
    number_of_cells = (grid > 0).sum()
    if number_of_cells == 0:
        return blocks
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            # TODO : think this is wrong - it will pick up skulls as a block. Change != 0 to > 0 ???
            if grid[x, y] > 0 and [x, y] not in visited:
                colour = grid[x, y]
                connected = [[x, y]]
                changed = True
                points_to_search = [[x, y]]
                while changed:
                    number_in_block = len(connected)
                    new_points_to_search = []
                    for element in points_to_search:
                        for move in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                            new_point = [element[0] + move[0], element[1] + move[1]]
                            if -1 < new_point[0] < 6 and -1 < new_point[1] < 12 and new_point not in visited and new_point not in connected:
                                if grid[new_point[0], new_point[1]] == colour:
                                    connected.append(new_point)
                                    new_points_to_search.append(new_point)
                    changed = len(connected) > number_in_block
                    points_to_search = new_points_to_search
                blocks.append(connected)
                visited.extend(connected)
                if len(visited) == number_of_cells:
                    return blocks
    return blocks


def place_block(block, rotation, grid, col):
    block_place = []
    if rotation == 3:
        block_place.append([block[1], col])
        block_place.append([block[0], col])
    else:
        block_place.append([block[0], col])
        block_place.append([block[1], col + 1 - rotation])
    for colour, col in block_place:
        for i in range(len(grid[col])):
            if grid[col, i] == 0:
                grid[col, i] = colour
                break

def merge(grid, cp):
    b = 0
    gb = 0
    colours = set()
    blocks = find_blocks(grid)
    #print(blocks)
    for block in blocks:
        if len(block) >= 4:
            colours.add(grid[block[0][0], block[0][1]])
            b += len(block)
            gb += 8 if len(block) >= 11 else len(block) - 4
            for point in block:
                grid[point[0], point[1]] = 0
                for move in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                    new_point = [point[0] + move[0], point[1] + move[1]]
                    if -1 < new_point[0] < 6 and -1 < new_point[1] < 12:
                        if grid[new_point[0], new_point[1]] == -1:
                            grid[point[0], point[1]] = 0
    for x in range(len(grid)):
        lowest_free = -1
        for y in range(len(grid[x])):
            if lowest_free > -1:
                if grid[x, y] != 0:
                    grid[x, lowest_free] = grid[x, y]
                    grid[x, y] = 0
                    lowest_free += 1
            else:
                if grid[x, y] == 0:
                    lowest_free = y
    # score calculation
    cb = 0 if len(colours) == 1 else 2**(len(colours) - 1)
    score = (10 * b) * max(1, min(999, (cp + cb + gb)))
    return score

def turn(grid, block, rotation, col):
    place_block(block, rotation, grid, col)
    score = 0
    cp = 0
    step_score = 1
    while step_score > 0:
        step_score = merge(grid, cp)
        score += step_score
        cp = 8 if cp == 0 else cp * 2
    return score


# game loop
while True:
    print(grid, file=sys.stderr, flush=True)
    blocks = []
    grid = np.zeros((6, 12), dtype=int)
    for i in range(8):
        # color_a: color of the first block
        # color_b: color of the attached block
        color_a, color_b = [int(j) for j in input().split()]
        blocks.append([color_a, color_b])
    score_1 = int(input())
    for i in range(12):
        row = list(input())  # One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
        for j in range(6):
            block = 0 if row[j] == '.' else int(row[j])
            if row[j] == '0':
                block = -1
            grid[j, 11 - i] = block
    score_2 = int(input())
    for i in range(12):
        row = input()

    # Write an action using print
    print(grid, file=sys.stderr, flush=True)

    # Maximize score
    score_threshold = SCORE_THRESHOLD_MULTIPLIER * (grid == 0).sum()
    print(str(score_threshold), file=sys.stderr, flush=True)
    actions = {}
    for col in range(6):
        for rotation in range(4):
            if not ((col == 0 and rotation == 2) or (col == 5 and rotation == 0)):
                second_col = col + 1 if rotation == 0 else (col - 1 if rotation == 2 else col)
                # Don't go off the top of the grid
                if grid[col, 9] == 0 and grid[second_col, 9] == 0:
                    score = turn(deepcopy(grid), blocks[0], rotation, col)
                    print(str(col) + ' ' + str(rotation) + ' ' + str(score), file=sys.stderr, flush=True)
                    actions[score] = [col, rotation]

    #print(actions, file=sys.stderr, flush=True)
    scores = sorted(actions.keys())
    #print(scores, file=sys.stderr, flush=True)
    if scores[-1] > score_threshold:
        action = actions[scores[-1]]
    else:
        action = actions[scores[0]]
    #print(action, file=sys.stderr, flush=True)
    # "x": the column in which to drop your blocks
    print(' '.join([str(x) for x in action]))


'''
turn(grid, [3, 3], 0, 0)
turn(grid, [2, 2], 0, 0)
turn(grid, [1, 1], 0, 0)
print(grid)
new_block = [3, 3]
max_score = -1
for col in range(6):
    for rotation in range(4):
        if not ((col == 0 and rotation == 2) or (col == 5 and rotation == 0)):
            score = turn(deepcopy(grid), new_block, rotation, col)
            print(str(col) + ' ' + str(rotation) + ' ' + str(score))
            if score > max_score:
                max_score = score
                action = [col, rotation]

print(grid)
#print(find_blocks(grid))
merge(grid)
refill(grid)
print(grid)
'''