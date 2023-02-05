# Uses a priority queue (implemented with heapq) such that the order of points to visit is maintained
# as items are pushed and popped, thus avoiding need for expensive sorting procedures
# However, does not appear to yield significant speed improvements
from heapq import heappush, heappop

TESTING = False
TILE_MULTIPLIER = 1

def read_input():
    file.seek(0)
    risk_levels = [[int(num) for num in line.rstrip()] for line in file]
    return risk_levels


def get_cave_extents(risk_levels):
    max_y = TILE_MULTIPLIER * len(risk_levels) - 1
    max_x = TILE_MULTIPLIER * len(risk_levels[0]) - 1
    return max_x, max_y


def get_risk_level(point_x, point_y, risk_levels):
    adjustment_x, reference_x = divmod(point_x, len(risk_levels[0]))
    adjustment_y, reference_y = divmod(point_y, len(risk_levels))
    reference_risk_level = risk_levels[reference_y][reference_x]

    adjusted_risk_level = reference_risk_level + adjustment_x + adjustment_y

    constrained_risk_level = ((adjusted_risk_level - 1) % 9) + 1

    return constrained_risk_level


def visit_point(point, risk_levels, points_to_visit, visited_points, point_details):
    OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_x, max_y = get_cave_extents(risk_levels)

    if not (len(visited_points) % 1000):
        print(f"Visiting point {point}   {len(visited_points)} points visited so far")

    visited_points.update({point: point_details[point]})

    point_x, point_y = point
    point_min_risk = point_details[point]["min_risk"]

    for offset_x, offset_y in OFFSETS:
        adjacent_x = point_x + offset_x
        adjacent_y = point_y + offset_y
        adjacent_point = (adjacent_x, adjacent_y)

        if (max_x >= adjacent_x >= 0) and (max_y >= adjacent_y >= 0) and \
                not (adjacent_point in visited_points):
            min_risk = point_min_risk + get_risk_level(adjacent_x, adjacent_y, risk_levels)

            # Lowest possible risk assuming a direct path from here to the end with
            # every step along the way being a risk level of 1
            best_possible = min_risk + max_x - adjacent_x + max_y - adjacent_y

            if not (adjacent_point in [p[1] for p in points_to_visit]):
                heappush(points_to_visit, (best_possible, adjacent_point))
                point_details.update({adjacent_point: {"min_risk": min_risk, "previous": point}})
            elif min_risk < point_details[adjacent_point]["min_risk"]:
                point_details.update({adjacent_point: {"min_risk": min_risk, "previous": point}})

    return


def a_star_search(risk_levels, start, end):
    points_to_visit = []
    point_details = {start: {"min_risk": 0, "previous": None}}
    heappush(points_to_visit, (0, start))  #Tuple of: (best_possible, point) so that heapq orders by best_possible
    visited_points = {}

    _, point = heappop(points_to_visit)

    while point != end:
        visit_point(point, risk_levels, points_to_visit, visited_points, point_details)
        _, point = heappop(points_to_visit)

    return point_details[end]["min_risk"]


def part1():
    risk_levels = read_input()
    print(f"{risk_levels = }")

    start_point = (0, 0)
    end_point = get_cave_extents(risk_levels)

    return a_star_search(risk_levels, start_point, end_point)

def part2():
    global TILE_MULTIPLIER
    TILE_MULTIPLIER = 5

    risk_levels = read_input()
    print(f"{risk_levels = }")

    start_point = (0, 0)
    end_point = get_cave_extents(risk_levels)

    return a_star_search(risk_levels, start_point, end_point)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
