import random
import sys
import math
from copy import deepcopy

import numpy as np
# Save humans, destroy zombies!

# game loop
FIBBONACCI_SEQUENCE = [1, 2]

for i in range(100):
    FIBBONACCI_SEQUENCE.append(FIBBONACCI_SEQUENCE[-2] + FIBBONACCI_SEQUENCE[-1])


def get_distance(pos_1, pos_2):
    vector = pos_1 - pos_2
    return round(math.sqrt(vector.dot(vector)))


def remove_array(my_list, item_to_remove):
    for i in range(len(my_list)):
        if np.all(item_to_remove == my_list[i]):
            my_list.pop(i)
            break


class GameState:
    def __init__(self, ash_pos, zombies, humans):
        self.ash_pos = ash_pos
        self.zombies = zombies
        self.humans = humans
        self.zombie_targets = []

    def move_zombies(self):
        self.zombie_targets = []
        zombie_moves = []
        for zombie in self.zombies:
            best_human = -1
            best_human_dist = -1
            for human in self.humans + [self.ash_pos]:
                distance = math.sqrt((zombie[0] - human[0]) ** 2 + (zombie[1] - human[1]) ** 2)
                if distance < best_human_dist or best_human_dist == -1:
                    best_human = human
                    best_human_dist = distance
            self.zombie_targets.append(best_human)
            # total_dist_to_human = math.sqrt((zombie[0] - best_human[0]) ** 2 + (zombie[1] - best_human[1]) ** 2)
            total_dist_to_human = get_distance(zombie, best_human)
            zombie_moves.append(np.array(((best_human[0] - zombie[0]) * 400 / total_dist_to_human,
                                    (best_human[1] - zombie[1]) * 400 / total_dist_to_human)))
        for i in range(len(self.zombies)):
            zombie = self.zombies[i]
            move = zombie_moves[i]
            self.zombies[i] = np.array(zombie + move, dtype=int)

    def update(self, move):
        # print(self.ash_pos, file=sys.stderr, flush=True)
        self.move_zombies()
        self.ash_pos = np.array([min(16000, max(0, self.ash_pos[0] + move[0])), min(9000, max(0, self.ash_pos[1] + move[1]))])
        zombies_killed = []
        score = 0
        humans_alive_score = (len(self.humans) ** 2) * 10
        for i in range(len(self.zombies)):
            zombie = self.zombies[i]
            if get_distance(self.ash_pos, zombie) <= 2000:
                zombies_killed.append(zombie)
            elif get_distance(zombie, self.zombie_targets[i]) < 400:
                # print(self.zombies, self.zombie_targets, i, self.humans, file=sys.stderr, flush=True)
                self.zombies[i] = self.zombie_targets[i]
                remove_array(self.humans, self.zombie_targets[i])
                #self.humans.remove(self.zombie_targets[i])
        for i in range(len(zombies_killed)):
            remove_array(self.zombies, zombies_killed[i])
            #self.zombies.remove(zombies_killed[i])
            score += humans_alive_score * FIBBONACCI_SEQUENCE[i]
        return score


def score_moves(game_state, moves):
    score = 0
    state = deepcopy(game_state)
    for move in moves:
        score += state.update(move)
    return score


GENE_LENGTH = 20
POPULATION_SIZE = 10
GENERATIONS = 10
POWER_FLOOR = 10


def create_population(steps):
    population = []
    if steps is not None:
        for j in range(POPULATION_SIZE):
            moves = []
            for i in range(1, GENE_LENGTH):
                moves.append(np.array([max(-1000, min(1000, steps[i][k] + random.randint(-50, 50))) for k in range(2)]))
            moves.append(np.array((random.randint(-1000, 1000), random.randint(-1000, 1000))))
            population.append(moves)
    else:
        for x_step in range(-1000, 1001, 250):
            for y_step in range(-1000, 1001, 250):
                moves = []
                for i in range(GENE_LENGTH):
                    moves.append(np.array((x_step, y_step)))
                population.append(moves)

    return population


def genetic_algorithm(steps, game_state):
    population = create_population(steps)
    scored_population = []
    for moves in population:
        scored_population.append([moves, score_moves(game_state, moves)])
    scored_population.sort(key=lambda x: x[1], reverse=True)
    scored_population = scored_population[:POPULATION_SIZE + 1]
    # print(scored_population, file=sys.stderr, flush=True)
    # print('Best score : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
    for i in range(GENERATIONS):
        for j in range(2, POPULATION_SIZE):
            parents = random.sample([l[0] for l in scored_population[:j]], 2)
            new_moves = []
            for move in range(GENE_LENGTH):
                factor = 1.2 * random.random() - 0.1
                new_move = np.array(
                    [min(1000, max(-1000, parents[0][move][k] * factor + parents[1][move][k] * (1 - factor) + random.randint(-50, 50))) for k in
                     range(2)], dtype=int)
                new_moves.append(new_move)
            scored_population.append([new_moves, score_moves(game_state, new_moves)])
        scored_population.sort(key=lambda x: x[1], reverse=True)
        scored_population = scored_population[:POPULATION_SIZE + 1]
        # print(scored_population[0][1], scored_population[0][0], file=sys.stderr, flush=True)
        # print('Best score generation : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)

    print('Final best score : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
    print('Steps : ' + str(scored_population[0][0]), file=sys.stderr, flush=True)
    return scored_population[0][0]


if __name__ == "__main__":
    steps = None
    while True:
        humans = []
        zombies = []
        human_positions = []
        zombie_positions = []
        ash_x, ash_y = [int(i) for i in input().split()]
        ash_position = np.array((ash_x, ash_y))
        human_count = int(input())
        for i in range(human_count):
            human_id, human_x, human_y = [int(j) for j in input().split()]
            humans.append([human_id, human_x, human_y])
            human_positions.append(np.array((human_x, human_y)))
        zombie_count = int(input())
        for i in range(zombie_count):
            zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
            zombies.append([zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext])
            zombie_positions.append(np.array((zombie_x, zombie_y)))
        print(zombie_positions[0], file=sys.stderr, flush=True)
        # Write an action using print
        '''
        # Simple start - go for the closest Zombie
        closest_distance = -1
        target = None
        for zombie_position in zombie_positions:
            distance = get_distance(ash_position, zombie_position)
            if closest_distance < 0 or distance < closest_distance:
                target = zombie_position
    
        move = np.array((target - ash_position) * min(1000 / get_distance(ash_position, target), 1), dtype=int)
        '''
        state = GameState(ash_position, zombie_positions, human_positions)
        steps = genetic_algorithm(steps, state)
        move = steps[0]
        score = state.update(move)
        if len(state.zombies) > 0:
            print(state.zombies[0], file=sys.stderr, flush=True)
        print('Score : ' + str(score), file=sys.stderr, flush=True)

        print(min(16000, max(0, ash_x + move[0])), min(9000, max(0, ash_y + move[1])))
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
