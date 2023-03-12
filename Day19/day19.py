from collections import defaultdict

TESTING = False
OUTPUT_TO_CONSOLE = False

# Number of beacons that must be matching between two scanners to confirm overlap of their scan regions
REQUIRED_MATCHING_BEACONS = 12
REQUIRED_MATCHING_DISTANCE_SETS = (REQUIRED_MATCHING_BEACONS * (REQUIRED_MATCHING_BEACONS - 1)) / 2


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_input(filename):
    file = open(filename, "r")

    scan = {}
    beacons = []
    scanner_num = -1

    for line in file:
        if not line.strip():  # Blank line - end of this scanner's data
            scan.update({scanner_num: beacons})
        elif "---" in line:  # Start of data from next scanner
            scanner_num += 1
            beacons = []
        else:  # Beacon line
            x, y, z = line.split(",")
            beacons.append((int(x), int(y), int(z)))

    return scan


def distance_between(point1, point2):
    return point1 - point2


def absolute_distance_between(point1, point2):
    return abs(distance_between(point1, point2))


def calc_distances(scan):
    scan_distances = {}

    for scanner_num, beacons in scan.items():
        distances = {}

        for beacon1_index, beacon1 in enumerate(beacons):
            for beacon2_index in range(beacon1_index + 1, len(beacons)):
                beacon2 = beacons[beacon2_index]

                axis_distances = set(map(absolute_distance_between, beacon1, beacon2))

                log(f"{beacon1} --> {beacon2} = {axis_distances}")
                distances.update({(beacon1, beacon2): axis_distances})

        scan_distances.update({scanner_num: distances})

    return scan_distances


def extract_matching_beacons(scanner1_distances, scanner2_distances):
    matching_beacons = []

    for beacons1, distance_set1 in scanner1_distances.items():
        for beacons2, distance_set2 in scanner2_distances.items():
            if distance_set1 == distance_set2:
                matching_beacons.append((beacons1, beacons2))

    return matching_beacons


def find_matching_beacons(distances, scanner1_num):
    scanner1_distances = distances[scanner1_num]

    matching_beacons = {}

    for scanner2_num, scanner2_distances in distances.items():
        if scanner1_num != scanner2_num:
            matching = extract_matching_beacons(scanner1_distances, scanner2_distances)

            # Only record those where the number of matching beacons meets the requirement to confirm overlap
            if len(matching) >= REQUIRED_MATCHING_DISTANCE_SETS:
                matching_beacons[scanner2_num] = matching

    return matching_beacons


def map_beacons(common_beacons):
    potential_beacon_mappings = {}
    scanner1_beacon_set = set()

    for (s1b1, s1b2), (s2b1, s2b2) in common_beacons:
        if s1b1 not in potential_beacon_mappings:
            potential_beacon_mappings[s1b1] = defaultdict(int)

        if s1b2 not in potential_beacon_mappings:
            potential_beacon_mappings[s1b2] = defaultdict(int)

        scanner1_beacon_set.add(s1b1)
        scanner1_beacon_set.add(s1b2)

        potential_beacon_mappings[s1b1][s2b1] += 1
        potential_beacon_mappings[s1b1][s2b2] += 1
        potential_beacon_mappings[s1b2][s2b1] += 1
        potential_beacon_mappings[s1b2][s2b2] += 1

    mappings = []

    for scanner1_beacon in scanner1_beacon_set:
        max_occurrences = max(potential_beacon_mappings[scanner1_beacon].values())

        # There should be n-1 occurrences of the same mapping (where n is the number of matching beacons
        # required to confirm overlapping scan regions)
        if max_occurrences != (REQUIRED_MATCHING_BEACONS - 1):
            print(f"Inconclusive: Require {REQUIRED_MATCHING_BEACONS - 1} occurrences of the same mapping for "
                  f"{scanner1_beacon} but have {max_occurrences}")
            exit(1)

        scanner2_beacon = max(potential_beacon_mappings[scanner1_beacon],
                              key=potential_beacon_mappings[scanner1_beacon].get)
        mappings.append((scanner1_beacon, scanner2_beacon))

    return mappings


def calc_rotation_and_inversion(corresponding_beacons):
    s1_beacon1 = corresponding_beacons[0][0]
    s1_beacon2 = corresponding_beacons[1][0]
    s2_beacon1 = corresponding_beacons[0][1]
    s2_beacon2 = corresponding_beacons[1][1]

    s1_distances = list(map(distance_between, s1_beacon1, s1_beacon2))
    s2_distances = list(map(distance_between, s2_beacon1, s2_beacon2))

    rotation = []
    inversion = [1, 1, 1]

    for axis1, dist1 in enumerate(s1_distances):
        for axis2, dist2 in enumerate(s2_distances):
            if abs(dist1) == abs(dist2):
                # It's possible the distance between the beacons may be the same on two axes
                # If this is the case, we will need to use a different pair of beacons (NOT YET IMPLEMENTED)
                if axis2 in rotation:
                    print(f"{s1_distances} and {s2_distances} have the same separation on two different axes")
                    exit(1)

                rotation.append(axis2)

                if dist1 == -dist2:
                    inversion[axis1] = -1

    if len(rotation) != 3:
        print(f"{s1_distances} and {s2_distances} do not appear to match")
        exit(1)

    return rotation, inversion


def rotate_and_invert(beacon, rotation, inversion):
    converted_beacon = []

    for axis in range(3):
        converted_beacon.append(beacon[rotation[axis]] * inversion[axis])

    return converted_beacon


def translate(beacon, offset):
    converted_beacon = []

    for axis in range(3):
        converted_beacon.append(beacon[axis] + offset[axis])

    return tuple(converted_beacon)


def calc_offset(corresponding_beacons, rotation, inversion):
    s1_beacon = corresponding_beacons[0][0]
    s2_beacon = rotate_and_invert(corresponding_beacons[0][1], rotation, inversion)

    offset = []

    for axis in range(3):
        offset.append(s1_beacon[axis] - s2_beacon[axis])

    return offset


def normalise(beacon, rotation, inversion, offset):
    return translate(rotate_and_invert(beacon, rotation, inversion), offset)


def merge_scan_data(scan, distances):
    scanner_positions = {}
    normalised_beacons = set()

    # Use the first scanner in the list as the origin
    scanner_positions.update({0: (0, 0, 0)})
    normalised_beacons.update(scan.pop(0))

    current_scanner = 0
    scanners_to_check = set()

    while scan:
        matching_beacons = find_matching_beacons(distances, current_scanner)
        log(f"{matching_beacons = }")

        for scanner_num, scanner_matches in matching_beacons.items():
            if scanner_num in scan:
                scanners_to_check.add(scanner_num)

                # To determine which beacon is which, we must look at two or more pairs from scanner 1
                # with the same beacon and see which of the beacons in the corresponding scanner 2 pairs is the same
                # e.g: ((a, b) -> (c, d), (a, e) -> (f, c)) suggests that scanner1's beacon 'a' corresponds to
                # scanner2's beacon 'c'.  This can be further verified by checking the other instances of beacon 'a'
                corresponding_beacons = map_beacons(scanner_matches)
                log(f"{corresponding_beacons = }")

                rotation, inversion = calc_rotation_and_inversion(corresponding_beacons)
                offset = calc_offset(corresponding_beacons, rotation, inversion)
                log(f"Scanner {scanner_num} {rotation = }, {inversion = }, position/{offset = }")

                # The offset equals the position of the second scanner relative to the origin
                scanner_positions.update({scanner_num: tuple(offset)})

                scanner_beacons = scan.pop(scanner_num)

                for beacon in scanner_beacons:
                    normalised_beacons.add(normalise(beacon, rotation, inversion, offset))

                scanner_distances = distances.pop(scanner_num)
                converted_scanner_distances = {}

                for (beacon1, beacon2), distance in scanner_distances.items():
                    normalised_beacon1 = normalise(beacon1, rotation, inversion, offset)
                    normalised_beacon2 = normalise(beacon2, rotation, inversion, offset)
                    converted_scanner_distances.update({(normalised_beacon1, normalised_beacon2): distance})

                distances.update({scanner_num: converted_scanner_distances})

        distances.pop(current_scanner)
        current_scanner = scanners_to_check.pop()

    return scanner_positions, normalised_beacons


def find_max_scanner_separation(scanner_positions):
    max_separation = float('-inf')

    for scanner1_index, scanner1 in scanner_positions.items():
        for scanner2_index in range(scanner1_index + 1, len(scanner_positions)):
            scanner2 = scanner_positions[scanner2_index]

            manhattan_distance = sum(map(absolute_distance_between, scanner1, scanner2))
            log(f"{scanner1} --> {scanner2} = {manhattan_distance}")

            max_separation = max(max_separation, manhattan_distance)

    return max_separation


def solve():
    scan = read_input(filename)
    log(f"{scan = }")

    distances = calc_distances(scan)
    log(f"{distances = }")

    scanner_positions, beacon_positions = merge_scan_data(scan, distances)
    log(f"{scanner_positions = }")

    print(f"Part 1: {len(beacon_positions)} beacons")
    print(f"Part 2: Max scanner separation = {find_max_scanner_separation(scanner_positions)}")


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

solve()
