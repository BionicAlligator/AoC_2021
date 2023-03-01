from collections import defaultdict

TESTING = False
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


def extract_matching_beacons(scanner1_distances, scanner2_distances):
    matching_beacons = []

    for beacons1, distance_set1 in scanner1_distances.items():
        for beacons2, distance_set2 in scanner2_distances.items():
            if distance_set1 == distance_set2:
                matching_beacons.append((beacons1, beacons2))

    return matching_beacons


def find_matching_beacons(distances, all_beacons):
    matching_beacons = {}

    for scanner1_num, scanner1_distances in enumerate(distances):
        matching_beacons[scanner1_num] = {}

        for scanner2_num, scanner2_distances in enumerate(distances):
            if scanner1_num < scanner2_num:
                matching = extract_matching_beacons(scanner1_distances, scanner2_distances)

                if len(matching) not in [0, REQUIRED_MATCHING_DISTANCE_SETS]:
                    print(f"Found {len(matching)} matching distances between scanner {scanner1_num} and scanner {scanner2_num}")

                # Only record those where the number of matching beacons meets the requirement to confirm overlap
                if len(matching) >= REQUIRED_MATCHING_DISTANCE_SETS:
                    matching_beacons[scanner1_num][scanner2_num] = matching

                for _, (s2b1, s2b2) in matching:
                    if s2b1 in all_beacons[scanner2_num]:
                        all_beacons[scanner2_num].remove(s2b1)

                    if s2b2 in all_beacons[scanner2_num]:
                        all_beacons[scanner2_num].remove(s2b2)

    return matching_beacons


def determine_primary_scanner(matching_distances):
    primary_scanner = 0
    most_overlaps = 0

    for scanner_num, matches in matching_distances.items():
        scanner_overlaps = len(matches)

        # Check that we don't have any isolated scanners
        # If we do, we can simply add the number of beacons seen by this scanner to the total (NOT YET IMPLEMENTED)
        # However, we are not able to determine their positions relative to the other scanners
        if scanner_overlaps == 0:
            print(f"Scanner {scanner_num} has no overlaps")
            exit(1)

        if scanner_overlaps > most_overlaps:
            primary_scanner = scanner_num
            most_overlaps = scanner_overlaps

    return primary_scanner


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
            print(f"Inconclusive: Require {REQUIRED_MATCHING_BEACONS - 1} occurrences of the same mapping for {scanner1_beacon} but have {max_occurrences}")
            exit(1)

        scanner2_beacon = max(potential_beacon_mappings[scanner1_beacon],
                              key=potential_beacon_mappings[scanner1_beacon].get)
        mappings.append((scanner1_beacon, scanner2_beacon))

    return mappings


def calc_translation_and_inversion(corresponding_beacons):
    s1_beacon1 = corresponding_beacons[0][0]
    s1_beacon2 = corresponding_beacons[1][0]
    s2_beacon1 = corresponding_beacons[0][1]
    s2_beacon2 = corresponding_beacons[1][1]

    s1_distances = list(map(lambda i, j: i - j, s1_beacon1, s1_beacon2))
    s2_distances = list(map(lambda i, j: i - j, s2_beacon1, s2_beacon2))

    translation = []
    inversion = [1, 1, 1]

    for axis1, dist1 in enumerate(s1_distances):
        for axis2, dist2 in enumerate(s2_distances):
            if abs(dist1) == abs(dist2):
                # It's possible the distance between the beacons may be the same on two axes
                # If this is the case, we will need to use a different pair of beacons (NOT YET IMPLEMENTED)
                if axis2 in translation:
                    print(f"{s1_distances} and {s2_distances} have the same separation on two different axes")
                    exit(1)

                translation.append(axis2)

                if dist1 == -dist2:
                    inversion[axis1] = -1

    if len(translation) != 3:
        print(f"{s1_distances} and {s2_distances} do not appear to match")
        exit(1)

    return translation, inversion

def normalise_beacons(matching_beacons, scanner1):
    normalised_beacons = set()

    for scanner2, common_beacons in matching_beacons[scanner1].items():
        # To determine which beacon is which, we must look at two or more pairs from scanner 1
        # with the same beacon and see which of the beacons in the corresponding scanner 2 pairs is the same
        # e.g: ((a, b) -> (c, d), (a, e) -> (f, c)) suggests that scanner1's beacon 'a' corresponds to
        # scanner2's beacon 'c'.  This can be further verified by checking the other instances of beacon 'a'
        corresponding_beacons = map_beacons(common_beacons)
        log(f"{corresponding_beacons = }")

        translation, inversion = calc_translation_and_inversion(corresponding_beacons)
        log(f"Scanner {scanner2} {translation = }, {inversion = }")

        # offset = calc_sensor_offset()

    return normalised_beacons


def normalise_beacon_locations(matching_beacons):
    # We'll use the orientation of the scanner with the most overlaps as "normal"
    # and it's position as the origin (0,0,0)
    primary_scanner = determine_primary_scanner(matching_beacons)
    log(f"Scanner {primary_scanner} has the most overlaps; setting as primary")

    # We can add all the primary scanner's beacons directly
    beacons = set(scan[primary_scanner])

    # TODO: It's not just the matching beacons that need to be normalised and added to the set
    # TODO: We need to convert all of the secondary scanner's beacons and then recurse to do the same for
    # TODO: all scanners that overlap with that secondary scanner

    # Find the scanner with the most overlaps and set it as primary
    # Initialise a set containing the primary scanner plus all the overlapping scanners
    # If another scanner overlaps with any scanners in the set, remove those overlaps from the
    # second scanner's list.  If this leaves the scanner with no overlaps, remove it altogether
    # Find the scanner with the next highest number of overlaps and do the same, until all scanners appear
    # in the set
    # Find the scanner with the fewest overlapping scanners and normalise all the overlapping scanners' beacons
    # based on that scanner, adding them as if they were beacons that scanner can see
    # Repeat until all scanners have been normalised and all beacons are found

    normalised_beacons = normalise_beacons(matching_beacons, primary_scanner)

    beacons = beacons.union(normalised_beacons)

    return beacons


def part1(scan):
    log(f"{scan = }")

    distances = calc_distances(scan)
    log(f"{distances = }")

    all_beacons = scan.copy()

    matching_beacons = find_matching_beacons(distances, all_beacons)
    # log(f"{matching_beacons = }")

    num_beacons = sum([len(scanner_beacons) for scanner_beacons in all_beacons])
    log(f"{num_beacons = }: {all_beacons = }")
    log(f"{num_beacons = }")

    exit(1)

    beacons = normalise_beacon_locations(matching_beacons)
    log(f"{len(beacons)} {beacons = }")

    return len(beacons)


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

scan = read_input(filename)

print("Part 1: ", part1(scan))
