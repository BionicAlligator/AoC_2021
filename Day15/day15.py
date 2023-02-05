TESTING = True
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


def visit_point(point, details, risk_levels, points_to_visit, visited_points):
    OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_x, max_y = get_cave_extents(risk_levels)

    if not (len(visited_points) % 1000):
        print(f"Visiting point {point}   {len(visited_points)} points visited so far")

    visited_points.update({point: details})

    point_x, point_y = point
    point_min_risk = details["min_risk"]

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

            if not (adjacent_point in points_to_visit) or \
                    min_risk < points_to_visit[adjacent_point]["min_risk"]:
                points_to_visit.update({adjacent_point: {"previous": point,
                                                         "min_risk": min_risk,
                                                         "best_possible": best_possible}})

    points_to_visit = dict(sorted(points_to_visit.items(),
                                  key=lambda item: item[1].get("best_possible"),
                                  reverse=True))

    return points_to_visit


def a_star_search(risk_levels, start, end):
    points_to_visit = {start: {"previous": None, "min_risk": 0, "best_possible": 0}}
    visited_points = {}

    point, details = points_to_visit.popitem()

    while point != end:
        points_to_visit = visit_point(point, details, risk_levels, points_to_visit, visited_points)
        point, details = points_to_visit.popitem()

    return details["min_risk"]


# TODO: Implement "Fast Dijkstra" - when you first encounter an adjacent node, add it to a list
# with the risk to get there from the current node. After that, ignore it if it comes up as an adjacent
# node for a future visited node because the risk to get there can not be less than the current value it holds
# TODO: Implement with objects instead of dicts
# TODO: Implement DFS with pruning
# TODO: Implement BFS
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
