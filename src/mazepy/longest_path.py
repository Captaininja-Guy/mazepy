from mazepy.grids.grid import Grid
from mazepy.distances import Distances


def longest_path(grid: Grid, distances: Distances = None) -> Distances:
    '''
    Computes the longest path in the grid between any two cells
    '''
    if distances is None:
        distances = grid[0,0].distances()
    max_cell, _ = distances.max()
    distances2 = max_cell.distances()
    max_cell2, _ = distances2.max()
    return distances2.path_to(max_cell2)