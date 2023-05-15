import os

import matplotlib.pyplot as plt

# iterate over files in the directory of fitting data to get training data
x_train = []
y_train = []
target_angles = []
steer_angles = []
directory = 'training_data'
for filename in os.listdir(directory):
# for filename in ['nn_fit_data_5']:
    file = os.path.join(directory, filename)
    with open(file, 'r') as f:
        for line in f:
            line = line.rstrip().split(',')
            values = [float(x) for x in line]
            x_train.append(values[:6])
            y_train.append(values[6:])
            target_angles.append(values[2])
            steer_angles.append(values[6])

plt.scatter(target_angles, steer_angles)
plt.show()
