from ..distances import Distances


class Cell:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self._links = {}
        # self.contents_of = '  ' # For debugging

    # Linkes cell with target, bidi -> bidirectional
    def link(self, cell, bidi: bool = True) -> None:
        self._links[cell] = True
        if bidi:
            cell.link(self, False)
        return self

    def unlink(self, cell, bidi: bool =True) -> None:
        self._links.pop(cell, None)
        if bidi:
            cell.unlink(self, False)
        return self

    # Returns all cells linked with inputed cell
    def links(self):
        return list(self._links)

    # Returned weather inputed cell is linked with target
    def linkedq(self, cell) -> bool:
        return cell in self._links

    # Returns all neighbors of inputed cell, with no regard to links
    def neighbors(self):
        neighbors = []
        if self.north:
            neighbors.append(self.north)
        if self.south:
            neighbors.append(self.south)
        if self.east:
            neighbors.append(self.east)
        if self.west:
            neighbors.append(self.west)
        return neighbors
    
    # Returns a Distances object which links each cell with a distance from the inputed cell
    def distances(self) -> Distances:
        distances = Distances(self)
        frontier = [self]

        while frontier:
            new_frontier = []

            for cell in frontier:
                for linked in cell._links:
                    if linked in distances:
                        continue

                    distances[linked] = distances[cell] + 1
                    new_frontier.append(linked)
            
            frontier = new_frontier
       
        return distances
    
    def __str__(self):
        return f'Cell: ({self.row},{self.column})'#, Links: {self.links()}, Neighbors: {self.neighbors()}'
