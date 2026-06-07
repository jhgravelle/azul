"""
GameState class representing the complete game state at a point in time.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .player import Player, PlayerState
from .enums import Tile, Source


@dataclass
class GameState:
    """Immutable snapshot of the complete game state.

    Attributes:
        players: List of Player objects (static info, same throughout game).
        player_states: List of PlayerState objects (dynamic, one per player, in same order as players).
        round_number: Current round (1-indexed).
        turn_number: Global turn counter (ever-increasing throughout game).
        bag: Remaining tiles available to draw for factories.
        discard: Tiles that will return to bag at end of round.
        factories: Dict mapping Source to list of tiles in that source.
                  Includes F1, F2, F3, F4, F5, and CENTER.
    """

    players: List[Player]
    player_states: List[PlayerState]
    round_number: int
    turn_number: int
    bag: List[Tile] = field(default_factory=list)
    discard: List[Tile] = field(default_factory=list)
    factories: Dict[Source, List[Tile]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate game state on initialization."""
        if len(self.players) != len(self.player_states):
            raise ValueError("players and player_states must have same length")
        if len(self.players) == 0:
            raise ValueError("must have at least one player")
        if self.round_number < 1:
            raise ValueError("round_number must be >= 1")
        if self.turn_number < 0:
            raise ValueError("turn_number must be >= 0")

    @property
    def current_player_index(self) -> int:
        """Get the index of the player whose turn it is.

        Since turn_number is 1-indexed, turn 1 = player 0, turn 2 = player 1, etc.
        """
        return (self.turn_number - 1) % len(self.players)

    @property
    def current_player(self) -> Player:
        """Get the player whose turn it is."""
        return self.players[self.current_player_index]

    @property
    def current_player_state(self) -> PlayerState:
        """Get the state of the player whose turn it is."""
        return self.player_states[self.current_player_index]
