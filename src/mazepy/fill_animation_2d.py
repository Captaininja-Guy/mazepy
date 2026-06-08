from mazepy.grids.colored_grid import ColoredGrid
from mazepy.grid_not_supported_exception import GridNotSupportedException
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageDraw, Image
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
        GridNotSupportedException if grid is a weave grid
        TypeError is grid is not a ColoredGrid (or valid subclass)
        RuntimeError if no algorithm has not been applied to the grid

    Returns:
        The animation of the maze being filled
    '''
    if grid.type_of_grid == 'weave':
        raise GridNotSupportedException("Weave grids are not supported")
    if not hasattr(grid, 'base'):
        raise TypeError("Must be a Colored Grid")
    
    if grid.distances is None and (row_start is None or column_start is None):
        if grid.type_of_grid == 'polar':
            grid.distances = grid[0,0].distances()
        else:
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
    

    image = grid.to_png(edge_width=5, bypass_check=True)
    # Since the shapes will intersect the edges, create a mask that will only color the inside of the cell
    if grid.type_of_grid != 'regular':
        image = image.convert("RGBA")
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 255))
        mask = image.convert("L").point(lambda p: 255 if p == 0 else 0)
        
        draw = ImageDraw.Draw(image)
    else:
        image = np.array(image)

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

    match grid.type_of_grid:
        case 'regular':
            def update(frame):
                for row, col in by_dist[frame]:
                    x1 = col * 50 + 5
                    y1 = row * 50 + 5
                    x2 = x1 + 50
                    y2 = y1 + 50
                    
                    image[y1:y2, x1:x2][np.any(image[y1:y2, x1:x2] != 0, axis=-1)] = colors[frame]
            
                im.set_data(image)
                return (im,)
        case 'polar':
            center = (2*grid.rows * 30 + 20 + 1)/2
            def update(frame):
                for row, col in by_dist[frame]:
                    theta = 2*np.pi / len(grid.grid[row])
                    inner_radius = row * 30 
                    outer_radius = inner_radius + 30
                    theta_ccw = col * theta
                    theta_cw = theta_ccw + theta

                    ax = center + int(inner_radius * np.cos(theta_ccw))
                    ay = center + int(inner_radius * np.sin(theta_ccw))
                    bx = center + int(outer_radius * np.cos(theta_ccw))
                    by = center + int(outer_radius * np.sin(theta_ccw))
                    cx = center + int(inner_radius * np.cos(theta_cw))
                    cy = center + int(inner_radius * np.sin(theta_cw))
                    dx = center + int(outer_radius * np.cos(theta_cw))
                    dy = center + int(outer_radius * np.sin(theta_cw))

                    if row == 0:
                        verticies = []
                        for out in grid[0,0].outward:
                            theta_out = 2*np.pi / len(grid.grid[out.row])
                            inner_radius_out = out.row * 30
                            theta_cw_out = (out.column+1) * theta_out

                            x_out = center + int(inner_radius_out * np.cos(theta_cw_out))
                            y_out = center + int(inner_radius_out * np.sin(theta_cw_out))
                            verticies.append((x_out, y_out))

                        draw.polygon(verticies, fill=tuple(colors[frame]))
                    
                    elif len(grid[row, col].outward) == 2:
                        cell_out = grid[row, col].outward[0]
                        theta_out = 2*np.pi/len(grid.grid[cell_out.row])
                        inner_radius_out = cell_out.row * 30
                        theta_cw_out = (cell_out.column+1)*theta_out

                        x_out = center + int(inner_radius_out*np.cos(theta_cw_out))
                        y_out = center + int(inner_radius_out*np.sin(theta_cw_out))

                        draw.polygon([(ax, ay), (bx, by), (x_out, y_out), (dx, dy), (cx, cy)], fill=tuple(colors[frame]))
                    else:
                        draw.polygon([(ax, ay), (bx, by), (dx, dy), (cx, cy)], fill=tuple(colors[frame]))
                    
                image.paste(overlay, (0, 0), mask)
                im.set_data(image)
                return (im,)
        case 'hex':
            b_size = 25*3**.5
            height = 2*b_size
            def update(frame):
                for row, col in by_dist[frame]:
                    cx = 50+75*col
                    cy = b_size + row*height + b_size*(col%2==0)

                    x_fw = int(cx - 43)
                    x_nw = int(cx - 18)
                    x_ne = int(cx + 32)
                    x_fe = int(cx + 57)

                    y_n = int(cy - b_size + 7)
                    y_m = int(cy + 7)
                    y_s = int(cy + b_size + 7)
                    draw.polygon([(x_fw, y_m), (x_nw, y_n), (x_ne, y_n), (x_fe, y_m), (x_ne, y_s), (x_nw, y_s)], fill=tuple(colors[frame]))
                
                image.paste(overlay, (0,0), mask)
                im.set_data(image)
                return (im,)
        case 'triangle':
            height = 25 * 3**.5
            def update(frame):
                for row, col in by_dist[frame]:
                    cx = (1+col)*25
                    cy = (.5+row)*height

                    west_x = int(cx - 18)
                    mid_x = int(cx + 7)
                    east_x = int(cx + 32)

                    apex_y, base_y = (int(cy-height/2+7), int(cy+height/2+7)) if grid[row, col].uprightq() else (int(cy+height/2+7), int(cy-height/2+7))
                    draw.polygon([(west_x, base_y),(mid_x, apex_y),(east_x, base_y)], fill=tuple(colors[frame]))
                image.paste(overlay, (0,0), mask)
                im.set_data(image)
                return (im,)
            

    animation = FuncAnimation(fig=fig, func=update, frames=maximum+1, interval=interval, blit=True)
    if show:
        plt.show()
    return animation