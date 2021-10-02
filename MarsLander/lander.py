import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, random, sample

GRAVITY = -3.711
CHROMOSOME_LENGTH = 120
POPULATION_SIZE = 40
PARENT_FRACTION = 1
ELITISM_SIZE = 2
MAX_SCORE = 50000
MUTATION_RATE = 0
MUTATION_INCREMENT = 0.01
MAX_MUTATION = 0.05
LAST_BEST_SCORE = MAX_SCORE

SIN_R = []
COS_R = []


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


def get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y):
    points = max(0.8 * landing_min + 0.2 * landing_max - x, 0) + max(x - 0.8 * landing_max - 0.2 * landing_min, 0) + max(y - landing_y, 0)
    points += max(abs(hs) - 20, 0) * 25
    points += max(abs(vs) - 40, 0) * 25
    points += abs(r) * 25
    return round(points)


def create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init, landing_area_min, landing_area_max, landing_area_y):
    random_population = {}
    for i in range(POPULATION_SIZE):
        chromosome = []
        r_base = randint(-10, 10)
        for j in range(CHROMOSOME_LENGTH):
            power = randint(-1, 1) if j < CHROMOSOME_LENGTH // 2 else randint(0, 1)
            chromosome.append([min(15, max(-15, r_base + randint(-15, 15))), power])
        score = evaluate_path(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init, chromosome,
                      landing_area_min, landing_area_max, landing_area_y)[0]
        random_population[score] = {'chromosome': chromosome}
    return random_population


def evaluate_path(x, y, hs, vs, r, p, land_x, land_y, fuel, chromosome, landing_min, landing_max, landing_y):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = MAX_SCORE
    index = 0
    while state == State.Flying and index < CHROMOSOME_LENGTH:
        ha = -p * SIN_R[r + 90]
        va = p * COS_R[r + 90] + GRAVITY
        x += hs + ha / 2
        y += vs + va / 2
        hs += ha
        vs += va
        land_height = np.interp(x, land_x, land_y, left=None, right=None, period=None)
        if y <= land_height or fuel <= 0:
            score = get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y)
            state = State.Landed if score == 0 else State.Crashed
        else:
            r = max(-90, min(90, r + chromosome[index][0]))
            p = max(0, min(4, p + chromosome[index][1]))
        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
        fuel -= p
    return [score, state, fuel, index - 1, r, path_x, path_y]


def plot(population, land_x, land_y, pause_time):
    #fig, ax = plt.figure()
    #fig = plt.get_previous_run_figure()
    #ax = fig.axes

    #noise = np.random.rand(1, 100)
    #ax.plot(noise)
    #plt.draw()

    plt.figure(figsize=(11.5, 4.5))
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.xlim([0, 7000])
    plt.ylim([0, 3000])
    ax.plot(land_x, land_y, color='red')
    for score, organism in population.items():
        ax.plot(organism['path_x'], organism['path_y'], color='white' if score == 0 else 'green' if score < 1000 else 'yellow', zorder=1 if score == 0 else 0)
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def solve_lander(x_init, y_init, hs_init, vs_init, r_init, p_init, fuel_init, land_x, land_y):
    # Pre-calculate sin and cos values
    global LAST_BEST_SCORE, MUTATION_RATE, population
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

    initial = True
    found_solution = False
    while not found_solution:
        if initial:
            population = create_random_population(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init, landing_area_min, landing_area_max, landing_area_y)
            initial = False
        else:
            # Perform generic algorithm. First breed more organisms
            scores = list(population.keys())
            best_score = scores[0]
            if best_score < LAST_BEST_SCORE:
                LAST_BEST_SCORE = best_score
                MUTATION_RATE = 0
            MUTATION_RATE = min(MAX_MUTATION, MUTATION_RATE + MUTATION_INCREMENT)

            children = {}
            for replace_idx in range(2, POPULATION_SIZE):
                parent1, parent2 = [population[i] for i in sample(scores[:replace_idx], 2)]
                child_chromosome = []
                factor = random()
                cut_chromosome = randint(0, CHROMOSOME_LENGTH)
                for j in range(CHROMOSOME_LENGTH):
                    child_chromosome.append([randint(-15, 15), randint(-1, 1)] if random() < MUTATION_RATE else [round(parent1['chromosome'][j][m] * factor + parent2['chromosome'][j][m] * (1 - factor)) for m in range(2)])
                    if j == cut_chromosome:
                        factor = 1 - factor

                score, state, fuel_left, last_gene, last_r, path_x, path_y = evaluate_path(x_init, y_init, hs_init,
                                                                                           vs_init, r_init, p_init,
                                                                                           land_x, land_y, fuel_init,
                                                                                           child_chromosome,
                                                                                           landing_area_min,
                                                                                           landing_area_max,
                                                                                           landing_area_y)
                # Set latest rotation to maximise how upright we are
                orig = child_chromosome[last_gene][0]
                child_chromosome[last_gene][0] = max(-15, min(15, child_chromosome[last_gene][0] - last_r))
                change = child_chromosome[last_gene][0] - orig
                score -= abs(change) * 25
                children[score] = {'chromosome': child_chromosome}
            population.update(children)

            # Now select the fittest
            population = dict(sorted(population.items()))
            scores = list(population.keys())
            for i in range(len(scores) - 1, POPULATION_SIZE, -1):
                del population[scores[i]]
            found_solution = scores[0] == 0

            # Output data
            print(scores)
            #plot(population, land_x, land_y, 0.5)
    plot_chart = False
    plot_chart = True
    if plot_chart:
        for organism in population.values():
            score, state, fuel_left, last_gene, last_r, path_x, path_y = evaluate_path(x_init, y_init, hs_init,
                                                                                       vs_init, r_init, p_init,
                                                                                       land_x, land_y, fuel_init,
                                                                                       organism['chromosome'],
                                                                                       landing_area_min,
                                                                                       landing_area_max,
                                                                                       landing_area_y)
            organism['path_x'] = path_x
            organism['path_y'] = path_y
        plot(population, land_x, land_y, 20)
