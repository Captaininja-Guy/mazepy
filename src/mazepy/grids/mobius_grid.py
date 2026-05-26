from ..grids.grid import Grid
from ..grids.cylinder_grid import CylinderGrid
from PIL import Image, ImageDraw
import pyvista as pv
import numpy as np


class MobiusGrid(Grid): # If clear paper was a thing
    '''
    Mobius Strip grid intended to be viewed in 3d, see PaperMobiusGrid for something that can be cut out and folded
    '''
    type_of_grid = 'mobius'
        
    def __init__(self, rows, columns):
        '''
        Initialize attributes

        Parameters:
            rows (int) number of rows for the grid
            columns (int) number of columns for the grid
        '''
        super().__init__(rows, 2*columns)

    def __getitem__(self, position):
        row, column = position
        if not 0 <= row < self.rows:
            return None

        if not 0 <= column < self.columns:
            row = range(self.rows)[-row-1] # Flip the row about midpoint to emulate mobius 180 degree turn

        column %= len(self.grid[row])

        return self.grid[row][column]
    
    def view3d(self, *, edge_width: int = 3, show_axes: bool = False, **kwargs) -> None:
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3, edge width in pixels
            show_axes (optional bool) = False, weather or not to show the axes on the window
            kwargs any other keyword arguement to pyvista Plotter().show()
        '''
        plt = pv.Plotter()
        array = np.array(self.to_png(edge_width=edge_width, buffer=0))[1:,:,:]
        array[:,-1,:] = array[:, -2, :]
        tex = pv.numpy_to_texture(array)


        u = np.linspace(-np.pi,np.pi,100)
        v = np.linspace(-1,1,100)
        u, v = np.meshgrid(u,v)

        x = (1+v/2*np.cos(u/2))*np.cos(u)
        y = (1+v/2*np.cos(u/2))*np.sin(u)
        z = v/2*np.sin(u/2)

        mobius = pv.StructuredGrid(x, y, z).extract_surface(algorithm='dataset_surface')
        mobius.active_texture_coordinates = np.zeros((mobius.points.shape[0], 2))

        u = np.atan2(y, x)
        rho = np.sqrt(x**2+y**2)
        v = 2*np.sign(z*np.sin(u/2)+(rho-1)*np.cos(u/2))*np.sqrt((rho-1)**2+z**2)

        u = (u/(2*np.pi) + .5).flatten()
        v = ((v+1)/2).flatten()


        mobius.active_texture_coordinates[:,0] = u
        mobius.active_texture_coordinates[:,1] = v

        plt.add_mesh(mobius, texture=tex)
        if show_axes:
            plt.show_axes()
        plt.show(**kwargs)


class PaperMobiusGrid(CylinderGrid): # Since clear paper is not a thing
    '''
    Mobius Strip grid intended to be cut out and folded, hence the paper in the name. See MobuisGrid for 3d viewing
    '''
    type_of_grid = 'paper mobius'

    def __init__(self, rows, columns):
        '''
        Initialize attributes

        Parameters:
            rows (int) number of rows for the grid
            columns (int) number of columns for the grid
        '''
        super().__init__(rows, 2*columns)
    
    def to_png(self, *, cell_size=50, edge_width=3, buffer=1, inset=0) -> Image.Image:
        '''
        Gives a png representation of the maze ready to cut out and fold

        Parameters:
            cell_size (optional int) = 50, the pixel size of the square cells
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 1, the amount of white pixels between the edge of the maze and the end of the immage
            inset (optional float) = 0, % of cell width that cells would be shrunk
        
        Returns:
            The image representation of the grid
        '''
        grid_height = cell_size*self.rows
        mid_point = self.columns//2

        img_width = cell_size * mid_point + edge_width + 2*buffer
        img_height = grid_height*2 + edge_width + 2*buffer

        inset = int(cell_size * inset/2)

        img = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            for cell in self.each_cell():
                # Coordinates account for width and buffer
                x = cell.column%mid_point * cell_size
                y = cell.row * cell_size
                y += grid_height if cell.column >= mid_point else 0

                if inset > 0:
                    self.to_png_with_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y, inset)
                else:
                    self.to_png_without_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y)
        
        return img
    
    def show(self, *, cell_size=50, edge_width=3, buffer=1, inset=0) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        return super().show(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset)