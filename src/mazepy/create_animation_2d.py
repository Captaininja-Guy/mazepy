import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as rand
from mazepy.grids.grid import Grid
from mazepy.algorithms.kruskals import State
from mazepy.algorithms.ellers import _RowState
from typing import Callable


def play_create_2d(algorithm: str, size: int = 10, interval: int = 200, *, show: bool = True, 
              growing_tree_func: Callable = lambda x: rand.choice(x), origin_shift_times: int = 200) -> animation.FuncAnimation:
    '''
    Creates an animation of a square maze being created

    Parameters:
        algorithm (str) algorithm to show
        size (optional int) = 10, size of maze
        interval (opitonal int) = 200, ms interval for matplotlib animation frames

        show (optional bool) = True, wether to show animation after making it
        growing_tree_func (optional Callable) = lambda x: rand.choice(x), function used for GrowingTree
        origin_shift_times (optional int) = 200, times OriginShift shifts origin

    Returns:
        The animation of the maze being created

    Errors:
        TypeError if algorithm.lower() is not in this list:
        [binarytree, sidewinder, aldousbroder, wilsons, recursivebacktrack, huntandkill, kruskals, simplifiedprims,
        trueprims, modifiedprims, growingtree, ellers, originshift, recursivedivision]

    '''
    algorithms = {'binarytree': _play_BinaryTree2d, 'sidewinder': _play_Sidewinder2d, 'aldousbroder': _play_AldousBroder2d,
                  'wilsons': _play_Wilsons2d, 'recursivebacktrack': _play_RecursiveBacktrack2d, 'huntandkill': _play_HuntandKill2d,
                  'kruskals': _play_Kruskals2d, 'simplifiedprims': _play_SimplifiedPrims2d, 
                  'trueprims': _play_TruePrims2d, 'modifiedprims': _play_ModifiedPrims2d, 'growingtree': _play_GrowingTree2d,
                  'ellers': _play_Ellers2d, 'originshift': _play_OriginShift2d, 'recursivedivision': _play_RecursiveDivision2d}
    
    function = algorithms.get(algorithm.lower())
    if function is None:
        raise TypeError('Algorithm Unknown')
    
    anim = function(algorithm, size, show, interval, growing_tree_func, origin_shift_times)
    
    return anim

def _prepare_animation(function):
    def wrapper(*args):
        algorithm, size, show, interval, growing_tree_func, origin_shift_times = args

        grid = Grid(size, size)
        
        if algorithm.lower() == 'originshift':
            for cell in grid.each_cell():
                if cell.row == grid.rows-1:
                    if cell.east:
                        cell.link(cell.east, bidi=False)
                else:
                    cell.link(cell.south, bidi=False)

        if algorithm.lower() == 'recursivedivision':
            grid.clear()

        image = np.array(grid.to_png())
        fig, ax = plt.subplots()
        img = ax.imshow(image)
        ax.axis('off')
        
        def update(frame, *args):
            return function(frame, *args)
        
        paused = False
        def toggle_pause(*args):
            nonlocal paused
            if paused:
                animation.resume()
            else:
                animation.pause()
            paused = not paused
        fig.canvas.mpl_connect('button_press_event', toggle_pause)


        match algorithm.lower():
            case 'binarytree':
                done = [False]
                animation = _bintree_anim(fig, update, grid, image, img, interval, done)
            case 'sidewinder':
                run = []
                animation = _sidewinder_anim(fig, update, grid, image, img, run, interval)
            case 'aldousbroder':
                before_cell = []
                unvisited = [grid.size - 1]
                animation = _ab_anim(fig, update, grid, image, img, before_cell, unvisited, interval)
            case 'wilsons':
                path = ['start']
                unvisited = [cell for cell in grid.each_cell()]
                animation = _wilsons_anim(fig, update, image, img, path, unvisited, interval)
            case 'recursivebacktrack':
                stack = ['start']
                animation = _recurback_anim(fig, update, grid, image, img, stack, interval)
            case 'huntandkill':
                mode = ['kill']
                animation = _hak_anim(fig, update, grid, image, img, mode, interval)
            case 'kruskals':
                state = State(grid)
                animation = _kruskals_anim(fig, update, image, img, state, interval)
            case 'simplifiedprims':
                active = [grid.random_cell()]
                animation = _simplifiedprims_anim(fig, update, image, img, active, interval)
            case 'trueprims':
                active = [grid.random_cell()]
                costs = {}
                for cell in grid.each_cell(): costs[cell] = rand.randint(1,100)
                animation = _trueprims_anim(fig, update, image, img, active, costs, interval)
            case 'modifiedprims':
                _in = [grid.random_cell()]
                frontier = _in[0].neighbors()
                out = []
                for cell in grid.each_cell():
                    if cell not in _in and cell not in frontier:
                        out.append(cell)
                animation = _modifiedprims_anim(fig, update, image, img, _in, frontier, out, interval)
            case 'growingtree':
                active = [grid.random_cell()]
                animation = _growingtree_anim(fig, update, image, img, growing_tree_func, active, interval)
            case 'ellers':
                state = [_RowState()]
                animation = _ellers_anim(fig, update, grid, image, img, state, interval)
            case 'originshift':
                root = [grid[grid.rows-1, grid.columns-1]]
                animation = _originshift_anim(fig, update, origin_shift_times, grid, image, img, root, interval)
            case 'recursivedivision':
                region = [(0, 0, grid.rows, grid.columns)]
                animation = _recursivedivision_anim(fig, update, region, grid, image, img, interval)

        if show:
            plt.show()
        return animation

    
    return wrapper

# region image changing

def color_in_cell(cell, image, color: tuple|int, *args):
    x1 = cell.column * 50 + 5
    y1 = cell.row * 50 + 5
    x2 = x1 + 50
    y2 = y1 + 50
    image[y1+1:y2-1, x1+2:x2-1][np.any(image[y1+1:y2-1, x1+2:x2-1] != 0)] = color

def clear_north_wall(cell, image, *args):
    x1 = cell.column * 50 + 5
    y1 = cell.row * 50 + 5
    x2 = x1 + 50
    if args and args[0] == 'add':
        image[y1-1:y1+2, x1:x2,:] = (0, 0, 0)
    else:
        image[y1-1:y1+2, x1+2:x2-1,:] = (255, 255, 255)

def clear_east_wall(cell, image, *args):
    y1 = cell.row * 50 + 5
    x2 = cell.column * 50 + 55
    y2 = y1 + 50
    if args and args[0] == 'Kruskals':
        y1 += 1
    if args and args[0] == 'add':
        image[y1-1:y2-1, x2-1:x2+2,:] = (0, 0, 0)
    else:
        image[y1+1:y2-1, x2-1:x2+2,:] = (255, 255, 255)

def clear_south_wall(cell, image, *args):
    x1 = cell.column * 50 + 5
    x2 = x1 + 50
    y2 = cell.row * 50 + 55
    if args and args[0] == 'add':
        image[y2-1:y2+2, x1:x2,:] = (0, 0, 0)
    else:
        image[y2-1:y2+2, x1+2:x2-1,:] = (255, 255, 255)

def clear_west_wall(cell, image, *args):
    x1 = cell.column * 50 + 5
    y1 = cell.row * 50 + 5
    y2 = y1 + 50
    if args and (args[0] == 'Kruskals' or args[0] == 'Ellers') :
        y1 += 1
    if args and args[0] == 'add':
        image[y1-1:y2-1, x1-1:x1+2,:] = (0, 0, 0)
    else:
        image[y1+1:y2-1, x1-1:x1+2,:] = (255, 255, 255)

def clear_wall(match_cell, case_cell, image, *args):
    if args: args = args[0]
    match match_cell:
        case case_cell.north:
            clear_north_wall(case_cell, image, args)
        case case_cell.south:
            clear_south_wall(case_cell, image, args)
        case case_cell.east:
            clear_east_wall(case_cell, image, args)
        case case_cell.west:
            clear_west_wall(case_cell, image, args)

def add_arrow(cell, image, direction):
    x1 = cell.column * 50 + 5
    y1 = cell.row * 50 + 5
    match direction:
        case 'left':
            x1 += 11
            y1 += 24
            image[y1, x1:x1+26, :] = (0, 0, 0)
            for i in range(1, 6):
                x1 += 1
                for sign in 1,-1:
                    y2 = y1 + sign*i
                    image[y2, x1:x1+2, :] = (0, 0, 0)
                    if i == 5:
                        image[y2+sign, x1+1, :] = (0, 0, 0)
        case 'right':
            x1 += 11
            y1 += 24
            image[y1, x1:x1+26, :] = (0, 0, 0)
            x1 += 25
            for i in range(1, 6):
                x1 -= 1
                for sign in 1,-1:
                    y2 = y1 + sign*i
                    image[y2, x1-1:x1+1, :] = (0, 0, 0)
                    if i == 5:
                        image[y2+sign, x1-1, :] = (0, 0, 0)
        case 'up':
            x1 += 24
            y1 += 11
            image[y1:y1+26, x1, :] = (0, 0, 0)
            for i in range(1, 6):
                y1 += 1
                for sign in 1,-1:
                    x2 = x1 + sign*i
                    image[y1:y1+2, x2, :] = (0, 0, 0)
                    if i == 5:
                        image[y1+1, x2+sign, :] = (0, 0, 0)
        case 'down':
            x1 += 24
            y1 += 11
            image[y1:y1+26, x1, :] = (0, 0, 0)
            y1 += 25
            for i in range(1, 6):
                y1 -= 1
                for sign in 1,-1:
                    x2 = x1 + sign*i
                    image[y1-1:y1+1, x2, :] = (0, 0, 0)
                    if i == 5:
                        image[y1-1, x2+sign, :] = (0, 0, 0)

# endregion

# region Binary Tree
@_prepare_animation
def _play_BinaryTree2d(frame, *args):
    grid, image, img, done = args
    if not done[0]:
        grid_size = grid.rows
        cell = grid[divmod(frame, grid_size)]

        if (rand.randrange(2) == 0 or cell.column == grid_size-1) and cell.row != 0:
            clear_north_wall(cell, image)
        elif cell.column != grid.columns - 1:
            clear_east_wall(cell, image)
        
        if cell.row == grid.rows-1 and cell.column == grid.columns-1:
            done[0] = True

    img.set_data(image)
    return (img,)

def _bintree_anim(fig, update, grid, image, img, interval, done):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, 
                                   fargs=(grid, image, img, done), interval=interval, blit=True)

#endregion

# region Sidewinder
@_prepare_animation
def _play_Sidewinder2d(frame, *args):
    grid, image, img, run = args
    if run and run[0] == 'done':
        return (img,)
    grid_size = grid.rows
    cell = grid[divmod(frame, grid_size)]
    
    run.append(cell)
    should_close_out = (cell.column == grid_size-1) or (not cell.row == 0 and rand.randrange(2) == 0)
    
    if should_close_out:
        member = rand.choice(run)
        if member.north:
            clear_north_wall(member, image)
        run.clear()
    else:
        clear_east_wall(cell, image)
    
    if cell.row == grid.rows-1 and cell.column == grid.columns-1:
        run.append('done')
    
    img.set_data(image)
    return (img,)

def _sidewinder_anim(fig, update, grid, image, img, run, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, fargs=(grid, image, img, run), interval=interval, blit=True)

# endregion

# region Aldous Broder
@_prepare_animation
def _play_AldousBroder2d(frame, *args):
    grid, image, img, before_cell, unvisited = args
    if unvisited[0] != 'done':
        if unvisited[0] == 0:
            prev_cell = before_cell.pop(0)

            color_in_cell(prev_cell, image, 255)
            img.set_data(image)
            unvisited[0] = 'done'
            return (img,)

        if not before_cell:
            cell = grid.random_cell()
        else:
            prev_cell = before_cell.pop(0)

            color_in_cell(prev_cell, image, 255)

            cell = rand.choice(prev_cell.neighbors())
            if not cell.links():
                cell.link(prev_cell)
                unvisited[0] -= 1
                clear_wall(cell, prev_cell, image)

        color_in_cell(cell, image, (100, 251, 0))
        before_cell.append(cell)

    
    
    img.set_data(image)
    return (img,)
    
def _ab_anim(fig, update, grid, image, img, prev_cell, unvisited, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, 
                         fargs=(grid, image, img, prev_cell, unvisited), interval=interval, blit=True)

# endregion

# region Wilsons
@_prepare_animation
def _play_Wilsons2d(frame, *args):
    image, img, path, unvisited = args
    if not unvisited:
        return (img,)
    
    if path and path[0] == 'start':
        first = rand.choice(unvisited)
        unvisited.remove(first)
        color_in_cell(first, image, (83, 173, 91))
        path.pop()
    
    if not path:
        cell = rand.choice(unvisited)
        path.append(cell)
        color_in_cell(cell, image, (222, 162, 22))
    else:
        cell = path[-1]
        if cell in unvisited:
            neighbor = rand.choice(cell.neighbors())
            try:
                position = path.index(neighbor)
            except ValueError:
                position = None
            
            if position is not None:
                for _ in range(position+1, len(path)):
                    bad_cell = path.pop()
                    color_in_cell(bad_cell, image, 255)
            else:
                path.append(neighbor)
                color_in_cell(neighbor, image, (242, 181, 39))
                color_in_cell(cell, image, (134, 145, 132))

        else:
            while path:
                cell_to_fill = path.pop()
                if cell_to_fill != cell:
                    unvisited.remove(cell_to_fill)
                if path:
                    cell_to_fill.link(path[-1])
                    clear_wall(path[-1], cell_to_fill, image)

                color_in_cell(cell_to_fill, image, 255)
    
    img.set_data(image)
    return (img,)

def _wilsons_anim(fig, update, image, img, path, unvisited, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50, 
                         fargs=(image, img, path, unvisited), interval=interval, blit=True)

# endregion

# region RecursiveBacktrack
@_prepare_animation
def _play_RecursiveBacktrack2d(frame, *args):
    grid, image, img, stack = args
    if stack:
        append_cell = True
        if stack[0] == 'start':
            stack.pop()
            cell = grid.random_cell()
        else:
            prev_cell = stack[-1]
            color_in_cell(prev_cell, image, 255)

            unvisited_neighbors = [cell for cell in prev_cell.neighbors() if not cell.links()]
            if unvisited_neighbors:
                cell = rand.choice(unvisited_neighbors)
                cell.link(prev_cell)
                clear_wall(cell, prev_cell, image)
            else:
                stack.pop(-1)
                if len(stack) == 0:
                    color_in_cell(prev_cell, image, 255)
                    img.set_data(image)
                    return (img,)
                cell = stack[-1]
                append_cell = False


        color_in_cell(cell, image, (100, 251, 0))
        if append_cell:
            stack.append(cell)

        img.set_data(image)
    return (img,)

def _recurback_anim(fig, update, grid, image, img, stack, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, 
                                   fargs=(grid, image, img, stack), interval=interval, blit=True)

# endregion

# region Hunt and Kill
@_prepare_animation
def _play_HuntandKill2d(frame, *args):
    grid, image, img, mode = args

    if mode[0] == 'done':
        return (img,)
    if mode[0] == 'kill' and len(mode) == 1:
        cell = grid.random_cell()
        color_in_cell(cell, image, (83, 173, 91))
        mode.append(cell)
    elif mode[0] == 'kill':
        prev_cell = mode[1]
        if len(mode) == 3:
            mode.pop()
            for cell in grid.grid[prev_cell.row]:
                if cell is not prev_cell:
                    color_in_cell(cell, image, 255)
            for neighbor in prev_cell.neighbors():
                if neighbor.links():
                    neighbor.link(prev_cell)
                    clear_wall(neighbor, prev_cell, image)
                    break
        else:
            color_in_cell(prev_cell, image, 255)
            free_neighbors = [cell for cell in prev_cell.neighbors() if not cell.links()]
            if free_neighbors:
                cell = rand.choice(free_neighbors)
                color_in_cell(cell, image, (83, 173, 91))
                cell.link(prev_cell)
                clear_wall(cell, prev_cell, image)
                
                mode[1] = cell
            else:
                mode[0] = 'hunt'
                mode[1] = 0
    else:
        row = mode[1]
        found = None
        for cell in sorted(grid.grid[row], key=lambda cell: cell.column):
            color_in_cell(cell, image, (83, 173, 91))
            visited_neighbors = list(filter(lambda cell: cell.links(), cell.neighbors()))
            if found is None and not cell.links() and visited_neighbors:
                found = cell
        
        if row != 0:
            for cell in grid.grid[row-1]:
                color_in_cell(cell, image, 255)

        if found is not None:
            mode[0] = 'kill'
            mode[1] = found
            mode.append('hunted')
        else:
            mode[1] += 1
            if mode[1] == grid.rows:
                for cell in grid.grid[row]:
                    color_in_cell(cell, image, 255)
                mode[0] = 'done'

    img.set_data(image)
    return (img,)

def _hak_anim(fig, update, grid, image, img, mode, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, 
                                   fargs=(grid, image, img, mode), interval=interval, blit=True)

# endregion

# region Kruskals
@_prepare_animation
def _play_Kruskals2d(frame, *args):
    image, img, state = args
    neighbors = state.neighbors
    
    if frame == 0:
        rand.shuffle(neighbors)

    if not neighbors:
        return (img,)
    
    left, right = neighbors.pop()
    while not state.can_merge(left, right):
        if neighbors:
            left, right = neighbors.pop()
        else:
            return (img,)

    state.merge(left, right)
    clear_wall(right, left, image, 'Kruskals')

    img.set_data(image)
    return (img,)

def _kruskals_anim(fig, update, image, img, state, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50, 
                         fargs=(image, img, state), interval=interval, blit=True)

# endregion

# region Simplified Prims
@_prepare_animation
def _play_SimplifiedPrims2d(frame, *args):
    image, img, active = args
    if not active:
        return (img,)
    
    cell = rand.choice(active)
    availible_neighbors = [c for c in cell.neighbors() if not c.links()]

    if availible_neighbors:
        neighbor = rand.choice(availible_neighbors)
        cell.link(neighbor)
        active.append(neighbor)
        if len(availible_neighbors) == 1:
            color_in_cell(cell, image, 255)
        
        color_in_cell(neighbor, image, (83, 173, 91))

        clear_wall(neighbor, cell, image)
    else:
        active.remove(cell)
        color_in_cell(cell, image, 255)
    
    
    img.set_data(image)
    return (img,)

def _simplifiedprims_anim(fig, update, image, img, active, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50, 
                                   fargs=(image, img, active), interval=interval, blit=True)

# endregion

# region True Prims
@_prepare_animation
def _play_TruePrims2d(frame, *args):
    image, img, active, costs = args

    if not active:
        return (img,)
    
    cell = min(active, key=lambda x: costs[x])
    color_in_cell(cell, image, (83, 173, 91))

    availible_neighbors = [c for c in cell.neighbors() if not c.links()]

    if availible_neighbors:
        neighbor = min(availible_neighbors, key=lambda x: costs[x])
        cell.link(neighbor)
        active.append(neighbor)
        if len(availible_neighbors) == 1:
            color_in_cell(cell, image, 255)

        clear_wall(neighbor, cell, image)
    else:
        active.remove(cell)
        color_in_cell(cell, image, 255)

    for loop_cell in active:
        if loop_cell is not cell:
            color_in_cell(loop_cell, image, 255)
    
    img.set_data(image)
    return (img,)

def _trueprims_anim(fig, update, image, img, active, costs, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50, 
                                   fargs=(image, img, active, costs), interval=interval, blit=True)

# endregion

# region Modified Prims
@_prepare_animation
def _play_ModifiedPrims2d(frame, *args):
    image, img, _in, frontier, out = args
    if not frontier:
        return (img,)
    
    cell = rand.choice(frontier)
    _in.append(cell)
    frontier.remove(cell)
    color_in_cell(cell, image, 255)
    linked_flag = False
    neighbors = cell.neighbors()
    rand.shuffle(neighbors)

    for neighbor_cell in neighbors:
        if neighbor_cell in _in and not linked_flag:
            cell.link(neighbor_cell)
            linked_flag = True
            clear_wall(neighbor_cell, cell, image)
        if neighbor_cell in out:
            out.remove(neighbor_cell)
            frontier.append(neighbor_cell)
            color_in_cell(neighbor_cell, image, (83, 173, 91))
    
    img.set_data(image)
    return (img,)

def _modifiedprims_anim(fig, update, image, img, _in, frontier, out, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50,
                                   fargs=(image, img, _in, frontier, out), interval=interval, blit=True)

# endregion

# region Growing Tree
@_prepare_animation
def _play_GrowingTree2d(frame, *args):
    image, img, func, active = args
    if not active:
        return (img,)
    
    cell = func(active)
    availible_neighbors = [c for c in cell.neighbors() if not c.links()]

    if availible_neighbors:
        neighbor = rand.choice(availible_neighbors)
        cell.link(neighbor)
        clear_wall(cell, neighbor, image)
        active.append(neighbor)
        color_in_cell(neighbor, image, (83, 173, 91))
        if len(availible_neighbors) == 1:
            color_in_cell(cell, image, 255)
    else:
        active.remove(cell)
        color_in_cell(cell, image, 255)
    
    img.set_data(image)
    return (img,)

def _growingtree_anim(fig, update, image, img, func, active, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=image.shape[0]//50, 
                                   fargs=(image, img, func, active), interval=interval, blit=True)

# endregion

# region Ellers
@_prepare_animation
def _play_Ellers2d(frame, *args):
    grid, image, img, state = args
    row_state = state[0]

    if state[0] == 'done':
        return (img,)
    
    coords = divmod(frame, grid.rows)
    cell = grid[coords]
    if not cell.west:
        return (img,)
    
    _set = row_state.set_for(cell)
    prior_set = row_state.set_for(cell.west)

    if _set != prior_set and (cell.south is None or rand.randrange(2) == 0):
        cell.link(cell.west)
        clear_west_wall(cell, image, 'Ellers')
        row_state.merge(prior_set, _set)
    
    if coords[1] == grid.columns-1 and cell.south:
        next_row = row_state._next()
        for _, _list in row_state.each_set():
                list2 = _list.copy()
                rand.shuffle(list2)
                for index, cell in enumerate(list2):
                    if index == 0 or rand.randrange(3) == 0:
                        cell.link(cell.south)
                        clear_south_wall(cell, image)
                        next_row.record(row_state.set_for(cell), cell.south)
        
        state[0] = next_row
    
    if coords[1] == grid.columns-1 and not cell.south:
        state[0] = 'done'

    img.set_data(image)
    return (img,)
    
def _ellers_anim(fig, update, grid, image, img, state, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, 
                                   fargs=(grid, image, img, state), interval=interval, blit=True)

# endregion

# region Origin Shift
@_prepare_animation
def _play_OriginShift2d(frame, *args):
    grid, image, img, root_list = args

    if frame == 0:
        for cell in grid.each_cell():
            if cell.row != grid.rows-1:
                add_arrow(cell, image, 'down')
            elif cell.column != grid.columns-1:
                add_arrow(cell, image, 'left')
            else:
                color_in_cell(cell, image, (83, 173, 91))
        
        img.set_data(image)
        return (img,)

    root = root_list[0]
    _next = rand.choice(root.neighbors())
    root_list[0] = _next

    if _next.linkedq(root):
        _next.unlink(root, bidi=False)
        root.link(_next, bidi=False)
    else:
        root.link(_next, bidi=False)
        clear_wall(root, _next, image)
        bad_cell = _next.links()[0]
        _next._links.clear()
        clear_wall(_next, bad_cell, image, 'add')
    
    color_in_cell(root, image, 255)
    match _next:
        case root.north:
            add_arrow(root, image, 'up')
        case root.south:
            add_arrow(root, image, 'down')
        case root.east:
            add_arrow(root, image, 'right')
        case root.west:
            add_arrow(root, image, 'left')
    color_in_cell(_next, image, (83, 173, 91))

    img.set_data(image)
    return (img,)

def _originshift_anim(fig, update, times, grid, image, img, root, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=times+1, fargs=(grid, image, img, root), 
                                   interval=interval, blit=True, repeat=False)

# endregion

# region Recursive Division
@_prepare_animation
def _play_RecursiveDivision2d(frame, *args):
    region, grid, image, img = args

    if region[0] == 'done':
        return (img,)
    
    while region[-1][2] <= 1 or region[-1][3] <= 1:
        region.pop()
        if not region:
            region.append('done')
            return (img,)
    
    row, column, height, width = region[-1]

    if height > width or height == width and rand.randrange(2) == 0: # Horizontal
        divide_south_of = rand.randrange(height-1)
        passage_at = rand.randrange(width)

        for x in range(width):
            if x == passage_at: continue
            cell = grid[row+divide_south_of, column+x]
            clear_south_wall(cell, image, 'add')
        
        region.pop()
        region.append((row, column, divide_south_of+1, width))
        region.append((row+divide_south_of+1, column, height-(divide_south_of+1), width))

    else: # Vertical
        divide_east_of = rand.randrange(width-1)
        passage_at = rand.randrange(height)

        for y in range(height):
            if y == passage_at: continue
            cell = grid[row+y, column+divide_east_of]
            clear_east_wall(cell, image, 'add')
        
        region.pop()

        region.append((row, column, height, divide_east_of+1))
        region.append((row, column+divide_east_of+1, height, width-(divide_east_of+1)))


    img.set_data(image)
    return (img,)


def _recursivedivision_anim(fig, update, region, grid, image, img, interval):
    return animation.FuncAnimation(fig=fig, func=update, frames=grid.size, fargs=(region, grid, image, img), 
                                   interval=interval, blit=True)

# endregion
