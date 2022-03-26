import sys
import math
from copy import deepcopy
from random import shuffle
import numpy as np

SCORE_THRESHOLD_MULTIPLIER = 4
FILL_BONUS = 2
rotation_dict = {0: 1, 1: 0, 2: -1, 3: 0}

grid = np.zeros((6, 12), dtype=int)
visited = np.zeros((6, 12), dtype=int)
# List of actions by [col, rotation]
possible_things = [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
    [0, 4],
    [1, 0],
    [1, 1],
    [1, 2],
    [1, 3],
    [1, 4],
    [1, 5],
    [2, 1],
    [2, 2],
    [2, 3],
    [2, 4],
    [2, 5],
    [3, 0],
    [3, 1],
    [3, 2],
    [3, 3],
    [3, 4],
    [3, 5]
]


def find_blocks(grid):
    global vis_grid
    blocks = []
    number_sorted = 0
    visited.fill(0)
    number_of_cells = (grid > 0).sum()
    if number_of_cells == 0:
        return blocks
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x, y] > 0 and visited[x, y] == 0:
                colour = grid[x, y]
                connected = [[x, y]]
                changed = True
                points_to_search = [[x, y]]
                while changed:
                    number_in_block = len(connected)
                    new_points_to_search = []
                    for element in points_to_search:
                        for move in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                            new_point_x = element[0] + move[0]
                            new_point_y = element[1] + move[1]
                            new_point = [new_point_x, new_point_y]
                            if -1 < new_point_x < 6 and -1 < new_point_y < 12 and visited[new_point_x, new_point_y] == 0 and new_point not in connected:
                                if grid[new_point_x, new_point_y] == colour:
                                    connected.append(new_point)
                                    visited[new_point_x, new_point_y] = 1
                                    new_points_to_search.append(new_point)
                    changed = len(connected) > number_in_block
                    points_to_search = new_points_to_search
                blocks.append(connected)
                if visited.sum() == number_of_cells:
                    return blocks
    return blocks


def place_block(block, rotation, grid, col):
    row = 11 - (grid[col,:] == 0).sum()
    if rotation == 3:
        grid[col, row] = block[1]
        grid[col, row + 1] = block[0]
    else:
        grid[col, row] = block[0]
        col += 1 - rotation
        grid[col, 11 - (grid[col,:] == 0).sum()] = block[1]


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
    # print(grid, file=sys.stderr, flush=True)

    # Maximize score
    score_threshold = SCORE_THRESHOLD_MULTIPLIER * (grid == 0).sum()
    # print(str(score_threshold), file=sys.stderr, flush=True)
    actions = {}
    for rotation, col in (possible_things if blocks[0][0] != blocks[0][1] else possible_things[:11]):
        second_col = col + rotation_dict[rotation]
        for rotation2, col2 in (possible_things if blocks[1][0] != blocks[1][1] else possible_things[:11]):
            # second_col = col + 1 if rotation == 0 else (col - 1 if rotation == 2 else col)
            second_col2 = col2 + rotation_dict[rotation2]
            # Don't go off the top of the grid
            if grid[col, 9] == 0 and grid[second_col, 9] == 0:
                temp_grid = deepcopy(grid)
                score = turn(temp_grid, blocks[0], rotation, col)
                if temp_grid[col2, 9] == 0 and temp_grid[second_col2, 9] == 0:
                    score += turn(temp_grid, blocks[1], rotation2, col2)
                    score += (temp_grid == 0).sum() * FILL_BONUS
                    # print(str(col) + ' ' + str(rotation) + ' ' + str(col2) + ' ' + str(rotation2) + ' ' + str(score), file=sys.stderr, flush=True)
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