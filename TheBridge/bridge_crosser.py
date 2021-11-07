import copy

COMMANDS = ['SPEED', 'SLOW', 'JUMP', 'WAIT', 'UP', 'DOWN']

#def get_score():


def evaluate_bike(bike_count, bike_required, grid, speed_init, bike_data, chromosome):
    finished = False
    index = 0
    x = 0
    speed = speed_init
    bridge_length = len(grid[0])
    sim_bike_data = [copy.deepcopy(bike_data)]
    while not finished and index < len(chromosome):
        #print(bike_data, bridge_length, file=sys.stderr, flush=True)
        gene = chromosome[index]
        dy = 1 if (gene == 5 and bike_data[-1][1] < 3) else -1 if (gene == 4 and bike_data[0][1] > 0) else 0
        speed += 1 if gene == 0 else -1 if (gene == 1 and speed > 0) else 0
        jumping = gene == 2
        for i in range(len(bike_data)):
            if bike_data[i][2] == 1:
                y = bike_data[i][1]
                # See if bike fell in hole
                in_hole = False
                if not jumping:
                    x_max = min(bridge_length, x + speed - 1)
                    for xx in range(x + 1, x_max):
                        in_hole |= grid[y][xx] == '0'
                        if abs(dy) > 0:
                            in_hole |= grid[y + dy][xx] == '0'
                if x + speed < bridge_length:
                    in_hole |= grid[y + dy][x + speed] == '0'
                if in_hole:
                    bike_data[i][2] = 0
                bike_data[i][0] += speed
                bike_data[i][1] += dy
        x += speed
        finished = x >= bridge_length
        sim_bike_data.append(copy.deepcopy(bike_data))
        index += 1
    number_at_end = sum([bike_data[i][2] for i in range(bike_count)])
    score = 10 * (bike_required - number_at_end) + max(0, bridge_length - x)
    return [score, sim_bike_data]


def solve_bridge(bike_count, bike_required, grid, speed, bike_data):
    # Do something
    i = 0



