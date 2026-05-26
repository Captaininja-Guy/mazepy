import random as rand
from ..grids.grid import Grid
from ..grid_not_supported_exception import GridNotSupportedException
import warnings



def BinaryTree(grid: Grid) -> None:
    '''
    Performs Binary Tree algorithm on a given Grid in place
    Most non-triangle Grids can be used with satisfactory results

    Parameters:
        grid (Grid)

    Returns:
        None the grid is modified in place

    Warnings:
        RuntimeWarning Binary tree cannot produce weaving on weaved grids
    
    Errors:
        Throws GridNotSupportedException when given a TriangleGrid

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.BinaryTree(grid)
        grid.show()
    '''

    if grid.type_of_grid == 'triangle':
        raise GridNotSupportedException('TriangleGrid not compatible with Binary Tree')
    if grid.type_of_grid == 'weave': # Warning for Weaved Grids as weaving will not occur
        warnings.warn('Binary Tree will NOT produce weaved grid')

    _hex, polar, three_d = grid.type_of_grid == 'hex', grid.type_of_grid == 'polar', grid.type_of_grid == '3d'
    
    for cell in grid.each_cell():
        neighbors = []
        if cell.north:
            neighbors.append(cell.north)
        if cell.east:
            neighbors.append(cell.east)
        if _hex: # HexGrid support
            if cell.northeast:
                neighbors.append(cell.northeast)
            elif cell.southeast:
                neighbors.append(cell.southeast)
        elif polar: # Polar support
            if cell is grid[0,0]:
                neighbors = cell.outward[0:2]
            else:
                if cell.column != 0:
                    neighbors.append(cell.ccw)
                if cell.outward:
                    neighbors.append(cell.outward[0])
                    
        if three_d and cell.up:
            neighbors.append(cell.up)

        if len(neighbors) > 0:
            neighbor = rand.choice(neighbors)
            cell.link(neighbor)
