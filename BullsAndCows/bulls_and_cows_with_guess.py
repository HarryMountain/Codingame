import sys
import math
import itertools
from collections import Counter
from random import choice

def bulls_and_cows(list_1, list_2):
    common_elements = len(list((Counter(list_1) & Counter(list_2)).elements()))
    b = len([x for x in range(len(list_1)) if list_1[x] == list_2[x]])
    return b, common_elements - b


length = int(input())
x = list(range(10))
combos = [p for p in itertools.permutations(x, length) if p[0] != 0]

while True:
    bulls, cows = [int(z) for z in input().split()]
    if bulls != -1:
        combos = [x for x in combos if bulls_and_cows(guess, x) == (bulls, cows)]
    print(len(combos), file=sys.stderr, flush=True)
    guess = choice(combos)
    print(*guess, sep='')
