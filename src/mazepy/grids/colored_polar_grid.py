from ..grids.polar_grid import PolarGrid
from ..grids.colored_grid import ColoredGrid

class ColoredPolarGrid(PolarGrid, ColoredGrid):
    '''
    A polar Grid that supports colored cells in its png representation
    '''
    def __init__(self, rows: int, columns: int = None, *, base: tuple[int]|str = (255, 255, 255), 
                 end: tuple[int]|str = (255, 0, 0)):
        '''
            Initializes class atributes

            Parameters:
                rows (int)
                
                columns (optional int) does nothing, just incase you changed from a different grid type and forgot
                base (optional tuple|str) = (255, 255, 255), The *color that the distance 0 cell will be
                end (optional tuple|str) = (255, 0, 0), The *color that the max distance cell will be

                *Must be recognized by PIL/pillow or an RGB tuple
                
            Returns:
                None
            
            Errors:
                TypeError if multiple positional arguements given and rows != columns
                AttributeError is base or end is not a valid color recognized by PIL/pillow
            '''
        if columns is not None and rows != columns:
            raise TypeError('PolarGrid requires rows = columns or 1 positional arguement')
        super().__init__(rows, columns, base=base, end=end)