TESTING = False

def read_input():
    file.seek(0)
    points = [[int(p) for p in line.rstrip()] for line in file]
    print ("Input points:", points)
    return points

def is_lowest_in_vicinity(position, cell, points):
    ADJACENT_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for offset in ADJACENT_OFFSETS:
        adj_x, adj_y = tuple(map(sum, zip(position, offset)))

        if (0 <= adj_y < len(points)) and (0 <= adj_x < len(points[0])):
            # print(f"Checking {position}={cell} against {(adj_x, adj_y)}={points[adj_y][adj_x]}")

            if points[adj_y][adj_x] <= cell:
                return False

    return True

def find_low_points(points):
    low_points = {}

    for y, row in enumerate(points):
        for x, cell in enumerate(row):
            if is_lowest_in_vicinity((x, y), cell, points):
                low_points.update({(x, y): cell + 1})

    print(f"Low points: {low_points}")

    return low_points

def part1():
    points = read_input()
    return sum(find_low_points(points).values())

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
