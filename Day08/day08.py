TESTING = False

def read_input():
    file.seek(0)
    notes = [tuple(map(lambda s: s.split(" "), line.rstrip().split(" | "))) for line in file]
    # print("Notes:", notes)
    return notes

def part1():
    notes = read_input()

    easy_patterns = list(map(lambda entry: list(filter(lambda pattern: len(pattern) in [2, 3, 4, 7], entry[1])), notes))
    print(f"Easy patterns: {easy_patterns}")

    return sum(len(pattern) for pattern in easy_patterns)

def part2():
    notes = read_input()

    total = 0

    for input, output in notes:
        digits = [""] * 10

        for pattern in (input + output):
            match len(pattern): #First find the easy digits
                case 2:
                    digits[1] = sorted(pattern)
                case 4:
                    digits[4] = sorted(pattern)
                case 3:
                    digits[7] = sorted(pattern)
                case 7:
                    digits[8] = sorted(pattern)

        for pattern in (input + output):
            match len(pattern):
                case 6: #Either 0, 6 or 9
                    #6 if it doesn't have both of the characters in 1
                    if len(set(pattern) & set(digits[1])) < 2:
                        digits[6] = sorted(pattern)
                    #9 if it has all of the characters in 4
                    elif len(set(pattern) & set(digits[4])) == 4:
                        digits[9] = sorted(pattern)
                    #else 0
                    else:
                        digits[0] = sorted(pattern)

                case 5: #Either 2, 3 or 5
                    #3 if it has all of the characters in 1
                    if len(set(pattern) & set(digits[1])) == 2:
                        digits[3] = sorted(pattern)
                    #5 if it has 3 of the characters in 4
                    elif len(set(pattern) & set(digits[4])) == 3:
                        digits[5] = sorted(pattern)
                    #else 2
                    else:
                        digits[2] = sorted(pattern)

        # print (digits)
        output_num = ""

        for pattern in output:
            for digit, digit_pattern in enumerate(digits):
                if sorted(pattern) == digit_pattern:
                    output_num += str(digit)

        # print(f"{output_num}")
        total += int(output_num)

    return total


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
