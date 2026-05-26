from ..grids.weave_grid import WeaveGrid, PreconfiguredWeaveGrid
from ..grids.colored_grid import ColoredGrid

class ColoredWeaveGrid(WeaveGrid, ColoredGrid):
    '''
    A weave Grid that supports colored cells in its png representation
    '''
    def __init__(self, rows: int, columns: int, *, base: tuple[int]|str = (255, 255, 255), 
                 end: tuple[int]|str = (255, 0, 0)):
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
                AttributeError is base or end is not a valid color recognized by PIL/pillow
            '''
        super().__init__(rows, columns, base=base, end=end)

class ColoredPreconfiguredWeaveGrid(PreconfiguredWeaveGrid, ColoredGrid):
    '''
    A preconfigured weave Grid that supports colored cells in its png representation
    '''
    def __init__(self, rows: int, columns: int, *, base: tuple[int]|str = (255, 255, 255), 
                 end: tuple[int]|str = (255, 0, 0)):
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
            AttributeError is base or end is not a valid color recognized by PIL/pillow
        '''
        super().__init__(rows, columns, base=base, end=end)