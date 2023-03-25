from utils import log


class Die:
    def __init__(self, sides=100, deterministic=True):
        self.sides = sides
        self.deterministic = deterministic
        self.face = 0
        self.rolls = 0

    def roll(self):
        self.rolls += 1

        if self.deterministic:
            self.face = (self.face + 1) % self.sides

    def get_value(self):
        # Face is zero-indexed but the die itself returns 1-indexed values
        value = self.face if self.face != 0 else self.sides
        log(f"Die shows {value}")
        return value

    def get_rolls(self):
        log(f"Die has been rolled {self.rolls} times")
        return self.rolls
