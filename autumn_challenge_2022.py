import sys
import math
from copy import deepcopy

import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


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
                if self.grid[fromX, fromY].owner == owner and self.grid[fromX, fromY].robot_count >= number and not self.grid[toX, toY].is_grass():
                    # Find path
                    path = self.get_best_path(fromX, fromY, toX, toY)

                    # Update robots with first move in the path
                    self.grid[fromX, fromY].robot_count -= number
                    self.grid[path[0][0], path[0][1]].robot_count += number

            elif action[0] == 'BUILD':
                x = action[1]
                y = action[2]
                if self.grid[x, y].owner == owner:
                    self.grid[x, y].recycler = True
            elif action[0] == 'SPAWN':
                number = action[1]
                x = action[2]
                y = action[3]
                if grid[x, y].owner == owner and not grid[x, y].recycler:
                    grid[x, y].robot_count += number


width, height = [int(i) for i in input().split()]
grid = Grid(width, height)

# game loop
while True:
    print(grid.grid[0, 0].owner)
    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print("WAIT")
