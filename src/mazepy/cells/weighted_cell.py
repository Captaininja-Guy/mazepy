from ..cells.cell import Cell
from ..distances import Distances

class WeightedCell(Cell):
    def __init__(self, row: int, column: int):
        super().__init__(row, column)
        self.weight = 1

    def distances(self) -> Distances:
        weights = Distances(self)
        pending = [self]

        while pending:
            cell = sorted(pending, key=lambda c: weights[c])[0]
            pending.remove(cell)


            for neighbor in cell.links():
                total_weight = weights[cell] + neighbor.weight
                if neighbor not in weights or total_weight < weights[neighbor]:
                    pending.append(neighbor)
                    weights[neighbor] = total_weight

        return weights