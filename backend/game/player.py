"""
Player and PlayerState classes.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .enums import Tile
from .constants import BOARD_SIZE


@dataclass(frozen=True)
class Player:
    """Static player information that doesn't change during the game.

    Attributes:
        player_id: Unique integer identifier for the player.
        name: Player's name.
        avatar: Emoji or character representing the player.
        color: Player's display color.
        player_type: "human" or "bot".
    """

    player_id: int
    name: str
    avatar: str
    color: str
    player_type: str  # "human" or "bot"

    def __post_init__(self) -> None:
        """Validate player_type on initialization."""
        if self.player_type not in ("human", "bot"):
            raise ValueError(f"player_type must be 'human' or 'bot', got {self.player_type}")


@dataclass
class PlayerState:
    """Dynamic state of a player that changes during the game.

    Attributes:
        player_id: Reference to the Player's id.
        score: Current score.
        pattern_lines: 5 rows, each can hold tiles waiting to be placed on wall.
                      Row i can hold at most i+1 tiles (row 0 can hold 1, row 4 can hold 5).
        floor: Tiles in the floor area (penalty zone).
        wall: 5x5 grid of tiles placed on the wall. None if position is empty.
    """

    player_id: int
    score: int = 0
    pattern_lines: List[List[Tile]] = field(
        default_factory=lambda: [[] for _ in range(BOARD_SIZE)]
    )
    floor: List[Tile] = field(default_factory=list)
    wall: List[List[Optional[Tile]]] = field(
        default_factory=lambda: [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    )
