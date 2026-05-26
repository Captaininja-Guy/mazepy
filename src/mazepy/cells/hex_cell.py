from ..cells.cell import Cell

class HexCell(Cell):
    def __init__(self, row, column):
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        super().__init__(row, column)

    def neighbors(self):
        neighbors = []
        if self.north:
            neighbors.append(self.north)
        if self.northeast:
            neighbors.append(self.northeast)
        if self.northwest:
            neighbors.append(self.northwest)
        if self.south:
            neighbors.append(self.south)
        if self.southeast:
            neighbors.append(self.southeast)
        if self.southwest:
            neighbors.append(self.southwest)
        return neighbors

    def __str__(self):
        return f'HexCell: ({self.row},{self.column}), Links: {self.links()}, Neighbors: {self.neighbors()}'