from mazepy.grids.grid import Grid
from mazepy.algorithms.binary_tree import BinaryTree
from mazepy.algorithms.sidewinder import Sidewinder
from mazepy.algorithms.aldous_broder import AldousBroder
from mazepy.algorithms.wilsons import Wilsons
from mazepy.algorithms.hunt_and_kill import HuntandKill
from mazepy.algorithms.recursive_backtrack import RecursiveBacktrack
from mazepy.algorithms.origin_shift import OriginShift
from mazepy.algorithms.kruskals import Kruskals
from mazepy.algorithms.prims import SimplifiedPrims, TruePrims, ModifiedPrims
from mazepy.algorithms.ellers import Ellers
from mazepy.algorithms.recursive_division import RecursiveDivision

from math import log10
from typing import Callable

def Deadends(algorithms: list[Callable], tries: int = 100, size: int = 20) -> None:
    '''
    Prints the average number of deadends in a maze from each algorithm

    Parameters:
        algorithms (list[Callable]) algorithms to use
        tries (optional int) = 100, number of mazes to make for each algorithm
        size (optionla int) = 20, size of each maze

    Returns:
        None, output is printed
    '''
    averages = {}

    # Calculating dead-ends in each algorithm
    for algorithm in algorithms:
        print(f'Running {algorithm.__name__}...')
        deadend_counts = []
        for _ in range(tries):
            grid = Grid(size, size)
            algorithm(grid)
            deadend_counts.append(len(grid.deadends()))
        averages[algorithm] = round(sum(deadend_counts) / len(deadend_counts))

    print(f"\n\nAverage dead-ends per {size}x{size} maze ({size**2} cells):\n")

    # Getting the longest number of digits in the number of deadends for formatting
    longest_digits = 0
    for value in averages.values():
        a = int(log10(value))+1
        if a > longest_digits:
            longest_digits = a

    # Sorting the algorithms by number of dead-ends
    sorted_algorithms = sorted(algorithms, key=lambda x: averages[x], reverse=True)

    longest_name = 0
    for algorithm in algorithms:
        longest_name = max(longest_name, len(algorithm.__name__))

    for algorithm in sorted_algorithms:
        # Calculating percentage of dead-ends
        percentage = round(averages[algorithm] * 100 / (size**2))

        # Formatting output
        space = " " * (longest_name - len(algorithm.__name__))
        space2 = " " * (3 - (int(log10(averages[algorithm]))))
        space3 = " " if int(log10(percentage)) > 0 else ""

        print(f'{space}{algorithm.__name__} : {space2}{averages[algorithm]}/{size**2} {space3}({percentage}%)')

if __name__ == '__main__':
    algorithms = [BinaryTree, Sidewinder, AldousBroder, Wilsons, HuntandKill, OriginShift, 
                  RecursiveBacktrack, Kruskals, SimplifiedPrims, TruePrims, ModifiedPrims, Ellers, RecursiveDivision]
    
    Deadends(algorithms)