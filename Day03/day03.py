TESTING = False

def read_input():
    file.seek(0)
    lines = [list(map(int, list(line.rstrip()))) for line in file]
    # print ("Input lines:", lines)
    return lines

def part1():
    report = read_input()
    most_common_bit = []
    least_common_bit = []

    for bit_num in range(0, len(report[0])):
        most_common_bit.append(1 if sum([bit[bit_num] for bit in report]) > (len(report) / 2) else 0)
        least_common_bit.append(1 - most_common_bit[bit_num])

    gamma_rate = int("".join(str(bit) for bit in most_common_bit), 2)
    epsilon_rate = int("".join(str(bit) for bit in least_common_bit), 2)

    return gamma_rate * epsilon_rate

def bit_matches(num, bit_num, bit):
    if num[bit_num] == bit:
        return True

    return False

def check_bit(bit_num, bit, nums):
    matching_nums = []

    for num in nums:
        if bit_matches(num, bit_num, bit):
            # print(f"{num} has {bit} at position {bit_num}")
            matching_nums.append(num)
        # else:
            # print(f"{num} does not have {bit} at position {bit_num}")

    return matching_nums

def determine_rating(rating_type, report):
    filter_value = 1 if rating_type == "oxygen" else 0

    matching_nums = report.copy()

    if len(matching_nums) == 1:
        return matching_nums

    bit_mask = ["-" for bit in report[0]]

    for bit_num in range(0, len(report[0])):
        filter_bit = filter_value if sum([bit[bit_num] for bit in matching_nums]) >= (len(matching_nums) / 2) else (1 - filter_value)
        bit_mask[bit_num] = filter_bit

        # print(f"Checking bit {bit_num} against {filter_bit}")
        matching_nums = check_bit(bit_num, filter_bit, matching_nums)
        # print(f"Matching nums: {matching_nums}\n")

        if len(matching_nums) == 1:
            # print(f"Rating determined: {matching_nums}\n")
            return matching_nums[0]

    print(f"MORE OR LESS THAN ONE NUM MATCHING {bit_mask} IN {matching_nums}")
    exit(1)

def part2():
    report = read_input()

    oxygen_binary = determine_rating("oxygen", report)
    co2_binary = determine_rating("co2", report)

    # print(f"Oxygen binary = {oxygen_binary}, CO2 binary = {co2_binary}")

    oxygen_generator_rating = int("".join(str(bit) for bit in oxygen_binary), 2)
    co2_scrubber_rating = int("".join(str(bit) for bit in co2_binary), 2)

    print(f"Oxygen generator rating = {oxygen_generator_rating}, CO2 scrubber rating = {co2_scrubber_rating}")

    return oxygen_generator_rating * co2_scrubber_rating


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
