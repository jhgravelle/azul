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
