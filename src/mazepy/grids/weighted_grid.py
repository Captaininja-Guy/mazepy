from ..cells.weighted_cell import WeightedCell
from ..grids.grid import Grid

class WeightedGrid(Grid):
    '''
    Grid with weights for cells instead of normal colors, see weight_grid_ex for use case
    '''
    type_of_grid = 'weighted'

    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns)
        self._distances = None
        self.maximum = None

    def prepare_grid(self):
        return [[WeightedCell(row, column) for column in range(self.columns)] for row in range(self.rows)]
    
    @property
    def distances(self):
        return self._distances
    
    @distances.setter
    def distances(self, distances):
        self._distances = distances
        _, self.maximum = distances.max()

    def background_color_for(self, cell: WeightedCell) -> tuple[int] | None:
        if cell.weight > 1:
            return (255, 0, 0)
        elif self.distances:
            distance = self.distances[cell]
            if distance is None:
                return None
            intensity = int(64 + 191*(self.maximum - distance)/self.maximum)
            return (intensity, intensity, 0)
        return None
