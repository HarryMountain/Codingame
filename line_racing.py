import sys
import math
from copy import deepcopy

import numpy as np
import random

MAX_X = 30
MAX_Y = 20

moves = {(0, -1): 'UP', (0, 1): 'DOWN', (-1, 0): 'LEFT', (1, 0): 'RIGHT'}

grid = np.zeros((30, 20), dtype=int)
player_head = np.zeros(2, dtype=int)
neighbours = {}

for x in range(MAX_X):
    for y in range(MAX_Y):
        xy_neighbours = []
        for move in moves.keys():
            new_x = x + move[0]
            new_y = y + move[1]
            if 0 <= new_x < MAX_X and 0 <= new_y < MAX_Y:
                xy_neighbours.append((new_x, new_y))
        neighbours[(x, y)] = xy_neighbours


def flood_fill(grid, n, p, player_order):
    '''
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
    '''
    done = False
    last_visited = {}
    for player in player_order:
        last_visited[player] = [snake_heads[player]]
    index = 0
    while not done:
        done = True
        for player in player_order:
            new_visited = []
            for cell in last_visited[player]:
                for neighbour in neighbours[cell]:
                    if grid[neighbour[0], neighbour[1]] == 0:
                        grid[neighbour[0], neighbour[1]] = player
                        new_visited.append(neighbour)
                        done = False
                        if player == p + 1:
                            index += 1
            last_visited[player] = new_visited
        # print(np.count_nonzero(grid  == 1), np.count_nonzero(grid  == 2), np.count_nonzero(grid  == 0), file=sys.stderr, flush=True)
    print(grid, file=sys.stderr, flush=True)
    score = 0
    no_my_cell = np.count_nonzero(grid == p + 1)
    score += no_my_cell
    score += index * 10
    # score -= 600 - no_my_cell - np.count_nonzero(grid == 0)
    print(score, file=sys.stderr, flush=True)
    return score


snake_heads = {}
initialized = False
while True:
    moves_can_do = []
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    if not initialized:
        # todo : think this is wrong, we need to let other players go first in flood fill
        player_order = list(range(p + 2, n + 1)) + list(range(1, p + 2))
        initialized = True
    # print(p, file=sys.stderr, flush=True)
    for i in range(1, n + 1):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if x1 == -1:
            if i in player_order:
                player_order.remove(i)
                for x in range(MAX_X):
                    for y in range(MAX_Y):
                        if grid[x, y] == i:
                            grid[x, y] = 0
        else:
            snake_heads[i] = (x1, y1)
            grid[x1, y1] = i
            grid[x0, y0] = i

    #print(player_order, file=sys.stderr, flush=True)

    # print(grid, file=sys.stderr, flush=True)
    # print(player_head, file=sys.stderr, flush=True)
    '''
    directions_scores = {0: 'LEFT'}
    for direction, move in moves.items():
        new_position = (player_head[0] + move[0], player_head[1] + move[1])
        if -1 < new_position[0] < MAX_X and -1 < new_position[1] < MAX_Y:
            if grid[new_position[0], new_position[1]] == 0:
                score = flood_fill(grid, new_position)
                directions_scores[score] = direction
    print(directions_scores[max(directions_scores.keys())])
    '''
    my_head = snake_heads[p + 1]
    scores = {}
    # print(grid, file=sys.stderr, flush=True)
    for neighbour in neighbours[my_head]:
        # print('Trying ' + str(neighbour), file=sys.stderr, flush=True)
        if grid[neighbour[0], neighbour[1]] == 0:
            # for neighbour2 in neighbours[neighbour]:
                # if grid[neighbour2[0], neighbour2[1]] == 0:
            snake_heads[p + 1] = neighbour
            new_grid = deepcopy(grid)
            new_grid[neighbour[0], neighbour[1]] = p + 1
            # new_grid[neighbour2[0], neighbour2[1]] = p + 1
            score = flood_fill(new_grid, n, p, player_order)
            scores[score] = neighbour
    # print(scores, file=sys.stderr, flush=True)
    best_score = max(scores.keys())
    new_pos = scores[best_score]
    movement = (new_pos[0] - my_head[0], new_pos[1] - my_head[1])
    print(moves[movement])