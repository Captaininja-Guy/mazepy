import random as rand
from ..grids.grid import Grid
from ..grid_not_supported_exception import GridNotSupportedException

def Wilsons(grid: Grid) -> None:
    '''
    Performs the Sidewinder algorithm on a given Grid in place
    Any non weaved grid can be used

    Parameters:
        grid (Grid)

    Returns:
        None the grid is modified in place

    Errors:
        Throws GridNotSupportedException when given a WeaveGrid

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.Wilsons(grid)
        grid.show()
    '''
    if grid.type_of_grid == 'weave':
        raise GridNotSupportedException('Weave Grids are not compatible with Wilsons due to impossible grids being formed')
    unvisited = [cell for cell in grid.each_cell()]
    
    first = rand.choice(unvisited)
    unvisited.remove(first)

    while unvisited:
        cell = rand.choice(unvisited)
        path = [cell]

        while cell in unvisited:
            cell = rand.choice(cell.neighbors())
            try: 
                position = path.index(cell)
            except ValueError:
                position = None

            if position is not None:
                path = path[0:position + 1]
            else:
                path.append(cell)

        for index in range(len(path) - 1):
            path[index].link(path[index + 1])
            unvisited.remove(path[index])