TESTING = False

def read_input():
    file.seek(0)
    lines = [int(line.rstrip()) for line in file]
    return lines

def part1():
    depths = read_input()

    depth_increases = 0
    previous_depth = float('inf')

    for reading in depths:
        depth_increases += 1 if reading > previous_depth else 0
        previous_depth = reading

    return depth_increases

def part2():
    depths = read_input()

    depth_increases = 0
    previous_window = float('inf')

    for reading_num in range(0, len(depths) - 2):
        window = sum(depths[reading_num:reading_num+3])
        # print(f"Comparing {window} with {previous_window}")
        depth_increases += 1 if window > previous_window else 0
        previous_window = window

    return depth_increases


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
