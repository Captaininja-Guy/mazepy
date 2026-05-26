from mazepy.grids.colored_grid import ColoredGrid
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def play_fill_2d(grid: ColoredGrid, row_start: int|None = None, column_start: int|None = None, *, 
                show: bool = True, interval: int = 200) -> FuncAnimation:
    '''
    Creates an animation of a given grid filling up with a color gradient

    Parameters:
        grid (ColoredGrid)
        row_start (optional int) = row of the starting cell
        column_start (optional int) = column of the starting cell

        show (optional bool) = True, whether to the animation after creating it
        interval (optional int) = 200, milisecond interval between frames

    Errors:
        RuntimeError if grid is not rectangular
        RuntimeError if no algorithm has not been applied to the grid

    Returns:
        The animation of the maze being filled
    '''
    if grid.type_of_grid != 'regular':
        raise RuntimeError("Only rectangular grids are supported in animations")
    
    if grid.distances is None and (row_start is None or column_start is None):
        grid.distances = grid[grid.rows//2, grid.columns//2].distances()
    elif grid.distances is None:
        grid.distances = grid[row_start, column_start].distances()


    distances = {cell: dist for cell, dist in sorted(grid._distances.cells.items(), key=lambda x: x[1])}
    maximum = grid.maximum
    if maximum == 0:
        raise RuntimeError("Algorithm has not been applied to grid")
    del grid._distances
    del grid.maximum


    base = ColoredGrid.color_to_RGB(grid.base)
    end = ColoredGrid.color_to_RGB(grid.end)
    colors = np.array([ColoredGrid.interoplate(base, end, i/maximum) for i in range(maximum+1)], dtype=np.uint8)
    

    image = np.array(grid.to_png(edge_width=5, bypass_check=True))
    fig, ax = plt.subplots()
    im = ax.imshow(image)
    ax.axis('off')


    paused = False
    def toggle_pause(*args):
        nonlocal paused
        if paused:
            animation.resume()
        else:
            animation.pause()
        paused = not paused
    fig.canvas.mpl_connect('button_press_event', toggle_pause)


    by_dist = [[] for _ in range(maximum + 1)]
    for cell, dist in distances.items():
        by_dist[dist].append((cell.row, cell.column))


    def update(frame):
        for row, col in by_dist[frame]:
            x1 = col * 50 + 5
            y1 = row * 50 + 5
            x2 = x1 + 50
            y2 = y1 + 50
            
            image[y1:y2, x1:x2][np.any(image[y1:y2, x1:x2] != 0, axis=-1)] = colors[frame]
    
        im.set_data(image)
        return (im,)
    

    animation = FuncAnimation(fig=fig, func=update, frames=maximum+1, interval=interval, blit=True)
    if show:
        plt.show()
    return animation

