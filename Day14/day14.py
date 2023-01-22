TESTING = False

def read_input():
    file.seek(0)
    template = file.readline().rstrip()
    file.readline()
    raw_insertion_rules = [line.rstrip() for line in file.readlines()]

    insertion_rules = {}

    for rule in raw_insertion_rules:
        insertion_rules.update({(rule[0], rule[1]): rule[6]})

    return template, insertion_rules


def apply_rules(polymer, insertion_rules):
    new_polymer = ""

    for index in range(len(polymer) - 1):
        new_polymer += polymer[index]
        pair = (polymer[index], polymer[index + 1])

        if pair in insertion_rules:
            new_polymer += insertion_rules[pair]

    new_polymer += polymer[len(polymer) - 1]

    return new_polymer


def score_polymer(polymer):
    char_counts = []

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        count = polymer.count(char)

        if count > 0:
            char_counts.append(count)

    print(f"{char_counts = }, Max = {max(char_counts)}, Min = {min(char_counts)}")

    return max(char_counts) - min(char_counts)

def part1():
    polymer, insertion_rules = read_input()

    print(f"{polymer = }, {insertion_rules = }")

    for step in range(10):
        polymer = apply_rules(polymer, insertion_rules)

    print(f"{polymer = }")

    return score_polymer(polymer)


def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
