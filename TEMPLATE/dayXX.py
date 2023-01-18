TESTING = True

def read_input():
    file.seek(0)
    lines = [line.rstrip() for line in file]
    return lines

def part1():
    input = read_input()
    print("Input:", input)
    return

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
