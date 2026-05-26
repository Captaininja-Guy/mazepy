import random as rand
from ..grids.grid import Grid
from ..cells.cell import Cell

def HuntandKill(grid: Grid, start: Cell | None = None) -> None:
    '''
    Performs the Hunt and Kill algorithm on a given Grid in place
    Any type of grid can be used

    Parameters:
        grid (Grid)
        start (optional Cell) starting cell of of first path
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.HuntandKill(grid)
        grid.show()
    '''
    if start is None:
        start = grid.random_cell()
    current = start

    while current:
        unvisited_neighbors = [cell for cell in current.neighbors() if not cell.links()]

        if unvisited_neighbors:
            neighbor = rand.choice(unvisited_neighbors)
            current.link(neighbor)
            current = neighbor
        else:
            current = None

            for cell in grid.each_cell():
                visited_neighbors = [cell for cell in cell.neighbors() if cell.links()]
                if not cell.links() and visited_neighbors:
                    current = cell

                    neighbor = rand.choice(visited_neighbors)
                    current.link(neighbor)
                    break