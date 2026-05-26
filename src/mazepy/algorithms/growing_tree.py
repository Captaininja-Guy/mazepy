from ..grids.grid import Grid
from ..cells.cell import Cell
import random as rand
from typing import Callable

def GrowingTree(grid: Grid, func: Callable = lambda x: rand.choice(x), start_at: Cell|None = None) -> None:
    '''
    Performs the GrowingTree algorithm on a given Grid in place.
    Any type of grid can be used

    Parameters:
        grid (Grid)
        func (optional Callable) = lambda x: rand.choice(x), function to select next cell from visited list (list -> element from it)
        start_at (optional Cell) = grid.random_cell(), which cell to start algorithm at
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.GrowingGree(grid)
        grid.show()
    '''
    if start_at is None:
        start_at = grid.random_cell()

    active = [start_at]

    while active:
        cell = func(active) # func takes a list and returns an element of it
        availible_neighbors = [c for c in cell.neighbors() if not c.links()]

        if availible_neighbors:
            neighbor = rand.choice(availible_neighbors)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)