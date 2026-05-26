from ..cells.cell import Cell
from ..grids.grid import Grid

class OverCell(Cell):
    def __init__(self, row: int, column: int, grid: Grid):
        super().__init__(row, column)
        self.grid = grid
    
    def neighbors(self):
        l = super().neighbors()
        if self.can_tunnel_northq(): l.append(self.north.north)    
        if self.can_tunnel_southq(): l.append(self.south.south)
        if self.can_tunnel_eastq(): l.append(self.east.east)
        if self.can_tunnel_westq(): l.append(self.west.west)
        return l
    
    def can_tunnel_northq(self) -> bool:
        return self.north and self.north.north and self.north.horizontal_passageq()
    
    def can_tunnel_southq(self) -> bool:
        return self.south and self.south.south and self.south.horizontal_passageq()
    
    def can_tunnel_eastq(self) -> bool:
        return self.east and self.east.east and self.east.vertical_passageq()
    
    def can_tunnel_westq(self) -> bool:
        return self.west and self.west.west and self.west.vertical_passageq()
    
    def horizontal_passageq(self) -> bool:
        return self.linkedq(self.east) and self.linkedq(self.west) and not (self.linkedq(self.north) or self.linkedq(self.south))
    
    def vertical_passageq(self) -> bool:
        return self.linkedq(self.north) and self.linkedq(self.south) and not (self.linkedq(self.east) or self.linkedq(self.west))
    
    def link(self, cell, bidi: bool = True) -> None:
        neighbor = None
        if self.north and self.north == cell.south: 
            neighbor = self.north
        elif self.south and self.south == cell.north:
            neighbor = self.south
        elif self.east and self.east == cell.west:
            neighbor = self.east
        elif self.west and self.west == cell.east:
            neighbor = self.west
        
        if neighbor:
            self.grid.tunnel_under(neighbor)
        else:
            super().link(cell, bidi)
    

class UnderCell(Cell):
    def __init__(self, over_cell: OverCell):
        super().__init__(over_cell.row, over_cell.column)
        self.overcell = over_cell
        if over_cell.horizontal_passageq():
            self.north = over_cell.north
            over_cell.north.south = self
            self.south = over_cell.south
            over_cell.south.north = self
            self.link(self.north)
            self.link(self.south)
        else:
            self.east = over_cell.east
            over_cell.east.west = self
            self.west = over_cell.west
            over_cell.west.east = self

            self.link(self.east)
            self.link(self.west)
    
    def horizontal_passageq(self) -> bool:
        return self.east or self.west
    
    def vertical_passageq(self) -> bool:
        return self.north or self.south
    
class SimpleOverCell(OverCell):
    def neighbors(self):
        return Cell.neighbors(self)