import re

TESTING = "False"
OUTPUT_TO_CONSOLE = True

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


def determine_range(reboot_steps):
    x_range = (float('inf'), float('-inf'))
    y_range = (float('inf'), float('-inf'))
    z_range = (float('inf'), float('-inf'))

    for on_off, x, y, z in reboot_steps:
        if on_off == "on":
            x_range = (min(x[0], x_range[0]), max(x[1], x_range[1]))
            y_range = (min(y[0], y_range[0]), max(y[1], y_range[1]))
            z_range = (min(z[0], z_range[0]), max(z[1], z_range[1]))

    log(f"{x_range = }, {y_range = }, {z_range = }")
    return x_range, y_range, z_range


def intersects(range1, range2):
    return True if (range1[0] <= range2[0] <= range1[1]) or \
                   (range2[0] <= range1[0] <= range2[1]) else False


def intersects_3d(x_range1, y_range1, z_range1, x_range2, y_range2, z_range2):
    return True if intersects(x_range1, x_range2) and \
                   intersects(y_range1, y_range2) and \
                   intersects(z_range1, z_range2) else False


def intersects_init_area(x_range, y_range, z_range):
    return True if intersects_3d(INIT_RANGE, INIT_RANGE, INIT_RANGE,
                                 x_range, y_range, z_range) else False

def constrain(value):
    return max(min(value, INIT_RANGE[1]), INIT_RANGE[0])


# Ideas:
# 1. With set of 3D coords:
#   Start from bottom and work up
#   Set on or off only cubes that are not already in the output set
#   Count total set to on
#
# 2. Determine intersections
#
# 3. Create a set of all "on" coords
#   This works for -50..50 but not for -100000..100000
#   Work out max and min values for each axis to properly evaluate the scale
#   Test creation of set of full range of coords
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


if TESTING == "Basic":
    filename = "sampleInput.txt"
elif TESTING == "Advanced":
    filename = "sampleInput1.txt"
else:
    filename = "input.txt"

print("Part 1: ", part1(filename))
