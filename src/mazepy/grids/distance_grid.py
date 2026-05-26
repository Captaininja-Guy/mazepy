from ..grids.grid import Grid


class DistanceGrid(Grid):
    '''
    Grid with distances to and from each cell built in, calls the cells 'distances()' method when printing, default is cell [0,0]
    Distances are in base 36 (10 -> A, ... 35 -> Z, .. [36^2-1] 1295 -> ZZ)
    '''
    type_of_grid = 'distance'

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.distances = None

    @staticmethod
    def _to_36(n) -> str:
        if n == 0:
            return ' 0'
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nk = ''
        while n:
            nk += digits[n % 36]
            n //= 36
        number = nk[::-1]
        if len(number) == 1:
            return " " + number
        if len(number) > 2:
            raise OverflowError(f"Distance {number} is too large to be represented in Grid")
        return number

    def contents_of(self, cell) -> str:
        if self.distances and (cell in self.distances):
            return self._to_36(self.distances[cell])
        else:
            return super().contents_of(cell)
