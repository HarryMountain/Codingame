import random

import numpy as np
import pygad

from CarDriving.config import NUM_GENES, races
from CarDriving.display_race import plot_pod_paths
from CarDriving.game import Game

CURRENT_COURSE = 0


def fitness_func_maker(game, write_out):
    def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
        actions = game.convert_inputs_to_actions(solution)
        path, checks = game.run_through_game(actions, False)
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


def generate_seed_population(population_size, checkpoints):
    # Run the race pointing at the next checkpoint
    population = []
    for thrust in random.sample(range(10, 150), population_size):
    #for solution_idx in range(population_size):
        game = Game(checkpoints)
        inputs = []
        finished = False
        for i in range(NUM_GENES // 2):
            if not finished:
                angle = max(-18, min(18, Game.get_relative_angle(Game.get_angle(game.position, game.checkpoints[game.next_checkpoint]), game.angle)))
                inputs.extend(Game.convert_actions_to_inputs([angle, thrust]))
                finished = game.apply_action(angle, thrust)
            else:
                inputs.extend(inputs[-2:])
        population.append(inputs)
    return population


def fit_genetic_algorithm(game):
    fitness_function = fitness_func_maker(game, False)

    num_genes = NUM_GENES
    init_range_low = -1
    init_range_high = 1
    gene_space = {'low': -1, 'high': 1}

    num_generations = 10  # todo
    num_parents_mating = 20
    population_size = 100

    parent_selection_type = "sss"
    keep_parents = 3
    crossover_type = "uniform"
    mutation_type = "scramble"
    mutation_percent_genes = 2

    def on_generation(ga_instance):
        print(ga_instance.generations_completed)

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=population_size,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           gene_space=gene_space, on_generation=on_generation)

    # Get initial population and override the first few elements with our generated paths
    init_pop = ga_instance.initial_population
    seed_population = generate_seed_population(population_size, checkpoints)
    fitness = [fitness_func_maker(game, False)(None, x, None) for x in seed_population]
    seed_inputs = seed_population[np.array(fitness).argmax()]
    for i in range(NUM_GENES):
        init_pop[0][i] = seed_inputs[i]

    for x in init_pop:
        # path = game.run_through_game(game.convert_inputs_into_action(x), True)[0]
        # plot_pod_paths(game.checkpoints, [path], True, 5)
        print(fitness_func_maker(game, False)(None, x, None))

    ga_instance.run()
    ga_instance.plot_fitness()

    # Plot initial population
    # paths = [game.run_through_game(game.convert_inputs_into_action(x), True)[0] for x in init_pop]
    # plot_pod_paths(game.checkpoints, paths, 10)

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(solution_fitness)
    actions = game.convert_inputs_to_actions(solution)

    print(fitness_func_maker(game, True)(None, solution, None))

    path, checks = game.run_through_game(actions, False)
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

    # Only get the part of the path to the end
    return solution[:game.time]


#checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
checkpoints = races[CURRENT_COURSE]
game = Game(checkpoints)
best_solution = fit_genetic_algorithm(game)

# Write out the NN inputs and outputs
actions = game.convert_inputs_to_actions(best_solution)
positions, checks, angles, speeds, inputs = game.run_through_game(actions, True)
with open('training_data/nn_fit_data_' + str(CURRENT_COURSE), 'w') as f:
    # 1. angle of the speed
    # 2. magnitude of the speed
    # 3. Angle to next checkpoint
    # 4. Distance to next checkpoint
    for i in range(len(positions)):
        if checks[i] < len(checkpoints):
            speed_angle = Game.get_relative_angle(Game.get_angle(speeds[i], [0, 0]), angles[i])
            speed_magnitude = Game.get_pythagorean_distance([0, 0], speeds[i])
            next_checkpoint_angle = Game.get_relative_angle(Game.get_angle(positions[i], game.checkpoints[checks[i]]), angles[i])
            next_checkpoint_distance = Game.get_pythagorean_distance(positions[i], game.checkpoints[checks[i]])
            f.write(','.join(map(str, [speed_angle, speed_magnitude, next_checkpoint_angle, next_checkpoint_distance, inputs[i][0], inputs[i][1]])) + '\n')
