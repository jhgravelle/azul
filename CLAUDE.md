# Claude Project Documentation

## Project Overview
Interactive Azul board game - a learning project building full-stack web development skills.

## Key Characteristics
- **Type**: Learning project (not production)
- **Learning focus**: Full-stack dev, game mechanics, eventually ML/AI for bots
- **Development style**: One function at a time, with detailed explanations
- **Documentation**: Maintained alongside code development

## Technology Decisions

### Frontend: React (Vite) + TypeScript
- Vite for fast dev feedback loops
- TypeScript for early error catching
- React ecosystem for component management and turn-based game state

### Backend: Python + FastAPI
- Python for ML/AI capability (future bot development)
- FastAPI for modern, fast API design
- Game logic written in pure Python functions (testable, reusable)

### Database: SQLite (v1) → PostgreSQL (future)
- Start simple with in-memory/SQLite
- Add persistence when stats/multiplayer is needed

## Development Approach

**One Method at a Time**: 
- Write a single game function (e.g., `validate_move()`)
- Explain its purpose, implementation, and design choices
- User reviews and asks questions for full understanding
- Move to next function
- Incrementally build complete game

## Key Files

### Game Logic
- `backend/game/` - Core Azul mechanics
  - State representation
  - Move validation
  - Scoring calculation
  - Win detection

### API
- `backend/api/` - FastAPI endpoints
  - Game endpoints (create game, make move, get state)
  - Player endpoints (future)

### Frontend Components
- `frontend/src/components/` - React UI
  - GameBoard - main game display
  - PlayerPanel - player areas
  - TileGrid - tile interactions

### Documentation
- `docs/DECISIONS.md` - Architecture and tech decisions
- `docs/GAME_RULES.md` - Azul rules and mechanics
- `docs/API.md` - API endpoint documentation
- `docs/DEVELOPMENT.md` - How to run and develop

## Testing Strategy

**Backend**: pytest for game logic unit tests
- Test each function independently
- Validate game rules enforcement
- Edge case coverage

**Frontend**: React Testing Library for components
- Test user interactions
- Verify correct rendering
- Integration tests for game flow

## CI/CD Pipeline
GitHub Actions runs on every commit:
- Linting (Python, TypeScript)
- Type checking (mypy, TypeScript)
- Unit tests (pytest, vitest)
- Build verification (Python, React)

## Related Documentation
- See `docs/DECISIONS.md` for detailed decision log
- See `docs/GAME_RULES.md` for Azul game mechanics
- See `docs/DEVELOPMENT.md` for setup and running instructions
