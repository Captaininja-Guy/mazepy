from ..cells.cell import Cell
from ..grids.grid import Grid
import random as rand
from collections.abc import Iterator
from PIL import Image, ImageDraw
import numpy as np
import pyvista as pv


class Cell3D(Cell):
    def __init__(self, level, row, column):
        self.level = level
        self.up = None
        self.down = None
        super().__init__(row, column)
    
    def neighbors(self):
        list_ = super().neighbors()
        if self.up:
            list_.append(self.up)
        if self.down:
            list_.append(self.down)
        
        return list_

    def __str__(self):
        return f'3d Cell: ({self.level},{self.row},{self.column})'#, Links: {self.links()}, Neighbors: {self.neighbors()}'

class Grid3D(Grid):
    type_of_grid = '3d'

    def __init__(self, levels, rows, columns):
        '''
        Initialize attributes

        Parameters:
            levels (int) number of levels
            rows (int) number of rows for the levels
            columns (int) number of columns for the levels
        '''
        self.levels = levels
        super().__init__(rows, columns)
        self.size = self.levels * self.rows * self.columns
    
    def prepare_grid(self):
        return [[[Cell3D(level, row, column) for column in range(self.columns)] for row in range(self.rows)] for level in range(self.levels)]
    
    def configure_cells(self):
        for cell in self.each_cell():
            level, row, column = cell.level, cell.row, cell.column

            cell.north = self[level, row-1, column]
            cell.south = self[level, row+1, column]
            cell.west = self[level, row, column-1]
            cell.east = self[level, row, column+1]
            cell.up = self[level+1, row, column]
            cell.down = self[level-1, row, column]
    
    def __getitem__(self, position: tuple[int]) -> Cell3D:
        level, row, column = position
        if (not 0 <= level < self.levels 
            or not 0 <= row < len(self.grid[level]) 
            or not 0 <= column < len(self.grid[level][row])):
            return None
        
        return self.grid[level][row][column]
    
    def random_cell(self) -> Cell3D:
        level = rand.choice(range(self.levels))
        row = rand.choice(range(len(self.grid[level])))
        column = rand.choice(range(len(self.grid[level][row])))

        return self.grid[level][row][column]
    
    def each_level(self) -> Iterator[list[list[Cell3D]]]:
        for level in self.grid:
            yield level
    
    def each_row(self) -> Iterator[list[Cell3D]]:
        for level in self.grid:
            for row in level:
                yield row
    
    def to_png(self, *, cell_size: int = 50, edge_width: int = 3,
               buffer: int = 4, inset: float = 0, margin: int = None) -> Image.Image:
        '''
        Gives a png representation of the maze ready to cut out and fold

        Parameters:
            cell_size (optional int) = 50, the pixel size of the square cells
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 4, the amount of white pixels between the edge of the maze and the end of the immage
            inset (optional float) = 0, % of cell width that cells would be shrunk
            margin (optional int) = cell_size//2, how many pixels to seperate levels by
        
        Returns:
            The image representation of the grid
        '''
        inset = int(cell_size * inset)
        if margin is None:
            margin = cell_size // 2

        grid_width = cell_size * self.columns
        grid_height = cell_size * self.rows

        img_width = grid_width*self.levels + (self.levels-1)*margin + edge_width + 2*buffer
        img_height = grid_height + edge_width + 2*buffer

        img = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            for cell in self.each_cell():

                x = cell.level * (grid_width+margin) + cell.column * cell_size
                y = cell.row * cell_size

                if inset > 0:
                    self.to_png_with_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y, inset)
                else:
                    self.to_png_without_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y)

                if mode == 'walls':
                    mid_x = x+cell_size//2
                    mid_y = y+cell_size//2

                    if cell.linkedq(cell.down):
                        draw.line([(mid_x, mid_y+3), (mid_x+2, mid_y+1)], fill='orange')
                        draw.line([(mid_x, mid_y+3), (mid_x-2, mid_y+1)], fill='orange')
                    
                    if cell.linkedq(cell.up):
                        draw.line([(mid_x, mid_y-3), (mid_x+2, mid_y-1)], fill='orange')
                        draw.line([(mid_x, mid_y-3), (mid_x-2, mid_y-1)], fill='orange')
        
        return img
    
    def show(self, *, cell_size: int = 50, edge_width: int = 3,
               buffer: int = 4, inset: float = 0, margin: float = None) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer,
                          inset=inset, margin=margin)
        
        if img is not None:
            img.show()

    def view3d(self, *, cell_size: int = 50, edge_width: int = 3, 
               show_axes: bool = False, seperation: float = .5, **kwargs):
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3, edge width in pixels
            show_axes (optional bool) = False, whether or not to show the axes on the window
            seperation (optional float) = .5, how much to seperate each grid, they are 1 length and width
            kwargs any other keyword arguement to pyvista Plotter().show()
        '''
        image = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=0, margin=0)

        # Set corners to black
        image.putpixel((0,0), (0, 0, 0))
        image.putpixel((0,image.height-1), (0, 0, 0))
        image.putpixel((image.width-1,0), (0, 0, 0))
        image.putpixel((image.width-1, image.height-1), (0, 0, 0))

        grid_width = cell_size * self.columns

        x_left = 0
        x_right = grid_width + edge_width - 1

        textures = []
        planes = []
        for i in range(self.levels):
            textures.append(pv.numpy_to_texture(np.array(image.crop((x_left, 0, x_right, image.height)))))
            x_left += grid_width
            x_right += grid_width

            planes.append(pv.Plane(center=(0, 0, i*seperation)))

        plt = pv.Plotter()
        for tex, plane in zip(textures, planes):
            plt.add_mesh(plane, texture=tex)
        
        if show_axes:
            plt.show_axes()
        plt.show(**kwargs)
