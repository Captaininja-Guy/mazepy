from ..grids.grid import Grid
from ..grids.colored_grid import ColoredGrid
import random as rand
from itertools import product
from ..grid_not_supported_exception import GridNotSupportedException

def FractalTessalation(grid: Grid|None = None, times: int = 4, base: tuple[int]|str|None = None, end: tuple[int]|str|None = None) -> ColoredGrid|None:
    '''
    Performs fractal tesselation on an existing Grid or generates a Grid

    Parameters:
        grid (optional Grid)
        times (optional int) = 4, how many iterations to perform
        base (optional tuple[int]|str) PIL/pillow valid color for return grid
        end (optional tuple[int]|str) PIL/pillow valid color for return grid

    Returns:
        ColoredGrid
    
    Errors:
        GridNotSupportedException if grid is not rectangular
    '''
    if grid is None:
        grid = Grid(1, 1)
    elif hasattr(grid, 'base'):
        base = grid.base
        end = grid.end
    
    if grid.type_of_grid != 'regular':
        raise GridNotSupportedException('Non-rectangular grids not compatible with Fractal Tessalation')

    for i in range(times):
        if base is not None and i == times - 1:
            grid_new = ColoredGrid(grid.rows*2, grid.columns*2, base=base, end=end)
        else:
            grid_new = Grid(grid.rows*2, grid.columns*2)
        for cell in grid.each_cell():
            new_row, new_column = cell.row+grid.rows, cell.column+grid.columns
            for row, col in product((cell.row, new_row), (cell.column, new_column)):
                links = cell.links()
                cell2 = grid_new[row, col]
                if cell.north in links:
                    cell2.link(cell2.north)
                if cell.east in links:
                    cell2.link(cell2.east)
                if cell.south in links:
                    cell2.link(cell2.south)
                if cell.west in links:
                    cell2.link(cell2.west)
        
        exc_path = rand.randrange(2)
        if exc_path == 0:
            num1, num2, num3 = rand.randrange(grid.columns), rand.randrange(grid.columns), rand.randrange(grid.rows)
            cell1 = grid_new[grid.rows, num1]
            cell2 = grid_new[grid.rows, grid.columns+num2]
            cell3 = grid_new[grid.rows*rand.randrange(2) + num3, grid.columns]

            cell1.link(cell1.north)
            cell2.link(cell2.north)
            cell3.link(cell3.west)
        else:
            num1, num2, num3 = rand.randrange(grid.columns), rand.randrange(grid.rows), rand.randrange(grid.rows)
            cell1 = grid_new[grid.rows, num1 + grid.columns*rand.randrange(2)]
            cell2 = grid_new[num2, grid.columns]
            cell3 = grid_new[grid.rows + num3, grid.columns]

            cell1.link(cell1.north)
            cell2.link(cell2.west)
            cell3.link(cell3.west)
        
        grid = grid_new
    
    return grid_new
        
