import tensorflow as tf

from CarDriving.codingame_run import get_nn_inputs, convert_inputs_to_actions
from CarDriving.config import races, NUM_GENES
from CarDriving.display_race import plot_pod_paths, plot_race
from CarDriving.game import Game
from CarDriving.neural_net import create_nn_from_json

checkpoints = races[0]
game = Game(checkpoints)

nn_from_file = create_nn_from_json('saved_nn.json')

positions = []
inputs = []
next_checkpoints = []
for i in range(NUM_GENES):
    next_checkpoint = game.checkpoints[game.next_checkpoint + (1 if game.next_checkpoint < (len(game.checkpoints) - 1) else 0)]
    nn_inputs = get_nn_inputs(game.angle, game.speed, game.position, game.checkpoints[game.next_checkpoint], next_checkpoint)
    nn_outputs = nn_from_file.evaluate(nn_inputs)
    print(nn_outputs)
    steer, thrust = convert_inputs_to_actions(nn_outputs)
    print(*nn_inputs)
    print(int(steer), int(thrust))
    finished = game.apply_action(steer, thrust)
    positions.append(game.position)
    inputs.append([steer, thrust])
    next_checkpoints.append(game.next_checkpoint)
    if finished:
        break

plot_race(game.checkpoints, positions, inputs, next_checkpoints)
#plot_pod_paths(game.checkpoints, [positions], True, 100)
