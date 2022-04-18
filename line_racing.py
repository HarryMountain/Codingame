import sys
import math
import numpy as np
import random

MAX_X = 30
MAX_Y = 20

moves = {'UP': [0, -1], 'DOWN': [0, 1], 'LEFT': [-1, 0], 'RIGHT': [1, 0]}

grid = np.zeros((30, 20), dtype=int)
player_head = np.zeros(2, dtype=int)


def flood_fill(grid, head):
    positions = [head]
    positions_been_to = {head}
    while len(positions) > 0:
        new_positions = set()
        for position in positions:
            for move in moves.values():
                new_position = (position[0] + move[0], position[1] + move[1])
                if -1 < new_position[0] < MAX_X and -1 < new_position[1] < MAX_Y:
                    if grid[new_position[0], new_position[1]] == 0 and new_position not in positions_been_to:
                        new_positions.add(new_position)
        positions = new_positions
        positions_been_to.update(new_positions)
    return len(positions_been_to)


while True:
    moves_can_do = []
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    for i in range(n):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if i == p:
            player_head = [x1, y1]
        grid[x1, y1] = i + 1
        grid[x0, y0] = i + 1

    print(grid, file=sys.stderr, flush=True)
    # print(player_head, file=sys.stderr, flush=True)
    directions_scores = {0: 'LEFT'}
    for direction, move in moves.items():
        new_position = (player_head[0] + move[0], player_head[1] + move[1])
        if -1 < new_position[0] < MAX_X and -1 < new_position[1] < MAX_Y:
            if grid[new_position[0], new_position[1]] == 0:
                score = flood_fill(grid, new_position)
                directions_scores[score] = direction
    print(directions_scores[max(directions_scores.keys())])
