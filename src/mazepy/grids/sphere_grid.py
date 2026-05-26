from ..grids.polar_grid import PolarGrid
from ..cells.polar_cell import PolarCell
from collections.abc import Iterator
from ..grids.grid import Grid
from PIL import Image, ImageDraw
import random as rand
import numpy as np
import pyvista as pv

class HemisphereCell(PolarCell):
    def __init__(self, hemisphere: int, row: int, column: int):
        self.hemisphere = hemisphere
        super().__init__(row, column)


class HemisphereGrid(PolarGrid):
    def __init__(self, _id, rows):
        self._id = _id
        super().__init__(rows)
    
    def h_row_size(self, row: int) -> int:
        return len(self.grid[row])

    def prepare_grid(self):
        grid = [None]*self.rows
        angular_height = np.pi / (2*self.rows)

        grid[0] = [HemisphereCell(self._id, 0, 0)]

        for row in range(1, self.rows):
            theta = (row+1)*angular_height
            radius = np.sin(theta)
            circumference = 2*np.pi*radius

            prev_count = len(grid[row-1])
            est_cell_width = circumference / prev_count
            ratio = int(est_cell_width/angular_height + .5)

            cells = prev_count * ratio

            grid[row] = [HemisphereCell(self._id, row, column) for column in range(cells)]
        
        return grid
    

class SphereGrid(Grid):
    '''
    Spherical Grid
    '''
    type_of_grid = 'sphere'

    def __init__(self, rows):
        if not rows%2 == 0:
            raise TypeError("Rows must be an even number")
        
        self.equator = rows//2
        super().__init__(rows, 1)
    
    def prepare_grid(self):
        return [HemisphereGrid(_id, self.equator) for _id in range(2)]
    
    def configure_cells(self):
        belt = self.equator - 1
        for index in range(self.s_row_size(belt)):
            a, b = self[0, belt, index], self[1, belt, index]
            a.outward.append(b)
            b.outward.append(a)
            # Connects the 2 equators to each other
    
    def __getitem__(self, position):
        hemi, row, column = position
        return self.grid[hemi][row, column]

    def each_cell(self) -> Iterator[PolarCell]:
        for hemi in self.grid:
            for cell in hemi.each_cell():
                yield cell
    
    def random_cell(self) -> PolarCell:
        return rand.choice(self.grid).random_cell()
    
    def s_row_size(self, row) -> int:
        return self.grid[0].h_row_size(row)
    
    def to_png(self, *, ideal_size: int = 10) -> Image.Image:
        '''
        Converts the Grid to a png representation to be cut out and folded

        Parameters:
            ideal_size (optional int) = 10, ideal cell size, will be distorted to make image rectangular

        Returns:
            The image representation of the grid
        '''
        img_height = ideal_size * self.rows
        img_width = ideal_size * self.grid[0].h_row_size(self.equator - 1)

        img = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for cell in self.each_cell():
            row_size = self.s_row_size(cell.row)
            cell_width = img_width / row_size

            x1 = cell.column*cell_width
            x2 = x1+cell_width

            y1 = cell.row*ideal_size
            y2 = y1 + ideal_size

            if cell.hemisphere > 0:
                y1 = img_height - y1
                y2 = img_height - y2
            
            x1 = int(x1+.5); x2 = int(x2+.5)
            y1 = int(y1+.5); y2 = int(y2+.5)

            if cell.row > 0:
                if not cell.linkedq(cell.cw):
                    draw.line([(x2, y1), (x2, y2)], 'black')
                if not cell.linkedq(cell.inward):
                    draw.line([(x1, y1), (x2, y1)], 'black')
            
            if cell.hemisphere == 0 and cell.row == self.equator-1:
                if not cell.linkedq(cell.outward[0]):
                    draw.line([(x1, y2), (x2, y2)], 'black')
        
        return img
    
    def show(self, *, ideal_size: int = 10) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        img = self.to_png(ideal_size=ideal_size)
        img.show()

    def view3d(self, *, ideal_size: int = 10, show_axes: bool = False, **kwargs) -> None:
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3
            show_axes (optional bool) = False, whether or not to show the axes on the window
            filled (optional bool) = True, whether to fill the caps of the cylinder
            kwargs any other keyword arguement to pyvista Plotter().show()'
        '''
        array = np.array(self.to_png(ideal_size=ideal_size))

        plt = pv.Plotter()
        sphere = pv.Sphere(
            radius=1,
            theta_resolution=120,
            phi_resolution=120,
            start_theta=270.001,
            end_theta=270,
        )

        # Initialize the texture coordinates array
        sphere.active_texture_coordinates = np.zeros((sphere.points.shape[0], 2))

        # Populate by manually calculating
        sphere.active_texture_coordinates[:, 0] = 0.5 + np.arctan2(-sphere.points[:, 0], sphere.points[:, 1])/(2 * np.pi)
        sphere.active_texture_coordinates[:, 1] = 0.5 + np.arcsin(sphere.points[:, 2]) / np.pi

        tex = pv.numpy_to_texture(array)
        plt.add_mesh(sphere, texture=tex)
        if show_axes:
            plt.show_axes()
            
        plt.show(**kwargs)