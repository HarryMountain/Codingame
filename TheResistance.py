import time

test_mode = True
input_data = []


def get_input():
    if test_mode and len(input_data) == 0:
        with open('the_resistance_inputs', 'r') as f:
            for line in f:
                input_data.append(line.rstrip())
    return input_data.pop(0) if test_mode else input()


morse_code = {'A': '.-', 'B': '-...',
              'C': '-.-.', 'D': '-..', 'E': '.',
              'F': '..-.', 'G': '--.', 'H': '....',
              'I': '..', 'J': '.---', 'K': '-.-',
              'L': '.-..', 'M': '--', 'N': '-.',
              'O': '---', 'P': '.--.', 'Q': '--.-',
              'R': '.-.', 'S': '...', 'T': '-',
              'U': '..-', 'V': '...-', 'W': '.--',
              'X': '-..-', 'Y': '-.--', 'Z': '--..'}

# To debug: print("Debug messages...", file=sys.stderr, flush=True)
time_start = time.time()
paths = {0: 1}
dot_words = []
dash_words = []
message = get_input()
message_length = len(message)
n = int(get_input())
for i in range(n):
    w = get_input()
    morse_w = []
    for char in w:
        morse_w.append(morse_code[char])
    the_word = ''.join(morse_w)
    if the_word in message:
        if morse_w[0][0] == '.':
            dot_words.append([the_word, len(the_word)])
        else:
            dash_words.append([the_word, len(the_word)])
total = 0
while len(paths) > 0:
    new_paths = {}
    for pos, number in paths.items():
        for word, length in dot_words if message[pos] == '.' else dash_words:
            new_pos = pos + length
            if message[pos:new_pos] == word:
                # if all([message[i] == word[i - pos] for i in range(pos, new_pos)]):
                if new_pos == message_length:
                    total += number
                else:
                    new_paths[new_pos] = new_paths.get(new_pos, 0) + number
    paths = new_paths
print(total)
