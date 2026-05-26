from ..grids.grid import Grid
from ..cells.cell import Cell
from ..mask import Mask

class MaskedGrid(Grid):
    type_of_grid = 'masked'

    def __init__(self, mask: Mask):
        self.mask = mask
        super().__init__(mask.rows, mask.columns)
        self.size = mask.count()
    
    def prepare_grid(self):
        return [[Cell(row, column) if self.mask[row, column] else None for column in range(self.columns)] for row in range(self.rows)]

    def random_cell(self) -> Cell:
        row, col = self.mask.random_location()
        return self[row, col] 