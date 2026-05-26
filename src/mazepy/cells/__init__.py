from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cell import Cell
    from .hex_cell import HexCell
    from .polar_cell import PolarCell
    from .triangle_cell import TriangleCell
    from .weighted_cell import WeightedCell
    from .weave_cells import OverCell, UnderCell, SimpleOverCell

def __getattr__(name):
    if name == "Cell":
        from .cell import Cell
        return Cell
    
    if name == "HexCell":
        from .hex_cell import HexCell
        return HexCell
    
    if name == "PolarCell":
        from .polar_cell import PolarCell
        return PolarCell
    
    if name == "TriangleCell":
        from .triangle_cell import TriangleCell
        return TriangleCell
    
    if name == "UnderCell":
        from .weave_cells import UnderCell
        return UnderCell
    
    if name == "SimpleOverCell":
        from .weave_cells import SimpleOverCell
        return SimpleOverCell
    
    if name == "WeightedCell":
        from .weighted_cell import WeightedCell
        return WeightedCell 

    if name == "OverCell":
        from .weave_cells import OverCell
        return OverCell

    raise AttributeError(name)

__all__ = ["Cell",
           "HexCell",
           "PolarCell",
           "TriangleCell",
           "WeightedCell",
           "OverCell",
           "UnderCell",
           "SimpleOverCell"]