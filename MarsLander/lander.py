import math
import matplotlib.pyplot as plt
from enum import Enum
from random import randint, random, sample

X_MAX = 7000
Y_MAX = 3000
GRAVITY = -3.711
CHROMOSOME_LENGTH = 200
POPULATION_SIZE = 40
PARENT_FRACTION = 0.5
MUTATION_INCREMENT = 0.005
MAX_MUTATION = 0.02
MAX_SCORE = 50000

SIN_R = []
COS_R = []

MIN_LAND_X = []
MAX_LAND_X = []

class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


def get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y, debug_on, land_segment_lengths, target_landing_segment, actual_landing_segment, land_x):
    #points = sum(land_segment_lengths[min(target_landing_segment, actual_landing_segment): max(target_landing_segment, actual_landing_segment)]) if actual_landing_segment is not None else sum(land_segment_lengths)
    points = 0
    if actual_landing_segment is None:
        if x < 0:
            actual_landing_segment = 0
        elif x > 7000:
            actual_landing_segment = len(land_x) - 1
        else:
            for i in range(len(land_x) - 1):
                if land_x[i] <= x <= land_x[i + 1]:
                    actual_landing_segment = i
    points += sum(land_segment_lengths[min(target_landing_segment, actual_landing_segment) + 1: max(target_landing_segment,
                                                                                                 actual_landing_segment) - 1])
    points += round(max(0.9 * landing_min + 0.1 * landing_max - x, 0) + max(x - 0.9 * landing_max - 0.1 * landing_min, 0))
    points += round(max(0, abs(y - landing_y) - abs(vs) - 4))
    points += max(abs(round(hs)) - 20, 0) * 25
    points += max(abs(round(vs)) - 40, 0) * 25
    points += abs(r) * 25
    if debug_on and False:
        print('xpos: ' + str(x) + ' ypos: ' + str(y) + 'x: ' + str(round(max(0.8 * landing_min + 0.2 * landing_max - x, 0) + max(x - 0.8 * landing_max - 0.2 * landing_min, 0)))
              + '  y: ' + str(round(max(0, abs(y - landing_y) - abs(vs)))) + '  hs: ' + str(max(abs(round(hs)) - 20, 0) * 25) + '  vs: ' + str(max(abs(round(vs)) - 40, 0) * 25) + '  r: ' + str(abs(r) * 25))
    return round(points)


def hit_land(old_x, old_y, new_x, new_y, land_x, land_y):
    grad_path = 1e9 if new_x == old_x else (new_y - old_y) / (new_x - old_x)
    intercept_path = new_y - grad_path * new_x
    min_x = min(old_x, new_x)
    max_x = max(old_x, new_x)
    for i in range(len(land_x) - 1):
        land_x_low, land_x_high = land_x[i: i + 2]
        land_y_low, land_y_high = land_y[i: i + 2]
        if old_y > land_y_low and old_y > land_y_high and new_y > land_y_low and new_y > land_y_high:
            continue
        if max_x < MIN_LAND_X[i] or min_x > MAX_LAND_X[i]:
            continue
        grad_line = (land_y[i + 1] - land_y[i]) / (land_x_high - land_x_low)
        intercept_line = land_y[i] - grad_line * land_x_low
        cross_x = (intercept_line - intercept_path) / (grad_path - grad_line)
        if max(min_x, MIN_LAND_X[i]) < cross_x < min(max_x, MAX_LAND_X[i]):
            return i
    return None


def evaluate_path(x, y, hs, vs, r, p, land_x, land_y, fuel, chromosome, landing_min, landing_max, landing_y, land_segment_lengths, target_landing_segment, debug_on):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = -1
    index = 0
    while state == State.Flying and index < CHROMOSOME_LENGTH:
        r = max(-90, min(90, r + chromosome[index][0]))
        p = max(0, min(4, p + chromosome[index][1]))
        ha = -p * SIN_R[r + 90]
        va = p * COS_R[r + 90] + GRAVITY
        #r_radians = math.radians(r)
        #ha = -p * math.sin(r_radians)
        #va = p * math.cos(r_radians) + GRAVITY
        old_x = x
        old_y = y
        x += hs + ha / 2
        y += vs + va / 2
        hs += ha
        vs += va
        landing_segment = hit_land(old_x, old_y, x, y, land_x, land_y)
        #if x < 0 or x > X_MAX or y < 0 or y > Y_MAX:
        #    score = MAX_SCORE
        #    state = State.Crashed
        if landing_segment is not None or fuel <= 0 or index == CHROMOSOME_LENGTH - 1 or x < 0 or x > X_MAX or y < 0 or y > Y_MAX:
            score = get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y, debug_on, land_segment_lengths, target_landing_segment, landing_segment, land_x)
            state = State.Landed if score == 0 else State.Crashed

        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
        fuel -= p
    return [score, state, fuel, index - 1, r, vs - va, path_x, path_y]


def create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init,
                             landing_area_min, landing_area_max, landing_area_y, land_segment_lengths, target_landing_segment):
    random_population = {}
    landing_direction_left = (landing_area_min + landing_area_max) // 2 - x_init < 0
    angle_min = 0 if landing_direction_left else -30
    angle_max = 31 if landing_direction_left else 1
    for power in range(3, 5):
        for angle in range(angle_min, angle_max, 5):
            for power2 in range(2, 5):
                for angle2 in range(-10, 11, 3):
                    chromosome = []
                    r = r_init
                    p = p_init
                    for j in range(CHROMOSOME_LENGTH):
                        angle_to_use = angle if j < CHROMOSOME_LENGTH // 2 else angle2
                        power_to_use = power if j < CHROMOSOME_LENGTH // 2 else power2
                        dr = max(-15, min(15, angle_to_use - r))
                        dp = max(-1, min(1, power_to_use - p))
                        chromosome.append([dr, dp])
                        r += dr
                        p += dp
                    score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init,
                                                                                                        hs_init, vs_init,
                                                                                                        r_init, p_init,
                                                                                                        land_x, land_y,
                                                                                                        fuel_init,
                                                                                                        chromosome,
                                                                                                        landing_area_min,
                                                                                                        landing_area_max,
                                                                                                        landing_area_y,
                                                                                                        land_segment_lengths,
                                                                                                        target_landing_segment,
                                                                                                        False)
                    random_population[score] = {'chromosome': chromosome, 'path_x': path_x, 'path_y': path_y}

    return random_population


def plot(plot_population, land_x, land_y, pause_time):
    # fig, ax = plt.figure()
    # fig = plt.get_previous_run_figure()
    # ax = fig.axes

    # noise = np.random.rand(1, 100)
    # ax.plot(noise)
    # plt.draw()

    plt.figure(figsize=(11.5, 4.5))
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.xlim([0, 7000])
    plt.ylim([0, 3000])
    ax.plot(land_x, land_y, color='red')
    for score, organism in plot_population.items():
        ax.plot(organism['path_x'], organism['path_y'],
                color='white' if score == 0 else 'blue' if score < 100 else 'green' if score < 1000 else 'yellow', zorder=3 if score == 0 else 2 if score < 100 else 1 if score < 1000 else 0)
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def solve_lander(x_init, y_init, hs_init, vs_init, r_init, p_init, fuel_init, land_x, land_y):
    # Pre-calculate land data
    for i in range(len(land_x) - 1):
        MIN_LAND_X.append(min(land_x[i], land_x[i + 1]))
        MAX_LAND_X.append(max(land_x[i], land_x[i + 1]))

    global LAST_BEST_SCORE, MUTATION_RATE
    for r in range(-90, 91):
        r_radians = math.radians(r)
        SIN_R.append(math.sin(r_radians))
        COS_R.append(math.cos(r_radians))

    # Pre-calculate sin and cos values
    global LAST_BEST_SCORE, MUTATION_RATE
    for r in range(-90, 91):
        r_radians = math.radians(r)
        SIN_R.append(math.sin(r_radians))
        COS_R.append(math.cos(r_radians))

    # Find landing zone
    landing_area_min = 0
    landing_area_max = 7000
    landing_area_y = 0
    target_landing_segment = -1
    land_segment_lengths = []
    for i in range(len(land_x) - 1):
        land_segment_lengths.append(abs(land_x[i] - land_x[i + 1]) + abs(land_y[i] - land_y[i + 1]))
        if land_y[i] == land_y[i + 1]:
            target_landing_segment = i
            landing_area_min = land_x[i]
            landing_area_max = land_x[i + 1]
            landing_area_y = land_y[i]

    population = create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y,
                                          fuel_init, landing_area_min, landing_area_max, landing_area_y, land_segment_lengths, target_landing_segment)
    #plot(population, land_x, land_y, 20)
    found_solution = False
    last_best_score = 100000
    mutation_rate = MUTATION_INCREMENT
    while not found_solution:
        # Perform generic algorithm. First breed more organisms
        scores = list(population.keys())
        best_score = scores[0]
        #mutation_rate = max(MUTATION_INCREMENT, min(MAX_MUTATION,
         #                                           mutation_rate + (-MUTATION_INCREMENT if best_score < last_best_score else MUTATION_INCREMENT)))
        mutation_rate = MUTATION_INCREMENT if best_score < last_best_score else min(MAX_MUTATION, mutation_rate + MUTATION_INCREMENT)
        distance_to_solution = best_score / (scores[min(POPULATION_SIZE // 2, len(scores) - 1)] - best_score + 1)
        #mutation_rate = min(MAX_MUTATION, distance_to_solution / 20)
        # mutation_rate = MAX_MUTATION
        last_best_score = best_score
        #print(mutation_rate)

        max_parent_index = 2
        while scores[max_parent_index] < 2 * best_score and max_parent_index < len(scores) - 2:
            max_parent_index += 1
        for child_idx in range(2, int(POPULATION_SIZE * PARENT_FRACTION)):
            #parent1, parent2 = [population[i] for i in sample(scores[:max_parent_index], 2)]
            parent1, parent2 = [population[i] for i in sample(scores[:2 + child_idx // 2], 2)]
            #parent1 = population[sample(scores[:5], 1)[0]]
            #parent2 = population[sample(scores[:2 + child_idx // 2], 1)[0]]
            child_chromosome = []
            # factor = random()
            #factor = 1.5 * random() - 0.25
            factor = 1.2 * random() - 0.1
            for j in range(CHROMOSOME_LENGTH):
                mutation = [randint(-15, 15), randint(-1, 1)] if random() < mutation_rate else [0, 0]
                new_gene = [round(parent1['chromosome'][j][m] * factor + parent2['chromosome'][j][m] * (1 - factor)) + mutation[m]
                            for m in range(2)]
                new_gene = [min(15, max(-15, new_gene[0])), min(1, max(-1, new_gene[1]))]
                child_chromosome.append(new_gene)
            score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init, hs_init, vs_init, r_init, p_init,
                                                                                                land_x, land_y, fuel_init, child_chromosome,
                                                                                                landing_area_min, landing_area_max,
                                                                                                landing_area_y, land_segment_lengths, target_landing_segment, False)
            population[score] = {'chromosome': child_chromosome, 'path_x': path_x, 'path_y': path_y}

            # Set latest rotation to maximise how upright we are
            rotated_child_chromosome = child_chromosome.copy()
            rotated_child_chromosome[last_gene][0] = max(-15, min(15, child_chromosome[last_gene][0] - last_r))
            if last_vs < -40:
                for i in range(4):
                    rotated_child_chromosome[last_gene - i][1] += 1

            # Score and add the rotated version
            adjusted_score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init, hs_init,vs_init, r_init, p_init,
                                                                                                         land_x, land_y, fuel_init, rotated_child_chromosome,
                                                                                                         landing_area_min, landing_area_max,
                                                                                                         landing_area_y, land_segment_lengths, target_landing_segment, False)
            population[adjusted_score] = {'chromosome': rotated_child_chromosome, 'path_x': path_x, 'path_y': path_y}

        # Now select the fittest
        population = dict(sorted(population.items()))
        scores = list(population.keys())
        for i in range(len(scores) - 1, POPULATION_SIZE, -1):
            del population[scores[i]]
        found_solution = scores[0] == 0

        # Output data
        #print(scores)
        #plot(population, land_x, land_y, 0.5)
        if False:
            evaluate_path(x_init, y_init, hs_init,
                          vs_init, r_init, p_init,
                          land_x, land_y, fuel_init,
                          population[scores[0]]['chromosome'],
                          landing_area_min, landing_area_max, landing_area_y,
                          land_segment_lengths, target_landing_segment, True)
    #plot(population, land_x, land_y, 20)
