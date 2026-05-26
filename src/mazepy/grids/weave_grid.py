from ..grids.grid import Grid
from PIL import Image
from collections.abc import Iterator
from ..cells.weave_cells import OverCell, UnderCell, SimpleOverCell

class WeaveGrid(Grid):
    '''
    Grid with paths that can burrow under one another
    '''
    type_of_grid = 'weave'

    def __init__(self, rows: int, columns: int, **kwargs):
        self.under_cells = []
        super().__init__(rows, columns, **kwargs)
    
    def prepare_grid(self):
        return [[OverCell(row, column, self) for column in range(self.columns)] for row in range(self.rows)]
    
    def tunnel_under(self, over_cell: OverCell) -> None:
        self.under_cells.append(UnderCell(over_cell))
    
    def each_cell(self) -> Iterator[OverCell|UnderCell|SimpleOverCell]:
        for cell in super().each_cell():
            yield cell

        for under_cell in self.under_cells:
            yield under_cell
    
    def to_png(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 4, inset: float = None) -> Image.Image:
        '''
        Converts the Grid to a png representation

        Parameters:
            cell_size (optional int) = 50, pixel size of the square cell
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 4, pixels between the edge of the maze and end of the png
            inset (optional float) = .2, % of cell_width that would be shrunk
            bypass_check (optional bool) = False, it will warn you if you call to_png on a colored grid that will not be colored if False

        Returns:
            The image representation of the grid
        '''
        return super().to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset or .2)

    def to_png_with_inset(self, draw, cell, mode, cell_size, edge_width, buffer, x, y, inset):
        if isinstance(cell, OverCell):
            add_inset = []
            if isinstance(cell.east, UnderCell):
                add_inset.append('east')
            if isinstance(cell.west, UnderCell):
                add_inset.append('west')
            if isinstance(cell.north, UnderCell):
                add_inset.append('north')            
            if isinstance(cell.south, UnderCell):
                add_inset.append('south')
            super().to_png_with_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y, inset, add_inset)
        else:
            x += .5*edge_width + buffer
            y += .5*edge_width + buffer
            x1, x4, y1, y4 = x, x+cell_size, y, y+cell_size
            x2, x3, y2, y3 = x1+inset, x4-inset, y1+inset, y4-inset

            if cell.horizontal_passageq():
                if mode == 'backgrounds':
                    color = self.background_color_for(cell)
                    if color:
                        draw.rectangle([(x1, y2+inset//2), (x2-inset//2, y3-inset//2)], fill=color)
                        draw.rectangle([(x3+inset//2, y2+inset//2), (x4, y3-inset//2)], fill=color)

            else:
                if mode == 'backgrounds':
                    color = self.background_color_for(cell)
                    if color:
                        draw.rectangle([(x2+inset//2, y1), (x3-inset//2, y2-inset//2)], fill=color)
                        draw.rectangle([(x2+inset//2, y3+inset//2), (x3-inset//2, y4)], fill=color)
                        
                draw.line([(x1, y2), (x2, y2)], fill='black', width=edge_width)
                draw.line([(x1, y3), (x2, y3)], fill='black', width=edge_width)
                draw.line([(x3, y2), (x4, y2)], fill='black', width=edge_width)
                draw.line([(x3, y3), (x4, y3)], fill='black', width=edge_width)

class PreconfiguredWeaveGrid(WeaveGrid):
    '''
    See precon_grid_ex for use case
    '''
    def prepare_grid(self):
        return [[SimpleOverCell(row, column, self) for column in range(self.columns)] for row in range(self.rows)]