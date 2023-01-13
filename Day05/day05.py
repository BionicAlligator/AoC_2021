import re

TESTING = True

def read_input():
    file.seek(0)

    horizontals = []
    verticals = []
    # diagonals_tl-br = []
    # diagonals_bl-tr = []

    for line in file:
        nums = re.match("(\d+),(\d+) -> (\d+),(\d+)", line.rstrip())
        x1, y1, x2, y2 = int(nums[1]), int(nums[2]), int(nums[3]), int(nums[4])

        if x1 == x2:
            verticals.append(( (x1, min(y1, y2)), (x1, max(y1, y2)) ))
        elif y1 == y2:
            horizontals.append(( (min(x1, x2), y1), (max(x1, x2), y1) ))
        else:
            #Diagonal
            continue

    return horizontals, verticals

def intersect(area1, area2):
    (start1_x, start1_y), _ = area1
    (start2_x, start2_y), _ = area2

    left = area1 if start1_x <= start2_x else area2
    right = area1 if left == area2 else area2
    top = area1 if start1_y <= start2_y else area2
    bottom = area1 if top == area2 else area2

    right_start = right[0][0]
    left_end = left[1][0]
    right_end = right[1][0]
    bottom_start = bottom[0][1]
    bottom_end = bottom[1][1]
    top_end = top[1][1]

    if (right_start <= left_end) and (bottom_start <= top_end):   #The areas intersect
        return ((right_start, bottom_start), (min(left_end, right_end), min(top_end, bottom_end)))

    return False  #No intersection

def count_intersection_points(intersections, num_areas_intersecting):
    intersection_points = set()

    for (start_x, start_y), (end_x, end_y) in intersections[num_areas_intersecting - 1]:
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                intersection_points.add((x, y))

    return len(intersection_points)

def part1():
    intersections = []

    # Split into horizontal, vertical and diagonal lines
    # Normalise such that top/left point is first coordinate in pair
    horizontal_vents, vertical_vents = read_input()

    intersections.append(horizontal_vents + vertical_vents)

    print(f"Intersections (1+): {intersections}")

    intersections.append([])

    for area1_num in range(0, len(intersections[0])):
        for area2_num in range(area1_num + 1, len(intersections[0])):
            area1 = intersections[0][area1_num]
            area2 = intersections[0][area2_num]

            intersection = intersect(area1, area2)
            if intersection:
                intersections[1].append(intersection)

    print(f"Intersections (2+): {intersections[1]}")

    return count_intersection_points(intersections, 2)

    # There are only 1m squares, so probably best to just use a 2D (1000x1000) grid
    # Iterate through each line, incrementing every point
    # Scan map and count all points where value is greater than 1

    # Alternative (more efficient) is to first work out overlaps, then just map those,
    # or expand them to points in a set and count how many entries the set has at the end

    return

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
