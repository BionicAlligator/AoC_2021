import math
import re

TESTING = False
OUTPUT_TO_CONSOLE = False


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


class Node:
    def __init__(self, parent=None, left=None, right=None, value=-1):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        if self.value > -1:
            return f"{self.value}"
        else:
            return f"[{self.left},{self.right}]"

    def parse(self, num_string):
        if num_string[0].isdigit():
            groups = re.match('^(\d+)(.*)$', num_string)
            self.value = int(groups[1])
            return groups[2]

        if num_string[0] == "[":
            self.left = Node(parent=self)
            num_string = self.left.parse(num_string[1:])

            if num_string[0] != ",":
                log(f"Expecting comma but got {num_string}")

            self.right = Node(parent=self)
            num_string = self.right.parse(num_string[1:])

        if num_string[0] != "]":
            log(f"Expecting ] but got {num_string}")

        return num_string[1:]  # Ignore ]

    def increment_predecessor(self, increment):
        current_node = self

        while current_node.parent and current_node.parent.left == current_node:
            current_node = current_node.parent

        if current_node.parent:  # We have found a path to the left
            current_node = current_node.parent.left

            while current_node.right:
                current_node = current_node.right

            current_node.value += increment

    def increment_successor(self, increment):
        current_node = self

        while current_node.parent and current_node.parent.right == current_node:
            current_node = current_node.parent

        if current_node.parent:  # We have found a path to the right
            current_node = current_node.parent.right

            while current_node.left:
                current_node = current_node.left

            current_node.value += increment

    def explode(self):
        log(f"Exploding {self}")

        left_value = self.left.value
        right_value = self.right.value

        self.value = 0
        self.left = None
        self.right = None

        self.increment_predecessor(left_value)
        self.increment_successor(right_value)

    def do_explosion(self, depth):
        if self.value > -1:  # This is a leaf (value) node
            return False

        if depth >= 4:
            self.explode()
            return True

        if self.left.do_explosion(depth + 1):
            return True

        return self.right.do_explosion(depth + 1)

    def split(self):
        log(f"Splitting {self}", end="")

        self.left = Node(parent=self, value=(self.value // 2))
        self.right = Node(parent=self, value=(math.ceil(self.value / 2)))
        self.value = -1

        log(f" into {self}")

    def do_split(self):
        if self.value > -1:  # This is a leaf node
            if self.value > 9:
                self.split()
                return True
            else:
                return False

        if self.left.do_split():
            return True

        return self.right.do_split()

    def reduce(self):  # Only ever run on root node
        if self.parent:
            log(f"Reduce run on non-root node: {self}")
            exit(1)

        exploded = True
        split = True

        while split:
            while exploded:
                exploded = self.do_explosion(0)
                if exploded:
                    log(f"After Explosion: {self}")

            exploded = True  # If there is a split, we need to check for further explosions

            split = self.do_split()
            if split:
                log(f"After Split: {self}")

    def magnitude(self):
        if self.value > -1:
            return self.value

        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())


def read_tests(test_filename):
    tests = []
    inputs = []
    expected = ""

    file = open(test_filename, "r")

    for line in file:
        if "=" in line:  # Line with equals sign means it is the expected output
            expected = line.split(" ")[0]
        elif "[" in line:
            inputs.append(line.rstrip())
        else:  # Blank line means end of test specification
            tests.append((expected, inputs.copy()))
            inputs = []

    return tests


def read_input(filename):
    num_strings = []

    file = open(filename, "r")

    for line in file:
        num_strings.append(line.rstrip())

    return num_strings


def snailfish_add(num1, num2):
    total = Node(left=num1, right=num2)
    num1.parent = total
    num2.parent = total
    total.reduce()
    return total


def part1(num_strings):
    nums = []

    for num_string in num_strings:
        node = Node()
        node.parse(num_string)
        nums.append(node)

    total = nums[0]

    for index in range(1, len(nums)):
        total = snailfish_add(total, nums[index])

        log(f"Total = {total}")

    return total.magnitude()


def part2(num_strings):
    max_magnitude = float('-inf')

    for index1, num_string1 in enumerate(num_strings):
        for index2, num_string2 in enumerate(num_strings):
            if index1 != index2:
                num1 = Node()
                num1.parse(num_string1)

                num2 = Node()
                num2.parse(num_string2)

                total = snailfish_add(num1, num2)
                magnitude = total.magnitude()
                max_magnitude = max(max_magnitude, magnitude)

    return max_magnitude


if TESTING:
    print("Part 1")
    # tests = read_tests("sampleInput_additions.txt")
    tests = read_tests("sampleInput_magnitude.txt")

    for expected, inputs in tests:
        actual = part1(inputs)

        if expected == str(actual):
            print(f"Passed: {inputs} -> {actual}\n\n")
        else:
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n\n")

    print("Part 2")
    tests = read_tests("sampleInput_part2.txt")

    for expected, inputs in tests:
        actual = part2(inputs)

        if expected == str(actual):
            print(f"Passed: {inputs} -> {actual}\n\n")
        else:
            print(f"Failed: {inputs} -> {actual}, expected {expected}\n\n")

else:
    num_strings = read_input("input.txt")

    print("Part 1: ", part1(num_strings))
    print("Part 2: ", part2(num_strings))


# def test_exploding():
#     print("TESTING EXPLOSIONS")
#
#     tests = read_tests("sampleInput_explosions.txt")
#
#     for expected, inputs in tests:
#         test = Node()
#         test.parse(inputs[0])
#         test.do_explosion(0)
#
#         if expected == str(test):
#             print(f"Passed: {inputs} -> {test}\n")
#         else:
#             print(f"Failed: {inputs} -> {test}, expected {expected}\n")
#
# test_exploding()
