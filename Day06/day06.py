TESTING = False

def read_input():
    file.seek(0)
    raw_nums = list(map(int, file.readline().rstrip().split(",")))

    lanternfish = [0] * 9

    for num in raw_nums:
        lanternfish[num] += 1

    # print ("Lanternfish:", lanternfish)
    return lanternfish

def part1():
    #Store an array of 9 numbers: each number represents the number of lanternfish with
    #a timer value equal to the array index
    #Repeatedly update the array such that the value at each index equals the value of
    #the index above, except:
    #The value at index 8 equals the value at index 0
    #The value at index 6 equals the value at index 7 plus the value at index 0

    lanternfish = read_input()

    for day in range(80):
        fish_reproducing = lanternfish[0]

        for num in range(8):
            lanternfish[num] = lanternfish[num + 1]

        lanternfish[8] = fish_reproducing
        lanternfish[6] += fish_reproducing

    return sum(lanternfish)

def part2():
    lanternfish = read_input()

    for day in range(256):
        fish_reproducing = lanternfish[0]

        for num in range(8):
            lanternfish[num] = lanternfish[num + 1]

        lanternfish[8] = fish_reproducing
        lanternfish[6] += fish_reproducing

    return sum(lanternfish)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
