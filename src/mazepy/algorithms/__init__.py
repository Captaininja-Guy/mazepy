from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .aldous_broder import AldousBroder
    from .binary_tree import BinaryTree
    from .ellers import Ellers
    from .fractal_tesselation import FractalTessalation
    from .growing_tree import GrowingTree
    from .hunt_and_kill import HuntandKill
    from .kruskals import Kruskals
    from .origin_shift import OriginShift
    from .prims import Prims, TruePrims, ModifiedPrims, SimplifiedPrims
    from .recursive_backtrack import RecursiveBacktrack
    from .recursive_division import RecursiveDivision
    from .sidewinder import Sidewinder
    from .wilsons import Wilsons


def __getattr__(name):
    if name == "AldousBroder":
        from .aldous_broder import AldousBroder
        return AldousBroder
    if name == "BinaryTree":
        from .binary_tree import BinaryTree
        return BinaryTree
    if name == "Ellers":
        from .ellers import Ellers
        return Ellers
    if name == "FractalTessalation":
        from .fractal_tesselation import FractalTessalation
        return FractalTessalation
    if name == "GrowingTree":
        from .growing_tree import GrowingTree
        return GrowingTree
    if name == "HuntandKill":
        from .hunt_and_kill import HuntandKill
        return HuntandKill
    if name == "Kruskals":
        from .kruskals import Kruskals
        return Kruskals
    if name == "OriginShift":
        from .origin_shift import OriginShift
        return OriginShift
    if name == "Prims":
        from .prims import Prims
        return Prims
    if name == "TruePrims":
        from .prims import TruePrims
        return TruePrims
    if name == "ModifiedPrims":
        from .prims import ModifiedPrims
        return ModifiedPrims
    if name == "SimplifiedPrims":
        from .prims import SimplifiedPrims
        return SimplifiedPrims
    if name == "RecursiveBacktrack":
        from .recursive_backtrack import RecursiveBacktrack
        return RecursiveBacktrack
    if name == "RecursiveDivision":
        from .recursive_division import RecursiveDivision
        return RecursiveDivision
    if name == "Sidewinder":
        from .sidewinder import Sidewinder
        return Sidewinder
    if name == "Wilsons":
        from .wilsons import Wilsons
        return Wilsons

    raise AttributeError(name)


__all__ = ["AldousBroder",
           "BinaryTree",
           "Ellers",
           "FractalTessalation",
           "GrowingTree",
           "HuntandKill",
           "Kruskals",
           "OriginShift",
           "Prims",
           "TruePrims",
           "ModifiedPrims",
           "SimplifiedPrims",
           "RecursiveBacktrack",
           "RecursiveDivision",
           "Sidewinder",
           "Wilsons"]