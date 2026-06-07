"""
Move class representing a single player action.
"""

from dataclasses import dataclass
from .enums import Source, Destination, Tile


@dataclass
class Move:
    """Represents one player's move.

    Attributes:
        source: Which source to take tiles from (factory or center).
        tile: Which color tile is being taken.
        destination: Where the tiles are being placed (pattern line or floor).
        includes_first_player_token: Whether the first player token is being taken from center.
        count: Number of tiles of this color being taken.
    """

    source: Source
    tile: Tile
    destination: Destination
    includes_first_player_token: bool = False
    count: int = 0
