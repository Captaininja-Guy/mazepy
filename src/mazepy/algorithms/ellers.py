from ..grids.grid import Grid
from ..cells.cell import Cell
import random as rand
from ..grid_not_supported_exception import GridNotSupportedException
import warnings

class _RowState:
    def __init__(self, starting_set: int = 0):
        self.cells_in_set = {}
        self.set_for_cell = []
        self.next_set = starting_set

    def record(self, _set: int, cell: Cell) -> None:
        while cell.column >= len(self.set_for_cell):
            self.set_for_cell.append(None)

        self.set_for_cell[cell.column] = _set
        self.cells_in_set.setdefault(_set, [])
        self.cells_in_set[_set].append(cell)
    
    def set_for(self, cell: Cell) -> int:
        if cell.column >= len(self.set_for_cell) or self.set_for_cell[cell.column] is None:
            self.record(self.next_set, cell)
            self.next_set += 1
        
        return self.set_for_cell[cell.column]
    
    def merge(self, winner: int, loser: int) -> None:
        for cell in self.cells_in_set[loser]:
            self.set_for_cell[cell.column] = winner
            self.cells_in_set[winner].append(cell)
        
        del self.cells_in_set[loser]
    
    def _next(self):
        return _RowState(self.next_set)
    
    def each_set(self):
        for set_, cells in self.cells_in_set.items():
            yield set_, cells

def Ellers(grid: Grid) -> None:
    '''
    Performs Ellers algorithm on a given Grid in place.
    Triangle grids not supported 3d and cube Grids are not perfect

    Parameters:
        grid (Grid)
    
    Returns:
        None, the grid is modified in place

    Errors:
        GridNotSupportedException if Grid is triangular
    
    Warnings:
        RuntimeWarning Ellers produced non-perfect mazes on 3d and cube grids

    Example:
        import mazepy as mp

        grid = mp.grids.Grid(20,20)
        mp.algorithms.Ellers(grid)
        grid.show()
    '''

    if grid.type_of_grid == 'triangle':
        raise GridNotSupportedException('Triangle Grids not compatible with Ellers')
    _hex = grid.type_of_grid == 'hex'
    polar = grid.type_of_grid == 'polar'
    if threed := grid.type_of_grid == '3d':
        warnings.warn('Ellers on 3d grids produces seperate 2d grids with no up/down connections', RuntimeWarning)
    if grid.type_of_grid == 'cube':
        warnings.warn('Ellers on a cube grid may not produce a perfect maze', RuntimeWarning)
    if grid.type_of_grid == 'weave':
        warnings.warn('Sidewinder will NOT produce weaved grid', RuntimeWarning)

    if threed:
        each_level = grid.each_level()
    else:
        each_level = [grid]
    
    for level in each_level:
        row_state = _RowState()
        if threed:
            rows = level
        else:
            rows = level.each_row()

        for row in rows:
            for cell in row:
                if not _hex and not polar and not cell.west: continue
                elif _hex and cell.column%2 == 0 and not cell.northwest: continue
                elif polar and len(row) == 1: 
                    out_cell = rand.choice(cell.outward)
                    cell.link(out_cell)
                    continue


                _set = row_state.set_for(cell)
                if not _hex and not polar:
                    prior_set = row_state.set_for(cell.west)
                elif _hex:
                    prior_set = row_state.set_for(cell.southwest) if cell.column%2 == 1 else row_state.set_for(cell.northwest)
                elif polar:
                    prior_set = row_state.set_for(cell.ccw)


                if not polar and _set != prior_set and (cell.south is None or rand.randrange(2) == 0):
                    if not _hex and not polar:
                        cell.link(cell.west)
                    else:
                        if cell.column % 2 == 1:
                            cell.link(cell.southwest)
                        else:
                            cell.link(cell.northwest)
                    row_state.merge(prior_set, _set)

                elif polar and _set != prior_set and (not cell.outward or rand.randrange(2) == 0):
                    cell.link(cell.ccw)
                    row_state.merge(prior_set, _set)

            if row[0].south:
                next_row = row_state._next()

                for _, _list in row_state.each_set():
                    list2 = _list.copy()
                    rand.shuffle(list2)

                    for index, cell in enumerate(list2):
                        if index == 0 or rand.randrange(3) == 0:
                            cell.link(cell.south)
                            next_row.record(row_state.set_for(cell), cell.south)

            elif polar and row[0].outward:
                next_row = row_state._next()

                for _, _list in row_state.each_set():
                    list2 = _list.copy()
                    rand.shuffle(list2)
                    for index, cell in enumerate(list2):
                        if index == 0 or rand.randrange(3) == 0:
                            cell2 = cell.outward[rand.randrange(len(cell.outward))]
                            cell.link(cell2)
                            next_row.record(row_state.set_for(cell), cell2)
            

            row_state = next_row