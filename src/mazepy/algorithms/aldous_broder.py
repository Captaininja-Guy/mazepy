import random as rand
from ..grids.grid import Grid

def AldousBroder(grid: Grid) -> None:
    '''
    Performs the AldousBroder algorithm on a given Grid in place.
    Any type of grid can be used

    Parameters:
        grid (Grid)
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.AldousBroder(grid)
        grid.show()
    '''
    cell = grid.random_cell()
    unvisited = grid.size - 1

    while unvisited > 0:
        neighbor = rand.choice(cell.neighbors())

        if not neighbor.links():
            cell.link(neighbor)
            unvisited -= 1
        
        cell = neighbor
