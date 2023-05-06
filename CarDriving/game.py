import random
import sys
import numpy as np
import math

from CarDriving.config import CHECKPOINT_RADIUS


class Game:

    def __init__(self, starting_position, starting_angle, checkpoints):
        self.starting_position = starting_position
        self.starting_angle = starting_angle
        self.checkpoints = checkpoints
        self.speed = np.array([0, 0], dtype=float)
        self.angle = starting_angle
        self.position = starting_position
        self.next_checkpoint = 1
        self.time = 0

    def apply_action(self, rotation, thrust):
        self.angle += max(-18, min(18, rotation))
        if self.angle < -180:
            self.angle += 360
        elif self.angle > 180:
            self.angle -= 360
        angle_radians = math.radians(self.angle)
        facing_vector = [math.cos(angle_radians), math.sin(angle_radians)]
        facing_vector = np.array(facing_vector)
        facing_vector *= thrust
        print(self.speed, facing_vector)
        self.speed += facing_vector
        self.position = self.position + self.speed
        self.speed *= 0.85
        self.speed = np.trunc(self.speed)
        self.position = np.trunc(self.position)
        self.angle = round(self.angle)
        self.hit_checkpoint()

    def run_through_game(self, actions):
        self.reset()
        for action in actions:
            self.apply_action(action, 100)  # TODO Use thrust in genetic algorithm as well

    def hit_checkpoint(self):
        checkpoint = self.checkpoints[self.next_checkpoint]
        distance_from_checkpoint = math.sqrt((self.position[0] - checkpoint[0])**2 + (self.position[1] - checkpoint[1])**2)
        if distance_from_checkpoint <= CHECKPOINT_RADIUS:
            self.next_checkpoint += 1

    @staticmethod
    def get_angle(position, target):
        facing = [position[0] - target[0], position[1] - target[1]]
        angle = math.atan2(facing[1], facing[0])
        return math.degrees(angle)

    def reset(self):
        self.position = self.starting_position
        self.angle = self.starting_angle
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0