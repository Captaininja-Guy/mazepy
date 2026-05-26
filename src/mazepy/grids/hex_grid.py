from ..grids.grid import Grid
from ..cells.hex_cell import HexCell
from PIL import Image, ImageDraw

class HexGrid(Grid):
    type_of_grid = 'hex'

    def prepare_grid(self):
        return [[HexCell(row, column) for column in range(self.columns)] for row in range(self.rows)]
    
    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column

            north_diagonal, south_diagonal = (row-1, row) if col%2 != 0 else (row, row+1)

            cell.northwest = self[north_diagonal, col-1]
            cell.north = self[row-1, col]
            cell.northeast = self[north_diagonal, col+1]
            cell.southwest = self[south_diagonal, col-1]
            cell.south = self[row+1, col]
            cell.southeast = self[south_diagonal, col+1]

    def to_png(self, *, cell_size: int = 50, edge_width: int = 3, 
               buffer: int = 7, bypass_check: bool = False) -> Image.Image:
        '''
        Converts the Grid to a png representation

        Parameters:
            cell_size (optional int) = 50, pixel size of the square cell
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 7, pixels between the edge of the maze and end of the png
            inset (optional float) = 0, % of cell_width that would be shrunk
            bypass_check (optional bool) = False, it will warn you if you call to_png on a colored grid that will not be colored if False

        Returns:
            The image representation of the grid
        '''
        if not bypass_check and hasattr(self, 'base') and self.distances is None:
            print("\033[93mWarning:\033[00m", 'Distances not set, colors will not be shown')
            cont = input('Continue (y/N): ')
            if cont.lower() != 'y':
                return
            
        a_size = cell_size / 2
        b_size = cell_size * (3**.5) / 2
        height = b_size * 2

        img_width = int(3*a_size * self.columns + a_size + 2*buffer)
        img_height = int(height*self.rows + b_size + 2*buffer)
        img = Image.new('RGB', (img_width+1, img_height+1), 'white')
        draw = ImageDraw.Draw(img)

        

        for mode in 'backgrounds', 'walls':
            if mode == 'backgrounds' and not hasattr(self, 'distances'):
                continue
            for cell in self.each_cell():
                cx = cell_size + 3*cell.column*a_size
                cy = b_size + cell.row*height + b_size*(cell.column%2 == 0)

                x_fw = int(cx - cell_size + buffer)
                x_nw = int(cx - a_size + buffer)
                x_ne = int(cx + a_size + buffer)
                x_fe = int(cx + cell_size + buffer)

                y_n = int(cy - b_size + buffer)
                y_m = int(cy + buffer)
                y_s = int(cy + b_size + buffer)
                
                if mode == 'backgrounds':
                    color = self.background_color_for(cell)
                    if color:
                        draw.polygon([(x_fw, y_m), (x_nw, y_n), (x_ne, y_n), (x_fe, y_m), (x_ne, y_s), (x_nw, y_s)], fill=color)
                else:
                    if not cell.southwest:
                        draw.line([(x_fw, y_m), (x_nw, y_s)], width=edge_width, fill='black')
                    if not cell.northwest:
                        draw.line([(x_fw, y_m), (x_nw, y_n)], width=edge_width, fill='black')
                    if not cell.north:
                        draw.line([(x_nw, y_n), (x_ne, y_n)], width=edge_width, fill='black')
                    if not cell.linkedq(cell.northeast):
                        draw.line([(x_ne, y_n), (x_fe, y_m)], width=edge_width, fill='black')
                    if not cell.linkedq(cell.southeast):
                        draw.line([(x_fe, y_m), (x_ne, y_s)], width=edge_width, fill='black')
                    if not cell.linkedq(cell.south):
                        draw.line([(x_ne, y_s), (x_nw, y_s)], width=edge_width, fill='black')
        
        return img

    def show(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 7) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer)
        if img is not None:
            img.show()