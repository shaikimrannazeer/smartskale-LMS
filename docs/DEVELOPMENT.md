# SmartSkale LMS - Development Guide

## Project Setup

### Prerequisites

- Git
- Docker & Docker Compose
- Python 3.12 (for local backend development)
- Node.js 18+ (for local frontend development)

### Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/yourusername/smartskale-lms.git
cd smartskale-lms

# Start all services
docker-compose up --build
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### Local Development Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Start with local PostgreSQL:
```bash
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
```

Start development server:
```bash
npm run dev
```

## Code Structure

### Backend Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── health.py       # Health check endpoint
│   ├── core/
│   │   ├── config.py           # Settings from .env
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── logging.py           # Logger setup
│   ├── db/
│   │   └── database.py          # SQLAlchemy configuration
│   ├── middleware/
│   │   ├── request_logger.py    # Request logging
│   │   └── security_headers.py  # Security headers
│   ├── models/                  # SQLAlchemy models (future)
│   ├── schemas/                 # Pydantic schemas (future)
│   ├── services/                # Business logic (future)
│   ├── repositories/            # Data access (future)
│   ├── utils/
│   │   └── response.py          # Response formatting
│   ├── tests/
│   │   ├── conftest.py          # Pytest configuration
│   │   └── test_health.py       # Health check tests
│   └── main.py                  # Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

### Frontend Structure

```
frontend/
├── src/
│   ├── assets/                  # Images, fonts
│   ├── components/
│   │   ├── Navbar.tsx           # Navigation bar
│   │   ├── Sidebar.tsx          # Side navigation
│   │   └── Footer.tsx           # Footer
│   ├── layouts/
│   │   └── DefaultLayout.tsx    # Main layout
│   ├── pages/
│   │   └── HomePage.tsx         # Home page
│   ├── hooks/
│   │   └── useHealthCheck.ts    # Health check hook
│   ├── services/
│   │   ├── api.ts               # Axios instance
│   │   └── health.ts            # Health service
│   ├── store/
│   │   └── appStore.ts          # Zustand store
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── utils/
│   │   └── formatting.ts        # Utility functions
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

## Coding Standards

### Python Backend

#### Style Guide
- Follow PEP 8
- Use type hints for all functions
- Use docstrings for modules, classes, and functions
- Max line length: 88 characters (Black)

#### Example:
```python
"""Module description."""

from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    """User schema."""
    
    id: str
    name: str
    email: str
    
    def get_display_name(self) -> str:
        """Get user display name.
        
        Returns:
            Formatted display name
        """
        return self.name.title()
```

#### Architecture Patterns

1. **Service Layer**
```python
class UserService:
    """User business logic."""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def create_user(self, data: UserCreate) -> User:
        # Business logic
        return self.repo.create(data)
```

2. **Repository Pattern**
```python
class UserRepository:
    """User data access."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, data: UserCreate) -> User:
        # Database query
        pass
```

### TypeScript Frontend

#### Style Guide
- Use TypeScript strict mode
- Proper type annotations
- Use functional components
- Use React hooks
- CSS modules or Tailwind

#### Example:
```typescript
import { FC, useState } from 'react';

interface Props {
  title: string;
  onSubmit: (value: string) => void;
}

export const Form: FC<Props> = ({ title, onSubmit }) => {
  const [value, setValue] = useState<string>('');
  
  const handleSubmit = () => {
    onSubmit(value);
  };
  
  return (
    <div>
      <h1>{title}</h1>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};
```

## Testing

### Backend Testing

```bash
cd backend
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest app/tests/test_health.py # Run specific test
pytest --cov=app               # With coverage
```

### Frontend Testing

```bash
cd frontend
npm test                        # Run tests (when configured)
npm run type-check              # TypeScript check
npm run lint                    # Linting
```

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

### Commit Messages
```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: Add user authentication

Implement JWT-based authentication with refresh tokens.
- Add auth router
- Add JWT utilities
- Add auth middleware

Closes #123
```

## Common Tasks

### Adding a New API Endpoint

1. Create schema in `app/schemas/`
2. Create model in `app/models/` (if needed)
3. Create repository in `app/repositories/` (if needed)
4. Create service in `app/services/`
5. Create router in `app/api/v1/`
6. Include router in `app/main.py`
7. Add tests in `app/tests/`
8. Update documentation

### Adding a New Frontend Page

1. Create component in `src/pages/`
2. Create route in `src/App.tsx`
3. Create service if needed in `src/services/`
4. Create store if needed in `src/store/`
5. Add components in `src/components/` if needed
6. Add types in `src/types/`
7. Update navigation in components

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
# Docker: docker-compose logs db
# Local: psql -U postgres -d smartskale
```

### API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Test health endpoint
curl http://localhost:8000/api/v1/health
```

### Frontend Build Issues
```bash
# Clear node modules and reinstall
rm -rf node_modules
npm install

# Clear build cache
rm -rf dist
npm run build
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
