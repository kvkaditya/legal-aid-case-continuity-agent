# Backend - Legal Aid Case Continuity Agent

FastAPI + Python backend for the Legal Aid Case Continuity Agent.

## Setup

```bash
pip install -e ".[dev]"
python main.py
```

API will be available at http://localhost:8000

## Available Scripts

- `python main.py` - Run development server
- `pytest` - Run tests
- `black .` - Format code
- `isort .` - Sort imports
- `flake8 .` - Lint code
- `mypy .` - Type checking

## Project Structure

- `app/api/` - API route handlers
- `app/models/` - SQLAlchemy models
- `app/services/` - Business logic
- `app/schemas/` - Pydantic validation schemas
- `app/database/` - Database configuration
- `app/agents/` - Agent logic
- `app/hindsight/` - Hindsight integration
- `app/document_processing/` - Document processing
- `tests/` - Test suite
- `config/` - Configuration files

## Technologies

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Python 3.10+

## API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation.
