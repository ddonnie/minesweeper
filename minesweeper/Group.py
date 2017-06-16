class Group:
    def __init__(self):
        self.cells = set()
        self.weight = 0

    def addCell(self,cell):
        self.cells.append(cell)

    def __repr__(self):
        return str(self.cells) + " " + str(self.weight)

