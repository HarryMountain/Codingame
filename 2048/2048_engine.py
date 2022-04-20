import sys
import math
import random
from copy import deepcopy

SIZE = 4
TARGET_START_DIR = {"U": 0, "R": SIZE - 1, "D": SIZE * (SIZE - 1), "L": 0}
TARGET_STEP_DIR = {"U": 1, "R": SIZE, "D": 1, "L": SIZE}
SOURCE_STEP_DIR = {"U": SIZE, "R": -1, "D": -SIZE, "L": 1}


def update_seed(seed):
    return seed ** 2 % 50515093


def spawn_tile(grid, seed):
    # print(grid, file=sys.stderr, flush=True)
    free_cells = []
    for x in range(SIZE):
        for y in range(SIZE):
            if grid[x][y] == 0:
                free_cells.append(x + y * SIZE)
    spawn_index = free_cells[seed % len(free_cells)]
    value = 2 if seed & 0x10 == 0 else 4

    grid[spawn_index % SIZE][spawn_index // SIZE] = value


def apply_move(grid, direction):
    turn_score = 0
    merged = [[False for i in range(SIZE)] for j in range(SIZE)]
    target_start = TARGET_START_DIR[direction]
    target_step = TARGET_STEP_DIR[direction]
    source_step = SOURCE_STEP_DIR[direction]

    for i in range(SIZE):
        final_target = target_start + i * target_step
        for j in range(1, SIZE):
            source = final_target + j * source_step
            source_x = source % SIZE
            source_y = source // SIZE
            if grid[source_x][source_y] == 0:
                continue
            for k in range(j - 1, -1, -1):
                intermediate = final_target + k * source_step

                intermediate_x = intermediate % SIZE
                intermediate_y = intermediate // SIZE

                if grid[intermediate_x][intermediate_y] == 0:
                    grid[intermediate_x][intermediate_y] = grid[source_x][source_y]
                    grid[source_x][source_y] = 0
                    source = intermediate
                    source_x = source % SIZE
                    source_y = source // SIZE
                else:
                    if not merged[intermediate_x][intermediate_y] and grid[intermediate_x][intermediate_y] == \
                            grid[source_x][source_y]:
                        grid[source_x][source_y] = 0
                        grid[intermediate_x][intermediate_y] *= 2
                        merged[intermediate_x][intermediate_y] = True
                        turn_score += grid[intermediate_x][intermediate_y]
                    break
    return turn_score


def can_move(grid):
    for direction in 'URDL':
        new_grid = deepcopy(grid)
        apply_move(new_grid, direction)
        for x in range(SIZE):
            for y in range(SIZE):
                if grid[x][y] != new_grid[x][y]:
                    return True
    return False


def game_turn(grid, direction, seed):
    old_grid = deepcopy(grid)
    turn_score = apply_move(grid, direction)
    changed = False
    for x in range(SIZE):
        for y in range(SIZE):
            if grid[x][y] != old_grid[x][y]:
                changed = True
                break
    if changed:
        spawn_tile(grid, seed)
    # if not changed:
    #    return -1
    # if not can_move(grid):
    return turn_score if changed else -1


def determine_next_move(grid, seed):
    next_move_dict = [{}, {}, {}]
    for direction1 in 'URDL':
        for direction2 in 'URDL':
            for direction3 in 'URDL':
                directions = [direction1, direction2, direction3]
                new_grid = deepcopy(grid)
                total_score = 0
                for i in range(len(directions)):
                    direction = directions[i]
                    potential_score = game_turn(new_grid, direction, seed)
                    if potential_score == -1:
                        total_score = -1
                        break
                    else:
                        total_score += potential_score
                    if total_score != -1:
                        all_scores = new_grid[0] + new_grid[1] + new_grid[2] + new_grid[3]
                        all_scores_sorted = sorted(all_scores, reverse=True)
                        # print(all_scores, file=sys.stderr, flush=True)
                        total_score += sum([-abs(all_scores_sorted[i] - all_scores[i]) for i in range(len(all_scores))])
                        # if new_grid[0][0] == all_scores_sorted[0]:
                        #    total_score += 5000
                        total_score += all_scores_sorted[0] * all_scores.count(0) // 4
                        # if new_grid[0][1] == all_scores[1] or new_grid[1][0] == all_scores[1]:
                        #     total_score += all_scores[1] // 4
                        next_move_dict[i][total_score] = directions[0]
    print(next_move_dict, file=sys.stderr, flush=True)
    for i in range(len(next_move_dict) - 1, -1, -1):
        if len(next_move_dict[i]) > 0:
            return next_move_dict[i][max(next_move_dict[i].keys())] if len(next_move_dict[i].keys()) != 0 else ''
    return ''


# game loop
while True:
    seed = int(input())  # needed to predict the next spawns
    score = int(input())
    grid = [[], [], [], []]
    for i in range(4):
        index = 0
        for j in input().split():
            cell = int(j)
            grid[index].append(cell)
            index += 1

    actions = []
    actions.append(determine_next_move(grid, seed))
    print(actions, file=sys.stderr, flush=True)
    if actions[0] != '':
        game_turn(grid, actions[0], seed)
        seed = update_seed(seed)
        actions.append(determine_next_move(grid, seed))
    print(actions, file=sys.stderr, flush=True)
    print(''.join(actions))
