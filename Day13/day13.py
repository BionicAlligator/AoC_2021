import re

TESTING = False

def print_page(dots):
    max_x = float('-inf')
    max_y = float('-inf')

    for x, y in dots:
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)

    for y in range(0, max_y):
        for x in range(0, max_x):
            char_to_print = "#" if (x, y) in dots else "."
            print(char_to_print, end="")

        print()

def read_input():
    file.seek(0)

    dots = set()
    folds = []

    for line in file:
        dot = re.match("(\d+),(\d+)", line)

        if dot:
            dots.add((int(dot[1]), int(dot[2])))
        else:
            fold = re.match("fold along ([xy])=(\d+)", line)

            if fold:
                folds.append((0 if fold[1]=='x' else 1, int(fold[2])))

    # print("Dots:", dots)
    # print("Folds:", folds)
    return dots, folds

def fold(dots, axis, line):
    new_dots = set()

    for dot in dots:
        new_dot = dot

        if new_dot[axis] > line:
            new_dot_list = list(new_dot)
            new_dot_list[axis] = (2 * line) - new_dot_list[axis]
            new_dot = tuple(new_dot_list)

        new_dots.add(new_dot)

    return new_dots

def part1():
    dots, folds = read_input()

    axis, line = folds[0]

    dots = fold(dots, axis, line)

    # print_page(dots)
    return len(dots)

def part2():
    dots, folds = read_input()

    for axis, line in folds:
        dots = fold(dots, axis, line)

    print_page(dots)
    return len(dots)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
