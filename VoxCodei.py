import sys
import math
from copy import deepcopy
from itertools import permutations
import numpy as np

directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
node_dict = {'@': -1, '.': 0, '#': -2}
# width: width of the firewall grid
# height: height of the firewall grid
width, height = [int(i) for i in input().split()]
grid = np.zeros((width, height), dtype=int)
for i in range(height):
    map_row = input()  # one line of the firewall grid
    for j in range(len(map_row)):
        grid[j, i] = node_dict[map_row[j]]
no_to_destroy = np.count_nonzero(grid == -1)
# game loop


def explode_bomb(grid, x, y, bla):
    grid[x, y] = 0
    destroyed = 0
    nodes_destroyed = []
    for direction in directions:
        new_x = x
        new_y = y
        for i in range(3):
            new_x += direction[0]
            new_y += direction[1]
            if not 0 <= new_x < width or not 0 <= new_y < height or grid[new_x, new_y] == -2:
                break
            elif grid[new_x, new_y] > 0:
                destroyed += explode_bomb(grid, new_x, new_y, False)
            elif grid[new_x, new_y] == -1:
                grid[new_x, new_y] = 0
                if bla:
                    nodes_destroyed.append((new_x, new_y))
                destroyed += 1
    return destroyed if not bla else nodes_destroyed


def do_turn(move, grid):
    no_destroyed = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x, y] > 1:
                grid[x, y] = grid[x, y] - 1
            if grid[x, y] == 1:
                no_destroyed += explode_bomb(grid, x, y, False)
    if move != 'WAIT':
        grid[move[0], move[1]] = 3
    return no_destroyed


def solve_problem(rounds, bombs):
    actions = []
    possible_locations = {}
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x, y] == 0:
                new_grid = deepcopy(grid)
                nodes_destroyed = explode_bomb(new_grid, x, y, True)
                if len(nodes_destroyed) > 0:
                    possible_locations[tuple(nodes_destroyed)] = (x, y)
    print(len(possible_locations.values()), file=sys.stderr, flush=True)
    for bomb_config in permutations(possible_locations.values(), bombs):
        # print(bomb_config, file=sys.stderr, flush=True)
        check_grid = deepcopy(grid)
        total_destroyed = 0
        for location in bomb_config:
            total_destroyed += do_turn(location, check_grid)
            # print(check_grid, file=sys.stderr, flush=True)
        for i in range(2):
            total_destroyed += do_turn('WAIT', check_grid)
            # print(check_grid, file=sys.stderr, flush=True)
        if total_destroyed == no_to_destroy:
            actions = [str(action[0]) + ' ' + str(action[1]) for action in bomb_config] + ['WAIT'] * (rounds - bombs)
            break
    # print(actions, file=sys.stderr, flush=True)
    return actions


initialized = False
while True:
    # rounds: number of rounds left before the end of the game
    # bombs: number of bombs left
    rounds, bombs = [int(i) for i in input().split()]

    if not initialized:
        actions = solve_problem(rounds, bombs)
        initialized = True

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    move = actions.pop(0)
    # move = [1, 1] if rounds == 15 else 'WAIT'
    # do_turn(move, grid)
    # print(grid, file=sys.stderr, flush=True)
    # if move == 'WAIT':
    #     print(move)
    # else:
    #     print(*move)
    print(move)
