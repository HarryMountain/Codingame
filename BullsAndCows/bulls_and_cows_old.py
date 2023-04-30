import sys
import math
import random

number_length = int(input())
best_numbers = [[0] * 10 for i in range(number_length)]
output = []
while True:
    numbers = list(range(10))
    bulls, cows = [int(i) for i in input().split()]
    if len(output) == 0:
        output = sorted(random.sample(range(10), number_length), reverse=True)
    else:
        for i in range(number_length):
            for j in range(10):
                if j in output:
                    if output[i] == j:
                        best_numbers[i][j] += bulls
                    else:
                        best_numbers[i][j] += cows * 0.2
                else:
                    best_numbers[i][j] += (number_length - bulls - cows) * 0.2
        output = []
        for number in range(number_length):
            highest_score = -1
            highest_score_number = -1
            for i in range(10):
                if number == 0 and i == 0:
                    continue
                if best_numbers[number][i] > highest_score and i not in output:
                    highest_score = best_numbers[number][i]
                    highest_score_number = i
            if random.randint(1, 3) == 1:
                highest_score_number = random.sample(numbers[1:] if number == 0 else numbers, 1)[0]

            output.append(highest_score_number)
            numbers.remove(highest_score_number)

    print(''.join(map(str, output)))
