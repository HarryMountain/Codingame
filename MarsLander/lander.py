import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, random, sample

GRAVITY = -3.711
CHROMOSOME_LENGTH = 100
POPULATION_SIZE = 40
PARENT_FRACTION = 0.5
MAX_SCORE = 50000
MUTATION_INCREMENT = 0.02
MAX_MUTATION = 0.1

SIN_R = []
COS_R = []


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


def get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y, debug_on):
    points = round(max(0.8 * landing_min + 0.2 * landing_max - x, 0) + max(x - 0.8 * landing_max - 0.2 * landing_min, 0))\
             + round(max(0, abs(y - landing_y) - abs(vs) - 4))
    points += max(abs(round(hs)) - 20, 0) * 25
    points += max(abs(round(vs)) - 40, 0) * 25
    points += abs(r) * 25
    if debug_on:
        print('x: ' + str(round(max(0.8 * landing_min + 0.2 * landing_max - x, 0) + max(x - 0.8 * landing_max - 0.2 * landing_min, 0)))
              + '  y: ' + str(round(max(0, abs(y - landing_y) - abs(vs)))) + '  hs: ' + str(max(abs(round(hs)) - 20, 0) * 25) + '  vs: ' + str(max(abs(round(vs)) - 40, 0) * 25) + '  r: ' + str(abs(r) * 25))
    return round(points)


def evaluate_path(x, y, hs, vs, r, p, land_x, land_y, fuel, chromosome, landing_min, landing_max, landing_y, debug_on):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = MAX_SCORE
    index = 0
    while state == State.Flying and index < CHROMOSOME_LENGTH:
        r = max(-90, min(90, r + chromosome[index][0]))
        p = max(0, min(4, p + chromosome[index][1]))
        ha = -p * SIN_R[r + 90]
        va = p * COS_R[r + 90] + GRAVITY
        #r_radians = math.radians(r)
        #ha = -p * math.sin(r_radians)
        #va = p * math.cos(r_radians) + GRAVITY
        x += hs + ha / 2
        y += vs + va / 2
        hs += ha
        vs += va
        land_height = np.interp(x, land_x, land_y, left=None, right=None, period=None)
        if y <= land_height or fuel <= 0:
            score = get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y, debug_on)
            state = State.Landed if score == 0 else State.Crashed

        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
        fuel -= p
    return [score, state, fuel, index - 1, r, vs - va, path_x, path_y]


def create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init,
                             landing_area_min, landing_area_max, landing_area_y):
    random_population = {}
    for i in range(POPULATION_SIZE):
        chromosome = []
        r_base = randint(-90, 90)
        p_base = randint(0, 4)
        r_act = 0
        p_act = 0
        for j in range(CHROMOSOME_LENGTH):
            r_base += randint(-30, 30)
            dr = min(15, max(-15, r_base - r_act))
            r_act += dr
            #p_base += randint(-2, 2) if j < CHROMOSOME_LENGTH // 2 else randint(0, 2)
            p_base += randint(-2, 2)
            dp = min(1, max(-1, p_base - p_act))
            p_act += dp
            chromosome.append([dr, dp])
        score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init, hs_init, vs_init,
                                                                                   r_init, p_init, land_x, land_y,
                                                                                   fuel_init, chromosome,
                                                                                   landing_area_min, landing_area_max,
                                                                                   landing_area_y, False)
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
    for i in range(len(land_x) - 1):
        if land_y[i] == land_y[i + 1]:
            landing_area_min = land_x[i]
            landing_area_max = land_x[i + 1]
            landing_area_y = land_y[i]

    population = create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y,
                                          fuel_init, landing_area_min, landing_area_max, landing_area_y)
    found_solution = False
    last_best_score = MAX_SCORE
    mutation_rate = MUTATION_INCREMENT
    while not found_solution:
        # Perform generic algorithm. First breed more organisms
        scores = list(population.keys())
        best_score = scores[0]
        mutation_rate = max(MUTATION_INCREMENT, min(MAX_MUTATION,
                                   mutation_rate + (-MUTATION_INCREMENT if best_score < last_best_score else MUTATION_INCREMENT)))
        #mutation_rate = MUTATION_INCREMENT if best_score < last_best_score else min(MAX_MUTATION, mutation_rate + MUTATION_INCREMENT)
        distance_to_solution = best_score / (scores[POPULATION_SIZE // 2] - best_score + 1)
        mutation_rate = min(MAX_MUTATION, distance_to_solution / 20)
        last_best_score = best_score
        #print(mutation_rate)

        for child_idx in range(2, int(POPULATION_SIZE * PARENT_FRACTION)):
            parent1, parent2 = [population[i] for i in sample(scores[:2 + child_idx // 2], 2)]
            child_chromosome = []
            # factor = random()
            #factor = 2 * random() - 0.5
            factor = 1.2 * random() - 0.1
            cut_chromosome = randint(0, CHROMOSOME_LENGTH)
            gene_total = [r_init, p_init]
            for j in range(CHROMOSOME_LENGTH):
                mutation = [randint(-15, 15), randint(-1, 1)] if random() < mutation_rate else [0, 0]
                new_gene = [round(parent1['chromosome'][j][m] * factor + parent2['chromosome'][j][m] * (1 - factor)) + mutation[m]
                            for m in range(2)]
                new_gene = [min(15, max(-15, new_gene[0])), min(1, max(-1, new_gene[1]))]
                """
                gene_total[0] += new_gene[0]
                gene_total[1] += new_gene[1]
                if gene_total[0] > 90:
                    new_gene[0] -= gene_total[0] - 90
                elif gene_total[0] < -90:
                    new_gene[0] -= gene_total[0] + 90
                if gene_total[1] > 4:
                    new_gene[1] -= gene_total[1] - 4
                elif gene_total[1] < 0:
                    new_gene[1] -= gene_total[1]
                """
                child_chromosome.append(new_gene)
                #if j == cut_chromosome:
                #    factor = 1 - factor
            score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init, hs_init,
                                                                                       vs_init, r_init, p_init,
                                                                                       land_x, land_y, fuel_init,
                                                                                       child_chromosome,
                                                                                       landing_area_min,
                                                                                       landing_area_max,
                                                                                       landing_area_y, False
                                                                                       )
            population[score] = {'chromosome': child_chromosome, 'path_x': path_x, 'path_y': path_y}

            # Set latest rotation to maximise how upright we are
            rotated_child_chromosome = child_chromosome.copy()
            rotated_child_chromosome[last_gene][0] = max(-15, min(15, child_chromosome[last_gene][0] - last_r))
            if last_vs < -40:
                for i in range(4):
                    #rotated_child_chromosome[last_gene - randint(0, 3)][1] += 1
                    rotated_child_chromosome[last_gene - i][1] += 1

            # Score and add the rotated version
            adjusted_score, state, fuel_left, last_gene, last_r, last_vs, path_x, path_y = evaluate_path(x_init, y_init, hs_init,
                                                                                       vs_init, r_init, p_init,
                                                                                       land_x, land_y, fuel_init,
                                                                                       rotated_child_chromosome,
                                                                                       landing_area_min,
                                                                                       landing_area_max,
                                                                                       landing_area_y, False)
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
        #evaluate_path(x_init, y_init, hs_init,
        #              vs_init, r_init, p_init,
        #              land_x, land_y, fuel_init,
        #              population[scores[0]]['chromosome'],
        #              landing_area_min,
        #              landing_area_max,
        #              landing_area_y, True)
    #print(last_gene)
    #plot(population, land_x, land_y, 20)
