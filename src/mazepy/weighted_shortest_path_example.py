import mazepy.grids.weighted_grid as WeightedGrid
import mazepy.algorithms.hunt_and_kill as HuntandKill
import random as rand



def weight_grid_ex():
    '''
    Example showing functionality of WeightedGrid
    '''
    grid = WeightedGrid(10, 10)
    HuntandKill(grid)
    grid.braid()

    start, finish = grid[0,0], grid[grid.rows-1, grid.columns-1]


    grid.distances = start.distances().path_to(finish)
    grid.show()


    # Set it to a random cell and it will block a random cell, or chose a cell to block
    lava = rand.choice(list(grid.distances.cells.keys()))
    lava.weight = 500

    grid.distances = start.distances().path_to(finish)
    grid.show()
