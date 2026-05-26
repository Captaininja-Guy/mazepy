from ..grids.grid import Grid
from ..cells.cell import Cell
import random as rand
from collections.abc import Iterator
from PIL import Image, ImageDraw
import pyvista as pv
import numpy as np

class CubeCell(Cell):
    def __init__(self, face, row, column):
        self.face = face
        super().__init__(row, column)


class CubeGrid(Grid):
    '''
    A 3d cube grid
    '''
    type_of_grid = 'cube'
    
    def __init__(self, dim: int):
        '''
        Initialized class attributes

        Parameters:
            dim (int) row and column length for each face
        '''
        super().__init__(dim, dim)
        self.size = 6 * self.dim**2
    
    def prepare_grid(self):
        self.dim = self.rows
        return [[[CubeCell(face, row, column)for column in range(self.dim)] for row in range(self.dim)] for face in range(6)]
    
    def each_face(self) -> Iterator[list[list[CubeCell]]]:
        for face in self.grid:
            yield face
    
    def each_row(self) -> Iterator[list[CubeCell]]:
        for face in self.grid:
            for row in face:
                yield row
    
    def random_cell(self) -> CubeCell:
        face = rand.randint(0,5)
        row = rand.randrange(self.dim)
        column = rand.randrange(self.dim)

        return self.grid[face][row][column]
    
    def configure_cells(self):
        for cell in self.each_cell():
            face, row, column = cell.face, cell.row, cell.column

            cell.west = self[face, row, column-1]
            cell.east = self[face, row, column+1]
            cell.north = self[face, row-1, column]
            cell.south = self[face, row+1, column]
    
    def __getitem__(self, position):
        face, row, column = position

        if face < 0 or face >= 6: return None
        face, row, column = self._wrap(face, row, column)
        return self.grid[face][row][column]
    
    def _wrap(self, face, row, column):
        n = self.dim-1

        if row < 0:
            match face:
                case 0:
                    return 4, column, 0
                case 1:
                    return 4, n, column
                case 2:
                    return 4, n-column, n
                case 3:
                    return 4, 0, n-column
                case 4:
                    return 3, 0, n-column
                case 5:
                    return 1, n, column
        elif row >= self.dim:
            match face:
                case 0:
                    return 5, n-column, 0
                case 1:
                    return 5, 0, column
                case 2:
                    return 5, column, n
                case 3:
                    return 5, n, n-column
                case 4:
                    return 1, 0, column
                case 5:
                    return 3, n, n-column
        elif column < 0:
            match face:
                case 0:
                    return 3, row, n
                case 1:
                    return 0, row, n
                case 2:
                    return 1, row, n
                case 3:
                    return 2, row, n
                case 4:
                    return 0, 0, row
                case 5:
                    return 0, n, n-row
        elif column >= self.dim:
            match face:
                case 0:
                    return 1, row, 0
                case 1:
                    return 2, row, 0
                case 2:
                    return 3, row, 0
                case 3:
                    return 0, row, 0
                case 4:
                    return 2, 0, n-row
                case 5:
                    return 2, n, row
        return face, row, column
    
    def to_png(self, *, cell_size: int = 50, edge_width: int = 3, buffer: int = 4, inset: float = 0) -> Image.Image:
        '''
        Gives a png representation of the maze ready to cut out and fold into a cube

        Parameters:
            cell_size (optional int) = 50, the pixel size of the square cells
            edge_width (optional int) = 3, width of each edge in pixels
            buffer (optional int) = 4, the amount of white pixels between the edge of the maze and the end of the immage
            inset (optional float) = 0, % of cell width that cells would be shrunk
        
        Returns:
            The image representation of the grid
        '''
        inset = int(cell_size * inset)

        face_width = face_height = cell_size * self.dim

        img_width = 4*face_width + edge_width + 2*buffer
        img_height = 3*face_height + edge_width + 2*buffer

        offsets = ((0,1), (1,1), (2,1), (3,1), (1,0), (1,2))

        outline_color = (208, 208, 208)
        img = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for mode in 'backgrounds', 'walls':
            for cell in self.each_cell():
                x = offsets[cell.face][0] * face_width+cell.column*cell_size
                y = offsets[cell.face][1] * face_height+cell.row*cell_size

                if inset > 0:
                    self.to_png_with_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y, inset)
                else:
                    self.to_png_without_inset(draw, cell, mode, cell_size, edge_width, buffer, x, y)
                
                # Outline of Cube
                if mode == 'walls':
                    x1, y1 = int(x + .5*edge_width + buffer), int(y + .5*edge_width + buffer)
                    x2, y2 = int(x1 + cell_size), int(y1 + cell_size)
                    if cell.face in (0,4,5) and cell.west.face != cell.face:
                        draw.line([(x1, y1), (x1, y2)], width=edge_width, fill=outline_color)

                    if cell.face in (0,2,3,5) and cell.south.face != cell.face:
                        draw.line([(x1, y2), (x2, y2)], width=edge_width, fill=outline_color)

                    if cell.face in (0,2,3,4) and cell.north.face != cell.face:
                        draw.line([(x1, y1), (x2, y1)], width=edge_width, fill=outline_color)
                    
                    if cell.face in (3,4,5) and cell.east.face != cell.face:
                        draw.line([(x2, y1), (x2, y2)], width=edge_width, fill=outline_color)


        return img
    
    def to_png_without_inset(self, draw, cell, mode, cell_size, edge_width, buffer, x, y):
        x1, y1 = int(x + .5*edge_width + buffer), int(y + .5*edge_width + buffer)
        x2, y2 = int(x1 + cell_size), int(y1 + cell_size)

        if mode == 'backgrounds':
            color = self.background_color_for(cell)
            if color:
                draw.rectangle([(x1, y1), (x2, y1)], fill=color)
        else:
            if cell.north.face != cell.face and not cell.linkedq(cell.north):
                draw.line([(x1, y1), (x2, y1)], width=edge_width, fill='black')
            if cell.west.face != cell.face and not cell.linkedq(cell.west):
                draw.line([(x1, y1), (x1, y2)], width=edge_width, fill='black')
            
            if not cell.linkedq(cell.east):
                draw.line([(x2, y1), (x2, y2)], width=edge_width, fill='black')
            if not cell.linkedq(cell.south):
                draw.line([(x1, y2), (x2, y2)], width=edge_width, fill='black')

    # Not perfect croping but it will do
    def to_face_arrays(self, *, edge_width: int = 3) -> list[np.ndarray]:
        base_image = self.to_png(edge_width=edge_width, buffer=0)

        face_width = face_height = 50 * self.dim
        img_height = 3*face_height + edge_width

        fh_ew = face_height + edge_width
        fw_ew = face_width + edge_width

        face0 = np.array(base_image.crop((edge_width, fh_ew-edge_width, face_width, 2*fh_ew-edge_width)).rotate(-90))

        face1 = np.array(base_image.crop((face_width, fh_ew-edge_width, 2*fw_ew-edge_width, 2*fh_ew-edge_width)).rotate(90))
        
        face2 = np.array(base_image.crop((2*fw_ew, fh_ew-edge_width, 3*fw_ew, 2*fh_ew-edge_width)).rotate(90))

        face3 = np.array(base_image.crop((3*face_width, fh_ew-edge_width, 4*fw_ew-edge_width, 2*fh_ew-edge_width)).rotate(90))

        face4 = np.array(base_image.crop((fw_ew-edge_width, 0, 2*fw_ew, face_height)))

        face5 = np.array(base_image.crop((fw_ew-edge_width, 2*fh_ew+edge_width, 2*fw_ew, img_height)).rotate(180))

        return [face0, face1, face2, face3, face4, face5]
        
    def view3d(self, *, edge_width: int = 3, show_axes: bool = False, **kwargs) -> None:
        '''
        Shows a pyvista window of the grid in 3d

        Parameters:
            edge_width (optional int) = 3, width of each edge in pixels
            show_axes (optional bool) = False, whether or not to show the axes on the window
            kwargs any other keyword arguement to pyvista Plotter().show()
        '''
        arrays = self.to_face_arrays(edge_width=edge_width)

        plt = pv.Plotter()

        tex0 = pv.numpy_to_texture(arrays[0])
        face0 = pv.Plane(center=(-.5, 0, 0), direction=(-1, 0, 0))

        tex1 = pv.numpy_to_texture(arrays[1])
        face1 = pv.Plane(center=(0, -.5, 0), direction=(0, -1, 0))

        tex2 = pv.numpy_to_texture(arrays[2])
        face2 = pv.Plane(center=(.5, 0, 0), direction=(1, 0, 0))

        tex3 = pv.numpy_to_texture(arrays[3])
        face3 = pv.Plane(center=(0, .5, 0), direction=(0, 1, 0))

        tex4 = pv.numpy_to_texture(arrays[4])
        face4 = pv.Plane(center=(0, 0, .5), direction=(0, 0, 1))

        tex5 = pv.numpy_to_texture(arrays[5])
        face5 = pv.Plane(center=(0, 0, -.5), direction=(0, 0, -1))

        plt.add_mesh(face0, texture=tex0)
        plt.add_mesh(face1, texture=tex1)
        plt.add_mesh(face2, texture=tex2)
        plt.add_mesh(face3, texture=tex3)
        plt.add_mesh(face4, texture=tex4)
        plt.add_mesh(face5, texture=tex5)
        if show_axes:
            plt.show_axes()
        plt.show(**kwargs)


