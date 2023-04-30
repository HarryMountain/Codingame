import sys
import math
from collections import Counter

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

magic_phrase = input()
# magic_phrase = 'AZ'
letters = Counter(magic_phrase)
stones = [' '] * 30
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

letters = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_steps(letter, stones, position):
    steps = []
    for i in range(len(stones)):
        steps_to_get_there = []
        stone = stones[i]
        no_loop = i - position
        with_loop = no_loop + (-30 if no_loop > 0 else 30)
        steps_to_get_there.append(min(no_loop, with_loop, key=abs))
        current = letters.index(stone)
        required = letters.index(letter)
        no_loop = required - current
        with_loop = no_loop + (-27 if no_loop > 0 else 27)
        steps_to_get_there.append(min(no_loop, with_loop, key=abs))
        steps.append(steps_to_get_there)
    return steps


position = 0
output = ''
for i in range(len(magic_phrase)):
    letter = magic_phrase[i]
    steps = get_steps(letter, stones, position)
    least_steps = [-1, -1]
    for j in range(len(steps)):
        step = steps[j]
        score = abs(step[0]) + abs(step[1])
        if least_steps[0] == -1 or score < least_steps[0]:
            least_steps[0] = score
            least_steps[1] = j
    step_to_take = steps[least_steps[1]]
    output += (('>' if step_to_take[0] > 0 else '<') * abs(step_to_take[0])) + (('+' if step_to_take[1] > 0 else '-') * abs(step_to_take[1])) + '.'
    position += step_to_take[0]
    stones[position] = letter
print(output)
