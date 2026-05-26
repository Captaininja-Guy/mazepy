import random as rand
from ..grids.grid import Grid
from ..cells.cell import Cell
from ..grid_not_supported_exception import GridNotSupportedException
import warnings



def OriginShift(grid: Grid, *, times: int|None = None, percentage: float = 1, setup: bool = True, 
                root: Cell|None = None, make_bidi: bool = True, return_root: bool = False) -> Cell|None:
    
    '''
    Performs the Origin Shift algorithm on a given Grid in place
    https://www.youtube.com/watch?v=zbXKcDVV4G0
    Any non masked grid can be used

    Parameters:
        grid (Grid)

        times (optional int) = the amount of origin shift to perform, this overrides percentage
        percentage (optional float) = 1, origin shifting stops when this percentage of the grid is visited
        setup (optional bool) = True, whether to perform initial setup of the grid, use for any blank grid
        root (optional Cell) = if given an already setup grid, a root must be defined
        make_bidi (optional bool) = True, whether to make all links bidirectional at the end of the algorithm
        return_root (optional bool) = False, whether to return the root cell
        
    Returns:
        Cell or None

    Errors:
        Throws GridNotSupportedException when given a masked grid

    Warnings:
        RuntimeWarning Origin Shift cannot produce weaving on weaved grids

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(10,10)
        mp.algorithms.OriginShift(grid)
        grid.show()
    '''
    # Defines the stopping condition, set itterations or grid visited precentage
    times_flag = times is not None
    
    if grid.type_of_grid == 'mask' and setup:
        raise GridNotSupportedException('MaskedGrid not comptible with OriginShift, setup grid manually and run with setup=False')
    
    if grid.type_of_grid == 'weave': # Warning for Weaved Grids as weaving will not occur
        warnings.warn('OriginShift will NOT produce weaved grid')
    
    threed = grid.type_of_grid == '3d'
    cube = grid.type_of_grid == 'cube'

    root_flag = False
    if root is None:
        root_flag = True
        root = grid[0, 0] if not threed and not cube else grid[0, 0, 0]

    # Initial Linking
    if setup or not root_flag:
        if grid.type_of_grid == 'polar':
            for cell in grid.each_cell():
                if cell is root:
                    continue
                cell.link(cell.inward, bidi=False)
        elif grid.type_of_grid == 'hex':
            for cell in grid.each_cell():
                if cell is root:
                    continue
                if cell.column == 0:
                    cell.link(cell.north, bidi=False)
                elif cell.row == 0:
                    cell.link(cell.southwest, bidi=False)
                else:
                    cell.link(cell.northwest, bidi=False)
        elif grid.type_of_grid == 'triangle':
            for cell in grid.each_cell():
                if cell is root:
                    continue
                if cell.column > 1 or (cell.uprightq() and cell.column == 1) or cell is grid[0,1]:
                    cell.link(cell.west, bidi=False)
                elif not cell.uprightq():
                    cell.link(cell.north, bidi=False)
                elif cell.column == 0:
                    cell.link(cell.east, bidi=False)
        elif cube:
            for cell in grid.each_cell():
                if cell.face == 1:
                    if cell.west.face != 1:
                        cell.link(cell.north, bidi=False)
                    else:
                        cell.link(cell.west, bidi=False)
                elif cell.face == 4:
                    cell.link(cell.south, bidi=False)
                elif cell.face in (2,3):
                    cell.link(cell.west, bidi=False)
                elif cell.face == 0:
                    cell.link(cell.east, bidi=False)
                else:
                    cell.link(cell.north, bidi=False)
        else:
            for cell in grid.each_cell():
                if not threed or cell.level == 0:
                    if cell.row == 0:
                        if cell.west:
                            cell.link(cell.west, bidi=False)
                    else:
                        cell.link(cell.north, bidi=False)
                else:
                    cell.link(cell.down, bidi=False)
    
    if times_flag:
        i = 0
    else:
        num_been_root = 1
        if threed:
            visited = {(level, row, col): False for row in range(grid.rows) for col in range(grid.columns) for level in range(grid.levels)}
            visited[root.level, root.row, root.column] = True
            number_of_cells = grid.size
        elif cube:
            visited = {(face, row, col): False for row in range(grid.rows) for col in range(grid.columns) for face in range(6)}
            visited[root.face, root.row, root.column] = True
            number_of_cells = grid.size
        else:
            visited = {(row, col): False for row in range(grid.rows) for col in range(grid.columns)}
            visited[root.row, root.col] = True
            number_of_cells = sum(len(row) for row in grid.grid)

        if percentage > 1:
            percentage /= 100

    # Origin Shifting
    # Until percentage of the grid has been visited by the root or the set itterations has been reached
    while (not times_flag and num_been_root < percentage * number_of_cells) or (times_flag and i < times):
        _next = rand.choice(root.neighbors())
        if _next.linkedq(root):
            _next.unlink(root, bidi=False)
            root.link(_next, bidi=False)
        else:
            _next._links.clear()
            root.link(_next, bidi=False)
        
        root = _next
        if times_flag:
            i += 1
        else:
            if threed:
                visited[(root.level, root.row, root.column)] = True
            elif cube:
                visited[(root.face, root.row, root.column)] = True
            else:
                visited[(root.row, root.column)] = True
            num_been_root = sum(1 for v in visited.values() if v)
        


    # Making links bidirectional
    if make_bidi:
        grid.make_bidi()
    
    if return_root:
        return root