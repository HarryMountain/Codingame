import sys
import math
from copy import deepcopy

import numpy as np

grid = np.zeros((6, 12), dtype=int)


def find_blocks(grid):
    blocks = []
    number_sorted = 0
    visited = []
    number_of_cells = (grid > 0).sum()
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x, y] != 0 and [x, y] not in visited:
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
    for x in range(len(grid)):
        lowest_free = -1
        for y in range(len(grid[x])):
            if lowest_free > -1:
                if grid[x, y] != 0:
                    grid[x, lowest_free] = grid[x, y]
                    grid[x, y] = 0
            else:
                if grid[x, y] == 0:
                    lowest_free = y
    # score calculation
    cb = 0 if len(colours) == 1 else 2**(len(colours) - 1)
    score = (10 * b) * min((cp + cb + gb), 999)
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
    action = []
    max_score = -1
    for col in range(6):
        for rotation in range(4):
            if not ((col == 0 and rotation == 2) or (col == 5 and rotation == 0)):
                score = turn(deepcopy(grid), blocks[0], rotation, col)
                print(str(col) + ' ' + str(rotation) + ' ' + str(score), file=sys.stderr, flush=True)
                if score > max_score:
                    max_score = score
                    action = [col, rotation]


    print(action, file=sys.stderr, flush=True)
    # "x": the column in which to drop your blocks
    print(' '.join([str(x) for x in action]))


"""
place_block([3, 2], 0, grid, 3)
place_block([3, 2], 0, grid, 4)
place_block([3, 3], 0, grid, 3)
place_block([4, 4], 0, grid, 3)
print(grid)
#print(find_blocks(grid))
merge(grid)
refill(grid)
print(grid)
"""