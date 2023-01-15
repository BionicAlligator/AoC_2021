TESTING = False

DELIMITERS = {'(': ')', '[': ']', '{': '}', '<': '>'}
ILLEGAL_CHAR_VALUES = {')': 3, ']': 57, '}': 1197, '>': 25137}
AUTOCOMPLETE_CHAR_VALUES = {')': 1, ']': 2, '}': 3, '>': 4}
OK, INCOMPLETE, CORRUPTED = range(3)

def read_input():
    file.seek(0)
    lines = [[char for char in line.rstrip()] for line in file]
    # print ("Input lines:", lines)
    return lines

def parse_line(line):
    required_closing_chars = []

    for char in line:
        if char in DELIMITERS.keys():
            required_closing_chars.append(DELIMITERS[char])
        elif char != required_closing_chars[len(required_closing_chars) - 1]:
            return CORRUPTED, char
        else: #Must be a matching closing delimiter
            required_closing_chars.pop()

    return (INCOMPLETE, required_closing_chars) if required_closing_chars else (OK, "")

def parse(lines):
    error_chars = []
    completion_strings = []

    for line in lines:
        validity, error_detail = parse_line(line)

        if validity == CORRUPTED:
            error_chars.append(error_detail)
        elif validity == INCOMPLETE:
            completion_strings.append(error_detail)

    return error_chars, completion_strings

def syntax_checker_score(error_chars):
    score = 0

    for char in error_chars:
        score += ILLEGAL_CHAR_VALUES[char]

    return score

def autocompleter_score(completion_strings):
    scores = [0] * len(completion_strings)

    for string_num, completion_string in enumerate(completion_strings):
        completion_string.reverse()

        for char in completion_string:
            scores[string_num] *= 5
            scores[string_num] += AUTOCOMPLETE_CHAR_VALUES[char]

    scores.sort()

    return scores[len(scores) // 2]

def part1():
    lines = read_input()

    error_chars, _ = parse(lines)

    return syntax_checker_score(error_chars)

def part2():
    lines = read_input()

    _, completion_strings = parse(lines)

    return autocompleter_score(completion_strings)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
