import math
from copy import deepcopy

import numpy as np

from CarDriving.codingame_run import get_angle, get_pythagorean_distance
from CarDriving.config import CHECKPOINT_RADIUS, MAX_SPEED, MAX_ROUNDS, INPUTS_PER_GENE, \
    GENES_PER_CHECKPOINT


class Game:

    def __init__(self, checkpoints):
        self.checkpoints = checkpoints
        self.position = checkpoints[-1]
        self.angle = get_angle(self.position, checkpoints[0])
        self.velocity = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0
        self.effective_distance_between_current_checkpoints = self.get_effective_distance_to_checkpoint()
        self.steps_since_last_checkpoint = 0

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
        self.velocity += facing_vector
        self.position = self.position + self.velocity
        self.velocity *= 0.85
        self.velocity = np.trunc(self.velocity)
        self.position = np.trunc(self.position)
        self.angle = round(self.angle)
        self.steps_since_last_checkpoint += 1
        return self.hit_checkpoint()

    # Calculate an effective distance to next checkpoint - the actual distance plus an adjustment for current velocity
    def get_effective_distance_to_checkpoint(self):
        relative_effective_position = [self.checkpoints[self.next_checkpoint][i] - self.position[i] - 2 * self.velocity[i] for i in range(2)]
        return get_pythagorean_distance(relative_effective_position, [0, 0])

    def get_action_index(self, gene_length):
        #return max(0, min(gene_length - 2, INPUTS_PER_GENE * int(GENES_PER_CHECKPOINT * (
        #    self.next_checkpoint + 1 - self.get_effective_distance_to_checkpoint() / self.effective_distance_between_current_checkpoints))))
        return max(0, min(gene_length - INPUTS_PER_GENE, INPUTS_PER_GENE * (GENES_PER_CHECKPOINT * self.next_checkpoint + self.steps_since_last_checkpoint)))

    def run_through_game(self, actions, record_nn_fit_data):
        self.reset()
        positions = []
        checks = []
        angles = []
        velocities = []
        inputs = []

        self.time = len(actions) // 2
        for i in range(MAX_ROUNDS):
            action_index = self.get_action_index(len(actions))
            #print('Action index', action_index)
            angle, thrust = actions[action_index], actions[action_index + 1]
            #print('Generated inputs: ', action_index, angle, thrust)
            # Record data
            positions.append(self.position)
            checks.append(self.next_checkpoint)
            if record_nn_fit_data:
                angles.append(self.angle)
                velocities.append(self.velocity)
                inputs.append([angle, thrust])
            old_position = deepcopy(self.position)
            finished = self.apply_action(angle, thrust)
            #print('Generated position: ', self.position)
            if finished:
                # Hit the last checkpoint. Add the fraction of the last timestep needed to get to the end
                self.time = i // 2 - 1
                distance_to_checkpoint = get_pythagorean_distance(old_position, self.checkpoints[self.next_checkpoint - 1]) - CHECKPOINT_RADIUS
                self.time += distance_to_checkpoint / get_pythagorean_distance([0, 0], self.velocity)
                break
        return (positions, checks, angles, velocities, inputs) if record_nn_fit_data else (positions, checks)

    def hit_checkpoint(self):
        checkpoint = self.checkpoints[self.next_checkpoint % len(self.checkpoints)]
        distance_from_checkpoint = math.sqrt((self.position[0] - checkpoint[0])**2 + (self.position[1] - checkpoint[1])**2)
        if distance_from_checkpoint <= CHECKPOINT_RADIUS:
            self.next_checkpoint += 1
            self.steps_since_last_checkpoint = 0
            if self.next_checkpoint == len(self.checkpoints):
                return True
        return False

    def reset(self):
        self.position = self.checkpoints[-1]
        self.angle = get_angle(self.position, self.checkpoints[0])
        self.velocity = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0
        self.effective_distance_between_current_checkpoints = self.get_effective_distance_to_checkpoint()
        self.steps_since_last_checkpoint = 0
