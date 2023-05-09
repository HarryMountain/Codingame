import numpy as np
import pygad

from CarDriving.display_race import plot_race, plot_pod_paths
from CarDriving.game import Game


def fitness_func_maker(game):
    def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
        actions = game.convert_inputs_into_action(solution)
        path = game.run_through_game(actions, True)[0]
        score = 0
        distance_between_checkpoints = Game.get_pythagorean_distance(game.checkpoints[game.next_checkpoint], game.checkpoints[game.next_checkpoint - 1])
        distance_to_next_checkpoint = Game.get_pythagorean_distance(game.position, game.checkpoints[game.next_checkpoint])
        score += (1 - distance_to_next_checkpoint / distance_between_checkpoints) * 100
        score += 100 * game.next_checkpoint
        score -= game.time
        return score

    return fitness_func


def fit_genetic_algorithm(game):
    fitness_function = fitness_func_maker(game)

    num_generations = 5
    num_parents_mating = 4

    sol_per_pop = 10
    num_genes = 1200

    init_range_low = -1
    init_range_high = 1

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
    init_pop = ga_instance.initial_population
    paths = [game.run_through_game(game.convert_inputs_into_action(x), True)[0] for x in init_pop]
    print()
    for x in init_pop:
        path = game.run_through_game(game.convert_inputs_into_action(x), True)[0]
        plot_pod_paths(game.checkpoints, [path], 5)
        print(fitness_func_maker(game)(None, x, None))

    #plot_pod_paths(game.checkpoints, paths, 10)

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    actions = game.convert_inputs_into_action(solution)
    path, inputs = game.run_through_game(actions, True)
    plot_race(checkpoints, path, inputs)
    print(solution)
    print(solution_fitness)
    print(solution_idx)


checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
start_position = checkpoints[-1]
start_angle = Game.get_angle(start_position, checkpoints[0])
game = Game(start_position, start_angle, checkpoints)
fit_genetic_algorithm(game)
