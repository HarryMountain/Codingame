import random
import sys
import numpy as np
import math
class Game:
    def __init__(self, checkpoints):
        self.checkpoints = checkpoints
        self.thrust = 0
        self.speed = np.array([0, 0])
        self.angle = 0
        self.position = [0, 0]


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
        self.speed += facing_vector
        self.position += self.speed
        self.speed *= 0.85
        self.speed = np.trunc(self.speed)
        self.position = np.trunc(self.position)
        self.angle = round(self.angle)


checkpoint_count = int(input())  # Count of checkpoints to read
checkpoints = []
for i in range(checkpoint_count):
    # checkpoint_x: Position X
    # checkpoint_y: Position Y
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints.append([checkpoint_x, checkpoint_y])

game = Game(checkpoints)

# game loop
while True:
    # checkpoint_index: Index of the checkpoint to lookup in the checkpoints input, initially 0
    # x: Position X
    # y: Position Y
    # vx: horizontal speed. Positive is right
    # vy: vertical speed. Positive is downwards
    # angle: facing angle of this car
    checkpoint_index, x, y, vx, vy, angle = [int(i) for i in input().split()]
    print([x, y, vx, vy, angle], file=sys.stderr, flush=True)
    print([game.position[0], game.position[1], game.speed[0], game.speed[1], game.angle], file=sys.stderr, flush=True)
    game.position = [x, y]
    game.speed = [vx, vy]
    game.angle = angle
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    angle = random.randint(-18, 18)
    thrust = random.randint(0, 200)
    game.apply_action(angle, thrust)
    # X Y THRUST MESSAGE
    print(f"EXPERT {str(angle)} {str(thrust)}")
