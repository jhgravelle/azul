# Architecture & Design Decisions

This document tracks key decisions made during Azul game development, the rationale behind them, and when they were made.

## Format
Each decision includes:
- **Date**: When decided
- **Topic**: What was decided
- **Decision**: What we chose
- **Rationale**: Why
- **Implications**: What this enables or constrains
- **Alternatives Considered**: What we didn't choose and why

---

## Decision: Frontend Framework

**Date**: 2026-06-06  
**Topic**: Which web framework for the game UI?  
**Decision**: React (Vite) + TypeScript  

**Rationale**:
- Large ecosystem with extensive learning resources
- Excellent for component-based game UI
- React hooks provide elegant state management for turn-based games
- Vite enables fast feedback loops during development
- TypeScript catches errors early (important for learning)

**Implications**:
- Must learn React component patterns and hooks
- Good foundation for future features (multiplayer, animations)
- Large community for help and libraries

**Alternatives Considered**:
- Vue.js: Slightly simpler syntax, but smaller ecosystem
- Svelte: Cleanest code, but fewer learning resources
- Plain JavaScript: Faster to start, but harder to scale

---

## Decision: Backend Language & Framework

**Date**: 2026-06-06  
**Topic**: Backend language and web framework?  
**Decision**: Python + FastAPI  

**Rationale**:
- Python is industry standard for ML/AI development
- Future bot development will use scikit-learn, TensorFlow, PyTorch (all Python)
- FastAPI is modern, performant, and great for building APIs
- Pure Python functions for game logic are highly testable
- Same language throughout backend enables knowledge reuse

**Implications**:
- Different language than frontend (JavaScript/TypeScript)
- Enables sophisticated bot development using ML later
- Pure game logic in Python can be reused by both API and ML training

**Alternatives Considered**:
- Node.js + Express: Same language as frontend, but limits ML options
- Java/C#: Overkill for this learning project
- Go: Fast, but less suitable for ML integration

---

## Decision: Database Strategy

**Date**: 2026-06-06  
**Topic**: Database for v1 and beyond?  
**Decision**: SQLite for v1, PostgreSQL for future versions  

**Rationale**:
- SQLite is file-based, requires zero setup
- Good enough for single-device game
- When adding stats/persistence/multiplayer, migrate to PostgreSQL
- Keep v1 simple, no database infrastructure needed

**Implications**:
- V1 game state is in-memory or simple SQLite file
- No need to run separate database process during development
- Future migration path clear when needed

**Alternatives Considered**:
- PostgreSQL from start: Overkill for local game
- MongoDB: Unnecessary complexity for structured game state
- In-memory only: Works but loses data between sessions

---

## Decision: Development Approach - One Method at a Time

**Date**: 2026-06-06  
**Topic**: How to structure code learning during development?  
**Decision**: Build and explain one function/method at a time  

**Rationale**:
- Incremental understanding instead of overwhelming with full modules
- Each function is a discrete unit that can be tested independently
- Easy to verify correctness before moving to next function
- User can ask questions and fully understand before proceeding
- Natural progression: simple functions → complex game logic

**Implications**:
- Slower initial progress but deeper understanding
- Each commit documents one coherent piece of functionality
- Tests can be written and verified for each function

**Alternatives Considered**:
- Build whole modules at once: Faster but less understandable
- Pair with extensive code walkthroughs: More time-consuming
- Just hand over full codebase: No learning value

---

## Decision: CI/CD Pipeline

**Date**: 2026-06-06  
**Topic**: Continuous Integration setup?  
**Decision**: GitHub Actions with linting, type-checking, and tests  

**Rationale**:
- Free and built-in to GitHub
- Catches mistakes early (tests fail before merge)
- Enforces code quality (linting, types)
- Good learning of CI/CD practices
- Prevents broken code from being committed

**Implications**:
- All commits must pass CI checks
- Code must be tested and type-safe
- Early detection of regressions

---

## Decision: Documentation Alongside Development

**Date**: 2026-06-06  
**Topic**: How to maintain project documentation?  
**Decision**: Document decisions, API, and game rules as we build  

**Rationale**:
- Documentation written while knowledge is fresh
- Future readers (including you) can understand reasoning
- Clear decision log for learning journey
- API docs help when connecting frontend & backend
- Game rules reference prevents bugs

**Implications**:
- Every major feature includes documentation update
- DECISIONS.md grows over time with each choice
- Code is self-documenting (good naming, minimal comments)

---

## Decision: Game State Architecture - Immutable GameState Pattern

**Date**: 2026-06-07  
**Topic**: How to structure game state and moves?  
**Decision**: Immutable GameState pattern with separate Game class tracking history

**Rationale**:
- GameState is an immutable snapshot of the complete game at one point
- Game class holds list of all GameStates (nodes) and Moves (edges)
- Each move returns a new GameState rather than mutating current state
- Natural fit for exploring multiple moves from same state (useful for ML bots)
- Full replay capability - can load any state from history
- Clear testing: "given state X, after move Y, expect state Z"

**Implications**:
- More memory overhead (stores all states), but acceptable for turn-based game
- Pure functions for move validation and application
- Can implement undo/redo by replaying from specific state
- State transitions are explicit and trackable

**Alternatives Considered**:
- Mutable Game: Simpler code, but harder to explore alternate moves for ML
- Event sourcing: More complex, not needed for this learning project

---

## Decision: Tile Distribution and Shuffling

**Date**: 2026-06-07  
**Topic**: How to manage tile bag and discard?  
**Decision**: All tiles start in discard; start_round() moves to bag and shuffles

**Rationale**:
- Simplifies initialization (no need to distribute initial bag)
- Natural game flow: discard → bag shuffle → factory fill
- Each game has seeded RNG for reproducibility (critical for testing and ML training)
- Isolated RNG per game prevents other random operations from affecting gameplay

**Implications**:
- start_round() is required before first round can begin
- Game constructor must be followed by start_round() call
- Identical games with same seed will have identical tile draws

**Alternatives Considered**:
- Pre-fill bag at initialization: Less intuitive, harder to understand flow
- Global RNG: Would make games non-reproducible if other code uses random

---

## Decision: Turn Numbering (1-indexed)

**Date**: 2026-06-07  
**Topic**: How to number turns in the game?  
**Decision**: Turn numbers are 1-indexed and ever-increasing (not reset per round)

**Rationale**:
- Matches common game terminology ("turn 1", "turn 2", etc.)
- Never-increasing counter allows for clear game replay and logging
- current_player_index calculated as (turn_number - 1) % num_players

**Implications**:
- turn_number starts at 1, not 0
- Not limited to player count - continues incrementing all game
- Round number separate from turn number

**Alternatives Considered**:
- 0-indexed turns: Easier for modulo math, but less intuitive
- Turn reset per round: Would lose information about game duration

---

## Decision: Separate Player and PlayerState Classes

**Date**: 2026-06-07  
**Topic**: How to represent player information?  
**Decision**: Split into static Player and dynamic PlayerState

**Rationale**:
- Player holds static info (id, name, avatar, color, type) - set once
- PlayerState holds dynamic info (score, pattern_lines, floor, wall) - changes
- GameState contains list of Players and list of PlayerStates
- Matches immutable pattern: Players never change, only PlayerStates change
- Cleaner separation of concerns

**Implications**:
- Every GameState creation includes new PlayerStates but same Players
- Less memory overhead (don't duplicate static info)
- Clear intent: which data is mutable vs immutable

**Alternatives Considered**:
- Single Player class: Simpler but mixes static/dynamic data
- No separation: Would require full object copy for each state

---

## Future Decisions to Make

- [ ] Multiplayer architecture (local only vs. networked)
- [ ] Bot difficulty levels (random → ML-based)
- [ ] Stats persistence (player history, win rates)
- [ ] Animation framework (for tile movements)
- [ ] Deployment strategy (where to host)

---

## Notes
- This document is a living log - updated as new decisions are made
- Decisions can be revisited if assumptions change
- Alternatives not chosen are kept for reference
