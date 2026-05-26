from ..cells.cell import Cell

class TriangleCell(Cell):
    
    def uprightq(self) -> bool:
        return (self.row+self.column)%2 == 0
    
    def neighbors(self):
        neighbors = []
        if self.west:
            neighbors.append(self.west)
        if self.east:
            neighbors.append(self.east)
        if not self.uprightq() and self.north:
            neighbors.append(self.north)
        if self.uprightq() and self.south:
            neighbors.append(self.south)
        return neighbors
    
    def __str__(self):
        return f'TriangleCell: ({self.row},{self.column}), Links: {self.links()}, Neighbors: {self.neighbors()}'