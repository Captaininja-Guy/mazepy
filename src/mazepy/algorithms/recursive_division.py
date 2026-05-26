from ..grids.grid import Grid
from ..grid_not_supported_exception import GridNotSupportedException
import random as rand

def RecursiveDivision(grid: Grid, room_hight: int = 0, room_width: int = 0, p: float = 1) -> None:
    '''
    Performs the Recursive Division algorithm on a given Grid in place
    Only rectangular, cylindrical, toroidal, and paper Mobius grids can be used

    Parameters:
        grid (Grid)
        room_height (optional int) = 0, increases p if height of room is less than this
        room_width (optional int) = 0, increases p if width of room is less than this
        p (optional) float = 1, probability to keep subdividing, lower is large 'dungeonesqe' rooms are wanted
    
    Returns:
        None, the grid is modified in place

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.RecursiveDivision(grid)
        grid.show()
    '''
    
    if grid.type_of_grid not in ('regular', 'cylinder', 'toroidal', 'paper mobius'):
        raise GridNotSupportedException('Recursive Division only works on non-masked rectangular/cylindrical/toroidal/mobius 2d Grids')
    grid.clear()

    __divide(0, 0, grid.rows, grid.columns, grid, room_hight, room_width, p)

def __divide(row, column, height, width, grid, room_height, room_width, p):
    if height <= 1 or width <= 1:
        return
    
    if height < room_height or width < room_width:
        rand_num = rand.random()
        if height < room_height:
            ratio = height / room_height
            rand_num *= ratio
        if width < room_width:
            ratio = width / room_width
            rand_num *= ratio
        if rand_num < p:
            return


    if height > width or height == width and rand.randrange(2) == 0:
        __divide_horizontally(row, column, height, width, grid, room_height, room_width, p)
    else:
        __divide_vertically(row, column, height, width, grid, room_height, room_width, p)

def __divide_horizontally(row, column, height, width, grid, room_height, room_width, p):
    divide_south_of = rand.randrange(height-1)
    passage_at = rand.randrange(width)

    for x in range(width):
        if x == passage_at: continue

        cell = grid[row+divide_south_of, column+x]
        cell.unlink(cell.south)

    __divide(row, column, divide_south_of+1, width, grid, room_height, room_width, p)
    __divide(row+divide_south_of+1, column, height-(divide_south_of+1), width, grid, room_height, room_width, p)

def __divide_vertically(row, column, height, width, grid, room_height, room_width, p):
    divide_east_of = rand.randrange(width-1)
    passage_at = rand.randrange(height)

    for y in range(height):
        if y == passage_at: continue

        cell = grid[row+y, column+divide_east_of]
        cell.unlink(cell.east)
    
    __divide(row, column, height, divide_east_of+1, grid, room_height, room_width, p)
    __divide(row, column+divide_east_of+1, height, width-(divide_east_of+1), grid, room_height, room_width, p)