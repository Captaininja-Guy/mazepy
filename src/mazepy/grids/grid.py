from ..cells.cell import Cell
import random as rand
from PIL import Image, ImageDraw
import io
from collections.abc import Iterator


class Grid:
    '''
    rectangular grid
    '''
    type_of_grid = 'regular'
    
    def __init__(self, rows: int, columns: int, **kwargs):
        '''
        Initialize attributes

        Parameters:
            rows (int) number of rows for the grid
            columns (int) number of columns for the grid
        '''
        self.rows = rows
        self.columns = columns
        self.size = self.rows * self.columns
        self.grid = self.prepare_grid()
        self.configure_cells()

    # Returns 2D array of Cell objects
    def prepare_grid(self):
        return [[Cell(row, column) for column in range(self.columns)] for row in range(self.rows)]

    # Gives each cell its neighbors
    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column

            cell.north = self[row-1, col]
            cell.south = self[row+1, col]
            cell.east = self[row, col+1]
            cell.west = self[row, col-1]

    def __getitem__(self, position: tuple[int]) -> Cell:
        row, column = position
        if not 0 <= row < self.rows or not 0 <= column < len(self.grid[row]):
            return None
        return self.grid[row][column]

    def each_cell(self) -> Iterator[Cell]:
        for row in self.each_row():
            for cell in row:
                if cell:
                    yield cell

    def each_row(self) -> Iterator[list[Cell]]:
        for row in self.grid:
            yield row

    def random_cell(self) -> Cell:
        row = rand.choice(range(self.rows))
        column = rand.choice(range(len(self.grid[row])))
        return self[row, column]

    def contents_of(self, cell: Cell) -> str:
        # return cell.contents_of # For debugging
        return "  "
    
    def background_color_for(self, cell: Cell) -> tuple | None:
        return None
    
    def __str__(self):
        '''
        Represents the Grid as ASCII art
        '''
        output = io.StringIO()
        def corner_selector(rindex, index, cell): # Choses the correct NE corner
            wall_north, wall_south, wall_east, wall_west = False, False, False, False
            cell_north, cell_west = self[rindex-1, index], self[rindex, index-1]
            cell_NW = self[rindex-1, index-1]

            # If one of cell and W is none, or both are there and not linked
            if ((cell is None) ^ (cell_west is None)) or cell is not None and not cell.linkedq(cell_west):
                wall_south = True
            
            # If one of cell and N is none, or both are there and not linked
            if ((cell is None) ^ (cell_north is None)) or cell is not None and not cell.linkedq(cell_north):
                wall_east = True
            
            # One of N and NW is none, or both are there and not linked
            if ((cell_NW is None) ^ (cell_north is None)) or cell_north is not None and not cell_north.linkedq(cell_NW):
                wall_north = True
            
            # One of W and NW is none, or both are there and not linked
            if ((cell_NW is None) ^ (cell_west is None)) or cell_west is not None and not cell_west.linkedq(cell_NW):
                wall_west = True
            
            # Edge Checking
            if rindex == 0:
                wall_north = False
            if index == 0:
                wall_west = False
            if index == self.columns:
                wall_east = False
            if rindex == self.rows:
                wall_south = False

            return wall_north, wall_south, wall_east, wall_west
            
        def corner_to_UNICODE(rindex, index, cell): # Converts N,S,E,W -> Unicode corner character
            N,S,E,W = corner_selector(rindex, index, cell)
            
            match (N,S,E,W):
                case (True, True, True, True):
                    return ((N, S, E, W), '\u253c')
                case (True, True, True, False):
                    return ((N, S, E, W), '\u251c')
                case (True, True, False, True):
                    return ((N, S, E, W), '\u2524')
                case (True, True, False, False):
                    return ((N, S, E, W), '\u2502')
                case (True, False, True, True):
                    return ((N, S, E, W), '\u2534')
                case (True, False, True, False):
                    return ((N, S, E, W), '\u2514')
                case (True, False, False, True):
                    return ((N, S, E, W), '\u2518')
                case (True, False, False, False):
                    return ((N, S, E, W), '\u2575')
                case (False, True, True, True):
                    return ((N, S, E, W), '\u252c')
                case (False, True, True, False):
                    return ((N, S, E, W), '\u250c')
                case (False, True, False, True):
                    return ((N, S, E, W), '\u2510')
                case (False, True, False, False):
                    return ((N, S, E, W), '\u2577')
                case (False, False, True, True):
                    return ((N, S, E, W), '\u2500')
                case (False, False, True, False):
                    return ((N, S, E, W), '\u2576')
                case (False, False, False, True):
                    return ((N, S, E, W), '\u2574')
                case (False, False, False, False):
                    return ((N, S, E, W), '·')
        
        for rindex, row in enumerate(self.each_row()):
            top = io.StringIO()
            middle = io.StringIO()
            for index, cell in enumerate(row):
                (_, wall_South, wall_East, _), corner = corner_to_UNICODE(rindex, index, cell)
                if wall_South:
                    middle.write("\u2502 " + self.contents_of(cell) + " ")
                else:
                    middle.write("  " + self.contents_of(cell) + " ")
                if wall_East:
                    top.write(corner + "\u2500\u2500\u2500\u2500")
                else:
                    top.write(corner + "    ")
            
            (_, wall_South, _, _), corner = corner_to_UNICODE(rindex, self.columns, None)
            top.write(corner + '\n')
            if wall_South:
                middle.write("\u2502\n")
            else:
                middle.write(" \n")

            output.write(top.getvalue() + middle.getvalue())
        
        bottom = io.StringIO()
        for i in range(self.columns):
            (_, _, wall_East, _), corner = corner_to_UNICODE(self.rows, i, None)
            if wall_East:
                bottom.write(corner + "\u2500\u2500\u2500\u2500")
            else:
                bottom.write(corner + "    ")

        _, corner = corner_to_UNICODE(self.rows, self.columns, None)
        output.write(bottom.getvalue() + corner)

        return output.getvalue()
    
    def to_png_with_inset(self, draw, cell, mode, cell_size, edge_width, buffer, x, y, inset, *args):
        
        x += .5*edge_width + buffer
        y += .5*edge_width + buffer
        x1, x4, y1, y4 = int(x), int(x+cell_size), int(y), int(y+cell_size)
        x2, x3, y2, y3 = int(x1+inset), int(x4-inset), int(y1+inset), int(y4-inset)

        if mode == 'backgrounds':
            color = self.background_color_for(cell)
            if color:
                if cell.linkedq(cell.north):
                    _x1, _y1 = min(x2, x3), min(y1, y2)
                    _x2, _y2 = max(x2, x3), max(y1, y2)
                    draw.rectangle([(_x1, _y1), (_x2, _y2)], fill=color)
                if cell.linkedq(cell.east):
                    _x1, _y1 = min(x4, x3), min(y3, y2)
                    _x2, _y2 = max(x4, x3), max(y3, y2)
                    draw.rectangle([(_x1, _y1), (_x2, _y2)], fill=color)
                if cell.linkedq(cell.south):
                    _x1, _y1 = min(x2, x3), min(y3, y4)
                    _x2, _y2 = max(x2, x3), max(y3, y4)
                    draw.rectangle([(_x1, _y1), (_x2, _y2)], fill=color)
                if cell.linkedq(cell.west):
                    _x1, _y1 = min(x2, x1), min(y3, y2)
                    _x2, _y2 = max(x2, x1), max(y3, y2)
                    draw.rectangle([(_x1, _y1), (_x2, _y2)], fill=color)
                _x1, _y1 = min(x2, x3), min(y3, y2)
                _x2, _y2 = max(x2, x3), max(y3, y2)
                draw.rectangle([(_x1, _y1), (_x2, _y2)], fill=color)      
        else:
            add_inset = args[0] # This is just for WeavedGrids to make walls going under cells, meat the cross wall

            if cell.linkedq(cell.north):
                if add_inset and 'north' in add_inset:
                    y1 -= inset
                draw.line([(x2, y1), (x2, y2)], width=edge_width, fill='black')
                draw.line([(x3, y1), (x3, y2)], width=edge_width, fill='black')
            else:
                draw.line([(x2, y2), (x3, y2)], width=edge_width, fill='black')
            
            if cell.linkedq(cell.south):
                if add_inset and 'south' in add_inset:
                    y4 += inset
                draw.line([(x2, y3), (x2, y4)], width=edge_width, fill='black')
                draw.line([(x3, y3), (x3, y4)], width=edge_width, fill='black')
            else:
                draw.line([(x2, y3), (x3, y3)], width=edge_width, fill='black')

            if cell.linkedq(cell.east):
                if add_inset and 'east' in add_inset: 
                    x4 += inset
                draw.line([(x3, y2), (x4, y2)], width=edge_width, fill='black')
                draw.line([(x3, y3), (x4, y3)], width=edge_width, fill='black')
            else:
                draw.line([(x3, y2), (x3, y3)], width=edge_width, fill='black')
            
            if cell.linkedq(cell.west):
                if add_inset and 'west' in add_inset:
                    x1 -= inset
                draw.line([(x1, y2), (x2, y2)], width=edge_width, fill='black')
                draw.line([(x1, y3), (x2, y3)], width=edge_width, fill='black')
            else:
                draw.line([(x2, y2), (x2, y3)], width=edge_width, fill='black')

    def to_png_without_inset(self, draw, cell, mode, cell_size, edge_width, buffer, x, y):
            x1, y1 = int(x + .5*edge_width + buffer), int(y + .5*edge_width + buffer)
            x2, y2 = int(x1 + cell_size), int(y1 + cell_size)
            
            if mode == 'backgrounds':
                color = self.background_color_for(cell)
                if color:
                    draw.rectangle([(x1, y1), (x2, y2)], fill=color)
            else:
                # Since every cell draws its south and east walls, only the NW most cell has to draw its north and west walls
                if not cell.north:
                    draw.line([(x1, y1), (x2, y1)], width=edge_width, fill='black')
                if not cell.west:
                    draw.line([(x1, y1), (x1, y2)], width=edge_width, fill='black')

                if not cell.linkedq(cell.east):
                    draw.line([(x2, y1), (x2, y2)], width=edge_width, fill='black')
                if not cell.linkedq(cell.south):
                    draw.line([(x1, y2), (x2, y2)], width=edge_width, fill='black')

    def to_png(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 4, 
               inset: float = 0, bypass_check: bool = False) -> Image.Image:
        '''
        Converts the Grid to a png representation

        Parameters:
            cell_size (optional int) = 50, pixel size of the square cell
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 4, pixels between the edge of the maze and end of the png
            inset (optional float) = 0, % of cell_width that would be shrunk
            bypass_check (optional bool) = False, it will warn you if you call to_png on a colored grid that will not be colored if False

        Returns:
            The image representation of the grid
        '''

        if not bypass_check and hasattr(self, 'base') and self.distances is None:
            print('Distances not set, colors will not be shown')
            if input('Continue: y/N: ').lower() == 'n':
                return
            
        # Enough for the cells, width of border, and whitespace buffer
        img_width = cell_size * self.columns + edge_width + 2*buffer
        img_height = cell_size * self.rows + edge_width + 2*buffer
        inset = int(cell_size * inset/2)

        img = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            if mode == 'backgrounds' and not hasattr(self, 'distances'):
                continue
            for cell in self.each_cell():    
                # Coordinates account for width and buffer
                x = cell.column * cell_size
                y = cell.row * cell_size

                if inset > 0:
                    self.to_png_with_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y, inset)
                else:
                    self.to_png_without_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y)

        return img

    def show(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 4, inset: float = 0) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset)
        if img is not None:
            img.show()

    def deadends(self) -> list[Cell]:
        return [cell for cell in self.each_cell() if cell is not None and len(cell.links()) == 1]
    
    def braid(self, p: float = 1) -> None:
        '''
        Braids the Grid in place by connecting deadends to neighboring unlinked cells with probability p

        Parameters:
            p (optional float) = 1 probability to connect deadend to another cell 
        '''
        deadends = self.deadends()
        rand.shuffle(deadends)

        for cell in deadends:
            if len(cell.links()) != 1 or rand.random() > p:
                continue

            unlinked_neighbors = [neighbor for neighbor in cell.neighbors() if not cell.linkedq(neighbor)]
            if not unlinked_neighbors:
                continue
            
            best = [neighbor for neighbor in unlinked_neighbors if len(neighbor.links()) == 1]
            if not best:
                best = unlinked_neighbors
            neighbor = rand.choice(best)
            cell.link(neighbor)

    def make_bidi(self) -> None:
        for cell in self.each_cell():
            for neighbor in cell.neighbors():
                if not neighbor.linkedq(cell) and cell.linkedq(neighbor):
                    neighbor.link(cell, bidi=False)
    
    def clear(self):
        for cell in self.each_cell():
            for neighbor in cell.neighbors():
                if not cell.linkedq(neighbor):
                    cell.link(neighbor, False)