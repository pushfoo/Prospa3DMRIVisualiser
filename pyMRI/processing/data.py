from __future__ import annotations
from typing import NamedTuple, Literal
from enum import Enum, auto

from numpy import ndarray, complexfloating, reshape

from arcade.gl import Texture2D


class Unit(Enum):
    MM = auto()  # millimeters
    CM = auto()  # centimeters
    ME = auto()  # meters
    KM = auto()  # kilometers
    MG = auto()  # megameters
    IN = auto()  # inches
    FT = auto()  # feet
    MI = auto()  # miles
    LY = auto()  # lightyear

    @staticmethod
    def convert(value: float | int, x: Unit, y: Unit) -> float | int:
        if x == y:
            return value
        return value * UNIT_CONVERSIONS[x, y]

    @staticmethod
    def to_str(x: Unit) -> str:
        match x:
            case Unit.MM:
                return "millimeters"
            case Unit.CM:
                return "centimeters"
            case Unit.ME:
                return "meters"
            case Unit.KM:
                return "kilometers"
            case Unit.MG:
                return "megameters"
            case Unit.IN:
                return "inches"
            case Unit.FT:
                return "feet"
            case Unit.MI:
                return "miles"
            case Unit.LY:
                return "lightyear"


# TODO Imperial Units and lightyears
UNIT_CONVERSIONS = {
    (Unit.MM, Unit.CM): 1e-1,
    (Unit.MM, Unit.ME): 1e-3,
    (Unit.MM, Unit.KM): 1e-6,
    (Unit.MM, Unit.MG): 1e-9,
    (Unit.MM, Unit.IN): 1.0 / 25.4,
    (Unit.MM, Unit.FT): 1.0 / 304.8,
    (Unit.MM, Unit.MI): 1.0 / 1_609_344,
    (Unit.MM, Unit.LY): 1.0570008340247e-19,
    (Unit.CM, Unit.MM): 1e1,
    (Unit.CM, Unit.ME): 1e-1,
    (Unit.CM, Unit.KM): 1e-5,
    (Unit.CM, Unit.MG): 1e-8,
    (Unit.CM, Unit.IN): 1.0 / 2.54,
    (Unit.CM, Unit.FT): 1.0 / 30.48,
    (Unit.CM, Unit.MI): 1.0 / 160_034.4,
    (Unit.CM, Unit.LY): 1.0570008340247e-18,
    (Unit.ME, Unit.MM): 1e3,
    (Unit.ME, Unit.CM): 1e2,
    (Unit.ME, Unit.KM): 1e-3,
    (Unit.ME, Unit.MG): 1e-6,
    (Unit.ME, Unit.IN): 39.3701,
    (Unit.ME, Unit.FT): 3.28084,
    (Unit.ME, Unit.MI): 1.0 / 1609.344,
    (Unit.ME, Unit.LY): 1.0570008340247e-16,
    (Unit.KM, Unit.MM): 1e6,
    (Unit.KM, Unit.CM): 1e5,
    (Unit.KM, Unit.ME): 1e3,
    (Unit.KM, Unit.MG): 1e-3,
    (Unit.KM, Unit.IN): 39370.1,
    (Unit.KM, Unit.FT): 3280.84,
    (Unit.KM, Unit.MI): 0.621371,
    (Unit.KM, Unit.LY): 1.0570008340247e-13,
    (Unit.MG, Unit.MM): 1e9,
    (Unit.MG, Unit.CM): 1e8,
    (Unit.MG, Unit.ME): 1e6,
    (Unit.MG, Unit.KM): 1e3,
    (Unit.MG, Unit.IN): 39370078.74,
    (Unit.MG, Unit.FT): 3280839.895,
    (Unit.MG, Unit.MI): 621.37119224,
    (Unit.MG, Unit.LY): 1.0570008340237e-10,
    (Unit.IN, Unit.MM): 0.0,
    (Unit.IN, Unit.CM): 0.0,
    (Unit.IN, Unit.ME): 0.0,
    (Unit.IN, Unit.KM): 0.0,
    (Unit.IN, Unit.MG): 0.0,
    (Unit.IN, Unit.FT): 0.0,
    (Unit.IN, Unit.MI): 0.0,
    (Unit.IN, Unit.LY): 0.0,
    (Unit.MI, Unit.MM): 0.0,
    (Unit.MI, Unit.CM): 0.0,
    (Unit.MI, Unit.ME): 0.0,
    (Unit.MI, Unit.KM): 0.0,
    (Unit.MI, Unit.MG): 0.0,
    (Unit.MI, Unit.IN): 0.0,
    (Unit.MI, Unit.FT): 0.0,
    (Unit.MI, Unit.LY): 0.0,
    (Unit.LY, Unit.MM): 0.0,
    (Unit.LY, Unit.CM): 0.0,
    (Unit.LY, Unit.ME): 0.0,
    (Unit.LY, Unit.KM): 0.0,
    (Unit.LY, Unit.MG): 0.0,
    (Unit.LY, Unit.IN): 0.0,
    (Unit.LY, Unit.FT): 0.0,
    (Unit.LY, Unit.MI): 0.0,
}


class InterpolateModes(Enum):
    none = auto()  # Do no interpolation
    cube = auto()  # Make all voxels uniform in size
    double = auto()  # double voxel resolution
    triple = auto()  # triple voxel resolution
    quadruple = auto()  # quadruple voxel resolution
    minimum = auto()  # make the voxels as fine as possible


ORIENTATIONS = (
    "x",
    "y",
    "z",
    "xy",
    "yx",
    "yz",
    "zy",
    "xz",
    "zx",
    "xyz",
    "xzy",
    "yxz",
    "yzx",
    "zxy",
    "zyx",
)
type Orientation = Literal[
    "x",
    "y",
    "z",
    "xy",
    "yx",
    "yz",
    "zy",
    "xz",
    "zx",
    "xyz",
    "xzy",
    "yxz",
    "yzx",
    "zxy",
    "zyx",
]


class FileData(NamedTuple):
    orientation: Orientation
    voxel_dimensions: tuple[float, float, float]
    voxel_unit: Unit
    voxel_counts: tuple[int, int, int]
    voxel_data: ndarray[complexfloating]


type FourierData = FileData


class RenderData(NamedTuple):
    colour_map: Texture2D
    density_scalar: float
    emission_brightness: float
    orientation: Orientation
    voxel_dimensions: tuple[float, float, float]
    voxel_unit: Unit
    voxel_counts: tuple[int, int, int]
    voxel_data: ndarray[complexfloating]
