TESTING = False

def read_input():
    file.seek(0)
    crab_positions = list(map(int, file.readline().rstrip().split(",")))
    # print ("Crab positions:", crab_positions)
    return crab_positions

def part1():
    #Find the smallest and largest numbers
    #For each position in that range, sum the fuel required for each crab to reach it
    #Find the smallest fuel usage number

    crab_positions = read_input()

    lowest_position = min(crab_positions)
    highest_position = max(crab_positions)

    min_fuel_usage = float('inf')

    for pos in range(lowest_position, highest_position + 1):
        fuel_required = lambda crab_pos: abs(pos - crab_pos)

        min_fuel_usage = min(min_fuel_usage, sum(list(map(fuel_required, crab_positions))))

    return min_fuel_usage


def nth_triangular_number(n):
    return (n * (n + 1)) / 2

def part2():
    crab_positions = read_input()

    lowest_position = min(crab_positions)
    highest_position = max(crab_positions)

    min_fuel_usage = float('inf')

    for pos in range(lowest_position, highest_position + 1):
        fuel_required = lambda crab_pos: int(nth_triangular_number(abs(pos - crab_pos)))

        min_fuel_usage = min(min_fuel_usage, sum(list(map(fuel_required, crab_positions))))

    return min_fuel_usage


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
