import matplotlib.pyplot as plt
import matplotlib.animation as animation

X_MAX = 16000
Y_MAX = 9000
POD_SIZE = 500
CHECKPOINT_SIZE = 300
TIME_PER_FRAME = 0.01


def plot_pod_race(checkpoints, path):
    fig = plt.figure(figsize=(5, 4))
    ax = plt.axes(xlim=(0, X_MAX), ylim=(0, Y_MAX))
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()

    checkpoint_icons = []
    for checkpoint in checkpoints:
        circle = plt.Circle((checkpoint[0], checkpoint[1]), CHECKPOINT_SIZE, color='r')
        checkpoint_icons.append(circle)
    pod = plt.Circle((path[0][0], path[0][1]), POD_SIZE, color='b')
    ax.add_patch(pod)

    time_template = 'round %i'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        for j in range(3):
            checkpoint_icons[j].center = (checkpoints[j][0], checkpoints[j][1])
            ax.add_patch(checkpoint_icons[j])
        pod.center = (path[0][0], path[0][1])
        ax.add_patch(pod)
        return checkpoint_icons[0], checkpoint_icons[1], checkpoint_icons[2], pod, time_text

    def animate(i):
        pod.center = (path[i][0], path[i][1])
        time_text.set_text(time_template % i)
        return checkpoint_icons[0], checkpoint_icons[1], checkpoint_icons[2], pod, time_text

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(path), interval=TIME_PER_FRAME * 1000, blit=True)
    plt.show()


checkpoints = [
    [9000, 1000],
    [14000, 5000],
    [4000, 3000]
]
path = []
for i in range(100):
    path.append([i * 50 + 2000, -25 * i + 6000])
plot_pod_race(checkpoints, path)
