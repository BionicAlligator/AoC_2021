from math import prod
TESTING = False

def read_tests(test_filename):
    file = open(test_filename, "r")
    tests = [line.rstrip().split(" ") for line in file]
    return tests


def convert_to_binary_string(hex_transmission):
    # By default, the conversion to binary ignores (removes) leading zeroes, so we
    # need to add them back in afterwards
    expected_binary_digits = len(hex_transmission) * 4
    binary_transmission = str(bin(int(hex_transmission, 16)))[2:]
    return binary_transmission.zfill(expected_binary_digits)


def parse_literal(packet):
    literal = ""
    literal_bits = 0
    more_groups = True

    while more_groups:
        # If first bit is "0" then this is the last packet of literal
        # Next four bits are a segment of the literal value
        more_groups, group, packet = int(packet[:1]), packet[1:5], packet[5:]
        literal += group
        literal_bits += 5

    # Convert binary to decimal
    value = int(literal, 2)
    print(f"Literal: {value}")

    return literal_bits, value


def parse_sub_packet(operator_bits, operator_version_sum, packet, sub_packets):
    sub_packet_bits, sub_packet_version_sum, sub_packet = parse_packet(packet)
    sub_packets.append(sub_packet)
    packet = packet[sub_packet_bits:]
    operator_version_sum += sub_packet_version_sum
    operator_bits += sub_packet_bits
    return operator_bits, operator_version_sum, packet


def greater_than(args):
    return 1 if args[0] > args[1] else 0


def less_than(args):
    return 1 if args[0] < args[1] else 0


def equal(args):
    return 1 if args[0] == args[1] else 0


def parse_operator(operator, packet):
    evaluate = {
        "000": sum,
        "001": prod,
        "010": min,
        "011": max,
        "101": greater_than,
        "110": less_than,
        "111": equal
    }

    operator_bits = 0
    operator_version_sum = 0

    # First bit indicates how sub-packets should be extracted
    length_type, packet = packet[:1], packet[1:]
    operator_bits += 1
    sub_packets = []

    if length_type == "0":
        # Next 15 bits indicate length of sub-packets
        total_sub_packet_bits, packet = int(packet[:15], 2), packet[15:]
        operator_bits += 15
        end_of_subpackets = operator_bits + total_sub_packet_bits

        while operator_bits < end_of_subpackets:
            operator_bits, operator_version_sum, packet = parse_sub_packet(
                operator_bits,
                operator_version_sum,
                packet,
                sub_packets)

    else:  # length_type == 1
        # Next 11 bits indicate number of sub-packets
        num_sub_packets, packet = int(packet[:11], 2), packet[11:]
        operator_bits += 11

        for _ in range(num_sub_packets):
            operator_bits, operator_version_sum, packet = parse_sub_packet(
                operator_bits,
                operator_version_sum,
                packet,
                sub_packets)

    sub_packet_values = []

    for sub_packet in sub_packets:
        sub_packet_values.append(sub_packet["value"])

    value = evaluate[operator](sub_packet_values)

    print(f"Operator: {operator}, value: {value}")

    return operator_bits, operator_version_sum, sub_packets, value


def parse_packet(packet):
    parsed_packet = {}
    version_sum = 0

    # Initialise bit counter
    bit_count = 0

    # Read first three bits as version
    packet_version, packet = packet[:3], packet[3:]
    version_sum += int(packet_version, 2)

    # Read next three bits as type
    packet_type, packet = packet[:3], packet[3:]

    parsed_packet.update({"version": packet_version, "type": packet_type})

    bit_count += 6

    match packet_type:
        case '100':    # 4 (100): This is a Literal
            literal_bits, value = parse_literal(packet)
            bit_count += literal_bits
            parsed_packet.update({"value": value})

        case operator:   # This is an Operator
            operator_bits, operator_version_sum, sub_packets, value = parse_operator(operator, packet)
            bit_count += operator_bits
            version_sum += operator_version_sum
            parsed_packet.update({"sub_packets": sub_packets, "value": value})

    return bit_count, version_sum, parsed_packet


def part1(hex_transmission):
    # Convert to binary
    transmission = convert_to_binary_string(hex_transmission)

    # Parse packet
    _, version_sum, parsed_packet = parse_packet(transmission)

    return version_sum

def part2(hex_transmission):
    # Convert to binary
    transmission = convert_to_binary_string(hex_transmission)

    # Parse packet
    _, version_sum, parsed_packet = parse_packet(transmission)

    return parsed_packet["value"]


if TESTING:
    print("Part 1")
    tests = read_tests("sampleInput_1.txt")

    for expected, transmission in tests:
        actual = part1(transmission)

        if int(expected) == actual:
            print(f"Passed: {transmission} -> {actual}")
        else:
            print(f"Failed: {transmission} -> {actual}, expected {expected}")

    print("\n\nPart 2")
    tests = read_tests("sampleInput_2.txt")

    for expected, transmission in tests:
        actual = part2(transmission)

        if int(expected) == actual:
            print(f"Passed: {transmission} -> {actual}")
        else:
            print(f"Failed: {transmission} -> {actual}, expected {expected}")

else:
    file = open("input.txt", "r")
    file.seek(0)
    transmission = file.readline().rstrip()

    print(f"Part1: {part1(transmission)}")
    print(f"Part2: {part2(transmission)}")
