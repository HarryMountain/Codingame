import json
import math
import random
import sys
from copy import deepcopy

import numpy as np
import math

import numpy as np

FULL_CIRCLE = math.radians(360)
HALF_CIRCLE = math.radians(180)
MAX_STEER_PER_TURN = math.radians(18)
DISTANCE_SCALING = 1000
VELOCITY_SCALING = 100


def get_angle(vector):
    xx, yy = vector[0], vector[1]
    return math.atan2(xx, yy)


def get_angle_and_distance(vector):
    angle = math.atan2(vector[0], vector[1])
    distance = round(math.sqrt(vector.dot(vector)))
    return np.array((angle, distance))


def update_angle(current_angle, target_angle):
    clockwise = target_angle - current_angle + (FULL_CIRCLE if target_angle < current_angle else 0)
    anticlockwise = current_angle - target_angle + (FULL_CIRCLE if target_angle > current_angle else 0)
    if anticlockwise < clockwise:
        new_angle = current_angle - min(MAX_STEER_PER_TURN, anticlockwise)
        if new_angle < -HALF_CIRCLE:
            new_angle += FULL_CIRCLE
    else:
        new_angle = current_angle + min(MAX_STEER_PER_TURN, clockwise)
        if new_angle > HALF_CIRCLE:
            new_angle -= FULL_CIRCLE
    # print(target_angle * 180 / math.pi, current_angle * 180 / math.pi, new_angle * 180 / math.pi, file=sys.stderr, flush=True)
    return new_angle


def update_angle_with_steer(current_angle_radians, steer_gene):
    angle = current_angle_radians + convert_steer_gene_to_radians(steer_gene)
    if angle < -HALF_CIRCLE:
        angle += FULL_CIRCLE
    elif angle > HALF_CIRCLE:
        angle -= FULL_CIRCLE
    return angle


# Angles all in radians
def evaluate_game_step(position, velocity, old_angle, next_checkpoint_pos, input_angle, new_thrust):
    # Calculate new angle
    new_angle = update_angle(old_angle, input_angle)

    # Calculate thrust and update speed
    velocity[0] = velocity[0] + new_thrust * math.sin(new_angle)
    velocity[1] = velocity[1] + new_thrust * math.cos(new_angle)

    # Move
    position = np.round(position + velocity)

    # Apply Drag
    velocity[0] = np.trunc(0.85 * velocity[0])
    velocity[1] = np.trunc(0.85 * velocity[1])

    # See whether we hit a checkpoint
    touched_checkpoint = False
    if position[0] - next_checkpoint_pos[0] < 600:
        if position[1] - next_checkpoint_pos[1] < 600:
            touched_checkpoint = np.sum(np.square([position[0] - next_checkpoint_pos[0], position[1] - next_checkpoint_pos[1]])) < 360000

    return position, velocity, new_angle, touched_checkpoint


# Genetic Algorithm
GENE_LENGTH = 6
POPULATION_SIZE = 10
GENERATIONS = 10
POWER_FLOOR = 10
GENE_FLOORS = [0, POWER_FLOOR]

def convert_steer_degrees_to_gene(angle):
    return angle * 100 / 36 + 50


def convert_steer_gene_to_radians(angle):
    return math.radians((angle - 50) * 36 / 100)


def create_population(steps):
    population = []
    for j in range(POPULATION_SIZE):
        racer = []
        if steps is not None:
            racer = deepcopy(steps[1:])
            racer.append(np.array((random.randint(0, 100), random.randint(POWER_FLOOR, 100))))
        else:
            for i in range(GENE_LENGTH):
                racer.append(np.array((random.randint(0, 100), random.randint(POWER_FLOOR, 100))))
        population.append(racer)
    return population


def score(velocity, pos, angle, racer, checkpoints, next_checkpoint_idx):
    velocity = deepcopy(velocity)
    pos = deepcopy(pos)
    score = 0
    checkpoint = False
    for steer, thrust in racer:
        new_angle = update_angle_with_steer(angle, steer)
        pos, velocity, angle, touched_checkpoint = evaluate_game_step(pos, velocity, angle, checkpoints[next_checkpoint_idx], new_angle, thrust)
        if touched_checkpoint:
            checkpoint = True
            next_checkpoint_idx = (next_checkpoint_idx + 1) % len(checkpoints)
            score += 10000
    vector = checkpoints[next_checkpoint_idx] - pos
    score -= round(math.sqrt(vector.dot(vector)))
    return score


def genetic_algorithm(steps, velocity, pos, angle, checkpoints, next_checkpoint_idx):
    population = create_population(steps)
    scored_population = []
    for racer in population:
        racer_score = score(velocity, pos, angle, racer, checkpoints, next_checkpoint_idx)
        scored_population.append([racer, racer_score])
    scored_population.sort(key=lambda x: x[1], reverse=True)
    print(scored_population, file=sys.stderr, flush=True)
    for i in range(GENERATIONS):
        for j in range(2, POPULATION_SIZE):
            parents = random.sample([l[0] for l in scored_population[:j]], 2)
            new_racer = []
            for step in range(GENE_LENGTH):
                factor = 1.2 * random.random() - 0.1
                new_step = np.array(
                    [min(100, max(GENE_FLOORS[i], parents[0][step][i] * factor + parents[1][step][i] * (1 - factor) + random.randint(-5, 5))) for i in
                     range(2)])
                new_racer.append(new_step)
            scored_population.append([new_racer, score(velocity, pos, angle, new_racer, checkpoints, next_checkpoint_idx)])
        scored_population.sort(key=lambda x: x[1], reverse=True)
        scored_population = scored_population[:POPULATION_SIZE + 1]
        print(scored_population[0][1], scored_population[0][0], file=sys.stderr, flush=True)

    return scored_population[0][0]


checkpoints = []
steps = None
first_go = True
next_checkpoint_idx = 1
velocity = [0, 0]
angle = 0
touched_checkpoint = False
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    if first_go:
        checkpoints.append([x, y])
        angle = get_angle([next_checkpoint_x - x, next_checkpoint_y - y])
        first_go = False
        sim_pos = np.array((x, y))
    if [next_checkpoint_x, next_checkpoint_y] not in checkpoints:
        checkpoints.append([next_checkpoint_x, next_checkpoint_y])
    if touched_checkpoint:
        next_checkpoint_idx = (next_checkpoint_idx + 1) % len(checkpoints)
        touched_checkpoint = False
    opponent_x, opponent_y = [int(i) for i in input().split()]
    position = np.array((x, y))
    print(position, sim_pos, file=sys.stderr, flush=True)
    # Output the target position followed by the power (0 <= thrust <= 100)
    # target_angle = get_angle(np.array((next_checkpoint_x, next_checkpoint_y)) - position)
    # thrust = 100
    # target_position = position + 10000 * np.array((math.sin(target_angle), math.cos(target_angle)))
    steps = genetic_algorithm(steps, deepcopy(velocity), position, angle, checkpoints, next_checkpoint_idx)
    step = steps[0]

    steer, thrust = step
    angle_to_go = update_angle_with_steer(angle, steer)
    print(angle_to_go, thrust, file=sys.stderr, flush=True)
    target_position = [x + math.sin(angle_to_go) * 1000, y + math.cos(angle_to_go) * 1000]
    outputs = map(round, np.append(target_position, thrust))
    print(position, velocity, angle, checkpoints[next_checkpoint_idx], angle_to_go, thrust, file=sys.stderr, flush=True)
    sim_pos, velocity, angle, touched_checkpoint = evaluate_game_step(position, velocity, angle, checkpoints[next_checkpoint_idx], angle_to_go, thrust)
    # outputs = map(round, [next_checkpoint_x, next_checkpoint_y, 50])
    print(*outputs, 'Get out of my way')

# print(var, file=sys.stderr, flush=True)
