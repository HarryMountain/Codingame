import random

train_inputs = []
train_outputs = []
for i in range(1000):
    this_target_distance = random.randint(1, 8000)
    this_target_angle = random.randint(-180, 180)
    next_target_distance = random.randint(1, 8000)
    next_target_angle = random.randint(-180, 180)

    direction = this_target_angle
    thrust = min(100, this_target_distance // 20)

    train_inputs.append([this_target_distance, this_target_angle, next_target_distance, next_target_angle])
    train_outputs.append([direction, thrust])

for i in range(100):
    print(*(train_inputs[i] + train_outputs[i]))
