"""
Test basic game structure and initialization.
"""

import pytest
from backend.game.player import Player, PlayerState
from backend.game.gamestate import GameState
from backend.game.game import Game
from backend.game.move import Move
from backend.game.enums import Source, Destination, Tile
from backend.game.constants import TILES_PER_COLOR, COLORS


def test_player_creation():
    """Test creating a Player object."""
    player = Player(
        player_id=1,
        name="Alice",
        avatar="🎮",
        color="blue",
        player_type="human",
    )
    assert player.player_id == 1
    assert player.name == "Alice"
    assert player.avatar == "🎮"
    assert player.color == "blue"
    assert player.player_type == "human"


def test_player_invalid_type():
    """Test that invalid player_type raises ValueError."""
    with pytest.raises(ValueError, match="player_type must be 'human' or 'bot'"):
        Player(
            player_id=1,
            name="Alice",
            avatar="🎮",
            color="blue",
            player_type="invalid",
        )


def test_player_state_creation():
    """Test creating a PlayerState object."""
    state = PlayerState(player_id=1, score=10)
    assert state.player_id == 1
    assert state.score == 10
    assert len(state.pattern_lines) == 5
    assert len(state.floor) == 0
    assert len(state.wall) == 5
    assert all(len(row) == 5 for row in state.wall)


def test_game_creation():
    """Test creating a Game with two players."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2], random_seed=42)

    assert game.players == [p1, p2]
    assert len(game.states) == 1
    assert len(game.moves) == 0
    assert game.random_seed == 42


def test_game_initial_state():
    """Test that initial game state is properly configured."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2])
    state = game.current_state

    assert state.round_number == 1
    assert state.turn_number == 1
    assert len(state.players) == 2
    assert len(state.bag) == 0
    assert len(state.discard) == TILES_PER_COLOR * len(COLORS)
    assert state.current_player == p1
    assert state.current_player_index == 0


def test_game_player_count_validation():
    """Test that game validates player count."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")

    with pytest.raises(ValueError, match="Game must have 2-4 players"):
        Game([p1])

    with pytest.raises(ValueError, match="Game must have 2-4 players"):
        Game([p1] * 5)


def test_move_creation():
    """Test creating a Move object."""
    move = Move(
        source=Source.F1,
        tile=Tile.BLUE,
        destination=Destination.R1,
        includes_first_player_token=False,
        count=3,
    )
    assert move.source == Source.F1
    assert move.tile == Tile.BLUE
    assert move.destination == Destination.R1
    assert move.includes_first_player_token is False
    assert move.count == 3


def test_current_player_index():
    """Test that current_player_index is calculated correctly."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")
    p3 = Player(3, "Carol", "🧙", "green", "human")

    game = Game([p1, p2, p3])
    state = game.current_state

    assert state.current_player_index == 0
    assert state.current_player == p1

    # Simulate turn 4 (should wrap to player 0 in 3-player game)
    # This won't work yet since we can't directly create GameStates,
    # but the property should work correctly


def test_start_round_fills_factories():
    """Test that start_round fills all factories with tiles."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2], random_seed=42)

    # Initial state should have empty factories
    assert len(game.factories[Source.F1]) == 0
    assert len(game.factories[Source.F5]) == 0
    assert len(game.factories[Source.CENTER]) == 0

    # After start_round, each factory should have 4 tiles
    state = game.start_round()

    assert len(game.factories[Source.F1]) == 4
    assert len(game.factories[Source.F2]) == 4
    assert len(game.factories[Source.F3]) == 4
    assert len(game.factories[Source.F4]) == 4
    assert len(game.factories[Source.F5]) == 4
    assert len(game.factories[Source.CENTER]) == 0

    # Bag and discard should be updated
    total_tiles = len(game.bag) + len(game.discard)
    total_in_factories = sum(len(tiles) for tiles in game.factories.values())
    assert total_tiles + total_in_factories == TILES_PER_COLOR * len(COLORS)


def test_start_round_records_state_in_history():
    """Test that start_round records state in history."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2], random_seed=42)

    # Initial state in history
    assert len(game.states) == 1

    # After start_round, state is recorded
    game.start_round()
    assert len(game.states) == 2

    # Second start_round also records state
    game.start_round()
    assert len(game.states) == 3


def test_fill_factories_with_insufficient_tiles():
    """Test that fill_factories handles case when not enough tiles."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2], random_seed=42)

    # Reduce tiles to less than needed for full factories
    game.discard = game.discard[:10]  # Only 10 tiles

    game.start_round()

    # Should have filled as many as possible
    total_in_factories = sum(len(tiles) for tiles in game.factories.values())
    assert total_in_factories == 10


def test_fill_factories_refills_from_discard():
    """Test that fill_factories refills bag from discard during factory filling."""
    p1 = Player(1, "Alice", "🎮", "blue", "human")
    p2 = Player(2, "Bob", "🤖", "red", "bot")

    game = Game([p1, p2], random_seed=42)

    # Set up: only 12 tiles in discard (enough for 3 factories, will need to refill bag)
    game.discard = [Tile.BLUE] * 4 + [Tile.RED] * 4 + [Tile.YELLOW] * 4

    game.start_round()

    # Should have filled 3 factories completely (12 tiles), partial 4th
    assert len(game.factories[Source.F1]) == 4
    assert len(game.factories[Source.F2]) == 4
    assert len(game.factories[Source.F3]) == 4
    assert len(game.factories[Source.F4]) == 0  # Not enough tiles
    assert len(game.factories[Source.F5]) == 0
