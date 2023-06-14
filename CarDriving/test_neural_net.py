import tensorflow as tf

from CarDriving.codingame_run import get_nn_inputs, convert_inputs_to_actions
from CarDriving.config import races, MAX_TIMESTEPS
from CarDriving.display_race import plot_pod_paths
from CarDriving.game import Game

checkpoints = races[0]
game = Game(checkpoints)

model = tf.keras.models.load_model('driving_nn_config.h5')

positions = []
for i in range(MAX_TIMESTEPS):
    next_checkpoint = game.checkpoints[game.next_checkpoint + (1 if game.next_checkpoint < (len(game.checkpoints) - 1) else 0)]
    nn_inputs = get_nn_inputs(game.angle, game.speed, game.position, game.checkpoints[game.next_checkpoint], next_checkpoint)
    nn_outputs = model.predict([nn_inputs])
    print(nn_outputs)
    steer, thrust = convert_inputs_to_actions(nn_outputs[0])
    print(*nn_inputs)
    print(int(steer), int(thrust))
    finished = game.apply_action(steer, thrust)
    positions.append(game.position)
    if finished:
        break

plot_pod_paths(game.checkpoints, [positions], True, 100)
