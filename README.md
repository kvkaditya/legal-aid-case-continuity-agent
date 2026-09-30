# Legal Aid Case Continuity Agent - Root README

## Overview

This is the main repository for the Legal Aid Case Continuity Agent hackathon project. The project is structured as a monorepo with separate frontend and backend directories.

## Project Structure

```
legal-aid-case-continuity-agent/
├── frontend/                    # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   ├── hooks/              # Custom React hooks
│   │   ├── types/              # TypeScript type definitions
│   │   └── utils/              # Utility functions
│   ├── public/                 # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
├── backend/                     # FastAPI + Python
│   ├── app/
│   │   ├── api/                # API route handlers
│   │   ├── models/             # SQLAlchemy models
│   │   ├── services/           # Business logic
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── database/           # Database configuration
│   │   ├── agents/             # Agent logic
│   │   ├── hindsight/          # Hindsight integration
│   │   └── document_processing/ # Document processing
│   ├── tests/
│   │   ├── unit/               # Unit tests
│   │   └── integration/        # Integration tests
│   ├── config/                 # Configuration files
│   ├── main.py                 # Application entry point
│   ├── pyproject.toml
│   └── .env
│
├── docs/                        # Documentation
├── tests/                       # Project-level tests
│   ├── unit/
│   └── integration/
├── .env.example                 # Example environment variables
├── .gitignore
└── README.md
```

## Quick Start

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000 or http://localhost:5173

### Backend Setup

```bash
cd backend
pip install -e ".[dev]"
python main.py
```

Backend runs on http://localhost:8000

### Environment Configuration

1. Copy `.env.example` to `.env` files in both frontend and backend directories
2. Update the environment variables as needed

## Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript types
```

### Backend Development

```bash
cd backend
python main.py       # Run development server
pytest               # Run tests
black .              # Format code
isort .              # Sort imports
mypy .               # Type checking
```

## Architecture

### Frontend (React + TypeScript + Vite)

- **Components**: Reusable UI components
- **Pages**: Page-level components for routing
- **Services**: HTTP client for API communication
- **Hooks**: Custom React hooks for state management
- **Types**: TypeScript type definitions

### Backend (FastAPI + Python)

- **API**: RESTful API endpoints
- **Models**: SQLAlchemy ORM models
- **Services**: Business logic and data processing
- **Schemas**: Pydantic models for validation
- **Agents**: AI agent orchestration
- **Hindsight Integration**: Integration with Hindsight API
- **Document Processing**: Document handling and processing

## Key Features (To be implemented)

- [ ] Legal aid case management
- [ ] Case continuity tracking
- [ ] Document processing and management
- [ ] Hindsight integration
- [ ] AI-powered agent for case analysis
- [ ] User authentication and authorization
- [ ] Real-time notifications

## Contributing

Guidelines to be added.

## License

MIT License

## Contact

Development Team
