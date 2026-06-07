"""
Game class for orchestrating Azul game flow.
"""

import random
from typing import List, Optional
from .player import Player, PlayerState
from .gamestate import GameState
from .move import Move
from .constants import TILES_PER_COLOR, COLORS


class Game:
    """Orchestrates the game flow with full history tracking.

    States are like nodes and moves are like edges in the game graph.
    Tracks all previous states and moves for full replay capability.
    Includes random seed for reproducible games (useful for testing and ML).

    Attributes:
        players: The Player objects (static, same throughout).
        states: List of all GameState objects in chronological order.
        moves: List of all Move objects in chronological order.
        random_seed: Seed used for random number generator.
        random: Random number generator instance for shuffle and tile drawing.
    """

    def __init__(self, players: List[Player], random_seed: Optional[int] = None) -> None:
        """Initialize game with players.

        All tiles start in the discard pile. When start_round() is called,
        they move to bag and are shuffled.
        Round number starts at 1, turn number starts at 1.

        Args:
            players: List of Player objects participating in the game.
            random_seed: Seed for RNG (None for truly random, int for reproducible games).

        Raises:
            ValueError: If fewer than 2 players or more than 4 players.
        """
        if len(players) < 2 or len(players) > 4:
            raise ValueError("Game must have 2-4 players")

        self.players = players
        self.states: List[GameState] = []
        self.moves: List[Move] = []

        # Random number generation with seed for reproducibility
        # This RNG is isolated to the game and won't be affected by other random operations
        self.random_seed = random_seed
        self.random = random.Random(random_seed)

        # Create initial player states
        initial_player_states = [PlayerState(player_id=p.player_id) for p in players]

        # Create initial game state
        # Bag starts empty, discard has all tiles
        all_tiles = [tile for tile in COLORS for _ in range(TILES_PER_COLOR)]

        initial_state = GameState(
            players=players,
            player_states=initial_player_states,
            round_number=1,
            turn_number=1,
            bag=[],
            discard=all_tiles,
            factories={},
        )

        self.states.append(initial_state)

    @property
    def current_state(self) -> GameState:
        """Return current game state (the last state in history)."""
        return self.states[-1]

    def start_round(self) -> GameState:
        """Fill factories with tiles from the bag for a new round.

        1. Moves all tiles from discard to bag
        2. Shuffles bag using seeded random generator
        3. Distributes tiles to factories
        4. Center starts empty

        Returns:
            New GameState with factories filled and bag updated.

        Raises:
            ValueError: If not enough tiles in bag to fill factories.
        """
        # TODO: Move discard to bag
        # TODO: Shuffle bag
        # TODO: Distribute to factories
        # TODO: Create new GameState with updated bag and factories
        return self.current_state

    def make_move(self, move: Move) -> GameState:
        """Validate and apply a player move, updating game state.

        Args:
            move: The Move to apply.

        Returns:
            New GameState after the move.

        Raises:
            ValueError: If move is invalid.
        """
        # TODO: Validate move
        # TODO: Apply move
        # TODO: Increment turn_number
        # TODO: Append to states and moves
        return self.current_state

    def end_round(self) -> GameState:
        """Execute end-of-round scoring and wall placement.

        For each player:
        1. Move complete rows from pattern lines to wall
        2. Score points for adjacencies
        3. Apply floor penalties
        4. Clear floor and return tiles to discard

        Returns:
            New GameState after round scoring.
        """
        # TODO: Implement scoring logic
        # TODO: Check for game end condition
        # TODO: Create new GameState for next round
        return self.current_state

    def end_game(self) -> Player:
        """Determine and return the winner (highest score).

        Returns:
            The Player object with highest score.
        """
        # TODO: Find player with highest score in current state
        return self.players[0]
