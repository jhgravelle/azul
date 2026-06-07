"""
Enums for Azul game state and moves.
"""

from enum import IntEnum


class Source(IntEnum):
    """Sources where tiles can be taken from."""

    CENTER = -1
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 4


class Destination(IntEnum):
    """Destinations where tiles can be placed."""

    FLOOR = -1
    R1 = 0
    R2 = 1
    R3 = 2
    R4 = 3
    R5 = 4


class Column(IntEnum):
    """Wall columns (colors in standard Azul)."""

    C1 = 0
    C2 = 1
    C3 = 2
    C4 = 3
    C5 = 4


class Tile(IntEnum):
    """Tile types in the game."""

    FIRST = -1
    BLUE = 0
    YELLOW = 1
    RED = 2
    WHITE = 3
    BLACK = 4
