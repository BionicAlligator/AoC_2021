TESTING = False

def read_tests():
    file.seek(0)
    tests = [line.rstrip().split(" ") for line in file]
    return tests


def convert_to_binary_string(hex_transmission):
    # By default, the conversion to binary ignores (removes) leading zeroes, so we
    # need to add them back in afterwards
    expected_binary_digits = len(hex_transmission) * 4
    binary_transmission = str(bin(int(hex_transmission, 16)))[2:]
    return binary_transmission.zfill(expected_binary_digits)


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
            literal = ""
            more_groups = True

            while more_groups:
                # If first bit is "0" then this is the last packet of literal
                # Next four bits are a segment of the literal value
                more_groups, group, packet = int(packet[:1]), packet[1:5], packet[5:]
                literal += group
                bit_count += 5

            # Convert binary to decimal
            value = int(literal, 2)

            print(f"Literal: {value}")
            parsed_packet.update({"value": value})

        case operator:   # This is an Operator
            print(f"Operator: {operator}")

            # First bit indicates how sub-packets should be extracted
            length_type, packet = packet[:1], packet[1:]
            bit_count += 1

            sub_packets = []

            if length_type == "0":
                # Next 15 bits indicate length of sub-packets
                total_sub_packet_bits, packet = int(packet[:15], 2), packet[15:]
                bit_count += 15
                end_of_subpackets = bit_count + total_sub_packet_bits

                while bit_count < end_of_subpackets:
                    sub_packet_bits, sub_packet_version_sum, sub_packet = parse_packet(packet)
                    sub_packets.append(sub_packet)
                    packet = packet[sub_packet_bits:]
                    version_sum += sub_packet_version_sum
                    bit_count += sub_packet_bits

            else:  # length_type == 1
                # Next 11 bits indicate number of sub-packets
                num_sub_packets, packet = int(packet[:11], 2), packet[11:]
                bit_count += 11

                for _ in range(num_sub_packets):
                    sub_packet_bits, sub_packet_version_sum, sub_packet = parse_packet(packet)
                    sub_packets.append(sub_packet)
                    packet = packet[sub_packet_bits:]
                    version_sum += sub_packet_version_sum
                    bit_count += sub_packet_bits

            parsed_packet.update({"sub_packets": sub_packets})

    return bit_count, version_sum, parsed_packet

def part1(hex_transmission):
    # Convert to binary
    transmission = convert_to_binary_string(hex_transmission)

    # Parse packet
    _, version_sum, parsed_packet = parse_packet(transmission)

    return version_sum

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
    tests = read_tests()

    for expected, transmission in tests:
        actual = part1(transmission)

        if int(expected) == actual:
            print(f"Passed: {transmission} -> {actual}")
        else:
            print(f"Failed: {transmission} -> {actual}, expected {expected}")
else:
    file = open("input.txt", "r")
    file.seek(0)
    transmission = file.readline().rstrip()

    print(f"Part1: {part1(transmission)}")
    # print(f"Part2: {part2(transmission)}")
