import random
import sys
import numpy as np
import math

HEIGHT = 9000
WIDTH = 16000
CHECKPOINT_RADIUS = 600

class Game:

    def __init__(self, starting_position, starting_angle, checkpoints):
        self.starting_position = starting_position
        self.starting_angle = starting_angle
        self.checkpoints = checkpoints
        self.speed = np.array([0, 0], dtype=float)
        self.angle = starting_angle
        self.position = starting_position
        self.next_checkpoint = 0
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
        # print(self.speed, facing_vector)
        self.speed += facing_vector
        self.position += self.speed
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
        print([checkpoint, distance_from_checkpoint], file=sys.stderr, flush=True)
        if distance_from_checkpoint <= CHECKPOINT_RADIUS:
            self.next_checkpoint += 1

    def reset(self):
        self.position = self.starting_position
        self.angle = self.starting_angle
        self.speed = np.array([0, 0], dtype=float)
        self.next_checkpoint = 0
        self.time = 0


checkpoint_count = int(input())  # Count of checkpoints to read
checkpoints = []
for i in range(checkpoint_count):
    # checkpoint_x: Position X
    # checkpoint_y: Position Y
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints.append([checkpoint_x, checkpoint_y])

print(checkpoints, file=sys.stderr, flush=True)

game = Game(checkpoints[-1], 0, checkpoints)

# game loop
while True:
    # checkpoint_index: Index of the checkpoint to lookup in the checkpoints input, initially 0
    # x: Position X
    # y: Position Y
    # vx: horizontal speed. Positive is right
    # vy: vertical speed. Positive is downwards
    # angle: facing angle of this car
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
    print([checkpoint_index, x, y, vx, vy, angle], file=sys.stderr, flush=True)
    print([game.next_checkpoint, game.position[0], game.position[1]], file=sys.stderr, flush=True)
    game.angle = angle
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # angle = random.randint(-18, 18)
    angle = 0
    thrust = random.randint(0, 200)
    game.apply_action(angle, thrust)
    # X Y THRUST MESSAGE
    print(f"EXPERT {str(angle)} {str(thrust)}")