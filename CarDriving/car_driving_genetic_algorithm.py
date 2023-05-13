import numpy as np
import pygad

from CarDriving.config import NUM_GENES
from CarDriving.display_race import plot_race, plot_pod_paths
from CarDriving.game import Game


def fitness_func_maker(game, write_out):
    def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
        actions = game.convert_inputs_into_action(solution)
        path, inputs, checks = game.run_through_game(actions, True)
        score = 0
        score_from_dist_to_next_check = 0
        for i in range(len(path)):
            pos = path[i]
            check = checks[i]
            if check == game.next_checkpoint and check < len(game.checkpoints):
                distance_between_checkpoints = Game.get_pythagorean_distance(game.checkpoints[check],
                                                                             game.checkpoints[check - 1])
                distance_to_next_checkpoint = Game.get_pythagorean_distance(pos, game.checkpoints[check])
                score_from_dist_to_next_check = max(score_from_dist_to_next_check, (
                            1 - distance_to_next_checkpoint / distance_between_checkpoints) * 100)
                if i == len(path) - 1:
                    # score += 100 / (1 + distance_to_next_checkpoint / distance_between_checkpoints)
                    if write_out:
                        print('Distance to next checkpoint score : ' + str(score))
                if write_out:
                    print(pos, check, int(distance_to_next_checkpoint), i)
        score += score_from_dist_to_next_check
        if write_out:
            print('Closest approach to next checkpoint score : ' + str(score_from_dist_to_next_check))

        score += 100 * game.next_checkpoint
        score -= game.time

        if write_out:
            print('Checkpoints score : ' + str(100 * game.next_checkpoint))
            print('Game time score : ' + str(-game.time))
            # breakpoint()
            print('Total score : ' + str(score))
        return score

    return fitness_func


# def generate_initial_population(checkpoints, start_position, start_angle):

# Run the race pointing at the next checkpoint
# inputs = []
# position =


def fit_genetic_algorithm(game):
    fitness_function = fitness_func_maker(game, False)

    num_genes = NUM_GENES
    init_range_low = -1
    init_range_high = 1
    gene_space = {'low': -1, 'high': 1}

    num_generations = 200
    num_parents_mating = 20
    sol_per_pop = 100

    parent_selection_type = "sss"
    keep_parents = 3
    crossover_type = "uniform"
    mutation_type = "scramble"
    mutation_percent_genes = 2

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
                           mutation_percent_genes=mutation_percent_genes,
                           gene_space=gene_space)

    ga_instance.run()
    ga_instance.plot_fitness()
    init_pop = ga_instance.initial_population
    for x in init_pop:
        # path = game.run_through_game(game.convert_inputs_into_action(x), True)[0]
        # plot_pod_paths(game.checkpoints, [path], True, 5)
        print(fitness_func_maker(game, False)(None, x, None))

    # Plot initial population
    # paths = [game.run_through_game(game.convert_inputs_into_action(x), True)[0] for x in init_pop]
    # plot_pod_paths(game.checkpoints, paths, 10)

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(solution_fitness)
    actions = game.convert_inputs_into_action(solution)

    print(fitness_func_maker(game, True)(None, solution, None))

    path, inputs, checks = game.run_through_game(actions, True)
    # plot_race(checkpoints, path, inputs)
    plot_pod_paths(game.checkpoints, [path], True, 500)
    print(solution)
    print(actions)
    print(solution_fitness)
    print(solution_idx)

    # Plot final population
    # paths = [game.run_through_game(game.convert_inputs_into_action(x), True)[0] for x in ga_instance.population]
    # plot_pod_paths(game.checkpoints, paths, True, 5000)

    # for x in ga_instance.population:
    # path = game.run_through_game(game.convert_inputs_into_action(x), True)[0]
    # plot_pod_paths(game.checkpoints, [path], True, 5)
    # print(fitness_func_maker(game)(None, x, None))


checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
#checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
start_position = checkpoints[-1]
start_angle = Game.get_angle(start_position, checkpoints[0])
game = Game(start_position, start_angle, checkpoints)
fit_genetic_algorithm(game)
