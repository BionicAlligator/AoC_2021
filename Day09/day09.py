TESTING = True

def read_input():
    file.seek(0)
    points = [[int(p) for p in line.rstrip()] for line in file]
    print ("Input points:", points)
    return points

def adjacent_points(point, points):
    ADJACENT_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    adjacent_points = {}

    for offset in ADJACENT_OFFSETS:
        adj_x, adj_y = tuple(map(sum, zip(point, offset)))

        if (0 <= adj_y < len(points)) and (0 <= adj_x < len(points[0])):
            adjacent_points.update({(adj_x, adj_y): points[adj_y][adj_x]})

    return adjacent_points

def is_lowest_in_vicinity(point, point_height, points):
    for adjacent_point_height in adjacent_points(point, points).values():
        if adjacent_point_height <= point_height:
            return False

    return True

def find_low_points(points):
    low_points = {}

    for y, row in enumerate(points):
        for x, point_height in enumerate(row):
            if is_lowest_in_vicinity((x, y), point_height, points):
                low_points.update({(x, y): point_height})

    # print(f"Low points: {low_points}")

    return low_points

def find_basin(low_point, points):
    basin = []

    points_to_expand = [low_point]

    while points_to_expand:
        point = points_to_expand.pop()
        basin.append(point)

        # for adjacent_point, adjacent_point_height in adjacent_points(point, points).items():
        #     if adjacent_point_height >= point.value

    return basin

def find_basins(points):
    basins = []

    for low_point in find_low_points(points):
        basins.append(find_basin(low_point, points))

    return basins

def part1():
    points = read_input()

    low_points = find_low_points(points)

    return sum(low_points.values(), len(low_points))

def part2():
    points = read_input()

    basins = find_basins(points)

    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
