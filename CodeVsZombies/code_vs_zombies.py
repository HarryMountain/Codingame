import time
import pickle
import random
import sys
import math

import numpy as np

FIBBONACCI_SEQUENCE = [1, 2]

for i in range(100):
    FIBBONACCI_SEQUENCE.append(FIBBONACCI_SEQUENCE[-2] + FIBBONACCI_SEQUENCE[-1])


def get_distance(vector):
    # return round(vector.dot(vector))
    return vector[0]**2 + vector[1]**2


def remove_array(my_list, item_to_remove):
    for i in range(len(my_list)):
        if item_to_remove[0] == my_list[i][0] and item_to_remove[1] == my_list[i][1]:
            my_list.pop(i)
            break


# Zombie data is [
#     0 : Position
#     1 : Target
#     2 : TargetIsAsh
#     3 : ZombieMoveVector
#     4 : DistanceToTarget
#     5 : Id
#     6 : CountToCheckAsh
#     7 : DistanceToAsh
class GameState:
    def __init__(self, ash_pos, zombies, humans):
        self.ash_pos = ash_pos

        self.zombies = []
        for i in range(len(zombies)):
            self.zombies.append([zombies[i], None, False, None, -1, i, 0, get_distance(ash_pos - zombies[i])])
        self.humans = humans
        self.live_humans = len(humans)
        self.live_zombies = len(zombies)
        self.set_zombie_targets()

    def set_zombie_targets(self):
        for zombie in self.zombies:
            if zombie is not None:
                # Possibilities are
                # No target set - choose target from all humans and Ash
                # On target for a human but need ro recheck whether to target Ash
                # Targeting Ash - check whether there is a closer human to target

                target_ash = zombie[2]
                target_human = zombie[1] is not None and not target_ash
                recalc_move_vector = False

                if not target_ash and zombie[6] > 0:
                    # Don't need to check anything else
                    zombie[6] -= 1
                else:
                    ash_distance = zombie[7]
                    if target_human:
                        # Check if Ash is closer
                        # print('Ash distance : ' + str(ash_distance), file=sys.stderr, flush=True)
                        if ash_distance < zombie[4]:
                            zombie[1] = self.ash_pos
                            zombie[2] = True
                            zombie[4] = ash_distance
                            recalc_move_vector = True
                        else:
                            zombie[6] = ash_distance // 1400
                            # print("Hi", ash_distance, zombie[6])
                    else:
                        # Scan through all possible targets including Ash
                        best_human_dist = ash_distance
                        best_human = None
                        for human in self.humans:
                            distance = get_distance(zombie[0] - human)
                            if distance < best_human_dist:
                                best_human = human
                                best_human_dist = distance
                        if best_human is not None:
                            # Switch Zombie to target this human
                            zombie[1] = best_human
                            zombie[2] = False
                            # print('Best human distance: ' + str(best_human_dist), file=sys.stderr, flush=True)
                            zombie[4] = round(math.sqrt(best_human_dist))
                            # print('Set zombie distance : ' + str(zombie[4]), file=sys.stderr, flush=True)
                        else:
                            # Switch Zombie to target Ash
                            zombie[1] = self.ash_pos
                            zombie[2] = True
                            zombie[4] = ash_distance
                        zombie[6] = ash_distance // 1400
                        # print("Hello", ash_distance, zombie[6])
                        recalc_move_vector = True

                    # Set move vector if needed
                    if recalc_move_vector:
                        if zombie[4] > 0:
                            zombie[3] = np.array(
                                ((zombie[1][0] - zombie[0][0]) * 400 / zombie[4],
                                 (zombie[1][1] - zombie[0][1]) * 400 / zombie[4]),
                                dtype=int)
                        else:
                            zombie[3] = np.array((0, 0), dtype=int)

    def move_zombies(self):
        self.set_zombie_targets()
        for zombie in self.zombies:
            if zombie is not None:
                zombie[0] = np.add(zombie[0], zombie[3])
                zombie[4] -= 400

    def update(self, move):
        # print(self.ash_pos, file=sys.stderr, flush=True)
        self.move_zombies()
        self.ash_pos[0] = min(16000, max(0, self.ash_pos[0] + move[0]))
        self.ash_pos[1] = min(9000, max(0, self.ash_pos[1] + move[1]))
        #print(self.ash_pos)
        score = 0
        humans_alive_score = (self.live_humans ** 2) * 10
        # current_num_zombies = len(self.zombies)
        zombies_killed = 0
        for i in range(len(self.zombies)):
            if self.zombies[i] is not None:
                ash_distance = get_distance(self.ash_pos - self.zombies[i][0])
                self.zombies[i][7] = ash_distance
                if ash_distance < 4000000:
                    self.zombies[i] = None
                    zombies_killed += 1
                    self.live_zombies -= 1
        #self.zombies[:] = (x for x in self.zombies if get_distance(self.ash_pos - x[0]) > 4000000)
        #zombies_killed = current_num_zombies - len(self.zombies)
        score += humans_alive_score * sum(FIBBONACCI_SEQUENCE[:zombies_killed])

        for zombie in filter(None, self.zombies):
            if not zombie[2] and zombie[4] < 400 and zombie[1] is not None:
                # if zombie[1] is None:
                    # print('Zombie killing human ' + str(zombie[1]), file=sys.stderr, flush=True)
                zombie[0] = zombie[1]
                remove_array(self.humans, zombie[1])
                self.live_humans -= 1

                # print('Zombie[1] pre ' + str(zombie[0]) + str(zombie[1]), file=sys.stderr, flush=True)
                zombie[1] = None
                zombie[2] = False
                zombie[4] = -1
                # print('Zombie[1] after ' + str(zombie[0]) + str(zombie[1]), file=sys.stderr, flush=True)
                # print('HUMAN DEAD', file=sys.stderr, flush=True)
        return score


def score_moves(game_state_pkl, moves):
    state = pickle.loads(game_state_pkl)
    score = 0

    #print(state.zombies)
    for move in moves:
        score += state.update(move)
        if state.live_humans == 0:
            score = 0
            break
        if state.live_zombies == 0:
            break
    return score


GENE_LENGTH = 20
POPULATION_SIZE = 20


def create_population(steps):
    population = []
    for x_step in range(-1000, 1001, 250):
        for y_step in range(-1000, 1001, 250):
            moves = []
            for i in range(GENE_LENGTH):
                moves.append(np.array((x_step, y_step)))
            population.append(moves)
    if steps is not None:
        # Add existing steps to the population
        moves = []
        for i in range(1, GENE_LENGTH):
            moves.append(np.array([max(-1000, min(1000, steps[i][k] + random.randint(-50, 50))) for k in range(2)]))
        moves.append(np.array((random.randint(-1000, 1000), random.randint(-1000, 1000))))
        population.append(moves)

    return population


def genetic_algorithm(steps, game_state, max_time_seconds):
    # Store original settings
    game_state_pkl = pickle.dumps(game_state)

    # Record start time
    start_time = time.time()

    population = create_population(steps)
    scored_population = []
    for moves in population:
        scored_population.append([moves, score_moves(game_state_pkl, moves)])
    scored_population.sort(key=lambda x: x[1], reverse=True)
    scored_population = scored_population[:POPULATION_SIZE + 1]
    #print(scored_population, file=sys.stderr, flush=True)
    # print([x[1] for x in scored_population], file=sys.stderr, flush=True)
    # print('Best score : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
    generation = 0
    average_generation_time = 0
    while max_time_seconds - time.time() + start_time > 2 * average_generation_time: # todo comment out line below for speed test
    #while generation < 20: # todo
        for j in range(2, POPULATION_SIZE):
            parents = random.sample([l[0] for l in scored_population[:j]], 2)
            child_moves_breed = []
            child_moves_splice = []
            splice_point = random.randint(0, GENE_LENGTH)
            for move in range(GENE_LENGTH):
                factor = 1.2 * random.random() - 0.1
                new_move = np.array((min(1000, max(-1000, parents[0][move][0] * factor + parents[1][move][0] * (1 - factor) + random.randint(-50, 50))),
                                     min(1000, max(-1000, parents[0][move][0] * factor + parents[1][move][0] * (1 - factor) + random.randint(-50, 50)))), dtype=int)
                child_moves_breed.append(new_move)
                if move < splice_point:
                    child_moves_splice.append(np.array((parents[0][move][0], parents[0][move][1])))
                else:
                    child_moves_splice.append(np.array((parents[1][move][0], parents[1][move][1])))
            scored_population.append([child_moves_breed, score_moves(game_state_pkl, child_moves_breed)])
            scored_population.append([child_moves_splice, score_moves(game_state_pkl, child_moves_splice)])
        scored_population.sort(key=lambda x: x[1], reverse=True)
        scored_population = scored_population[:POPULATION_SIZE + 1]
        #print(scored_population[0][1], scored_population[0][0], file=sys.stderr, flush=True)
        #print('Best score generation : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
        generation += 1
        average_generation_time = (time.time() - start_time) / generation
        # print([x[1] for x in scored_population], file=sys.stderr, flush=True)
        # print(generation, average_generation_time, time.time() - start_time, file=sys.stderr, flush=True)

    #print('Final best score : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
    #print('Steps : ' + str(scored_population[0][0]), file=sys.stderr, flush=True)
    return scored_population[0][0]

first_go = True
last_time = None
start_time = None
initialized = False
if __name__ == "__main__":
    # game loop
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
        # print(ash_position, file=sys.stderr, flush=True)
        # print(zombie_positions, file=sys.stderr, flush=True)
        # print(human_positions, file=sys.stderr, flush=True)
        state = GameState(ash_position, zombie_positions, human_positions)
        steps = genetic_algorithm(steps, state, 0.09 if initialized else 0.99)
        initialized = True
        # print("Steps : " + str(steps), file=sys.stderr, flush=True)
        move = steps[0]
        #score = state.update(move)
        #if score > 0:
        #    steps = None
        #if len(state.zombies) > 0:
            #print(state.zombies[0], file=sys.stderr, flush=True)
        #print("Steps : " + str(steps), file=sys.stderr, flush=True)
        #print('Score : ' + str(score), file=sys.stderr, flush=True)


        '''
        if first_go:
            while True:
                ms = time.time() * 1000.0
                if start_time is None:
                    start_time = ms
                    last_time = ms
                elif ms - last_time > 10:
                    print(ms - start_time, file=sys.stderr, flush=True)
                    last_time = ms
        first_go = False
        '''

        print(min(16000, max(0, ash_x + move[0])), min(9000, max(0, ash_y + move[1])))
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
