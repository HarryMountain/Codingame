import sys
import math

# Save humans, destroy zombies!


# game loop
while True:
    humans = []
    zombies = []
    ash_x, ash_y = [int(i) for i in input().split()]
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans.append([human_id, human_x, human_y])
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombies.append([zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Get closest zombie to each human
    closest_zombie = []
    for human in humans:
        # Find closest zombie distance - index 3
        distances = []
        for zombie in zombies:
            x_far = zombie[1] - human[1]
            y_far = zombie[2] - human[2]
            distances.append(math.sqrt(x_far**2 + y_far**2))
        human.append(min(distances))

        # Find distance to Ash - index 4
        ash_diff_x = ash_x - human[1]
        ash_diff_y = ash_y - human[2]
        ash_distance = math.sqrt(ash_diff_x**2 + ash_diff_y**2)
        human.append(ash_distance)

        # Can this personbe eaten by a Zombie before Ash gets there - index 5
        can_zombie_get_this_human = math.floor(human[3] / 400) < math.floor(human[4] / 1000)
        human.append(can_zombie_get_this_human)
        # print(*[can_zombie_get_this_human, closest_zombie_distance, math.floor(closest_zombie_distance / 400), human[4], math.floor(ash_distance / 1000)], file=sys.stderr, flush=True)
    print(*[humans], file=sys.stderr, flush=True)

    most_humans = [-1, []]
    for x in range(0, 16000, 250):
        for y in range(0, 9000, 250):
            # Count how many people we can protect of those that can't be eaten by zombies before we get there
            protected = 0
            for human in humans:
                if not human[5]:
                    x_diff = x - human[1]
                    y_diff = y - human[2]
                    distance = math.sqrt(x_diff**2 + y_diff**2)
                    if distance < human[3]: # Look at distance to closest zombie
                        protected += 1

            zombie_death_oportunities = 0
            for zombie in zombies:
                x_diff = x - zombie[3]
                y_diff = y - zombie[4]
                if x_diff**2 + y_diff**2 < 2000 * 2000:
                    zombie_death_oportunities += 1
            score = (protected + zombie_death_oportunities) if protected > 0 else 0
            if score > most_humans[0]:
                most_humans = [score, [x, y], [protected, zombie_death_oportunities]]


    print(*most_humans[2], file=sys.stderr, flush=True)
    print(*humans, file=sys.stderr, flush=True)
    print(*most_humans[1])
