from ..grids.grid import Grid
from PIL import Image
import numpy as np
import pyvista as pv

class CylinderGrid(Grid):
    '''
    A 3d cylinder grid
    '''
    type_of_grid = 'cylinder'

    def __getitem__(self, position):
        row, column = position
        if not 0 <= row < self.rows:
            return None
        column %= len(self.grid[row])
        return self.grid[row][column]
    
    def to_png(self, *, cell_size = 50, edge_width = 3, buffer = 1, inset = 0, bypass_check = False) -> Image.Image:
        '''
        Gives a png representation of the maze ready to cut out and fold into a cylinder

        Parameters:
            cell_size (optional int) = 50, the pixel size of the square cells
            edge_width (optional int) = 3, width of each edge in pixels
            buffer (optional int) = 4, the amount of white pixels between the edge of the maze and the end of the immage
            inset (optional float) = 0, % of cell width that cells would be shrunk
            bypass_check (optional bool) = False it will warn you if you call to_png on a colored grid that will not be colored if False
        
        Returns:
            The image representation of the grid
        '''
        return super().to_png(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset, bypass_check=bypass_check)
    
    def show(self, *, cell_size = 50, edge_width = 3, buffer = 1, inset = 0) -> None:
        '''
        Shows to_png() in image viewer, see to_png for more info
        '''
        return super().show(cell_size=cell_size, edge_width=edge_width, buffer=buffer, inset=inset)
    
    def view3d(self, *, cell_size = 50, edge_width = 2, show_axes: bool = False, filled: bool = True, **kwargs) -> None:
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3
            show_axes (optional bool) = False weather or not to show the axes on the window
            filled (optional bool) = True weather to fill the caps of the cylinder
            kwargs any other keyword arguement to pyvista Plotter().show()'
        
        Errors:
            ValueError is edge_width is not even
        '''
        if edge_width%2 != 0:
            raise ValueError('Edge width must be even')
        
        image = self.to_png(cell_size=cell_size, edge_width=edge_width, buffer=0)

        array_left = np.array(image.crop((0, 1, image.width//2, image.height)))

        array_right = np.fliplr(np.array(image.crop((image.width//2, 0, image.width, image.height))))

        plt = pv.Plotter()
        tex1 = pv.numpy_to_texture(array_left)
        tex2 = pv.numpy_to_texture(array_right)
        cyl = pv.Cylinder(direction=(0,0,1), capping=False, height=self.rows/8)
        
        half = pv.Cube(bounds=(cyl.bounds[0], 0, cyl.bounds[2]-1, cyl.bounds[3]+1, cyl.bounds[-2]-1, cyl.bounds[-1]+1))
        clipped = cyl.clip_surface(half)
        plt.add_mesh(clipped, texture=tex1)

        half2 = pv.Cube(bounds=(0, cyl.bounds[1], cyl.bounds[2]-1, cyl.bounds[3]+1, cyl.bounds[-2]-1, cyl.bounds[-1]+1))
        clipped2 = cyl.clip_surface(half2)
        plt.add_mesh(clipped2, texture=tex2)

        if filled:
            disk1 = pv.Disc(center=(0, 0, cyl.bounds[-1]), inner=0, c_res=100)
            disk2 = pv.Disc(center=(0, 0, cyl.bounds[-2]), inner=0, c_res=100)

            plt.add_mesh(disk1, color='white')
            plt.add_mesh(disk2, color='white')

        if show_axes:
            plt.show_axes()

        plt.show(**kwargs)
