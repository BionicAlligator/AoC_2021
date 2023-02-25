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


def determine_primary_scanner(matching_distances):
    primary_scanner = 0
    most_overlaps = 0

    for scanner_num, matches in matching_distances.items():
        scanner_overlaps = len(matches)

        # Check that we don't have any isolated scanners
        # If we do, we can simply add the number of beacons seen by this scanner to the total
        # However, we are not able to determine their positions relative to the other scanners
        if scanner_overlaps == 0:
            log(f"Scanner {scanner_num} has no overlaps")
            exit(1)

        if scanner_overlaps > most_overlaps:
            primary_scanner = scanner_num
            most_overlaps = scanner_overlaps

    return primary_scanner


def part1(scan):
    log(f"{scan = }")

    distances = calc_distances(scan)
    log(f"{distances = }")

    matching_distances = calc_matching_distances(distances)
    log(f"{matching_distances = }")

    # We'll use the orientation of the scanner with the most overlaps as "normal"
    # and it's position as the origin (0,0,0)
    primary_scanner = determine_primary_scanner(matching_distances)
    log(f"Scanner {primary_scanner} has the most overlaps")

    # We can add all the primary scanner's beacons directly
    beacons = set(scan[primary_scanner])
    log(f"{len(beacons)} {beacons = }")

    return


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

scan = read_input(filename)

print("Part 1: ", part1(scan))
