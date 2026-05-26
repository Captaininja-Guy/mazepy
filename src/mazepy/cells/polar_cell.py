from ..cells.cell import Cell

class PolarCell(Cell):
    def __init__(self, row: int, column: int):
        super().__init__(row, column)

        self.cw = None
        self.ccw = None
        self.inward = None
        self.outward = []
        

    def neighbors(self):
        neighbors = []
        if self.cw:
            neighbors.append(self.cw)
        if self.ccw:
            neighbors.append(self.ccw)
        if self.inward:
            neighbors.append(self.inward)
        if self.outward:
            neighbors += self.outward
        
        return neighbors
    
    def __str__(self):
        return f'PolarCell: ({self.row},{self.column}), Links: {self.links()}'