TESTING = True
OUTPUT_TO_CONSOLE = True


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_input(filename):
    file = open(filename, "r")

    scan = []
    beacons = []

    for line in file:
        if not line.strip():  # Blank line
            scan.append(beacons)
        elif "---" in line:  # Start of data from next scanner
            beacons = []
        else:  # Beacon line
            x, y, z = line.split(",")
            beacons.append((int(x), int(y), int(z)))

    return scan


def calc_distances(scan):
    scan_distances = []

    for beacons in scan:
        distances = {}

        for beacon1_index, beacon1 in enumerate(beacons):
            for beacon2_index in range(beacon1_index + 1, len(beacons)):
                beacon2 = beacons[beacon2_index]

                axis_distances = tuple(map(lambda i, j: abs(i-j), beacon1, beacon2))
                manhattan_distance = sum(axis_distances)

                log(f"{beacon1} --> {beacon2} = {manhattan_distance}")
                distances.update({(beacon1, beacon2): manhattan_distance})

        scan_distances.append(distances)

    return scan_distances


def calc_matching_distances(distances):
    matching_distances = {}

    # Find how many of the distances match between scanner 0 and the others
    # Any with less than 12 matching distances can be discarded - assume there is no overlap
    # Work down the list, starting with the one with the most matching distances - most likely to be an overlap

    return matching_distances

def part1(scan):
    log(f"{scan = }")

    distances = calc_distances(scan)
    log(f"{distances = }")

    matching_distances = calc_matching_distances(distances)
    log(f"{matching_distances = }")

    # We'll use the first scanner's orientation as "normal" and it's position as the origin (0,0,0)
    # Therefore, we can add all of the first scanner's beacons directly
    beacons = set(scan[0])
    log(f"{len(beacons)} {beacons = }")

    return


if TESTING:
    scan = read_input("sampleInput.txt")

    print("Part 1: ", part1(scan))
else:
    inputs = read_input("input.txt")

    print("Part 1: ", part1(inputs))
