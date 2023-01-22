TESTING = False

def read_input():
    file.seek(0)
    template = file.readline().rstrip()
    file.readline()
    raw_insertion_rules = [line.rstrip() for line in file.readlines()]

    insertion_rules = {}

    for rule in raw_insertion_rules:
        insertion_rules.update({rule[0:2]: rule[6]})

    return template, insertion_rules


def apply_rules(polymer, insertion_rules):
    new_polymer = ""

    for index in range(len(polymer) - 1):
        new_polymer += polymer[index]

        pair = polymer[index:index + 2]

        if pair in insertion_rules:
            new_polymer += insertion_rules[pair]

    new_polymer += polymer[len(polymer) - 1]

    return new_polymer

def polymerize(template, insertion_rules, steps):
    polymer = template

    for step in range(steps):
        # print(f"Polymerization {step = }")
        polymer = apply_rules(polymer, insertion_rules)

    return polymer


def count_chars(polymer):
    char_counts = {}

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        count = polymer.count(char)

        if count > 0:
            char_counts.update({char: count})

    return char_counts


def score_polymer(char_counts):
    return max(char_counts.values()) - min(char_counts.values())


def expand_rules(insertion_rules):
    expanded_rules = {}
    rule_char_counts = {}

    for pair, insertion in insertion_rules.items():
        expanded_insertion = polymerize(pair, insertion_rules, 20)
        char_counts = count_chars(expanded_insertion[1:len(expanded_insertion) - 1])

        #Don't include the starting and ending characters - we just want the part to be inserted
        expanded_rules.update({pair: expanded_insertion[1:len(expanded_insertion) - 1]})
        rule_char_counts.update({pair: char_counts})

    return expanded_rules, rule_char_counts


def score_polymer_lookahead(polymer, rule_char_counts):
    polymer_char_counts = count_chars(polymer)

    for index in range(len(polymer) - 1):
        pair = polymer[index:index + 2]

        for char in rule_char_counts[pair]:
            polymer_char_counts[char] += rule_char_counts[pair][char]

    print(f"{polymer_char_counts = }")

    return score_polymer(polymer_char_counts)


def part1():
    polymer, insertion_rules = read_input()

    print(f"{polymer = }, {insertion_rules = }")

    polymer = polymerize(polymer, insertion_rules, 10)
    print(f"{polymer = }")

    char_counts = count_chars(polymer)
    score = score_polymer(char_counts)

    return score


def part2():
    polymer, insertion_rules = read_input()

    print(f"{polymer = }, {insertion_rules = }")

    expanded_rules, rule_char_counts = expand_rules(insertion_rules)
    print(f"{expanded_rules = }, {rule_char_counts = }")

    polymer = polymerize(polymer, expanded_rules, 1)

    score = score_polymer_lookahead(polymer, rule_char_counts)

    return score


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
