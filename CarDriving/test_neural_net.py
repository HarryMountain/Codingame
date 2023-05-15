import numpy as np
import tensorflow as tf

from CarDriving.config import races
from CarDriving.display_race import plot_pod_paths
from CarDriving.game import Game

checkpoints = races[1]
game = Game(checkpoints)

model = tf.keras.models.load_model('driving_nn_config.h5')

positions = []
for i in range(100):  # todo
    speed_angle = Game.get_relative_angle(Game.get_angle([0, 0], game.speed), game.angle)
    speed_magnitude = Game.get_pythagorean_distance([0, 0], game.speed)
    next_checkpoint_angle = Game.get_relative_angle(Game.get_angle(game.position, game.checkpoints[game.next_checkpoint]),
                                                    game.angle)
    next_checkpoint_distance = Game.get_pythagorean_distance(game.position, game.checkpoints[game.next_checkpoint])
    angle, thrust = model.predict(np.expand_dims([speed_angle, speed_magnitude, next_checkpoint_angle, next_checkpoint_distance, next_checkpoint_angle, next_checkpoint_distance * 2], 0))[0]  # todo
    # outputs = model.predict(
    #     np.expand_dims([speed_angle, speed_magnitude, next_checkpoint_angle, next_checkpoint_distance], 0))
    print(int(speed_angle), int(speed_magnitude), int(next_checkpoint_angle), int(next_checkpoint_distance))
    print(int(angle), int(thrust))
    finished = game.apply_action(angle, thrust)
    positions.append(game.position)
    if finished:
        break

plot_pod_paths(game.checkpoints, [positions], True, 100)
