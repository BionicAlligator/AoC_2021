TESTING = False

def read_input():
    file.seek(0)
    notes = [tuple(map(lambda s: s.split(" "), line.rstrip().split(" | "))) for line in file]
    print("Notes:", notes)
    return notes

def part1():
    notes = read_input()

    easy_patterns = list(map(lambda entry: list(filter(lambda pattern: len(pattern) in [2, 3, 4, 7], entry[1])), notes))

    print(f"Easy patterns: {easy_patterns}")

    return sum(len(pattern) for pattern in easy_patterns)

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
