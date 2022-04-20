import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = [int(input())]
l = int(input())

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


def make_next_line(prev_line):
    new_line = [0, prev_line[0]]
    for i in range(len(prev_line)):
        if prev_line[i] != new_line[-1]:
            new_line.extend([1, prev_line[i]])
        else:
            new_line[-2] += 1
    return new_line


for i in range(l - 1):
    r = make_next_line(r)

print(*r)
