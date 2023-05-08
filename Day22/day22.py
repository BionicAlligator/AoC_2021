import re

TESTING = "False"
OUTPUT_TO_CONSOLE = False

INIT_RANGE = (-50, 50)


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_input(filename):
    reboot_steps = []

    file = open(filename, "r")
    for line in file:
        m = re.match("(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", line)
        on_off = m.group(1)
        x_range = tuple(map(int, m.group(2, 3)))
        y_range = tuple(map(int, m.group(4, 5)))
        z_range = tuple(map(int, m.group(6, 7)))
        reboot_steps.append((on_off, x_range, y_range, z_range))

    return reboot_steps


def intersects(range1, range2):
    return True if (range1[0] <= range2[0] <= range1[1]) or \
                   (range2[0] <= range1[0] <= range2[1]) else False


def intersects_3d(x_range1, y_range1, z_range1, x_range2, y_range2, z_range2):
    return True if intersects(x_range1, x_range2) and \
                   intersects(y_range1, y_range2) and \
                   intersects(z_range1, z_range2) else False


def intersection(x_range1, y_range1, z_range1, x_range2, y_range2, z_range2):
    x_intersect = (max(x_range1[0], x_range2[0]), min(x_range1[1], x_range2[1]))
    y_intersect = (max(y_range1[0], y_range2[0]), min(y_range1[1], y_range2[1]))
    z_intersect = (max(z_range1[0], z_range2[0]), min(z_range1[1], z_range2[1]))
    return x_intersect, y_intersect, z_intersect


def intersects_init_area(x_range, y_range, z_range):
    return True if intersects_3d(INIT_RANGE, INIT_RANGE, INIT_RANGE,
                                 x_range, y_range, z_range) else False


def contains(range1, range2):
    return True if (range2[0] <= range1[0] <= range2[1]) and \
                   (range2[0] <= range1[1] <= range2[1]) else False


def contains_3d(x_range1, y_range1, z_range1, x_range2, y_range2, z_range2):
    return True if contains(x_range1, x_range2) and \
                   contains(y_range1, y_range2) and \
                   contains(z_range1, z_range2) else False


def constrain(value):
    return max(min(value, INIT_RANGE[1]), INIT_RANGE[0])


def volume(x_range, y_range, z_range):
    x = x_range[1] - x_range[0] + 1
    y = y_range[1] - y_range[0] + 1
    z = z_range[1] - z_range[0] + 1
    return x * y * z


# NOT USED - thought it might simplify but doesn't have much effect on the given input instructions
# Start at end and work toward beginning:
# For each step A, compare against every earlier step B
#   If A contains B, delete B (doesn't matter whether A and B are ON or OFF steps)
#   If A is OFF and does not intersect with any B, delete it
def reduce_reboot_steps(reboot_steps):
    new_reboot_steps = []

    while reboot_steps:
        on_off, x_range1, y_range1, z_range1 = reboot_steps.pop()
        new_reboot_steps.append((on_off, x_range1, y_range1, z_range1))

        # Only if this is an OFF step will we check for intersections to see if this step
        # has any effect. By setting this to True for ON steps, we skip further checking.
        off_intersection = (on_off == "on")
        step_num = 0

        while step_num < len(reboot_steps):
            _, x_range2, y_range2, z_range2 = reboot_steps[step_num]

            if contains_3d(x_range2, y_range2, z_range2, x_range1, y_range1, z_range1):
                reboot_steps.pop(step_num)
                step_num -= 1

            if not off_intersection and intersects_3d(x_range1, y_range1, z_range1, x_range2, y_range2, z_range2):
                off_intersection = True

            step_num += 1

        if not off_intersection:
            new_reboot_steps.pop()

    log(f"{new_reboot_steps = }")

    reboot_steps = list(reversed(new_reboot_steps))
    log(f"{reboot_steps = }")

    return reboot_steps


def volume_of_union(areas, levels_remaining):
    log(f"{levels_remaining =}")
    union_volume = 0

    for area_num, area1 in enumerate(areas):
        union_volume += volume(*area1)

        intersections = []

        for area2 in areas[area_num + 1:]:
            if intersects_3d(*area1, *area2):
                intersect = intersection(*area1, *area2)
                intersections.append(intersect)

        if levels_remaining:
            union_volume -= volume_of_union(intersections, levels_remaining - 1)

    return union_volume


def part1(filename):
    reboot_steps = read_input(filename)
    log(f"{reboot_steps = }")

    on = set()

    for on_off, (x1, x2), (y1, y2), (z1, z2) in reboot_steps:
        if intersects_init_area((x1, x2), (y1, y2), (z1, z2)):
            for x in range(constrain(x1), constrain(x2) + 1):
                for y in range(constrain(y1), constrain(y2) + 1):
                    for z in range(constrain(z1), constrain(z2) + 1):
                        if on_off == "on":
                            on.add((x, y, z))
                        else:
                            on.discard((x, y, z))

    return len(on)


def part2(filename):
    reboot_steps = read_input(filename)
    log(f"{reboot_steps = }")

    # reboot_steps = reduce_reboot_steps(reboot_steps)

    total_on = 0

    for step_num, (on_off, *area1) in enumerate(reboot_steps):
        log(f"{step_num = }")

        if on_off == "on":
            log("This step turns cubes on")

            total_on += volume(*area1)

            intersections = []

            for _, *area2 in reboot_steps[step_num + 1:]:
                if intersects_3d(*area1, *area2):
                    intersect = intersection(*area1, *area2)
                    intersections.append(intersect)

            total_on -= volume_of_union(intersections, len(intersections))

    return total_on


if TESTING == "Basic":
    filename = "sampleInput.txt"
elif TESTING == "Normal":
    filename = "sampleInput1.txt"
elif TESTING == "Advanced":
    filename = "sampleInput2.txt"
else:
    filename = "input.txt"

print("Part 1: ", part1(filename))
print("Part 2: ", part2(filename))
