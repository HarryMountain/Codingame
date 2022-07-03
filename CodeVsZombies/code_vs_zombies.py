import time
import pickle
import random
import sys
import math

import numpy as np

TARGET_NONE = -2
TARGET_ASH = -1

FIBBONACCI_SEQUENCE = [1, 2]

for i in range(100):
    FIBBONACCI_SEQUENCE.append(FIBBONACCI_SEQUENCE[-2] + FIBBONACCI_SEQUENCE[-1])


def get_distance(thing1, thing2):
    # return round(vector.dot(vector))
    return (thing1.x - thing2.x)**2 + (thing1.y - thing2.y)**2


class Zombie:
    def __init__(self, id, zombie):
        self.id = id
        self.is_alive = True
        self.x = zombie[0]
        self.y = zombie[1]
        # self.has_target = False
        self.target_x = None
        self.target_y = None
        # self.target_ash = False
        self.move_x = None
        self.move_y = None
        self.count_to_ash = 0
        self.distance_to_ash = -1
        self.distance_to_target = -1
        self.target_id = TARGET_NONE


class Human:
    def __init__(self, human, id):
        self.id = id
        self.x = human[0]
        self.y = human[1]
        self.is_alive = True


class GameState:
    def __init__(self, ash_pos, zombies, humans):
        self.ash = Human(ash_pos, TARGET_ASH)
        self.zombies = []
        for i in range(len(zombies)):
            # self.zombies.append([zombies[i], None, False, None, -1, i, 0, get_distance(ash_pos - zombies[i])])
            self.zombies.append(Zombie(i, zombies[i]))
            self.zombies[-1].distance_to_ash = get_distance(self.zombies[-1], self.ash)
        self.humans = []
        for i in range(len(humans)):
            human = humans[i]
            self.humans.append(Human(human, i))
        self.live_humans = len(humans)
        print(self.live_humans, file=sys.stderr, flush=True)
        self.live_zombies = len(zombies)
        self.set_zombie_targets()

    def set_zombie_targets(self):
        for zombie in self.zombies:
            if zombie.is_alive:
                # Possibilities are
                # No target set - choose target from all humans and Ash
                # On target for a human but need ro recheck whether to target Ash
                # Targeting Ash - check whether there is a closer human to target

                target_ash = zombie.target_id == TARGET_ASH
                target_human = zombie.target_id > -1
                recalc_move_vector = False

                if not target_ash and zombie.count_to_ash > 0:
                    # Don't need to check anything else
                    zombie.count_to_ash -= 1
                else:
                    ash_distance = zombie.distance_to_ash
                    if target_human:
                        # Check if Ash is closer
                        # print('Ash distance : ' + str(ash_distance), file=sys.stderr, flush=True)
                        if ash_distance < zombie.distance_to_target:
                            zombie.target_id = TARGET_ASH
                            zombie.target_x = self.ash.x
                            zombie.target_y = self.ash.y
                            zombie.distance_to_target = ash_distance
                            recalc_move_vector = True
                        else:
                            zombie.count_to_ash = ash_distance // 1400
                            # print("Hi", ash_distance, zombie[6])
                    else:
                        # Scan through all possible targets including Ash
                        best_human_dist = ash_distance
                        best_human = None
                        for human in self.humans:
                            distance = get_distance(zombie, human)
                            if distance < best_human_dist:
                                best_human = human
                                best_human_dist = distance
                        if best_human is not None:
                            # Switch Zombie to target this human
                            zombie.target_id = best_human.id
                            zombie.target_x = best_human.x
                            zombie.target_y = best_human.y
                            zombie.distance_to_target = round(math.sqrt(best_human_dist))
                        else:
                            # Switch Zombie to target Ash
                            zombie.target_id = TARGET_ASH
                            zombie.target_x = self.ash.x
                            zombie.target_y = self.ash.y
                            zombie.distance_to_target = ash_distance
                        zombie.count_to_ash = ash_distance // 1400
                        recalc_move_vector = True

                    # Set move vector if needed
                    if recalc_move_vector:
                        if zombie.distance_to_target > 0:
                            zombie.move_x = round((zombie.target_x - zombie.x) * 400 / zombie.distance_to_target)
                            zombie.move_y = round((zombie.target_y - zombie.y) * 400 / zombie.distance_to_target)
                        else:
                            zombie.move_x = 0
                            zombie.move_y = 0

    def move_zombies(self):
        self.set_zombie_targets()
        for zombie in self.zombies:
            if zombie.is_alive:
                zombie.x += zombie.move_x
                zombie.y += zombie.move_y
                zombie.distance_to_target -= 400

    def update(self, move):
        self.move_zombies()
        self.ash.x = min(16000, max(0, self.ash.x + move[0]))
        self.ash.y = min(9000, max(0, self.ash.y + move[1]))
        score = 0
        humans_alive_score = (self.live_humans ** 2) * 10
        zombies_killed = 0
        for zombie in self.zombies:
            if zombie.is_alive:
                ash_distance = get_distance(self.ash, zombie)
                zombie.distance_to_ash = ash_distance
                if ash_distance < 4000000:
                    zombie.is_alive = False
                    zombies_killed += 1
                    self.live_zombies -= 1
        score += humans_alive_score * sum(FIBBONACCI_SEQUENCE[:zombies_killed])

        for zombie in self.zombies:
            if zombie.is_alive and zombie.target_id > -1 and zombie.distance_to_target < 400 and self.humans[zombie.target_id].is_alive:
                zombie.x = zombie.target_x
                zombie.y = zombie.target_y
                self.humans[zombie.target_id].is_alive = False
                self.live_humans -= 1
                zombie.target_id = TARGET_NONE
                zombie.distance_to_target = -1
        return score


def score_moves(game_state_pkl, moves, output):
    state = pickle.loads(game_state_pkl)
    score = 0

    # print(state.zombies)
    for move in moves:
        score += state.update(move)
        if state.live_humans == 0:
            score = 0
            break
        if state.live_zombies == 0:
            break
    if output:
        print(state.live_humans, state.live_zombies, score, file=sys.stderr, flush=True)
    return score


GENE_LENGTH = 20
POPULATION_SIZE = 20


def create_population(last_steps):
    population = []
    for x_step in range(-1000, 1001, 250):
        for y_step in range(-1000, 1001, 250):
            moves = []
            for i in range(GENE_LENGTH):
                moves.append(np.array((x_step, y_step)))
            population.append(moves)
    if last_steps is not None:
        # Add existing steps to the population
        moves = []
        for i in range(1, GENE_LENGTH):
            moves.append(np.array([last_steps[i][k] for k in range(2)]))
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
        scored_population.append([moves, score_moves(game_state_pkl, moves, False)])
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
            scored_population.append([child_moves_breed, score_moves(game_state_pkl, child_moves_breed, False)])
            scored_population.append([child_moves_splice, score_moves(game_state_pkl, child_moves_splice, False)])
        scored_population.sort(key=lambda x: x[1], reverse=True)
        scored_population = scored_population[:POPULATION_SIZE + 1]
        #print(scored_population[0][1], scored_population[0][0], file=sys.stderr, flush=True)
        #print('Best score generation : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
        generation += 1
        average_generation_time = (time.time() - start_time) / generation
        print([x[1] for x in scored_population], file=sys.stderr, flush=True)
        score_moves(game_state_pkl, scored_population[0][0], True)
        # print(generation, average_generation_time, time.time() - start_time, file=sys.stderr, flush=True)

    #print('Final best score : ' + str(scored_population[0][1]), file=sys.stderr, flush=True)
    #print('Steps : ' + str(scored_population[0][0]), file=sys.stderr, flush=True)
    return scored_population[0][0]

# first_go = True
# last_time = None
# start_time = None
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
