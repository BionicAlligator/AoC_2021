TESTING = False

def read_input():
    file.seek(0)
    lines = [list(line.rstrip()) for line in file]
    print ("Input lines:", lines)
    return lines

def part1():
    report = read_input()
    most_common_bit = []
    least_common_bit = []

    for bit_num in range(0, len(report[0])):
        most_common_bit.append(1 if sum([int(bit[bit_num]) for bit in report]) > (len(report) // 2) else 0)
        least_common_bit.append(1 - most_common_bit[bit_num])

    gamma_rate = int("".join(str(bit) for bit in most_common_bit), 2)
    epsilon_rate = int("".join(str(bit) for bit in least_common_bit), 2)

    return gamma_rate * epsilon_rate

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
