from copy import deepcopy

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
    # print("Routes:", routes)

    for cave1, cave2 in routes:
        add_cave_info(caves, cave1, cave2)
        add_cave_info(caves, cave2, cave1)

    # print("Caves:", caves)
    return caves

def df_search(caves, current, target, path_so_far, successful_paths):
    current_path = path_so_far + "->"
    current_path += current[:-5] if "_copy" in current else current

    if current == target:
        successful_paths.add(current_path)
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

    paths = set()

    df_search(caves, "start", "end", "", paths)

    print(f"Successful paths: {paths}")
    return len(paths)

def part2():
    caves = read_input()

    paths = set()

    for cave_name, cave in caves.items():
        # if the cave is small and is not 'start' or 'end',
        # copy it, give it a different name (cave + "_copy") and
        # then go through each cave to check for routes to it and duplicate those routes
        # to point to the new duplicate cave
        if not cave["is_large"] and cave_name not in ["start", "end"]:
            cave_copy = deepcopy(cave)
            cave_copy_name = cave_name + "_copy"

            new_caves = deepcopy(caves)
            new_caves.update({cave_copy_name: cave_copy})

            for other_cave_name, other_cave in new_caves.items():
                other_cave_routes = other_cave["routes"]

                if cave_name in other_cave_routes:
                    other_cave_routes.append(cave_copy_name)

            df_search(new_caves, "start", "end", "", paths)

    print(f"Successful paths: {paths}")
    return len(paths)


if TESTING:
    file = open("sampleInput.txt", "r")  # 10 paths / 36 paths
    # file = open("sampleInput2.txt", "r")  # 19 paths / 103 paths
    # file = open("sampleInput3.txt", "r")  # 226 paths / 3509 paths
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
