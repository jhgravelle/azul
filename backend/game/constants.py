"""
Game constants for Azul.
"""

from .enums import Tile

# Board and game dimensions
BOARD_SIZE = 5
FACTORIES_COUNT = 5

# Tile distribution
TILES_PER_COLOR = 20
TILES_PER_FACTORY = 4
COLORS = [Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.WHITE, Tile.BLACK]

# Scoring
FLOOR_PENALTIES = [-1, -1, -2, -2, -2, -3, -3]

# Wall pattern: defines which color appears in each row and column
# wall_pattern[row][col] = Tile enum for that position
# In Azul, each row is a rotation of colors
WALL_PATTERN = [
    [Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.WHITE, Tile.BLACK],
    [Tile.BLACK, Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.WHITE],
    [Tile.WHITE, Tile.BLACK, Tile.BLUE, Tile.YELLOW, Tile.RED],
    [Tile.RED, Tile.WHITE, Tile.BLACK, Tile.BLUE, Tile.YELLOW],
    [Tile.YELLOW, Tile.RED, Tile.WHITE, Tile.BLACK, Tile.BLUE],
]

# Bonus points for complete rows/columns on wall
ROW_BONUS = 2
COLUMN_BONUS = 7
COLOR_BONUS = 10
