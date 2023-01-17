TESTING = False

def add_cave_info(caves, cave1, cave2):
    if cave1 not in caves:
        cave_entry = {"routes": [cave2], "is_large": cave1.isupper(), "visited": False}
        caves.update({cave1: cave_entry})
    else:
        cave_routes = caves[cave1]["routes"]

        if cave2 not in cave_routes:
            cave_routes.append(cave2)

def read_input():
    file.seek(0)
    caves = {}
    routes = [tuple(line.rstrip().split('-')) for line in file]
    print("Routes:", routes)

    for cave1, cave2 in routes:
        add_cave_info(caves, cave1, cave2)
        add_cave_info(caves, cave2, cave1)

    print("Caves:", caves)
    return caves

def df_search(caves, current, target, path_so_far, successful_paths):
    current_path = path_so_far.copy()
    current_path.append(current)

    if current == target:
        successful_paths.append(current_path)
    else:
        new_caves = caves.copy()
        current_cave = new_caves[current].copy()

        if current_cave["is_large"] or not current_cave["visited"]:
            current_cave["visited"] = True
            new_caves.update({current: current_cave})

            for cave in current_cave["routes"]:
                df_search(new_caves, cave, target, current_path, successful_paths)

def part1():
    caves = read_input()

    paths = []

    df_search(caves, "start", "end", [], paths)

    print(f"Successful paths: {paths}")
    return len(paths)

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")  # 10 paths / 36 paths
    # file = open("sampleInput2.txt", "r")  # 19 paths / 103 paths
    # file = open("sampleInput3.txt", "r")  # 226 paths / 3509 paths
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
