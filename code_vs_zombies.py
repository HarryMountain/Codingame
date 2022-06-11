import sys
import math
import numpy as np
# Save humans, destroy zombies!

# game loop
FIBBONACCI_SEQUENCE = [1, 2]

for i in range(100):
    FIBBONACCI_SEQUENCE.append(FIBBONACCI_SEQUENCE[-2] + FIBBONACCI_SEQUENCE[-1])


def get_distance(pos_1, pos_2):
    vector = pos_1 - pos_2
    return round(math.sqrt(vector.dot(vector)))


class GameState:
    def __init__(self, ash_pos, zombies, humans):
        self.ash_pos = ash_pos
        self.zombies = zombies
        self.humans = humans
        self.zombie_targets = []

    def move_zombies(self):
        self.zombie_targets = []
        zombie_moves = []
        for zombie in self.zombies:
            best_human = -1
            best_human_dist = -1
            for human in self.humans + [self.ash_pos]:
                distance = math.sqrt((zombie[0] - human[0]) ** 2 + (zombie[1] - human[1]) ** 2)
                if distance < best_human_dist or best_human_dist == -1:
                    best_human = human
                    best_human_dist = distance
            self.zombie_targets.append(best_human)
            # total_dist_to_human = math.sqrt((zombie[0] - best_human[0]) ** 2 + (zombie[1] - best_human[1]) ** 2)
            total_dist_to_human = get_distance(zombie, best_human)
            zombie_moves = np.array(((best_human[0] - zombie[0]) * 400 / total_dist_to_human,
                                    (best_human[1] - zombie[1]) * 400 / total_dist_to_human))
        for i in range(len(self.zombies)):
            zombie = self.zombies[i]
            move = zombie_moves[i]
            zombies[i] = zombie + move

    def update(self, move):
        self.ash_pos += move
        zombies_killed = []
        score = 0
        humans_alive_score = (len(self.humans)**2) * 10
        for i in range(len(self.zombies)):
            zombie = self.zombies[i]
            print(self.ash_pos, zombie, file=sys.stderr, flush=True)
            print(get_distance(self.ash_pos, zombie), file=sys.stderr, flush=True)
            if get_distance(self.ash_pos, zombie) <= 2000:
                zombies_killed.append(zombie)
            elif get_distance(zombie, self.zombie_targets[i]) < 400:
                self.zombies[i] = self.zombie_targets[i]
                self.humans.remove(self.zombie_targets[i])
        for i in range(len(zombies_killed)):
            self.zombies.remove(zombies_killed[i])
            score += humans_alive_score * FIBBONACCI_SEQUENCE[i]
        print(zombies_killed, file=sys.stderr, flush=True)
        return score


while True:
    humans = []
    zombies = []
    human_positions = []
    zombie_positions = []
    ash_x, ash_y = [int(i) for i in input().split()]
    ash_position = np.array((ash_x, ash_y))
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans.append([human_id, human_x, human_y])
        human_positions.append(np.array((human_x, human_y)))
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombies.append([zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext])
        zombie_positions.append(np.array((zombie_x, zombie_y)))

    # Write an action using print
    # Simple start - go for the closest Zombie
    closest_distance = -1
    target = None
    for zombie_position in zombie_positions:
        distance = get_distance(ash_position, zombie_position)
        if closest_distance < 0 or distance < closest_distance:
            target = zombie_position

    move = np.array((target - ash_position) * min(1000 / get_distance(ash_position, target), 1), dtype=int)
    state = GameState(ash_position, zombie_positions, human_positions)
    state.move_zombies()
    score = state.update(move)
    print('Score : ' + str(score), file=sys.stderr, flush=True)

    print(target[0], target[1])
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
