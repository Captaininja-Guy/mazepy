from ..grids.grid import Grid
from PIL import Image, ImageColor
from ..distances import Distances
from ..cells.cell import Cell


class ColoredGrid(Grid):
    '''
    A rectangular Grid that supports colored cells in its png representation
    '''
    def __init__(self, rows: int, columns: int, *, base: tuple[int]|str = (255, 255, 255), end: tuple[int]|str = (255, 0, 0), **kwargs):
        '''
        Initializes class atributes

        Parameters:
            rows (int)
            columns (int)
            
            base (optional tuple|str) = (255, 255, 255), The *color that the distance 0 cell will be
            end (optional tuple|str) = (255, 0, 0), The *color that the max distance cell will be

            *Must be recognized by PIL/pillow or an RGB tuple
            
        Returns:
            None
        
        Errors:
            AttributeError if base or end is not a valid color recognized by PIL/pillow
        '''
        # Valid Color Checking
        try:
            Image.new("RGB", (1, 1), base)
        except ValueError:
            raise AttributeError("Not a valid base")
        try:
            Image.new("RGB", (1, 1), end)
        except ValueError:
            raise AttributeError("Not a valid end")
        
        super().__init__(rows, columns)
        self.end = end
        self.base = base
        self._distances = None
        self.maximum = None
        
    @property
    def distances(self):
        return self._distances

    @distances.setter
    def distances(self, distances: Distances):
        self._distances = distances
        _, self.maximum = distances.max()
    
    @staticmethod
    def interoplate(start: tuple[int], end: tuple[int], proportion: float) -> tuple[int]:
        return tuple([round(b*(1-proportion) + c*proportion) for b,c in zip(start, end)])

    @staticmethod
    def color_to_RGB(color: tuple[int] | str) -> tuple[int]:
        if not isinstance(color, tuple):
            return ImageColor.getrgb(color)
        else:
            return color

    def background_color_for(self, cell: Cell) -> tuple[int]:
        if self.distances is None or cell not in self.distances:
            return None
        
        # Converting from Hex/word -> RGB
        end = ColoredGrid.color_to_RGB(self.end)
        base = ColoredGrid.color_to_RGB(self.base)
        
        prop = self.distances[cell] / self.maximum
        return ColoredGrid.interoplate(base, end, prop)