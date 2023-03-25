from utils import log

class Dirac:
    def __init__(self, die, player1, player2, squares=10):
        self.squares = squares
        self.die = die
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def loser(self):
        return self.player1 if self.player1.get_score() < self.player2.get_score() else self.player2

    def get_result(self):
        return self.loser().get_score() * self.die.get_rolls()

    def calc_new_pos(self, current_pos, dice_total):
        return ((current_pos + dice_total - 1) % self.squares) + 1

    def winner(self):
        if self.player1.get_score() >= 1000:
            return self.player1
        elif self.player2.get_score() >= 1000:
            return self.player2
        else:
            return False

    def roll_dice(self):
        total = 0

        for roll_num in range(3):
            self.die.roll()
            total += self.die.get_value()

        return total

    def play_turn(self):
        dice_total = self.roll_dice()
        new_pos = self.calc_new_pos(self.current_player.get_position(), dice_total)
        self.current_player.move_to(new_pos)
        log(f"{self.current_player.get_name()} rolls {dice_total} and moves to space {new_pos} for a total score of {self.current_player.get_score()}")

    def next_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def play_game(self):
        while not self.winner():
            self.play_turn()
            self.next_player()

        return
