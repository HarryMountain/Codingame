import math

import numpy as np

from CarDriving.config import CHECKPOINT_RADIUS


class Game:

    def __init__(self, checkpoints):
        self.checkpoints = checkpoints
        self.position = checkpoints[-1]
        self.angle = Game.get_angle(self.position, checkpoints[0])
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0

    def apply_action(self, rotation, thrust):
        self.angle += max(-18, min(18, rotation))
        if self.angle < -180:
            self.angle += 360
        elif self.angle > 180:
            self.angle -= 360
        thrust = max(0, min(200, thrust))
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
            finished = self.apply_action(angle, thrust)
            # Record data
            positions.append(self.position)
            checks.append(self.next_checkpoint)
            if record_nn_fit_data:
                angles.append(self.angle)
                speeds.append(self.speed)
                inputs.append([angle, thrust])
            if finished:
                self.time = i // 2
                break
        return (positions, checks, angles, speeds, inputs) if record_nn_fit_data else (positions, checks)

    def hit_checkpoint(self):
        checkpoint = self.checkpoints[self.next_checkpoint % len(self.checkpoints)]  # TODO Stop after all checkpoints
        distance_from_checkpoint = math.sqrt((self.position[0] - checkpoint[0])**2 + (self.position[1] - checkpoint[1])**2)
        if distance_from_checkpoint <= CHECKPOINT_RADIUS:
            self.next_checkpoint += 1
            if self.next_checkpoint == len(self.checkpoints):
                return True
        return False


    @staticmethod
    def get_angle(position, target):
        facing = [target[0] - position[0], target[1] - position[1]]
        angle = math.atan2(facing[1], facing[0])
        return math.degrees(angle)

    @staticmethod
    def get_relative_angle(target_angle, facing_angle):
        angle = ((target_angle - facing_angle + 180) % 360) - 180
        return angle

    @staticmethod
    def get_pythagorean_distance(position, target):
        return math.sqrt((target[0] - position[0])**2 + (target[1] - position[1])**2)

    @staticmethod
    def convert_inputs_to_actions(inputs):
        actions = [(inputs[i] * 18) if i % 2 == 0 else ((inputs[i] + 1) * 100) for i in range(len(inputs))]
        return actions

    @staticmethod
    def convert_actions_to_inputs(actions):
        inputs = [(actions[i] / 18) if i % 2 == 0 else (actions[i] / 100 - 1) for i in range(len(actions))]
        return inputs

    def reset(self):
        self.position = self.checkpoints[-1]
        self.angle = Game.get_angle(self.position, self.checkpoints[0])
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0
