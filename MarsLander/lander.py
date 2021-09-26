import math
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
from random import randint, choice, random, sample

GRAVITY = -3.711
CHROMOSOME_LENGTH = 80
POPULATION_SIZE = 40
INITIAL_HS = -100
INITIAL_R = 90
INITIAL_X = 6500
INITIAL_Y = 2800


class State(Enum):
    Flying = 1
    Landed = 2
    Crashed = 3


# land_x = [0, 1000, 1500, 3000, 4000, 5500, 6999]
# land_y = [100, 500, 1500, 1000, 150, 150, 800]
land_x = [0, 1000, 1500, 3000, 3500, 3700, 5000, 5800, 6000, 6999]
land_y = [100, 500, 100, 100, 500, 200, 1500, 300, 1000, 2000]
for i in range(len(land_x) - 1):
    if land_y[i] == land_y[i + 1]:
        landing_area_min = land_x[i]
        landing_area_max = land_x[i + 1]


def get_score(x, hs, vs, r):
    points = max(0.85 * landing_area_min + 0.15 * landing_area_max - x, 0) + max(x - 0.85 * landing_area_max - 0.15 * landing_area_min, 0)
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
        population[i] = {'chromosome': chromosome}
    return population


def evaluate_path(x, y, land_x, land_y, fuel, chromosome):
    path_x = [x]
    path_y = [y]
    state = State.Flying
    score = 50000
    current_r = INITIAL_R
    current_p = 0
    hs = INITIAL_HS
    vs = 0
    index = 0
    while state == State.Flying and index < CHROMOSOME_LENGTH:
        radians_r = math.radians(current_r)
        ha = -current_p * math.sin(radians_r)
        va = current_p * math.cos(radians_r) + GRAVITY
        x += hs + ha / 2
        y += vs + va / 2
        hs += ha
        vs += va
        land_height = np.interp(x, land_x, land_y, left=None, right=None, period=None)
        if y <= land_height:
            score = get_score(x, hs, vs, current_r)
            state = State.Landed if score == 0 else State.Crashed
        current_r = max(-90, min(90, current_r + chromosome[index][0]))
        current_p = max(0, min(4, current_p + chromosome[index][1]))
        path_x.append(round(x))
        path_y.append(round(y))
        index += 1
    return [state, path_x, path_y, score]


def plot(population):
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
    plt.pause(20)
    plt.close()


state = State.Crashed
initial = True
found_solution = False
while not found_solution:
    if initial:
        population = create_random_population()
        initial = False
    else:
        # Perform generic algorithm. First select the fittest
        removed_ids = []
        for id, organism in population.items():
            if organism['score'] >= average_score:
                removed_ids.append(id)
        for id in removed_ids:
            population.pop(id)

        # Now breed more organisms
        children = {}
        # sorted_population = sorted(population.keys(), key=population.get("score"))
        sorted_population = sorted(population.items(), key=lambda x: x[1]['score'])
        for i in range(len(removed_ids)):
            # parent1, parent2 = [e['chromosome'] for e in sample(list(population.values()), 2)]
            parent1 = sorted_population[randint(0, min(5, len(population) - 1))][1]["chromosome"]
            parent2 = sorted_population[randint(0, len(population) - 1)][1]["chromosome"]
            child_chromosome = []
            for j in range(CHROMOSOME_LENGTH):
                factor = random()
                # child_chromosome.append([round(parent1[j][m] * factor + parent2[j][m] * (1 - factor)) for m in range(2)])
                child_chromosome.append(parent1[j] if factor < 0.5 else parent2[j])
                if random() < 0.05:
                    child_chromosome[-1] = [randint(-1, 1), randint(-1, 1)]
            children[removed_ids[i]] = {'chromosome': child_chromosome}
        population.update(children)

    scores = []
    for organism in population.values():
        state, path_x, path_y, score = evaluate_path(INITIAL_X, INITIAL_Y, land_x, land_y, 1, organism['chromosome'])
        organism['path_x'] = path_x
        organism['path_y'] = path_y
        organism['score'] = score
        scores.append(score)
    scores.sort()
    found_solution = scores[0] == 0
    print(scores)
    average_score = scores[POPULATION_SIZE // 4]  # Take the median
    # plot(population)
plot(population)
