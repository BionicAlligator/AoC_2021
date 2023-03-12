import copy

TESTING = False
OUTPUT_TO_CONSOLE = False


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)


def read_input(filename):
    file = open(filename, "r")

    algorithm = [1 if char == '#' else 0 for char in file.readline().rstrip()]
    file.readline()
    input_image = [[1 if char == '#' else 0 for char in line.rstrip()] for line in file]

    return algorithm, input_image


def is_in_range(input_image, input_y, input_x):
    if input_y in range(len(input_image)) and input_x in range(len(input_image[0])):
        return True

    return False


def get_background_value(algorithm, cycle):
    if algorithm[0] == 1:
        return algorithm[0] if cycle % 2 else algorithm[-1]
    else:
        return 0


def enhance(algorithm, input_image, y, x, cycle):
    mapping_key = 0

    for offset_y in range(-1, 2):
        input_y = y + offset_y - 2

        for offset_x in range(-1, 2):
            input_x = x + offset_x - 2

            input_image_value = input_image[input_y][input_x] \
                if is_in_range(input_image, input_y, input_x) else get_background_value(algorithm, cycle)

            mapping_key = (mapping_key * 2) + input_image_value

    return algorithm[mapping_key]


def count_lit_pixels(output_image):
    return sum(map(sum, output_image))


def enhance_image(filename, num_cycles):
    algorithm, input_image = read_input(filename)
    log(f"{algorithm = }\n{input_image = }")

    lit_pixels = 0

    for cycle in range(num_cycles):
        output_image = []

        for y in range(len(input_image) + 4):
            output_image.append([])

            for x in range(len(input_image[0]) + 4):
                output_image[y].append(enhance(algorithm, input_image, y, x, cycle))

        lit_pixels = count_lit_pixels(output_image)

        log(f"Cycle {cycle} {lit_pixels = }, {output_image = }")
        input_image = copy.deepcopy(output_image)

    return lit_pixels


filename = "sampleInput.txt" if TESTING else "input.txt"

print("Part 1: ", enhance_image(filename, 2))
print("Part 2: ", enhance_image(filename, 50))
