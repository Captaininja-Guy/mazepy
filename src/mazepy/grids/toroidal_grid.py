from ..grids.grid import Grid
from PIL import Image
import pyvista as pv
import numpy as np

class ToroidalGrid(Grid):
    '''
    Toroidal (donut) grid
    '''
    type_of_grid = 'toroidal'

    def __getitem__(self, position):
        row, column = position

        row %= self.rows
        column %= len(self.grid[row])
        return self.grid[row][column]
    
    def to_png(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 1, 
               inset: float = 0, bypass_check = False) -> Image.Image:
        '''
        Converts the Grid to a png representation to be cut out and folded

        Parameters:
            cell_size (optional int) = 50, pixel size of the square cell
            edge_width (optional int) = 3, edge width in pixels
            buffer (optional int) = 1, pixels between the edge of the maze and end of the png
            inset (optional float) = 0, % of cell_width that would be shrunk
            bypass_check (optional bool) = False, it will warn you if you call to_png on a colored grid that will not be colored if False

        Returns:
            The image representation of the grid
        '''
        return super().to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset, bypass_check=bypass_check)
    
    def show(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 1, inset: float = 0) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        return super().show(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset)
    
    def view3d(self, *, edge_width: int = 3, show_axes: bool = False, **kwargs) -> None:
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3
            show_axes (optional bool) = False, whether or not to show the axes on the window
            kwargs any other keyword arguement to pyvista Plotter().show()'
        '''
        array = np.array(self.to_png(edge_width=edge_width, buffer=0))[1:, 1:, :]

        # Copy the last row because the edge will only be two pixels wide there
        array = np.hstack((array, array[:,-1:,:])) 

        tex = pv.numpy_to_texture(array)

        theta = np.linspace(-np.pi,np.pi, 100)
        theta, phi = np.meshgrid(theta, theta)

        plt = pv.Plotter()
        R, r = 1, .5
        x = (R + r*np.cos(theta))*np.cos(phi)
        y = (R + r*np.cos(theta))*np.sin(phi)
        z = r*np.sin(theta)
        rho = np.sqrt(x**2 + y**2)

        torus = pv.StructuredGrid(x, y, z).extract_surface(algorithm='dataset_surface')

        torus.active_texture_coordinates = np.zeros((torus.points.shape[0], 2))
        torus.active_texture_coordinates[:, 0] = (.5 + np.atan2(y, x)/(2*np.pi)).flatten()
        torus.active_texture_coordinates[:, 1] = (.5 + np.atan2(z, rho-1)/(2*np.pi)).flatten()

        plt.add_mesh(torus, texture=tex)
        if show_axes:
            plt.show_axes()
        plt.show(**kwargs)
