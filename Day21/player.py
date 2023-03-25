class Player:
    def __init__(self, name, starting_position=1):
        self.score = 0
        self.name = name
        self.position = starting_position

    def move_to(self, new_pos):
        self.position = new_pos
        self.score += new_pos

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def get_position(self):
        return self.position
