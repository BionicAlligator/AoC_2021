import re

TESTING = False

def read_input():
    file.seek(0)

    horizontals = []
    verticals = []
    diagonals_tlbr = []
    diagonals_bltr = []

    for line in file:
        nums = re.match("(\d+),(\d+) -> (\d+),(\d+)", line.rstrip())
        x1, y1, x2, y2 = int(nums[1]), int(nums[2]), int(nums[3]), int(nums[4])

        if x1 == x2:
            verticals.append(( (x1, min(y1, y2)), (x1, max(y1, y2)) ))
        elif y1 == y2:
            horizontals.append(( (min(x1, x2), y1), (max(x1, x2), y1) ))
        else:
            #Diagonal
            if x1 <= x2: #Already normalised
                if y1 <= y2:
                    diagonals_tlbr.append(((x1, y1), (x2, y2)))
                else:
                    diagonals_bltr.append(((x1, y1), (x2, y2)))
            else: #Reverse
                if y2 <= y1:
                    diagonals_tlbr.append(((x2, y2), (x1, y1)))
                else:
                    diagonals_bltr.append(((x2, y2), (x1, y1)))

    return horizontals, verticals, diagonals_tlbr, diagonals_bltr

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
    #Expand to points in a set and count how many entries the set has at the end
    intersection_points = set()

    for (start_x, start_y), (end_x, end_y) in intersections[num_areas_intersecting - 1]:
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                intersection_points.add((x, y))

    return len(intersection_points)

def part1():
    intersections = []

    # Split into horizontal, vertical and diagonal lines
    # Normalise such that topmost/leftmost point is first coordinate in pair
    horizontal_vents, vertical_vents, _, _ = read_input()

    intersections.append(horizontal_vents + vertical_vents)

    print(f"Intersections (1+): {intersections}")

    # Work out overlaps
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


def aggregate_vents_hv(vents):
    vent_points = {}

    for (start_x, start_y), (end_x, end_y) in vents:
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if (x, y) in vent_points:
                    num = vent_points.get((x, y))
                    vent_points.update({(x, y): num + 1})
                else:
                    vent_points.update({(x, y): 1})

    return vent_points

def aggregate_vents_tlbr(vent_points, vents):
    for (start_x, start_y), (end_x, end_y) in vents:
        x = start_x
        y = start_y

        while x <= end_x:
            if (x, y) in vent_points:
                num = vent_points.get((x, y))
                vent_points.update({(x, y): num + 1})
            else:
                vent_points.update({(x, y): 1})

            x += 1
            y += 1

    return vent_points

def aggregate_vents_bltr(vent_points, vents):
    for (start_x, start_y), (end_x, end_y) in vents:
        x = start_x
        y = start_y

        while x <= end_x:
            if (x, y) in vent_points:
                num = vent_points.get((x, y))
                vent_points.update({(x, y): num + 1})
            else:
                vent_points.update({(x, y): 1})

            x += 1
            y -= 1

    return vent_points

def count_intersections(vent_points, min_num_intersections):
    intersections = 0

    for num in vent_points.values():
        if num >= min_num_intersections:
            intersections += 1

    return intersections

def part2():
    # Split into horizontal, vertical and diagonal lines
    # Normalise such that topmost/leftmost point is first coordinate in pair
    horizontal_vents, vertical_vents, diagonal_vents_tlbr, diagonal_vents_bltr = read_input()

    vent_points = aggregate_vents_hv(horizontal_vents + vertical_vents)
    vent_points = aggregate_vents_tlbr(vent_points, diagonal_vents_tlbr)
    vent_points = aggregate_vents_bltr(vent_points, diagonal_vents_bltr)

    # print(f"Vent Points: {vent_points}")

    return count_intersections(vent_points, 2)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
