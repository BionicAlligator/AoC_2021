import re
from utils import log
from dirac import Dirac
from die import Die
from player import Player

TESTING = False

def read_input(filename):
    starting_positions = {}

    file = open(filename, "r")

    for line in file:
        starting_position_mapping = re.findall(r'\d+', line)
        starting_positions[int(starting_position_mapping[0])] = int(starting_position_mapping[1])

    return starting_positions


def part1(filename):
    starting_positions = read_input(filename)
    deterministic_die = Die()
    player1 = Player("Player 1", starting_positions[1])
    player2 = Player("Player 2", starting_positions[2])
    game = Dirac(deterministic_die, player1, player2)

    game.play_game()

    return game.get_result()


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

print("Part 1: ", part1(filename))
