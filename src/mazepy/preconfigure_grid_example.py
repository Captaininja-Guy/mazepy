from mazepy.grids.weave_grid import PreconfiguredWeaveGrid
from mazepy.algorithms.kruskals import Kruskals, State
import random as rand

def precon_grid_ex():
    '''
    Example showing functionality of PreconfiguredWeaveGrid
    '''
    grid = PreconfiguredWeaveGrid(20,20)
    state = State(grid)

    for _ in range(grid.size):
        row = rand.randint(1,grid.rows-2)
        column = rand.randint(1,grid.columns-2)
        state.add_crossing(grid[row, column])

    Kruskals(grid, state)
    grid.distances = grid[0,0].distances()
    grid.show()