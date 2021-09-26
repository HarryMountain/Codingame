import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, random

GRAVITY = -3.711
CHROMOSOME_LENGTH = 80
POPULATION_SIZE = 40

SIN_R = []
COS_R = []
for r in range(-90, 91):
    r_radians = math.radians(r)
    SIN_R.append(math.sin(r_radians))
    COS_R.append(math.cos(r_radians))


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


def get_score(x, y, hs, vs, r, landing_min, landing_max, landing_y):
    points = max(0.9 * landing_min + 0.1 * landing_max - x, 0) + max(x - 0.9 * landing_max - 0.1 * landing_min, 0) + max(y - landing_y, 0)
    points += max(abs(hs) - 20, 0) * 25
    points += max(abs(vs) - 40, 0) * 25
    points += abs(r) * 25
    return round(points)


def create_random_population(r_init, p_init):
    population = {}
    for i in range(POPULATION_SIZE):
        chromosome = []
        r = randint(-90, 90)
        p = randint(0, 4)
        r_base = randint(-10, 10)
        p_base = randint(-1, 1)
        #r_diff = randint(-15, 15)
        #p_diff = randint(-1, 1)
        last_saved_r = r_init
        last_saved_p = p_init
        #chromosome = [[r_diff, p_diff]] * CHROMOSOME_LENGTH

        for j in range(CHROMOSOME_LENGTH):
            chromosome.append([min(15, max(-15, r_base + randint(-15, 15))), min(1, max(-1, p_base + randint(-1, 1)))])
            """
            r = r + randint(-15, 15)
            p = p + randint(-1, 1)
            new_saved_r = min(15, max(-15, r - last_saved_r))
            new_saved_p = min(-1, max(1, p - last_saved_p))
            chromosome.append([min(15, max(-15, new_saved_r - last_saved_r)), min(1, max(-1, new_saved_p - last_saved_p))])
            last_saved_r = new_saved_r
            last_saved_p = new_saved_p
            """
        population[i] = {'chromosome': chromosome, 'calculated': False}
    return population


def evaluate_path(x, y, hs, vs, r, p, land_x, land_y, fuel, chromosome, landing_min, landing_max, landing_y):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = 50000
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
        r = max(-90, min(90, r + chromosome[index][0]))
        p = max(0, min(4, p + chromosome[index][1]))
        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
        fuel -= p
    return [state, path_x, path_y, score, fuel, index - 1, r]


def plot(population, land_x, land_y, pause_time):
    plt.figure(figsize=(11.5, 4.5))
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.xlim([0, 7000])
    plt.ylim([0, 3000])
    ax.plot(land_x, land_y, color='red')
    for i in range(POPULATION_SIZE):
        score = population[i]['score']
        ax.plot(population[i]['path_x'], population[i]['path_y'], color='white' if score == 0 else 'green' if score < 2000 else 'yellow', zorder=1 if score == 0 else 0)
    plt.show(block=False)
    plt.pause(pause_time)
    plt.close()


def solve_lander(x_init, y_init, hs_init, vs_init, r_init, p_init, fuel_init, land_x, land_y):
    # Find landing zone
    for i in range(len(land_x) - 1):
        if land_y[i] == land_y[i + 1]:
            landing_area_min = land_x[i]
            landing_area_max = land_x[i + 1]
            landing_area_y = land_y[i]

    initial = True
    found_solution = False
    while not found_solution:
        if initial:
            population = create_random_population(r_init, p_init)
            initial = False
        else:
            # Perform generic algorithm. First select the fittest
            sorted_population = sorted(population.items(), key=lambda x: x[1]['score'])
            number_to_keep = POPULATION_SIZE // 4
            removed_ids = [i[0] for i in sorted_population[number_to_keep:]]

            # Now breed more organisms
            children = {}
            parent_index = 0
            for i in range(len(removed_ids)):
                parent1 = sorted_population[parent_index][1]
                parent_index = (parent_index + 1) % number_to_keep
                parent2 = sorted_population[parent_index][1]
                parent_index = (parent_index + 1) % number_to_keep
                child_chromosome = []
                factor = random()
                for j in range(CHROMOSOME_LENGTH):
                    child_chromosome.append([round(parent1['chromosome'][j][m] * factor + parent2['chromosome'][j][m] * (1 - factor)) for m in range(2)])
                    mutation_rate = 0.1 if parent1['score'] == parent2['score'] else 0.05
                    if random() < mutation_rate:
                        child_chromosome[-1] = [randint(-15, 15), randint(-1, 1)]
                children[removed_ids[i]] = {'chromosome': child_chromosome, 'calculated': False}
            population.update(children)

        scores = []
        for organism in population.values():
            if not organism['calculated']:
                state, path_x, path_y, score, fuel_left, last_gene, last_r = evaluate_path(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init, organism['chromosome'], landing_area_min, landing_area_max, landing_area_y)
                organism['path_x'] = path_x
                organism['path_y'] = path_y
                organism['score'] = score
                organism['calculated'] = True
                # Set latest rotation to maximise how upright we are
                organism['chromosome'][last_gene][0] = max(-15, min(15, organism['chromosome'][last_gene][0] - last_r))
            scores.append(organism['score'])
        scores.sort()
        found_solution = scores[0] == 0
        print(scores)
        #plot(population, land_x, land_y, 0.5)
    plot(population, land_x, land_y, 20)
