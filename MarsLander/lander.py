import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, choice, random, sample

GRAVITY = -3.711
CHROMOSOME_LENGTH = 80
POPULATION_SIZE = 40


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


def get_score(x, hs, vs, r, landing_min, landing_max):
    points = max(0.85 * landing_min + 0.15 * landing_max - x, 0) + max(x - 0.85 * landing_max - 0.15 * landing_min, 0)
    points += max(abs(hs) - 20, 0) * 25
    points += max(abs(vs) - 40, 0) * 25
    points += abs(r) * 25
    return round(points)


def create_random_population():
    population = {}
    for i in range(POPULATION_SIZE):
        chromosome = []
        current_r = 0
        current_p = 0
        for j in range(CHROMOSOME_LENGTH):
            new_r = min(max(current_r + randint(-15, 15), -90), 90)
            new_p = min(max(current_p + randint(-1, 1), 0), 4)
            chromosome.append([new_r - current_r, new_p - current_p])
            current_r = new_r
            current_p = new_p
        population[i] = {'chromosome': chromosome, 'calculated': False}
    return population


def evaluate_path(x, y, hs, vs, r, p, land_x, land_y, fuel, chromosome, landing_min, landing_max):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = 50000
    index = 0
    while state == State.Flying and index < CHROMOSOME_LENGTH:
        radians_r = math.radians(r)
        ha = -p * math.sin(radians_r)
        va = p * math.cos(radians_r) + GRAVITY
        x += hs + ha / 2
        y += vs + va / 2
        hs += ha
        vs += va
        land_height = np.interp(x, land_x, land_y, left=None, right=None, period=None)
        if y <= land_height:
            score = get_score(x, hs, vs, r, landing_min, landing_max)
            state = State.Landed if score == 0 else State.Crashed
        r = max(-90, min(90, r + chromosome[index][0]))
        p = max(0, min(4, p + chromosome[index][1]))
        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
    return [state, path_x, path_y, score]


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


def solve_lander(x_init, y_init, hs_init, vs_init, r_init, p_init, fuel, land_x, land_y):
    # Find landing zone
    for i in range(len(land_x) - 1):
        if land_y[i] == land_y[i + 1]:
            landing_area_min = land_x[i]
            landing_area_max = land_x[i + 1]

    initial = True
    found_solution = False
    while not found_solution:
        if initial:
            population = create_random_population()
            initial = False
        else:
            # Perform generic algorithm. First select the fittest
            sorted_population = sorted(population.items(), key=lambda x: x[1]['score'])
            number_to_keep = POPULATION_SIZE // 2
            removed_ids = [i[0] for i in sorted_population[number_to_keep:]]

            # Now breed more organisms
            children = {}
            parent_index = 0
            for i in range(len(removed_ids)):
                parent1 = sorted_population[parent_index][1]['chromosome']
                parent_index = (parent_index + 1) % number_to_keep
                parent2 = sorted_population[parent_index][1]['chromosome']
                parent_index = (parent_index + 1) % number_to_keep
                child_chromosome = []
                for j in range(CHROMOSOME_LENGTH):
                    factor = random()
                    # child_chromosome.append([round(parent1[j][m] * factor + parent2[j][m] * (1 - factor)) for m in range(2)])
                    child_chromosome.append(parent1[j] if factor < 0.5 else parent2[j])
                    if random() < 0.01:
                        child_chromosome[-1] = [randint(-2, 2), randint(-1, 1)]
                children[removed_ids[i]] = {'chromosome': child_chromosome, 'calculated': False}
            population.update(children)

        scores = []
        for organism in population.values():
            if not organism['calculated']:
                state, path_x, path_y, score = evaluate_path(x_init, y_init, hs_init, vs_init, r_init, p_init, land_x, land_y, 1, organism['chromosome'], landing_area_min, landing_area_max)
                organism['path_x'] = path_x
                organism['path_y'] = path_y
                organism['score'] = score
                organism['calculated'] = True
            scores.append(organism['score'])
        scores.sort()
        found_solution = scores[0] == 0
        print(scores)
        #plot(population, land_x, land_y, 0.5)
    plot(population, land_x, land_y, 20)
