from ..grids.grid import Grid
from ..cells.cell import Cell
import random as rand

def SimplifiedPrims(grid: Grid, start_at: Cell|None = None) -> None:
    '''
    Performs the Simplified Prims algorithm on a given Grid in place
    Any type of grid can be used

    Parameters:
        grid (Grid)
        start_at (optional Cell) = grid.random_cell(), starting cell
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.SimplifiedPrims(grid)
        grid.show()
    '''
    if start_at is None:
        start_at = grid.random_cell()
    
    active = [start_at]

    while active:
        cell = rand.choice(active)
        availible_neighbors = [c for c in cell.neighbors() if not c.links()]

        if availible_neighbors:
            neighbor = rand.choice(availible_neighbors)
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)

def TruePrims(grid: Grid, start_at: Cell|None = None) -> None:
    '''
    Performs the True Prims algorithm on a given Grid in place
    Any type of grid can be used

    Parameters:
        grid (Grid)
        start_at (optional Cell) = grid.random_cell(), starting cell
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.TruePrims(grid)
        grid.show()
    '''
    if start_at is None:
        start_at = grid.random_cell()
    
    active = [start_at]
    costs = {}
    for cell in grid.each_cell(): costs[cell] = rand.randint(1,100)

    while active:
        cell = min(active, key=lambda x: costs[x])
        availible_neighbors = [c for c in cell.neighbors() if not c.links()]

        if availible_neighbors:
            neighbor = min(availible_neighbors, key=lambda x: costs[x])
            cell.link(neighbor)
            active.append(neighbor)
        else:
            active.remove(cell)

def ModifiedPrims(grid: Grid, start_at: Cell|None = None) -> None:
    '''
    Performs the Modified Prims algorithm on a given Grid in place
    Any type of grid can be used

    Parameters:
        grid (Grid)
        start_at (optional Cell) = grid.random_cell(), starting cell
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.ModifiedPrims(grid)
        grid.show()
    '''
    if start_at is None:
        start_at = grid.random_cell()
    
    _in = [start_at]
    frontier = start_at.neighbors()
    out = []
    for cell in grid.each_cell():
        if cell not in _in and cell not in frontier:
            out.append(cell)
    
    while frontier:
        cell = rand.choice(frontier)
        _in.append(cell)
        frontier.remove(cell)
        linked_flag = False
        neighbors = cell.neighbors()
        rand.shuffle(neighbors)
        
        for neighbor_cell in neighbors:
            if neighbor_cell in _in and not linked_flag:
                cell.link(neighbor_cell)
                linked_flag = True
            if neighbor_cell in out:
                out.remove(neighbor_cell)
                frontier.append(neighbor_cell)

def Prims(grid: Grid, start_at: Cell|None = None) -> None:
    '''
    Wrapper for the Simplified Prims algorithm, see SimplifiedPrims for more info
    '''
    SimplifiedPrims(grid, start_at)