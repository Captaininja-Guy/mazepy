from ..grids.grid import Grid
from ..cells.triangle_cell import TriangleCell
from PIL import Image, ImageDraw

class TriangleGrid(Grid):
    '''
    Triangular grid
    '''
    type_of_grid = 'triangle'

    def prepare_grid(self):
        return [[TriangleCell(row, column) for column in range(self.columns)] for row in range(self.rows)]
    
    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column
            cell.west = self[row, col-1]
            cell.east = self[row, col+1]

            if cell.uprightq():
                cell.south = self[row+1, col]
            else:
                cell.north = self[row-1, col]

    def to_png(self, *, cell_size: int = 50, edge_width: int = 2, 
               buffer: int = 7, bypass_check: bool = False) -> Image.Image:
        '''
        Converts the Grid to a png representation

        Parameters:
            cell_size (optional int) = 50, pixel size of the square cell
            edge_width (optional int) = 2, edge width in pixels
            buffer (optional int) = 7, pixels between the edge of the maze and end of the png
            inset (optional float) = 0, % of cell_width that would be shrunk
            bypass_check (optional bool) = False, it will warn you if you call to_png on a colored grid that will not be colored if False

        Returns:
            The image representation of the grid
        '''
        if not bypass_check and hasattr(self, 'base') and self.distances is None:
            print('Distances not set, colors will not be shown')
            if input('Continue: y/N: ').lower() == 'n':
                return
            
        height = cell_size * (3**.5)/2

        img_width = int(cell_size *(self.columns + 1) / 2 + 2*buffer)
        img_height = int(height * self.rows + 2*buffer)

        img = Image.new('RGB', (img_width+1, img_height+1), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            if mode == 'backgrounds' and not hasattr(self, 'distances'):
                continue
            for cell in self.each_cell():
                cx = (1 + cell.column) * cell_size/2
                cy = (.5 + cell.row) * height

                west_x = int(cx - cell_size/2 + buffer)
                mid_x = int(cx + buffer)
                east_x = int(cx + cell_size/2 + buffer)

                apex_y, base_y = (int(cy-height/2 + buffer), int(cy+height/2 + buffer)) if cell.uprightq() else (int(cy+height/2 + buffer), int(cy-height/2 + buffer))

                if mode == 'backgrounds':
                    color = self.background_color_for(cell)
                    if color:
                        draw.polygon([(west_x, base_y),(mid_x, apex_y),(east_x, base_y)], fill=color)
                else:
                    if not cell.west:
                        draw.line([(west_x, base_y), (mid_x, apex_y)], fill='black', width=edge_width)
                    if not cell.linkedq(cell.east):
                        draw.line([(east_x, base_y), (mid_x, apex_y)], fill='black', width=edge_width)

                    if (cell.uprightq() and cell.south is None) or (not cell.uprightq() and not cell.linkedq(cell.north)):
                        draw.line([(east_x, base_y), (west_x, base_y)], fill='black', width=edge_width)
        
        return img
    
    def show(self, *, cell_size: int = 50, edge_width: int = 2, buffer: int = 7):
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer)
        if img is not None:
            img.show()
