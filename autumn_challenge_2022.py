import sys
import math
from copy import deepcopy

import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

SCRAP_WEIGHT = 1
ROBOT_WEIGHT = 1
RECYLER_MATERIAL_WEIGHT = 0.25

class Cell:
    def __init__(self):
        self.scrap = 0
        self.owner = -1
        self.robot_count = 0
        self.recycler = False

    def update(self, scrap, who_owns_it, no_of_robots, has_recycler):
        self.scrap = scrap
        self.owner = who_owns_it
        self.robot_count = no_of_robots
        self.recycler = has_recycler

    def is_grass(self):
        return self.scrap == 0

    def score(self, owner):
        score = self.scrap * SCRAP_WEIGHT
        score += self.robot_count * ROBOT_WEIGHT * (1 if owner == self.owner else -1)


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.full((width, height), Cell(), dtype=Cell)
        '''
        for x in range(width):
            for y in range(height):
                self.grid[x, y]
        '''

    def get_best_path(self, fromX, fromY, toX, toY):
        paths = [[fromX, fromY]]
        while True:
            new_paths = []
            for path in paths:
                for step in [0, 1], [1, 0], [0, -1], [-1, 0]:
                    path_head = path[-1]
                    new_path_head = [path_head[0] + step[0], path_head[1] + step[1]]
                    if new_path_head not in path and (0 <= new_path_head[0] < width) and (0 <= new_path_head[1] < height) and not self.grid[new_path_head[0], new_path_head[1]].is_grass():
                        new_path = deepcopy(path)
                        new_path.append(new_path_head)
                        if new_path_head[0] == toX and new_path_head[1] == toY:
                            return new_path
                        new_paths.append(new_path)
            paths = new_paths
            if len(paths) == 0:
                return None

    def perform_actions(self, owner, actions):
        for action in actions:
            if action[0] == 'MOVE':
                number = action[1]
                fromX, fromY = action[2], action[3]
                toX, toY = action[4], action[5]
                if abs(toX - fromX) + abs(toY - fromY) != 1:
                    raise Exception("Bad MOVE action")
                if self.grid[fromX, fromY].owner == owner and self.grid[fromX, fromY].robot_count >= number and not self.grid[toX, toY].is_grass():
                    # Update robots with first move in the path
                    self.grid[fromX, fromY].robot_count -= number
                    if self.grid[toX, toY].owner == 0:
                        # Robots fight
                        their_robots = self.grid[toX, toY].robot_count
                        self.grid[toX, toY].robot_count = abs(their_robots - number)
                        if number > their_robots:
                            self.grid[toX, toY].owner = 1
                    else:
                        self.grid[toX, toY].owner = 1
                        self.grid[toX, toY].robot_count += number
                '''
                number = action[1]
                fromX, fromY = action[2], action[3]
                toX, toY = action[4], action[5]
                if self.grid[fromX, fromY].owner == owner and self.grid[fromX, fromY].robot_count >= number and not self.grid[toX, toY].is_grass():
                    # Find path
                    path = self.get_best_path(fromX, fromY, toX, toY)

                    # Update robots with first move in the path
                    self.grid[fromX, fromY].robot_count -= number
                    self.grid[path[0][0], path[0][1]].robot_count += number
                '''

            elif action[0] == 'BUILD':
                x = action[1]
                y = action[2]
                if self.grid[x, y].owner == owner and self.grid[x, y].robot_count == 0:
                    self.grid[x, y].recycler = True
            elif action[0] == 'SPAWN':
                number = action[1]
                x = action[2]
                y = action[3]
                if grid[x, y].owner == owner and not grid[x, y].recycler:
                    grid[x, y].robot_count += number

    def score(self, owner):
        score = 0
        for x in range(width):
            for y in range(height):
                cell = self.grid[x, y]
                if cell.owner == owner:
                    if cell.recycler:
                        # Score based on amount of matter around the cell
                        material = 0
                        for xx in range(max(0, x - 1), min(width, x + 2)):
                            for yy in range(max(0, y - 1), min(heighth, y + 2)):
                                material += self.grid[xx, yy].scrap
                        score = material * RECYLER_MATERIAL_WEIGHT
                    else:
                        score += cell.score(owner)
                else:
                    closest_robot_distance = None
                    for xx in range(width):
                        for yy in range(height):
                            if self.grid[xx, yy].owner == owner and self.grid[xx, yy].robot_count > 0:
                                distance = abs(x - xx) + abs(y - yy)
                                if closest_robot_distance is None or distance < closest_robot_distance:
                                    closest_robot_distance = distance
                    score += cell.score(owner) * max(0, 1 - 0.1 * closest_robot_distance)
        return score


width, height = [int(i) for i in input().split()]
grid = Grid(width, height)

# game loop
while True:
    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            grid.grid[j, i].scrap = scrap_amount
            grid.grid[j, i].owner = owner
            grid.grid[j, i].robot_count = units
            grid.grid[j, i].recycler = True if recycler == 1 else False
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    current_score = grid.score(1)

    # List possible moves
    possible_moves = []
    for x in range(width):
        for y in range(height):
            if grid.grid[x, y].owner == 1:
                number_of_robots = grid.grid[x, y].robot_count
                if number_of_robots > 0:
                    for direction in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                        new_x, new_y = [x, y] + direction
                        if grid.grid[new_x, new_y].scrap > 0:
                            possible_moves.append(['MOVE', 1, x, y, new_x, new_y])


    # Score each move
    move_scores = []
    for move in possible_moves:
        test_grid = deepcopy(grid)
        test_grid.perform_actions(1, move)
        move_scores.append(test_grid.score(1))

    # Output best action
    max_score = max(move_scores)
    if max_score < current_score:
        print("WAIT")

    print(*possible_moves[move_scores.index(max_score)])

