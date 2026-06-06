# Azul Game - Interactive Learning Project

An interactive implementation of the board game Azul, built as a learning project for full-stack web development, game mechanics, and eventually AI/bot development.

## Tech Stack

- **Frontend**: React (Vite) + TypeScript
- **Backend**: Python + FastAPI
- **Testing**: pytest (backend), React Testing Library (frontend)
- **Future ML**: scikit-learn / TensorFlow for bot AI

## Project Structure

```
├── frontend/               # React Vite app
│   ├── src/
│   │   ├── components/    # Game UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── utils/         # Utilities
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/               # Python FastAPI server
│   ├── game/              # Core Azul game logic
│   ├── api/               # API endpoints
│   ├── bots/              # AI/ML implementations
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
├── docs/                  # Project documentation
│   ├── DECISIONS.md       # Architecture & design decisions
│   ├── GAME_RULES.md      # Azul game rules & mechanics
│   ├── API.md             # API documentation
│   └── DEVELOPMENT.md     # Development guide
└── .github/
    └── workflows/         # CI/CD pipelines
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Development Workflow

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed instructions.

## Learning Goals

This project covers:
- Game logic and state management
- Full-stack web development (React + Python)
- API design and client-server communication
- Testing and CI/CD
- Machine learning for game-playing AI (phase 2)

## Progress

- [ ] Phase 1: Core game logic
- [ ] Phase 2: Frontend UI
- [ ] Phase 3: Connect frontend & backend
- [ ] Phase 4: Polish & testing
- [ ] Phase 5: ML bots

## Documentation

All design decisions, architecture choices, and learning notes are documented in `docs/`.
