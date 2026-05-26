import random as rand
from typing import Self
from PIL import Image
import numpy as np

class Mask():
    '''
    Which cells are too be omitted in a MaskedGrid
    '''
    def __init__(self, rows: int, columns: int):
        self.rows, self.columns = rows, columns
        self.bits = [[True] * columns for _ in range(rows)]
    
    @staticmethod
    def from_file(path_name: str) -> Self:
        '''
        Reads fils and creates mask from ASCII art inside it

        Parameters:
            path_name (str) path name
        '''
        with open(path_name, 'r') as file:
            lines = [line.rstrip() for line in file]
            return Mask.from_ASCII(lines)

    @staticmethod
    def from_input() -> Self:
        '''
        Creates mask from ASCII art inputed
        '''
        line = input('Type ASCII representation of Mask, q is quit, x is mask cell\n')
        lines = [line]
        while line.lower() != 'q':
            line = input()
            lines.append(line)
        lines.pop()
        return Mask.from_ASCII(lines)

    @staticmethod
    def from_ASCII(lines: list[str]) -> Self:
        '''
        Created mask from given ASCII art, x is mask cell

        Parameters:
            lines (list[str]) ASCII art to make mask from
        '''
        rows = len(lines)
        columns = len(lines[0])
        mask = Mask(rows, columns)

        for row in range(mask.rows):
            for column in range(mask.columns):
                if lines[row][column].lower() == 'x':
                    mask[row, column] = False
        
        return mask

    @staticmethod
    def from_png(path_name: str) -> Self:
        '''
        Creates mask from png inputed, black is mask cell

        Parameters:
            path_name (str) path name
        '''
        image = Image.open(path_name).convert('1')
        return np.array(image)

    def __getitem__(self, position: tuple[int]):
        row, col = position
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.bits[row][col]
        else:
            return False
        
    def __setitem__(self, position: tuple[int], is_on: bool):
        row, col = position
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.bits[row][col] = is_on
            pass
        else:
            raise IndexError("Index out of range")
    
    def count(self) -> int:
        count = 0

        for row in range(self.rows):
            for col in range(self.columns):
                count += 1 if self.bits[row][col] else 0
        return count
    
    def random_location(self) -> bool:
        while True:
            row = rand.randrange(self.rows)
            col = rand.randrange(self.columns)
            if self.bits[row][col]:
                return [row, col]

