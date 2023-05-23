import math
from copy import deepcopy

import numpy as np

from CarDriving.codingame_run import get_angle, get_pythagorean_distance
from CarDriving.config import CHECKPOINT_RADIUS, MAX_SPEED


class Game:

    def __init__(self, checkpoints):
        self.checkpoints = checkpoints
        self.position = checkpoints[-1]
        self.angle = get_angle(self.position, checkpoints[0])
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0

    def apply_action(self, rotation, thrust):

        self.angle += max(-18, min(18, rotation))
        if self.angle < -180:
            self.angle += 360
        elif self.angle > 180:
            self.angle -= 360
        thrust = max(0, min(MAX_SPEED, thrust))
        angle_radians = math.radians(self.angle)
        facing_vector = [math.cos(angle_radians), math.sin(angle_radians)]
        facing_vector = np.array(facing_vector)
        facing_vector *= thrust
        self.speed += facing_vector
        self.position = self.position + self.speed
        self.speed *= 0.85
        self.speed = np.trunc(self.speed)
        self.position = np.trunc(self.position)
        self.angle = round(self.angle)
        return self.hit_checkpoint()

    def run_through_game(self, actions, record_nn_fit_data):
        self.reset()
        positions = []
        checks = []
        angles = []
        speeds = []
        inputs = []

        self.time = len(actions) // 2
        for i in range(0, len(actions), 2):
            angle, thrust = actions[i], actions[i + 1]
            # Record data
            positions.append(self.position)
            checks.append(self.next_checkpoint)
            if record_nn_fit_data:
                angles.append(self.angle)
                speeds.append(self.speed)
                inputs.append([angle, thrust])
            old_position = deepcopy(self.position)
            finished = self.apply_action(angle, thrust)
            if finished:
                # Hit the last checkpoint. Add the fraction of the last timestep needed to get to the end
                self.time = i // 2 - 1
                distance_to_checkpoint = get_pythagorean_distance(old_position, self.checkpoints[self.next_checkpoint - 1]) - CHECKPOINT_RADIUS
                self.time += distance_to_checkpoint / get_pythagorean_distance([0, 0], self.speed)
                break
        return (positions, checks, angles, speeds, inputs) if record_nn_fit_data else (positions, checks)

    def hit_checkpoint(self):
        checkpoint = self.checkpoints[self.next_checkpoint % len(self.checkpoints)]
        distance_from_checkpoint = math.sqrt((self.position[0] - checkpoint[0])**2 + (self.position[1] - checkpoint[1])**2)
        if distance_from_checkpoint <= CHECKPOINT_RADIUS:
            self.next_checkpoint += 1
            if self.next_checkpoint == len(self.checkpoints):
                return True
        return False

    def reset(self):
        self.position = self.checkpoints[-1]
        self.angle = get_angle(self.position, self.checkpoints[0])
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0
