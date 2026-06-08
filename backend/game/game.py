"""
Game class for orchestrating Azul game flow.
"""

import random
from typing import Dict, List, Optional
from .player import Player, PlayerState
from .gamestate import GameState
from .move import Move
from .enums import Source, Tile
from .constants import TILES_PER_COLOR, TILES_PER_FACTORY, COLORS


class Game:
    """Orchestrates the game flow with mutable state and history tracking.

    Game maintains mutable state (current round, turn, bag, discard, factories, player states).
    GameState is a snapshot of the current state at a point in time.
    Tracks all previous states and moves as history for full replay capability.
    Includes random seed for reproducible games (useful for testing and ML).

    Attributes:
        players: The Player objects (static, same throughout).
        round_number: Current round number (mutable, starts at 1).
        turn_number: Current turn number (mutable, 1-indexed, ever-increasing).
        bag: Current tiles available in bag (mutable).
        discard: Current tiles in discard pile (mutable).
        factories: Current tiles in each factory/center (mutable).
        player_states: Current state of each player (mutable).
        states: List of all GameState snapshots in chronological order (history).
        moves: List of all Move objects in chronological order (history).
        random_seed: Seed used for random number generator.
        random: Random number generator instance for shuffle and tile drawing.
    """

    def __init__(
        self, players: List[Player], random_seed: Optional[int] = None
    ) -> None:
        """Initialize game with mutable state.

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

        # Random number generation with seed for reproducibility
        # This RNG is isolated to the game and won't be affected by other random operations
        self.random_seed = random_seed
        self.random = random.Random(random_seed)

        # Mutable game state
        self.round_number = 1
        self.turn_number = 1
        self.bag: List[Tile] = []
        self.discard: List[Tile] = [
            tile for tile in COLORS for _ in range(TILES_PER_COLOR)
        ]
        self.factories: Dict[Source, List[Tile]] = {
            Source.F1: [],
            Source.F2: [],
            Source.F3: [],
            Source.F4: [],
            Source.F5: [],
            Source.CENTER: [],
        }
        self.player_states: List[PlayerState] = [
            PlayerState(player_id=p.player_id) for p in players
        ]

        # History tracking
        self.states: List[GameState] = []
        self.moves: List[Move] = []
        self.states.append(self.current_state)

    @property
    def current_state(self) -> GameState:
        """Return snapshot of current game state."""
        return GameState(
            players=self.players,
            player_states=self.player_states,
            round_number=self.round_number,
            turn_number=self.turn_number,
            bag=self.bag,
            discard=self.discard,
            factories=self.factories,
        )

    def _fill_factories(self) -> None:
        """Fill all factories with tiles from bag, refilling from discard as needed.

        For each factory (F1-F5), takes 4 tiles one by one:
        - If bag is empty, transfers discard to bag and shuffles
        - If both bag and discard are empty, stops
        - Center starts empty
        """
        # Clear factories for new round
        for source in self.factories:
            self.factories[source] = []

        factory_sources = [Source.F1, Source.F2, Source.F3, Source.F4, Source.F5]

        for factory_source in factory_sources:
            for _ in range(TILES_PER_FACTORY):
                # If bag is empty, refill from discard
                if not self.bag:
                    if not self.discard:
                        # Can't fill more
                        break
                    # Move discard to bag and shuffle
                    self.bag = self.discard
                    self.discard = []
                    self.random.shuffle(self.bag)

                # Take one tile from bag and add to factory
                tile = self.bag.pop()
                self.factories[factory_source].append(tile)

    def start_round(self) -> GameState:
        """Fill factories for new round, record state, return snapshot."""
        self._fill_factories()
        self.states.append(self.current_state)
        return self.current_state

    def make_move(self, move: Move) -> GameState:
        """Validate and apply a player move, updating game state.

        Args:
            move: The Move to apply.

        Returns:
            Snapshot of game state after the move.

        Raises:
            ValueError: If move is invalid.
        """
        # TODO: Validate move
        # TODO: Apply move
        # TODO: Increment turn_number
        # TODO: Append to moves and states
        return self.current_state

    def end_round(self) -> GameState:
        """Execute end-of-round scoring and wall placement.

        For each player:
        1. Move complete rows from pattern lines to wall
        2. Score points for adjacencies
        3. Apply floor penalties
        4. Clear floor and return tiles to discard

        Returns:
            Snapshot of game state after round scoring.
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
        # TODO: Find player with highest score
        return self.players[0]
