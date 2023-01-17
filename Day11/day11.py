TESTING = False

def read_input():
    file.seek(0)
    octopii = [[int(num) for num in line.rstrip()] for line in file]
    return octopii

def inject_energy(octopii):
    return [[octopus + 1 for octopus in row] for row in octopii]

def increment_adjacents(octopus, octopii):
    new_octopii = octopii.copy()
    flashed_x, flashed_y = octopus

    for y in range(max(0, flashed_y - 1), min(len(new_octopii), flashed_y + 2)):
        for x in range(max(0, flashed_x - 1), min(len(new_octopii[0]), flashed_x + 2)):
            if not ((x == flashed_x) and (y == flashed_y)):
                new_octopii[y][x] += 1

    return new_octopii

def flash(flashes, octopii):
    new_flashes = flashes
    new_octopii = octopii.copy()

    flash = True
    flashed = []

    while flash:
        flash = False

        for y, row in enumerate(new_octopii):
            for x, octopus in enumerate(row):
                if octopus > 9 and (x, y) not in flashed:
                    flash = True
                    flashed.append((x, y))
                    new_flashes += 1
                    new_octopii = increment_adjacents((x, y), new_octopii)

    for x, y in flashed:
        new_octopii[y][x] = 0

    return new_flashes, new_octopii, len(flashed)

def part1():
    octopii = read_input()
    # print("Octopii:", octopii)

    flashes = 0

    for step in range(100):
        octopii = inject_energy(octopii)
        flashes, octopii, _ = flash(flashes, octopii)

    # print("Octopii:", octopii)

    return flashes

def part2():
    octopii = read_input()
    # print("Octopii:", octopii)

    flashes = 0
    flashed_this_step = 0
    step = 0

    while flashed_this_step < 100:
        step += 1
        octopii = inject_energy(octopii)
        flashes, octopii, flashed_this_step = flash(flashes, octopii)

    # print("Octopii:", octopii)

    print(f"{flashed_this_step} octopuses flashed on step {step}")
    return step


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
