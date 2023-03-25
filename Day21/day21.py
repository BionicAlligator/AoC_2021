import re
from collections import defaultdict

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
    WINNING_SCORE = 1000

    starting_positions = read_input(filename)
    deterministic_die = Die()
    player1 = Player("Player 1", starting_positions[1])
    player2 = Player("Player 2", starting_positions[2])
    game = Dirac(WINNING_SCORE, deterministic_die, player1, player2)

    game.play_game()

    return game.get_result()


def next_player(current_player):
    return (current_player + 1) % 2


def calc_new_positions(positions, dice_total, current_player):
    new_positions = list(positions)
    new_positions[current_player] = ((new_positions[current_player] - 1 + dice_total) % 10) + 1
    return tuple(new_positions)


def calc_new_scores(scores, new_positions, current_player):
    new_scores = list(scores)
    new_scores[current_player] += new_positions[current_player]
    return tuple(new_scores)


# --- PART 2 ---
# Given that we roll three times, the possible outcomes are:
#   3, 4, 5, 6, 7, 8, 9
# There are several ways to achieve some of these:
# 3 = 1,1,1 [1 universe]
# 4 = 1,1,2 / 1,2,1 / 2,1,1 [3 universes]
# 5 = 1,2,2 / 2,1,2 / 2,2,1 / 1,1,3 / 1,3,1 / 3,1,1 [6 universes]
# 6 = 2,2,2 / 1,2,3 / 1,3,2 / 2,1,3 / 2,3,1 / 3,1,2 / 3,2,1 [7 universes]
# 7 = 2,2,3 / 2,3,2 / 3,2,2 / 1,3,3 / 3,1,3 / 3,3,1 [6 universes]
# 8 = 2,3,3 / 3,2,3 / 3,3,2 [3 universes]
# 9 = 3,3,3 [1 universe]
# So instead of 27 'universes' needing to be tracked, we can track the number of universes
# covered by each of these scores
#
# We start with a single universe defined by its state:
#  {positions = (P1start, P2start), scores = (0, 0), current_player = P1}
# i.e: universes = {((P1start, P2start), (0, 0), P1) : 1}
#
# We then loop through all universes and generate the new universes that could result
# from each of the 7 possible dice combinations on the next player's turn:
#  new_universes = {((P1start+3, P2start), (P1start+3, 0), P2) : 1, ((P1start+4, P2start), (P1start+4, 0), P2): 3, etc}
#
# We check this list of new universes for any where a score >= 21.  Those universe totals are added to the
# total number of universes that result in a win for the player that has reached or exceeded 21 points and
# those universes are removed from the list of universes requiring further turns to be played.
#
# Continue until there are no universes left in the list.
def part2(filename):
    WINNING_SCORE = 21
    dice_combos = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    starting_positions = read_input(filename)

    universes = {((starting_positions[1], starting_positions[2]), (0, 0), 0): 1}
    winning_universes = [0, 0]

    while universes:
        new_universes = defaultdict(int)

        for (positions, scores, current_player), num_universes in universes.items():
            for dice_total, occurrences in dice_combos.items():
                new_positions = calc_new_positions(positions, dice_total, current_player)
                new_scores = calc_new_scores(scores, new_positions, current_player)

                if (new_scores[current_player] >= WINNING_SCORE):
                    winning_universes[current_player] += occurrences * num_universes
                else:
                    new_universes[(new_positions, new_scores, next_player(current_player))] += occurrences * num_universes

        universes = new_universes.copy()

    return max(winning_universes)


if TESTING:
    filename = "sampleInput.txt"
else:
    filename = "input.txt"

print("Part 1: ", part1(filename))
print("Part 2: ", part2(filename))
