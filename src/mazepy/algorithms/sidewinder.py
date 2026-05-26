import random as rand
from ..grids.grid import Grid
import warnings

def Sidewinder(grid: Grid) -> None:
    '''
    Performs the Sidewinder algorithm on a given Grid in place
    Any grid can be used

    Parameters:
        grid (Grid)

    Returns:
        None the grid is modified in place

    Warnings:
        RuntimeWarning Sidewinder cannot produce weaving on weaved grids
    
    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.Sidewinder(grid)
        grid.show()
    '''
    _hex, polar, triangle, threed = (grid.type_of_grid == 'hex', grid.type_of_grid == 'polar', 
    grid.type_of_grid == 'triangle', grid.type_of_grid == '3d')

    if grid.type_of_grid == 'weave': # Warning for Weaved Grids as weaving will not occur
        warnings.warn('Sidewinder will NOT produce weaved grid', RuntimeWarning)

    for row in grid.each_row():
        run = []
        for cell in row:
            run.append(cell)

            at_eastern_boundry = cell.east is None
            at_northern_boundry = cell.north is None

            if triangle: # TriangleGrid support
                if cell.uprightq():
                    if cell.east is None:
                        at_northern_boundry = cell.west.north is None
                    else:
                        at_northern_boundry = cell.east.north is None

                    if at_eastern_boundry and len(run) == 1:
                        cell.link(cell.west)
                        continue

            if _hex: # HexGrid support
                at_eastern_boundry = cell.northeast is None and cell.southeast is None

            should_close_out = at_eastern_boundry or ((not at_northern_boundry) and rand.randint(0, 1) == 0)

            if triangle:
                run_length = len(run)
                if run_length == 1 and run[0].uprightq():
                    should_close_out = False

            if polar: # PolarGrid support
                should_close_out = cell.column == len(row)-1 or ((cell.outward) and rand.randint(0, 1) == 0)


            if should_close_out:
                member = rand.choice(run)

                if polar and member.outward:
                    member.link(rand.choice(member.outward))
                if triangle:
                    while member.uprightq():
                        run.remove(member)
                        member = rand.choice(run)
                if threed: # 3d actions
                    if (not member.up or rand.randint(0,1) == 0) and member.north:
                        member.link(member.north)
                    if not member.north and member.up:
                        member.link(member.up)
                    
                elif member.north:
                    member.link(member.north)
                    
                run = []
            else:
                if _hex: # Hex actions
                    if not at_northern_boundry:
                        cell.link(cell.northeast)
                    else:
                        cell.link(cell.southeast)
                elif polar:
                    cell.link(cell.cw)
                else:
                    cell.link(cell.east)
