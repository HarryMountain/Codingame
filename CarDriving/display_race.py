import math
from CarDriving.config import WIDTH, HEIGHT, CHECKPOINT_RADIUS
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

TIME_PER_FRAME = 0.05
# TIME_PER_FRAME = 1 # todo
CAR_SIZE = 400


def plot_race(checkpoints, path, inputs):
    print(len(path), len(inputs))
    fig = plt.figure(figsize=(5, 4))
    ax = plt.axes(xlim=(0, WIDTH), ylim=(0, HEIGHT))
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()

    checkpoint_icons = []
    for checkpoint in checkpoints:
        circle = plt.Circle((checkpoint[0], checkpoint[1]), CHECKPOINT_RADIUS, color='r')
        checkpoint_icons.append(circle)
    car = plt.Circle((path[0][0], path[0][1]), CAR_SIZE, color='b')
    ax.add_patch(car)

    output_template = 'steer %i thrust %i'
    output_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        for j in range(3):
            checkpoint_icons[j].center = (checkpoints[j][0], checkpoints[j][1])
            ax.add_patch(checkpoint_icons[j])
        car.center = (path[0][0], path[0][1])
        ax.add_patch(car)
        return checkpoint_icons[0], checkpoint_icons[1], checkpoint_icons[2], car, output_text

    def animate(i):
        car.center = (path[i][0], path[i][1])
        angle = int(inputs[min(i, len(inputs) - 1)][0])
        output_text.set_text(output_template % (i, angle))
        #print([[round(x, 2) for x in nn_data[i][j]] for j in range(2)]) todo
        return checkpoint_icons[0], checkpoint_icons[1], checkpoint_icons[2], car, output_text

    _ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(path), interval=TIME_PER_FRAME * 1000, blit=True)
    plt.show()


# Test display race
if __name__ == "__main__":
    checkpoints = [np.array((1000, 3000)), np.array((5000, 2000)), np.array((10000, 7000))]
    path = [[3000 + int(2000 * math.cos(i / 20)), 3000 + int(1000 * math.sin(i / 20))] for i in range(400)]
    inputs = [[12, 70] for i in range(400)]
    plot_race(checkpoints, path, inputs)
