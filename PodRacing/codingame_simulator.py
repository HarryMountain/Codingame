import sys
import math
import random

MAX_STEER_PER_TURN = math.radians(18)
FULL_CIRCLE = math.radians(360)
HALF_CIRCLE = math.radians(180)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

sim_x = 0
sim_y = 0
sim_vx = 0
sim_vy = 0
i = 0
last_thrust = -1
angle = 0


def get_angle(x, y):
    return math.atan2(x, y)


def update_angle(x, y, angle):
    new_angle = get_angle(x, y)
    print("Angle  : " + str(math.degrees(angle)) + "  New angle : " + str(math.degrees(new_angle)), file=sys.stderr,
          flush=True)
    clockwise = new_angle - angle + (FULL_CIRCLE if new_angle < angle else 0)
    anticlockwise = angle - new_angle + (FULL_CIRCLE if new_angle > angle else 0)
    if anticlockwise < clockwise:
        new_angle = angle - min(MAX_STEER_PER_TURN, anticlockwise)
        print("Anticlocklwise. Old : " + str(angle) + "  New : " + str(new_angle), file=sys.stderr, flush=True)
        if new_angle < -HALF_CIRCLE:
            new_angle += FULL_CIRCLE
            print("Updated new angle adding " + str(FULL_CIRCLE) + " to " + str(new_angle), file=sys.stderr, flush=True)
    else:
        new_angle = angle + min(MAX_STEER_PER_TURN, clockwise)
        if new_angle > HALF_CIRCLE:
            new_angle -= FULL_CIRCLE
    return new_angle


# game loop
thrust = 0
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    if i == 0:
        sim_x = x
        sim_y = y
        dx = next_checkpoint_x - x
        dy = next_checkpoint_y - y
        target_x = next_checkpoint_x
        target_y = next_checkpoint_y
        angle = get_angle(dx, dy)
        print(math.degrees(angle), file=sys.stderr, flush=True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print("x : " + str(x) + "   sim_x : " + str(sim_x) + "  y : " + str(y) + "   sim_y : " + str(sim_y),
          file=sys.stderr, flush=True)
    print(x == sim_x, file=sys.stderr, flush=True)
    print(y == sim_y, file=sys.stderr, flush=True)
    print(next_checkpoint_x, next_checkpoint_y, file=sys.stderr, flush=True)

    thrust = random.randint(50, 100)
    thrust = 90
    target_x = next_checkpoint_x
    target_y = next_checkpoint_y

    output = [target_x, target_y, thrust]

    # Work out distances
    dx = target_x - x
    dy = target_y - y

    # Calculate New Angle
    angle = update_angle(dx, dy, angle)
    print("Angle : " + str(math.degrees(angle)), file=sys.stderr, flush=True)

    # Calculate Thrusts
    thrust_x = thrust * math.sin(angle)
    thrust_y = thrust * math.cos(angle)
    print("thrust_x : " + str(thrust_x) + "   thrust_y : " + str(thrust_y), file=sys.stderr, flush=True)

    # Update Speed
    sim_vx += thrust_x
    sim_vy += thrust_y
    print("sim_vx : " + str(sim_vx) + "   sim_vy : " + str(sim_vy), file=sys.stderr, flush=True)

    # Move
    sim_x = round(sim_x + sim_vx)
    sim_y = round(sim_y + sim_vy)

    # Apply Drag
    sim_vx = math.trunc(0.85 * sim_vx)
    sim_vy = math.trunc(0.85 * sim_vy)

    # print(math.trunc(sim_vx), math.trunc(sim_vy), file=sys.stderr, flush=True)
    print(sim_vx, sim_vy, file=sys.stderr, flush=True)
    last_thrust = thrust

    i += 1

    print(*output, 'Pod go BRRRR')