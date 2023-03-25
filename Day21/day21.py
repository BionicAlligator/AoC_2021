import re

TESTING = True
OUTPUT_TO_CONSOLE = True


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_input(filename):
    starting_positions = {}

    file = open(filename, "r")

    for line in file:
        starting_position_mapping = re.findall(r'\d+', line)
        starting_positions[int(starting_position_mapping[0])] = int(starting_position_mapping[1])

    return starting_positions


def part1(filename):
    starting_positions = read_input(filename)
    return


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

print("Part 1: ", part1(filename))
