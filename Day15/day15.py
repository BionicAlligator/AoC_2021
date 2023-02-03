TESTING = False

def read_input():
    file.seek(0)
    risk_levels = [[int(num) for num in line.rstrip()] for line in file]
    return risk_levels


def get_cave_extents(risk_levels):
    max_y = len(risk_levels) - 1
    max_x = len(risk_levels[0]) - 1
    return max_x, max_y


def a_star_search(risk_levels, start, end):
    OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_x, max_y = get_cave_extents(risk_levels)

    points_to_check = [{start: {"previous": None, "min_risk": 0, "best_possible": 0}}]
    visited_points = {}
    # print(f"{points_to_check = }")
    point, details = list(points_to_check.pop().items())[0]

    while point != end:
        if not (len(visited_points) % 100):
            print(f"Checking point {point} Num visited: {len(visited_points)}")
        visited_points.update({point: details})

        point_x, point_y = point
        point_min_risk = details["min_risk"]

        for offset_x, offset_y in OFFSETS:
            x = point_x + offset_x
            y = point_y + offset_y
            adjacent_point = (x, y)

            if (max_x >= x >= 0) and (max_y >= y >= 0) and \
                    not (adjacent_point in visited_points):
                min_risk = point_min_risk + risk_levels[y][x]
                best_possible = min_risk + max_x - x + max_y - y

                if adjacent_point in points_to_check:
                    if points_to_check[adjacent_point]["min_risk"] < min_risk:
                        continue

                points_to_check.append({adjacent_point: {"previous": point, "min_risk": min_risk, "best_possible": best_possible}})

        points_to_check.sort(key=lambda d: list(d.values())[0]["best_possible"], reverse=True)

        # print(f"{points_to_check = }")

        point, details = list(points_to_check.pop().items())[0]

    return details["min_risk"]


# TODO: Implement with objects instead of dicts
def part1():
    risk_levels = read_input()
    print("Input:", risk_levels)

    max_x, max_y = get_cave_extents(risk_levels)

    return a_star_search(risk_levels, (0, 0), (max_x, max_y))

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
