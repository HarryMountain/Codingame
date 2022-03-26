import sys
import math
from copy import deepcopy
import numpy as np

SCORE_THRESHOLD_MULTIPLIER = 4
FILL_BONUS = 2
ROTATION_DICT = {0: 1, 1: 0, 2: -1, 3: 0}
ONE_CELL_MOVES = [[1, 0], [0, 1], [-1, 0], [0, -1]]

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


def place_block(block, rotation, grid, col):
    row = 12 - (grid[col, :] == 0).sum()
    if rotation == 3:
        grid[col, row] = block[1]
        grid[col, row + 1] = block[0]
    else:
        grid[col, row] = block[0]
        col += 1 - rotation
        grid[col, 12 - (grid[col, :] == 0).sum()] = block[1]


def merge(grid, cp, prev_grid):
    global vis_grid

    # Find all blocks
    blocks = []
    visited.fill(0)
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x, y] > 0 and visited[x, y] == 0 and grid[x, y] != prev_grid[x, y]:
                colour = grid[x, y]
                connected = [[x, y]]
                changed = True
                points_to_search = [[x, y]]
                while changed:
                    number_in_block = len(connected)
                    new_points_to_search = []
                    for element in points_to_search:
                        for move in ONE_CELL_MOVES:
                            new_point_x = element[0] + move[0]
                            new_point_y = element[1] + move[1]
                            if -1 < new_point_x < 6 and -1 < new_point_y < 12:
                                if grid[new_point_x, new_point_y] == colour:
                                    new_point = [new_point_x, new_point_y]
                                    if new_point not in connected:
                                        connected.append(new_point)
                                        visited[new_point_x, new_point_y] = 1
                                        new_points_to_search.append(new_point)
                    changed = len(connected) > number_in_block
                    points_to_search = new_points_to_search
                if len(connected) >= 2:
                    blocks.append(connected)
    # print(blocks, file=sys.stderr, flush=True)

    b = 0
    gb = 0
    colours = set()
    for block in blocks:
        if len(block) >= 4:
            colours.add(grid[block[0][0], block[0][1]])
            b += len(block)
            gb += 8 if len(block) >= 11 else len(block) - 4
            for point in block:
                grid[point[0], point[1]] = 0
                # Delete skull blocks
                for move in ONE_CELL_MOVES:
                    new_point = [point[0] + move[0], point[1] + move[1]]
                    if -1 < new_point[0] < 6 and -1 < new_point[1] < 12:
                        if grid[new_point[0], new_point[1]] == -1:
                            grid[point[0], point[1]] = 0

    # Drop blocks into gaps
    for x in range(len(grid)):
        y_new_index = 0
        for y in range(len(grid[x])):
            if grid[x, y] != 0:
                colour = grid[x, y]
                grid[x, y] = 0
                grid[x, y_new_index] = colour
                y_new_index += 1

    # score calculation
    cb = 0 if len(colours) == 1 else 2 ** (len(colours) - 1)
    score = (10 * b) * max(1, min(999, (cp + cb + gb)))
    block_score = len(blocks) * 5
    return score, block_score


def turn(grid, block, rotation, col):
    prev_grid = deepcopy(grid)
    place_block(block, rotation, grid, col)
    score = 0
    block_score = 0
    cp = 0
    step_score = 1
    while step_score > 0:
        step_score, block_score = merge(grid, cp, prev_grid)
        if step_score > 0:
            prev_grid = deepcopy(grid)
            score += step_score
            cp = 8 if cp == 0 else cp * 2
    return score + block_score, cp


# game loop
while True:
    # print(grid, file=sys.stderr, flush=True)
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
    merge_actions = {}
    other_actions = {}
    for rotation, col in (possible_things if blocks[0][0] != blocks[0][1] else possible_things[:11]):
        second_col = col + ROTATION_DICT[rotation]
        # Don't go off the top of the grid
        if grid[col, 10] == 0 and grid[second_col, 10] == 0:
            temp_grid = deepcopy(grid)
            score, cp = turn(temp_grid, blocks[0], rotation, col)

            for rotation2, col2 in (possible_things if blocks[1][0] != blocks[1][1] else possible_things[:11]):
                second_col2 = col2 + ROTATION_DICT[rotation2]
                if temp_grid[col2, 10] == 0 and temp_grid[second_col2, 10] == 0:
                    temp_grid2 = deepcopy(temp_grid)
                    score2, cp2 = turn(temp_grid2, blocks[1], rotation2, col2)
                    score2 += score
                    cp2 += cp
                    score2 += (temp_grid == 0).sum() * FILL_BONUS
                    # print(str(col) + ' ' + str(rotation) + ' ' + str(col2) + ' ' + str(rotation2) + ' ' + str(score), file=sys.stderr, flush=True)
                    if cp2 > 0:
                        merge_actions[score2] = [col, rotation]
                    else:
                        other_actions[score2] = [col, rotation]

    # print(merge_actions, file=sys.stderr, flush=True)
    # print(other_actions, file=sys.stderr, flush=True)

    action = None
    if len(merge_actions) > 0:
        best_merge = max(merge_actions.keys())
        if best_merge > score_threshold:
            action = merge_actions[best_merge]
    if action is None:
        action = other_actions[max(other_actions.keys())]
    # "x": the column in which to drop your blocks
    print(' '.join([str(x) for x in action]))
