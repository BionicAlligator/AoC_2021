import re, math
TESTING = True


class Node:
    def __init__(self, parent=None, left=None, right=None, value=-1):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        if self.value > -1:
            return(f"{self.value}")
        else:
            return(f"[{self.left},{self.right}]")

    def parse(self, num_string):
        if num_string[0].isdigit():
            groups = re.match("^(\d+)(.*)$", num_string)
            self.value = int(groups[1])
            return groups[2]

        if num_string[0] == "[":
            self.left = Node(parent=self)
            num_string = self.left.parse(num_string[1:])

            if num_string[0] != ",":
                print(f"Expecting comma but got {num_string}")

            self.right = Node(parent=self)
            num_string = self.right.parse(num_string[1:])

        if num_string[0] != "]":
            print(f"Expecting ] but got {num_string}")

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
        print(f"Exploding {self}")

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
        print(f"Splitting {self}", end="")

        self.left = Node(parent=self, value=(self.value // 2))
        self.right = Node(parent=self, value=(math.ceil(self.value / 2)))
        self.value = -1

        print(f" into {self}")

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
            print(f"Reduce run on non-root node: {self}")
            exit(1)

        exploded = True
        split = True

        while split:
            while exploded:
                exploded = self.do_explosion(0)
                if exploded:
                    print(f"After Explosion: {self}")

            exploded = True  # If there is a split, we need to check for further explosions

            split = self.do_split()
            if split:
                print(f"After Split: {self}")

    def magnitude(self):
        return 0  # TODO: Implement this

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


def read_input():
    file.seek(0)
    lines = [line.rstrip() for line in file]
    return lines

def snailfish_add(num1, num2):
    total = Node(left=num1, right=num2)
    num1.parent = total
    num2.parent = total
    total.reduce()
    return total


def part1(inputs):
    input_nums = []

    for input_string in inputs:
        node = Node()
        node.parse(input_string)
        input_nums.append(node)

    total = input_nums[0]

    for num in range(1, len(input_nums)):
        total = snailfish_add(total, input_nums[num])

        print(f"Total = {total}")

    return total

def part2():
    return


if TESTING:
    print("Part 1")
    # tests = read_tests("sampleInput_isolation_6.txt")
    tests = read_tests("sampleInput_additions.txt")

    for expected, inputs in tests:
        print(f"\n\n{expected = }, {inputs = }")

        actual = part1(inputs)

        if expected == str(actual):
            print(f"Passed: {inputs} -> {actual}")
        else:
            print(f"Failed: {inputs} -> {actual}, expected {expected}")
else:
    file = open("input.txt", "r")
    # print("Part 1: ", part1())
    # print("Part 2: ", part2())


# def test_exploding():
#     print("\n\nTESTING EXPLOSIONS")
#     test = Node()
#     test.parse("[[[[8,7],[7,0]],[[7,8],[[7,7],15]]],[[[0,4],6],[8,7]]]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[[[[8,7],[7,0]],[[7,15],[0,22]]],[[[0,4],6],[8,7]]]":
#         print(" PASS")
#     else:
#         print(" FAIL")
#
#     test = Node()
#     test.parse("[[[[[9,8],1],2],3],4]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[[[[0,9],2],3],4]":
#         print(" PASS")
#
#     test = Node()
#     test.parse("[7,[6,[5,[4,[3,2]]]]]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[7,[6,[5,[7,0]]]]":
#         print(" PASS")
#
#     test = Node()
#     test.parse("[[6,[5,[4,[3,2]]]],1]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[[6,[5,[7,0]]],3]":
#         print(" PASS")
#
#     test = Node()
#     test.parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]":
#         print(" PASS")
#
#     test = Node()
#     test.parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
#     test.do_explosion(0)
#     print(f"After explosion: {test}", end="")
#     if str(test) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]":
#         print(" PASS")
#
# test_exploding()
