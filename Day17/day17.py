from re import findall
from math import sqrt

TESTING = False

MIN = 0
MAX = 1

def read_input():
    file.seek(0)
    x_min, x_max, y_min, y_max = findall("-?\d+", file.readline())
    return (int(x_min), int(x_max)), (int(y_min), int(y_max))


def in_target_area(current_x, current_y, target_x, target_y):
    if (target_x[MIN] <= current_x <= target_x[MAX]) and \
            (target_y[MIN] <= current_y <= target_y[MAX]):
        return True

    return False


def simulate_trajectory(speed_x, speed_y, target_x, target_y):
    current_x = 0
    current_y = 0
    max_height = 0

    while current_x <= target_x[MAX] and current_y >= target_y[MIN]:
        if in_target_area(current_x, current_y, target_x, target_y):
            return max_height

        current_x += speed_x
        current_y += speed_y
        max_height += max(0, speed_y)
        speed_x = max(0, speed_x - 1)
        speed_y -= 1

    return float('-inf')


def analyse_trajectory_options():
    # Lowest X speed is square root of double the lowest target x coord
    # (otherwise it does not make it to the target area)
    # (v^2 = u^2 + 2as   -->   0 = u^2 - 2s   -->   u = root(2s))
    #
    # Fastest X speed equals the largest target x coord (i.e: reaches far edge of target
    # area in one step)

    # When aiming for max height, on the way back down, there will always be a step
    # where the y coord is zero
    # At this time, the downward speed will be equal to the initial upward speed
    # On the following step (the first step below the start point), the downward distance
    # travelled will be equal to the initial y speed + 1.  If this takes the probe beyond
    # the lowest point in the target area, it is too fast.
    # Thus, the fastest upward y speed equals -(lowest target y coord + 1) [e.g: -10  --> 9]

    # It is also possible to shoot downwards and hit the target area, so the fastest downward
    # y speed equals the lowest target y coord (hit the target area in one step)

    target_x, target_y = read_input()

    possible_trajectories = []
    best_height = float('-inf')

    min_x_speed = int(sqrt(target_x[MIN] * 2))

    for speed_x in range(min_x_speed, target_x[MAX] + 1):
        for speed_y in range(target_y[MIN], -(target_y[MIN])):
            trajectory_max_height = simulate_trajectory(speed_x, speed_y, target_x, target_y)

            if trajectory_max_height > float('-inf'):
                possible_trajectories.append((speed_x, speed_y))

            if trajectory_max_height > best_height:
                best_trajectory = (speed_x, speed_y)
                best_height = trajectory_max_height

    return best_height, best_trajectory, len(possible_trajectories)

if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")


best_height, best_trajectory, num_possible_trajectories = analyse_trajectory_options()

print(f"Part 1: {best_height = }, {best_trajectory = }")
print(f"Part 2: {num_possible_trajectories = }")
