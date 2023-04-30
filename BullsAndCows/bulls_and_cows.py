import sys
import math
import itertools
from collections import Counter

def bulls_and_cows(list_1, list_2):
    common_elements = len(list((Counter(list_1) & Counter(list_2)).elements()))
    b = len([x for x in range(len(list_1)) if list_1[x] == list_2[x]])
    return b, common_elements - b

x = list(range(10))
combos = [p for p in itertools.product(x, repeat=4)]

n = int(input())
for i in range(n):
    inputs = input().split()
    guess = [int(y) for y in inputs[0]]
    bulls = int(inputs[1])
    cows = int(inputs[2])
    combos = [x for x in combos if bulls_and_cows(guess, x) == (bulls, cows)]
    print(len(combos), file=sys.stderr, flush=True)
print(*combos[0],sep='')

