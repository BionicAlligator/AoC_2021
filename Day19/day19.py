TESTING = True
OUTPUT_TO_CONSOLE = True

# Number of beacons that must be matching between two scanners to confirm overlap of their scan regions
REQUIRED_MATCHING_BEACONS = 12
REQUIRED_MATCHING_DISTANCE_SETS = (REQUIRED_MATCHING_BEACONS * (REQUIRED_MATCHING_BEACONS - 1)) / 2


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

                axis_distances = set(map(lambda i, j: abs(i-j), beacon1, beacon2))

                log(f"{beacon1} --> {beacon2} = {axis_distances}")
                distances.update({(beacon1, beacon2): axis_distances})

        scan_distances.append(distances)

    return scan_distances


def count_matching(scanner1_distances, scanner2_distances):
    num_matching = 0

    for distance_set1 in scanner1_distances.values():
        for distance_set2 in scanner2_distances.values():
            if distance_set1 == distance_set2:
                num_matching += 1

    return num_matching


def calc_matching_distances(distances):
    matching_distances = {}

    # Find how many of the distance sets match between scanner 0 and the others
    # Any with less than the required number of matching distance sets can be discarded - assume there is no overlap
    # Work down the list, starting with the one with the most matching distances - most likely to be an overlap

    for scanner1_num, scanner1_distances in enumerate(distances):
        matching_distances[scanner1_num] = {}

        for scanner2_num, scanner2_distances in enumerate(distances):
            if scanner1_num != scanner2_num:
                num_matching = count_matching(scanner1_distances, scanner2_distances)

                # Only record those where the number of matching beacons meets the requirement to confirm overlap
                if num_matching >= REQUIRED_MATCHING_DISTANCE_SETS:
                    matching_distances[scanner1_num][scanner2_num] = num_matching

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
