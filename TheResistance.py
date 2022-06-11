import time

test_mode = False
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
one_char_words = {}
paths = {0: 1}
words = {'..': {}, '.-': {}, '-.': {}, '--': {}}
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
        if len(the_word) == 1:
            one_char_words[the_word] = [1, 1]
        else:
            words[the_word[:2]][the_word] = [len(the_word), words[the_word[:2]].get(the_word, [0, 0])[1] + 1]

for key in words.keys():
    if key[0] in one_char_words.keys():
        words[key][key[0]] = [1, 1]


total = 0
while len(paths) > 0:
    new_paths = {}
    for pos, number in paths.items():
        words_to_search = one_char_words if pos == message_length - 1 else words[message[pos: pos + 2]]
        for word, data in words_to_search.items():
            length = data[0]
            count = data[1]
            new_pos = pos + length
            if message[pos:new_pos] == word:
                # if all([message[i] == word[i - pos] for i in range(pos, new_pos)]):
                if new_pos == message_length:
                    total += number * count
                else:
                    new_paths[new_pos] = new_paths.get(new_pos, 0) + number * count
    paths = new_paths
print(total)
