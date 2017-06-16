class Cell:
    def __init__(self, weight, pos):
        self.weight = weight
        self.is_mine = False
        self.is_open = False
        self.pos = pos

    def __repr__(self):
        return str(self.weight)