TESTING = False

DELIMITERS = {'(': ')', '[': ']', '{': '}', '<': '>'}
ILLEGAL_CHAR_VALUES = {')': 3, ']': 57, '}': 1197, '>': 25137}
OK, INCOMPLETE, CORRUPTED = range(3)

def read_input():
    file.seek(0)
    lines = [[char for char in line.rstrip()] for line in file]
    print ("Input lines:", lines)
    return lines

def parse_line(line):
    allowed_closing_chars = []

    for char in line:
        if char in DELIMITERS.keys():
            allowed_closing_chars.append(DELIMITERS[char])
        elif char != allowed_closing_chars.pop():
            return CORRUPTED, char

    return (INCOMPLETE, "") if allowed_closing_chars else (OK, "")

def parse(lines):
    error_chars = []

    for line in lines:
        validity, char = parse_line(line)

        if validity == CORRUPTED:
            error_chars.append(char)

    return error_chars

def score(error_chars):
    score = 0

    for char in error_chars:
        score += ILLEGAL_CHAR_VALUES[char]

    return score

def part1():
    lines = read_input()

    error_chars = parse(lines)

    return score(error_chars)

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
