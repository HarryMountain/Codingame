import math
import random

import pygad

from CarDriving.codingame_run import get_pythagorean_distance, get_relative_angle, convert_inputs_to_actions, \
    convert_actions_to_inputs, get_nn_inputs, get_angle
from CarDriving.config import RACES, INPUTS_PER_CHECKPOINT, MAX_ROUNDS
from CarDriving.display_race import plot_pod_paths, plot_race
from CarDriving.game import Game

CURRENT_COURSE = 2


def fitness_func_maker(game, write_out):
    def fitness_func(_ga_instance, solution, _solution_idx):  # Solution is the inputs every game turn
        path, next_checkpoints = game.run_through_game(convert_inputs_to_actions(solution), False)
        score = 0
        score_from_dist_to_next_check = 0
        for i in range(len(path)):
            pos = path[i]
            next_checkpoint = next_checkpoints[i]
            if next_checkpoint == game.next_checkpoint and next_checkpoint < len(game.checkpoints):
                distance_between_checkpoints = get_pythagorean_distance(game.checkpoints[next_checkpoint],
                                                                        game.checkpoints[next_checkpoint - 1])
                distance_to_next_checkpoint = get_pythagorean_distance(pos, game.checkpoints[next_checkpoint])
                score_from_dist_to_next_check = max(score_from_dist_to_next_check, (
                        1 - distance_to_next_checkpoint / distance_between_checkpoints) * 100)
                if i == len(path) - 1:
                    if write_out:
                        print('Distance to next checkpoint score : ' + str(score))
                if write_out:
                    print(pos, next_checkpoint, int(distance_to_next_checkpoint), i)
        score += score_from_dist_to_next_check
        if write_out:
            print('Closest approach to next checkpoint score : ' + str(score_from_dist_to_next_check))

        score += 100 * game.next_checkpoint
        score -= game.time

        if write_out:
            print('Checkpoints score : ' + str(100 * game.next_checkpoint))
            print('Game time score : ' + str(-game.time))
            print('Total score : ' + str(score))
        return score

    return fitness_func


def generate_seed_population(population_size, checkpoints, gene_length):
    # TODO  : adapt this to new gene definition
    # Run the race pointing at the next checkpoint
    population = []
    for item in range(population_size):
        game = Game(checkpoints)
        gene = []
        finished = False
        these_positions = [game.position]
        these_actions = []
        action_vector = []
        for i in range(MAX_ROUNDS):
            if not finished:
                angle = max(-18, min(18, get_relative_angle(
                    get_angle(game.position, game.checkpoints[game.next_checkpoint]), game.angle) + random.randint(-10, 10)))
                thrust = random.randint(20, 150)
                action_index = game.get_action_index(gene_length)
                # print(i, action_index)
                for j in range(len(gene), action_index, 2):
                    gene.extend(convert_actions_to_inputs([angle, thrust]))
                    action_vector.append([angle, thrust])
                these_actions.append([action_index, angle, thrust])
                finished = game.apply_action(angle, thrust)
                these_positions.append(game.position)
                print(action_index, angle, thrust, these_actions[-3:])
                print(gene[-10:])
            else:
                gene.extend(gene[-2:])
        #print(' Path', these_positions)  # todo
        #print(' Actions', these_actions)  # todo
        #print(' Actions', action_vector)  # todo
        print(these_positions)
        population.append(gene[:gene_length])
    return population


def fit_genetic_algorithm(game):
    # Gene configuration
    gene_length = INPUTS_PER_CHECKPOINT * len(game.checkpoints)
    population_size = 1 # todo
    init_range_low = 0
    init_range_high = 1
    gene_space = {'low': 0, 'high': 1}

    # Evolution configuration
    num_generations = 200  # todo
    num_parents_mating = 16
    parent_selection_type = "sss"
    keep_elitism = 15
    crossover_type = 'single_point' # None  # 'scattered'
    # crossover_type = None todo
    mutation_type = "adaptive"
    mutation_probability = [0.1, 0.01]

    def on_generation(_ga_instance):
        _solution, _solution_fitness, _solution_idx = _ga_instance.best_solution()
        print('Gens : ' + str(_ga_instance.generations_completed) + '. Fitness : ' + str(_solution_fitness))
        print(sorted(_ga_instance.previous_generation_fitness, reverse=True))
        paths = [game.run_through_game(convert_inputs_to_actions(x), True)[0] for x in _ga_instance.population]
        plot_pod_paths(game.checkpoints, paths, True, 30)
        #for path in paths:
        #    plot_pod_paths(game.checkpoints, [path], True, 0.5)
        #plot_pod_paths(game.checkpoints, [paths[0]], True, 0.5)

    # Create initial population
    seed_population = generate_seed_population(population_size, game.checkpoints, gene_length)
    # Plot best seed path
    fitness = [fitness_func_maker(game, False)(None, x, None) for x in seed_population]
    print(sorted(fitness, reverse=True))
    seed_inputs = [x for _, x in sorted(zip(fitness, seed_population), reverse=True)][:10]
    # for seed_input in seed_inputs:
    #    print(fitness_func_maker(game, True)(None, seed_input, None))
    paths = [game.run_through_game(convert_inputs_to_actions(x), True)[0] for x in seed_inputs]
    print('Run paths', paths[0])
    #plot_pod_paths(game.checkpoints, paths, True, 30)
    plot_pod_paths(game.checkpoints, [paths[0]], True, 30)
    print(paths[0])

    # Generate GA
    fitness_function = fitness_func_maker(game, False)
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=population_size,
                           initial_population=seed_population,
                           num_genes=gene_length,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           crossover_type=crossover_type,
                           keep_elitism=keep_elitism,
                           mutation_type=mutation_type,
                           mutation_probability=mutation_probability,
                           random_mutation_min_val=-0.1,
                           random_mutation_max_val=0.1,
                           gene_space=gene_space,
                           on_generation=on_generation)
    print(ga_instance.summary())
    ga_instance.run()
    ga_instance.plot_fitness()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    actions = convert_inputs_to_actions(solution)

    print(fitness_func_maker(game, True)(None, solution, None))

    path, checks = game.run_through_game(actions, False)
    plot_pod_paths(game.checkpoints, [path], True, 500)
    #print(solution)
    #print(actions)
    #print(solution_fitness)
    #print(solution_idx)

    # Plot final population
    # paths = [game.run_through_game(convert_inputs_into_action(x), True)[0] for x in ga_instance.population]
    # plot_pod_paths(game.checkpoints, paths, True, 5000)

    # for x in ga_instance.population:
    # path = game.run_through_game(game.convert_inputs_into_action(x), True)[0]
    # plot_pod_paths(game.checkpoints, [path], True, 5)
    # print(fitness_func_maker(game)(None, x, None))

    # Only get the part of the path to the end
    return solution[:(math.ceil(game.time) * 2)]


# checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
# checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000)),
#               np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000)),
#               np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
current_game = Game(RACES[CURRENT_COURSE])
best_solution = fit_genetic_algorithm(current_game)


# Write out the NN inputs and outputs
actions = convert_inputs_to_actions(best_solution)
positions, checks, angles, speeds, inputs = current_game.run_through_game(actions, True)

# Show driving
display_actions = [[actions[i], actions[i + 1]] for i in range(0, len(actions), 2)]
plot_race(current_game.checkpoints, positions, display_actions, checks)

"""
checkpoint_angles = []
steers = []
for i in range(len(positions)):
    if checks[i] < len(game.checkpoints):
        checkpoint_angles.append(Game.get_relative_angle(Game.get_angle(positions[i], game.checkpoints[checks[i]]), angles[i]))
        steers.append(inputs[i][0])
plt.scatter(checkpoint_angles, steers)
plt.show()
"""

with open('training_data/nn_fit_data_new_' + str(CURRENT_COURSE), 'w') as f:
    number_of_checkpoints = len(current_game.checkpoints)
    for i in range(len(positions)):
        if checks[i] < number_of_checkpoints:
            next_checkpoint = current_game.checkpoints[
                checks[i] + (1 if checks[i] < (number_of_checkpoints - 1) else 0)]
            nn_data = get_nn_inputs(angles[i], speeds[i], positions[i], current_game.checkpoints[checks[i]], next_checkpoint)
            outputs = convert_actions_to_inputs(inputs[i])
            nn_data.extend(outputs)
            f.write(','.join(map(str, nn_data)) + '\n')

# 0 746     816
# 1 749     730
# 2 1668
# 3 1873
# 4