import random as rand
from ..grid_not_supported_exception import GridNotSupportedException
from ..grids.grid import Grid
import warnings

class State:
    def __init__(self, grid):
        self.grid = grid
        self.neighbors = []
        self.set_for_cell = {}
        self.cells_in_set = {}
        threed = grid.type_of_grid == '3d'

        for cell in grid.each_cell():
            set = len(self.set_for_cell)
            self.set_for_cell[cell] = set
            self.cells_in_set[set] = [cell]

            if cell.south:
                self.neighbors.append((cell, cell.south))
            if cell.east:
                self.neighbors.append((cell, cell.east))
            if threed and cell.up:
                self.neighbors.append((cell, cell.up))

    def can_merge(self, left, right):
        return self.set_for_cell[left] != self.set_for_cell[right]
    
    def merge(self, left, right):
        left.link(right)

        winner = self.set_for_cell[left]
        loser = self.set_for_cell.get(right, None)
        if loser is not None:
            losers = self.cells_in_set[loser]
        else:
            losers = [right]

        for cell in losers:
            self.cells_in_set[winner].append(cell)
            self.set_for_cell[cell] = winner
        
        self.cells_in_set.pop(loser, None)
    
    def add_crossing(self, cell):
        if cell.links() or not self.can_merge(cell.east, cell.west) or not self.can_merge(cell.north, cell.south):
            return False
        
        self.neighbors = [lr for lr in self.neighbors if not cell in lr]

        if rand.randrange(2) == 0:
            self.merge(cell.west, cell)
            self.merge(cell, cell.east)

            self.grid.tunnel_under(cell)
            self.merge(cell.north, cell.north.south)
            self.merge(cell.south, cell.south.north)
        else:
            self.merge(cell.north, cell)
            self.merge(cell, cell.south)

            self.grid.tunnel_under(cell)
            self.merge(cell.west, cell.west.east)
            self.merge(cell.east, cell.east.west)
            
        return True


def Kruskals(grid: Grid, state=None) -> None:
    '''
    Performs Kruskals algorithm on a given Grid in place
    Only rectangular grids can be used

    Parameters:
        grid (Grid)
        state (optional State) starting state, used for Preconfigured Weave Grids
        
    Returns:
        None, the grid is modified in place

    Errors:
        Throws GridNotSupportedException when given a non rectangular grid

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.Kruskals(grid)
        grid.show()
    '''
    if grid.type_of_grid == 'polar':
        raise GridNotSupportedException('Polar Grid not compatible with Kruskals, it will show blank Grid')
    if grid.type_of_grid == 'hex':
        raise GridNotSupportedException('Hex Grid not compatible with Kruskals, it will show blank Grid')
    if grid.type_of_grid == 'sphere':
        raise GridNotSupportedException('Sphere Grid not compatible with Kruskals, it will show most grid lines only')
    if grid.type_of_grid == 'weave': # Warning for Weaved Grids as weaving will not occur
        warnings.warn('Sidewinder will NOT produce weaved grid', RuntimeWarning)
    if state is None:
        state = State(grid)

    neighbors = state.neighbors
    rand.shuffle(neighbors)

    while neighbors:
        left, right = neighbors.pop()
        if state.can_merge(left, right):
            state.merge(left, right)