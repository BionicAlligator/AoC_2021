# Uses a priority queue (implemented with heapq) such that the order of points to visit is maintained
# as items are pushed and popped, thus avoiding need for expensive sorting procedures
# This in itself does not appear to yield significant performance improvements

# However, this version also initialises the min_risks dictionary and uses it to determine whether to
# investigate an adjacent node, rather than checking if the adjacent node is in the list of nodes to be checked
# This massively improves performance (~30x speed improvement)

from heapq import heappush, heappop

TESTING = False

def read_input():
    file.seek(0)
    risk_levels = [[int(num) for num in line.rstrip()] for line in file]
    return risk_levels


def get_cave_extents(risk_levels):
    max_y = len(risk_levels) - 1
    max_x = len(risk_levels[0]) - 1
    return max_x, max_y


def get_risk_level(point_x, point_y, risk_levels):
    adjustment_x, reference_x = divmod(point_x, len(risk_levels[0]))
    adjustment_y, reference_y = divmod(point_y, len(risk_levels))
    reference_risk_level = risk_levels[reference_y][reference_x]

    adjusted_risk_level = reference_risk_level + adjustment_x + adjustment_y

    constrained_risk_level = ((adjusted_risk_level - 1) % 9) + 1

    return constrained_risk_level


def extend_map(risk_levels, multiplier):
    return [[get_risk_level(x, y, risk_levels) for x in range(len(risk_levels[0]) * multiplier)]
            for y in range(len(risk_levels) * multiplier)]


def visit_point(point, risk_levels, points_to_visit, visited_points, min_risks, previous):
    OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_x, max_y = get_cave_extents(risk_levels)

    # if not (len(visited_points) % 1000):
    #     print(f"Visiting point {point}   {len(visited_points)} points visited so far")

    visited_points.add(point)

    point_x, point_y = point
    point_min_risk = min_risks[point]

    for offset_x, offset_y in OFFSETS:
        adjacent_x = point_x + offset_x
        adjacent_y = point_y + offset_y
        adjacent_point = (adjacent_x, adjacent_y)

        if (max_x >= adjacent_x >= 0) and (max_y >= adjacent_y >= 0) and \
                not (adjacent_point in visited_points):
            min_risk = point_min_risk + risk_levels[adjacent_y][adjacent_x]

            if min_risk < min_risks[adjacent_point]:
                # Lowest possible risk assuming a direct path from here to the end with
                # every step along the way being a risk level of 1
                best_possible = min_risk + max_x - adjacent_x + max_y - adjacent_y

                heappush(points_to_visit, (best_possible, adjacent_point))
                min_risks[adjacent_point] = min_risk
                previous[adjacent_point] = point


def a_star_search(risk_levels, start, end):
    points_to_visit = []
    visited_points = set()
    min_risks = {}
    previous = {}

    for y in range(len(risk_levels)):
        for x in range(len(risk_levels[0])):
            min_risks[(x, y)] = float('Inf')

    min_risks[start] = 0
    previous[start] = None
    heappush(points_to_visit, (0, start))  #Tuple of: (best_possible, point) so that heapq orders by best_possible

    while points_to_visit:
        _, point = heappop(points_to_visit)
        visit_point(point, risk_levels, points_to_visit, visited_points, min_risks, previous)

    return min_risks[end]


def part1():
    risk_levels = read_input()
    # print(f"{risk_levels = }")

    start_point = (0, 0)
    end_point = get_cave_extents(risk_levels)

    return a_star_search(risk_levels, start_point, end_point)

def part2():
    risk_levels = extend_map(read_input(), 5)
    # print(f"{risk_levels = }")

    start_point = (0, 0)
    end_point = get_cave_extents(risk_levels)

    return a_star_search(risk_levels, start_point, end_point)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
