import random as rand
from ..grids.grid import Grid
from ..cells.cell import Cell


def RecursiveBacktrack(grid: Grid, start: Cell | None = None) -> None:
    '''
    Performs the Recursive Backtrack (DFS) algorithm on a given Grid in place
    Any type of grid can be used

    Parameters:
        grid (Grid)
        start_at (optional Cell) = grid.random_cell(), starting cell
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.RecursiveBacktrack(grid)
        grid.show()
    '''
    if start is None:
        start = grid.random_cell()
    stack = [start]

    while stack:
        current = stack[-1]
        unvisited_neighbors = [cell for cell in current.neighbors() if not cell.links()]

        if not unvisited_neighbors:
            stack.pop()
        else:
            neighbor = rand.choice(unvisited_neighbors)
            current.link(neighbor)
            stack.append(neighbor)