import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, random, sample

GRAVITY = -3.711
CHROMOSOME_LENGTH = 120
POPULATION_SIZE = 40
PARENT_FRACTION = 0.5
ELITISM_SIZE = 2
MAX_SCORE = 50000
MUTATION_RATE = 0
MUTATION_INCREMENT = 0.02
MAX_MUTATION = 0.1
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
    #if points < 5000:
    #    print(round(points), round(max(0.9 * landing_min + 0.1 * landing_max - x, 0) + max(x - 0.9 * landing_max - 0.1 * landing_min, 0) + max(y - landing_y, 0)), round(max(abs(hs) - 20, 0) * 25), max(abs(vs) - 40, 0) * 25, round(abs(r) * 25))
    return round(points)


def create_random_population(r_init, p_init):
    population = {}
    for i in range(POPULATION_SIZE):
        chromosome = []
        r_base = randint(-10, 10)
        for j in range(CHROMOSOME_LENGTH):
            power = randint(-1, 1) if j < CHROMOSOME_LENGTH // 2 else randint(0, 1)
            chromosome.append([min(15, max(-15, r_base + randint(-15, 15))), power])
        population[i] = {'chromosome': chromosome, 'calculated': False}
    return population


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
        r = max(-90, min(90, r + chromosome[index][0]))
        p = max(0, min(4, p + chromosome[index][1]))
        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
        fuel -= p
    return [state, path_x, path_y, score, fuel, index - 1, r]


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
    for i in range(POPULATION_SIZE):
        score = population[i]['score']
        ax.plot(population[i]['path_x'], population[i]['path_y'], color='white' if score == 0 else 'green' if score < 2000 else 'yellow', zorder=1 if score == 0 else 0)
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
            number_to_remove = 0
            for value in sorted_population:
                number_to_remove += 1 if value[1]['score'] == MAX_SCORE else 0
            #number_to_remove = max(number_to_remove, PARENT_FRACTION * POPULATION_SIZE)
            number_to_breed = POPULATION_SIZE - number_to_remove
            #number_to_keep = int(POPULATION_SIZE * PARENT_PERCENT)
            #removed_ids = [i[0] for i in sorted_population[ELITISM_SIZE:]]

            # Now breed more organisms
            best_score = sorted_population[0][1]['score']
            if best_score < LAST_BEST_SCORE:
                LAST_BEST_SCORE = best_score
                MUTATION_RATE = MUTATION_INCREMENT
            else:
                MUTATION_RATE = min(MAX_MUTATION, MUTATION_RATE + MUTATION_INCREMENT)

            children = {}
            parent_index = 0
            for replace_idx in range(POPULATION_SIZE - 1, ELITISM_SIZE - 1, -1):
                #parent1 = sorted_population[parent_index][1]
                #parent_index = (parent_index + 1) % number_to_keep
                #parent2 = sorted_population[parent_index][1]
                #parent_index = (parent_index + 1) % number_to_keep
                #print(replace_idx)
                parent1, parent2 = [i[1] for i in sample(sorted_population[:min(number_to_breed, 2 + replace_idx // 2)], 2)]
                child_chromosome = []
                factor = random()
                cut_chromosome = randint(0, CHROMOSOME_LENGTH)
                for j in range(CHROMOSOME_LENGTH):
                    child_chromosome.append([round(parent1['chromosome'][j][m] * factor + parent2['chromosome'][j][m] * (1 - factor)) for m in range(2)])
                    if j == cut_chromosome:
                        factor = 1 - factor
                    #mutation_rate = 0.05 if parent1['score'] == parent2['score'] else 0.02
                    # mutation_rate = 0.01
                    #mutation_rate = 0
                    if random() < MUTATION_RATE:
                        child_chromosome[-1] = [randint(-15, 15), randint(-1, 1)]

                #organism = {'chromosome': child_chromosome, 'calculated': False}
                score = evaluate_path(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, fuel_init, child_chromosome, landing_area_min, landing_area_max, landing_area_y)[3]
                if score < population[sorted_population[replace_idx][0]]['score']:
                    children[sorted_population[replace_idx][0]] = {'chromosome': child_chromosome, 'calculated': False, 'score': score}
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
    print(last_gene)
    plot(population, land_x, land_y, 20)
