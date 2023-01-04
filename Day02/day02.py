TESTING = False

def read_input():
    file.seek(0)
    lines = [line.rstrip().split(" ") for line in file]
    # print ("Input lines:", lines)
    return lines

def part1():
    commands = read_input()

    horizontal_position = 0
    depth = 0

    for command in commands:
        match command[0]:
            case "forward":
                horizontal_position += int(command[1])
            case "up":
                depth -= int(command[1])
            case "down":
                depth += int(command[1])

    return horizontal_position * depth

def part2():
    commands = read_input()

    horizontal_position = 0
    depth = 0
    aim = 0

    for command in commands:
        match command[0]:
            case "forward":
                horizontal_position += int(command[1])
                depth += aim * int(command[1])
            case "up":
                aim -= int(command[1])
            case "down":
                aim += int(command[1])

    return horizontal_position * depth


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
