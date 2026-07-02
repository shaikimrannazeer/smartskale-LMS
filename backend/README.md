# SmartSkale LMS Backend

FastAPI backend for SmartSkale Learning Management System.

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Redis (optional, for future modules)

### Installation

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

### Running the Application

```bash
uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Database Migrations

#### Initialize Alembic
```bash
alembic init migrations
```

#### Create a migration
```bash
alembic revision --autogenerate -m "Description"
```

#### Apply migrations
```bash
alembic upgrade head
```

### Testing

```bash
pytest
```

### Project Structure

```
app/
├── api/              # API routers
│   └── v1/          # API v1 endpoints
├── core/            # Core configuration
│   ├── config.py    # Application settings
│   ├── exceptions.py # Custom exceptions
│   └── logging.py   # Logging setup
├── db/              # Database configuration
│   └── database.py  # SQLAlchemy setup
├── middleware/      # Custom middleware
├── models/          # SQLAlchemy models
├── repositories/    # Data access layer
├── schemas/         # Pydantic schemas
├── services/        # Business logic layer
├── utils/           # Utility functions
├── tests/           # Test suite
└── main.py          # Application entry point
```

## Architecture

- **Clean Architecture**: Separation of concerns with distinct layers
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic isolation
- **Dependency Injection**: Loose coupling and testability
- **SOLID Principles**: Maintainable and scalable code
