from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hex_grid import HexGrid
    from .masked_grid import MaskedGrid
    from .mobius_grid import MobiusGrid, PaperMobiusGrid
    from .polar_grid import PolarGrid
    from .sphere_grid import SphereGrid
    from .toroidal_grid import ToroidalGrid
    from .triangle_grid import TriangleGrid
    from .weave_grid import WeaveGrid, PreconfiguredWeaveGrid
    from .weighted_grid import WeightedGrid
    from .cylinder_grid import CylinderGrid
    from .distance_grid import DistanceGrid
    from .grid_3D import Grid3D
    from .colored_grid import ColoredGrid
    from .grid import ColoredHexGrid
    from .colored_polar_grid import ColoredPolarGrid
    from .colored_triangle_grid import ColoredTriangleGrid
    from .colored_weave_grid import ColoredWeaveGrid, ColoredPreconfiguredWeaveGrid
    from .cube_grid import CubeGrid
    from .grid import Grid


def __getattr__(name):
    if name == "HexGrid":
        from .hex_grid import HexGrid
        return HexGrid
    
    if name == "MaskedGrid":
        from .masked_grid import MaskedGrid
        return MaskedGrid
    
    if name == "MobiusGrid":
        from .mobius_grid import MobiusGrid
        return MobiusGrid
    
    if name == "PaperMobiusGrid":
        from .mobius_grid import PaperMobiusGrid
        return PaperMobiusGrid
    
    if name == "PolarGrid":
        from .polar_grid import PolarGrid
        return PolarGrid
    
    if name == "SphereGrid":
        from .sphere_grid import SphereGrid
        return SphereGrid
    
    if name == "ToroidalGrid":
        from .toroidal_grid import ToroidalGrid
        return ToroidalGrid
    
    if name == "TriangleGrid":
        from .triangle_grid import TriangleGrid
        return TriangleGrid
    
    if name == "WeaveGrid":
        from .weave_grid import WeaveGrid
        return WeaveGrid
    
    if name == "PreconfiguredWeaveGrid":
        from .weave_grid import PreconfiguredWeaveGrid
        return PreconfiguredWeaveGrid
    
    if name == "WeightedGrid":
        from .weighted_grid import WeightedGrid
        return WeightedGrid

    if name == "CylinderGrid":
        from .cylinder_grid import CylinderGrid
        return CylinderGrid
    
    if name == "DistanceGrid":
        from .distance_grid import DistanceGrid
        return DistanceGrid
    
    if name == "Grid3D":
        from .grid_3D import Grid3D
        return Grid3D

    if name == "ColoredGrid":
        from .colored_grid import ColoredGrid
        return ColoredGrid
    
    if name == "ColoredHexGrid":
        from .colored_hex_grid import ColoredHexGrid
        return ColoredHexGrid
    
    if name == "ColoredPolarGrid":
        from .colored_polar_grid import ColoredPolarGrid
        return ColoredPolarGrid
    
    if name == "ColoredTriangleGrid":
        from .colored_triangle_grid import ColoredTriangleGrid
        return ColoredTriangleGrid
    
    if name == "ColoredWeaveGrid":
        from .colored_weave_grid import ColoredWeaveGrid
        return ColoredWeaveGrid
    
    if name == "ColoredPreconfiguredWeaveGrid":
        from .colored_weave_grid import ColoredPreconfiguredWeaveGrid
        return ColoredPreconfiguredWeaveGrid
    
    if name == "CubeGrid":
        from .cube_grid import CubeGrid
        return CubeGrid
    
    if name == "Grid":
        from .grid import Grid
        return Grid


    raise AttributeError(name)

__all__ = ["HexGrid",
           "MaskedGrid",
           "MobiusGrid",
           "PaperMobiusGrid",
           "PolarGrid",
           "SphereGrid",
           "ToroidalGrid",
           "TriangleGrid",
           "WeaveGrid",
           "PreconfiguredWeaveGrid",
           "WeightedGrid",
           "CylinderGrid",
           "DistanceGrid",
           "Grid3D",
           "ColoredGrid",
           "ColoredHexGrid",
           "ColoredPolarGrid",
           "ColoredTriangleGrid",
           "ColoredWeaveGrid",
           "ColoredPreconfiguredWeaveGrid",
           "CubeGrid",
           "Grid"]