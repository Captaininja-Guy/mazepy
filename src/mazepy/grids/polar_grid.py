from ..grids.grid import Grid
from ..cells.polar_cell import PolarCell
from math import sin, cos, pi
from PIL import Image, ImageDraw

class PolarGrid(Grid):
    '''
    Polar Grid, cells radiate outward from center of a circle
    '''
    type_of_grid = 'polar'

    def __init__(self, rows: int, columns: int = None, **kwargs):
        if columns is not None and rows != columns:
            raise TypeError('PolarGrid requires rows = columns or 1 positional arguement')
        super().__init__(rows, 1, **kwargs)
        self.size = sum(1 for _ in self.each_cell)

    def prepare_grid(self):
        rows = [None] * self.rows
        rows[0] = [PolarCell(0, 0)]

        for row in range(1, self.rows):
            radius = row / self.rows
            circumference = 2*pi*radius

            prev_count = len(rows[row - 1])
            est_cell_width = circumference / prev_count
            ratio = int(est_cell_width * self.rows + .5)

            cells = prev_count * ratio
            rows[row] = [PolarCell(row, col) for col in range(cells)]

        
        return rows

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column
            if row > 0:
                cell.cw = self[row, col + 1]
                cell.ccw = self[row, col - 1]

                ratio = len(self.grid[row]) // len(self.grid[row-1])
                parent = self.grid[row-1][col//ratio]
                parent.outward.append(cell)
                cell.inward = parent

    def __getitem__(self, position: tuple[int]):
        row, column = position
        if not 0 <= row < self.rows:
            return None
        return self.grid[row][column % len(self.grid[row])]

    def show(self, *, cell_size: int = 30, edge_width: int = 1, buffer: int = 10) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer)
        if img is not None:
            img.show()
    
    def to_png(self, *, cell_size: int = 30, edge_width: int = 1, buffer: int = 10, bypass_check: bool = False) -> Image.Image:
        '''
        Converts the Grid to a png representation

        Parameters:
            cell_size (optional int) = 30, pixel size of the square cell
            edge_width (optional int) = 1, edge width in pixels
            buffer (optional int) = 10, pixels between the edge of the maze and end of the png
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
            
        img_size = 2 * self.rows * cell_size + 2*buffer + 1
        center = img_size / 2

        img = Image.new("RGB", (img_size, img_size), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            if mode == 'backgrounds' and not hasattr(self, 'distances'):
                continue
            for cell in self.each_cell():
                if mode == 'walls' and cell.row == 0:
                    continue

                theta = 2*pi / len(self.grid[cell.row])
                inner_radius = cell.row * cell_size
                outer_radius = (cell.row+1)*cell_size
                theta_ccw = cell.column * theta
                theta_cw = (cell.column+1) * theta

                ax = center + int(inner_radius * cos(theta_ccw))
                ay = center + int(inner_radius * sin(theta_ccw))
                bx = center + int(outer_radius * cos(theta_ccw))
                by = center + int(outer_radius * sin(theta_ccw))
                cx = center + int(inner_radius * cos(theta_cw))
                cy = center + int(inner_radius * sin(theta_cw))
                dx = center + int(outer_radius * cos(theta_cw))
                dy = center + int(outer_radius * sin(theta_cw))

                if mode == 'backgrounds':
                    color = self.background_color_for(cell)
                    if color:
                        if cell.row == 0:
                            verticies = []
                            for out in cell.outward: # Drawing the hexagon for the center cell
                                theta_out = 2*pi / len(self.grid[out.row])
                                inner_radius_out = out.row * cell_size
                                theta_cw_out = (out.column+1) * theta_out

                                x_out = center + int(inner_radius_out * cos(theta_cw_out))
                                y_out = center + int(inner_radius_out * sin(theta_cw_out))
                                verticies.append((x_out, y_out))

                            draw.polygon(verticies, fill=color)

                        elif len(cell.outward) == 2: # If the cell splits, a pentagon must be drawn to account for multiple cells outwards
                            cell_out = cell.outward[0]
                            theta_out = 2*pi / len(self.grid[cell_out.row])
                            inner_radius_out = cell_out.row * cell_size
                            theta_cw_out = (cell_out.column+1) * theta_out

                            x_out = center + int(inner_radius_out * cos(theta_cw_out))
                            y_out = center + int(inner_radius_out * sin(theta_cw_out))

                            draw.polygon([(ax, ay), (bx, by), (x_out, y_out), (dx, dy), (cx, cy)], fill=color)
                        else:
                            draw.polygon([(ax, ay), (bx, by), (dx, dy), (cx, cy)], fill=color)
                else:
                    if not cell.linkedq(cell.inward):
                        draw.line([(ax, ay),(cx, cy)], fill='black', width=edge_width)
                    if not cell.linkedq(cell.cw):
                        draw.line([(cx, cy),(dx, dy)], fill='black', width=edge_width)
                    if cell.row == self.rows-1:
                        draw.line([(bx, by),(dx, dy)], fill='black', width=edge_width)
        
        return img
