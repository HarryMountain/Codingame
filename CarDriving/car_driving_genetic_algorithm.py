import random

import numpy as np
import pygad
from CarDriving.config import WIDTH, HEIGHT
from CarDriving.display_race import plot_race
from CarDriving.game import Game

'''
def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
    score = 0
    score += 100 * solution[2]
    score -= solution[3]
    print(score)
    return score
'''

'''
class fitness_func:  # Solution is the inputs every game turn
    def __init__(self, game):
        self.game = game

    def __call__(self, ga_instance, solution, _solution_idx):
        score = 0
        score += 100 * solution[2]
        score -= solution[3]
        print(score)
        return score

'''


def fitness_func_maker(game):
    def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
        game.run_through_game(solution, False)
        score = 0
        score += 100 * game.next_checkpoint
        score -= game.time
        return score

    return fitness_func


def fit_genetic_algorithm(game):
    fitness_function = fitness_func_maker(game)

    num_generations = 25
    num_parents_mating = 4

    sol_per_pop = 8
    num_genes = 1200

    init_range_low = -2
    init_range_high = 5

    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes)

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    path, inputs = game.run_through_game(solution, True)
    plot_race(checkpoints, path, inputs)
    print(solution)
    print(solution_fitness)
    print(solution_idx)


# checkpoints = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)]]
checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
start_position = checkpoints[-1]
start_angle = Game.get_angle(start_position, checkpoints[0])
game = Game(start_position, start_angle, checkpoints)
fit_genetic_algorithm(game)
