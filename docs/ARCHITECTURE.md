# SmartSkale LMS Architecture

## Overview

SmartSkale LMS is a scalable, modular learning management system built with modern technologies.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│         http://localhost:5173                            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTP/REST
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   API Gateway                            │
│         http://localhost:8000/api/v1                    │
└──────────────────────┬──────────────────────────��───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │ Router │    │Middleware   │Exception
    │ Layer  │    │ Layer  │    │ Handler
    └────────┘    └────────┘    └────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
    ┌──────────────────────────────────┐
    │       Service Layer              │
    │  (Business Logic - Future)       │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │    Repository Layer              │
    │  (Data Access - Future)          │
    └──────────┬───────────────────────┘
               │
               ▼
    ┌──────────────────────────────────┐
    │        ORM Layer                 │
    │      SQLAlchemy 2.0              │
    └──────────┬───────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
    ┌────────┐  ┌──────────┐
    │PostgreSQL  │  Redis   │
    │ Database   │  Cache   │
    └────────┘  └──────────┘
```

## Clean Architecture Principles

The application follows Clean Architecture with distinct layers:

### 1. **API Layer** (`app/api/`)
   - Route handlers
   - Request/response validation
   - HTTP status codes

### 2. **Service Layer** (`app/services/`)
   - Business logic (future)
   - Data transformation
   - Business rules enforcement

### 3. **Repository Layer** (`app/repositories/`)
   - Data access abstraction (future)
   - Database queries
   - Cache management

### 4. **Database Layer** (`app/db/`)
   - SQLAlchemy ORM configuration
   - Database session management
   - Connection pooling

### 5. **Core Layer** (`app/core/`)
   - Configuration management
   - Exception definitions
   - Logging setup
   - Constants

## Design Patterns Used

### 1. Repository Pattern
- Abstracts data access
- Enables easy testing with mock data
- Centralizes database queries

### 2. Service Layer Pattern
- Isolates business logic
- Reusable across endpoints
- Easy to test

### 3. Dependency Injection
- Loose coupling between components
- Easy to replace dependencies for testing
- Managed by FastAPI

### 4. Factory Pattern
- Application factory in `main.py`
- Middleware and exception handler setup
- Database initialization

### 5. Middleware Pattern
- Request logging
- Security headers
- CORS handling
- Error handling

## SOLID Principles

### S - Single Responsibility
- Each module has one reason to change
- Services handle business logic
- Repositories handle data access

### O - Open/Closed
- Open for extension (new endpoints)
- Closed for modification
- Middleware and exception handlers are extensible

### L - Liskov Substitution
- Interfaces are properly defined
- Implementations can be swapped
- Mock repositories for testing

### I - Interface Segregation
- Specific interfaces over general ones
- Schema validation via Pydantic
- Service interfaces are focused

### D - Dependency Inversion
- Depend on abstractions
- FastAPI dependency injection system
- Repository abstraction

## Frontend Architecture

```
┌─────────────────────────────────────────┐
│         App Component                    │
│     (Router Setup, Query Client)         │
└─────────────────────┬───────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
        ▼                            ▼
    ┌─────────┐              ┌────────────┐
    │  Pages  │              │   Layouts  │
    │ (Views) │              │ (Structure)│
    └────┬────┘              └────────────┘
         │
    ┌────▼────────────────┐
    │   Components        │
    │  (Reusable UI)      │
    └────┬────────────────┘
         │
    ┌────┴──────────────┐
    │   Hooks           │
    │ (Logic Reuse)     │
    └────┬──────────────┘
         │
    ┌────┴──────────────────────┐
    │   State Management        │
    │ (Zustand Store)           │
    └────┬──────────────────────┘
         │
    ┌────┴──────────────────────┐
    │   API Services            │
    │ (HTTP Requests)           │
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │   Axios Instance          │
    │ (HTTP Client with Auth)   │
    └───────────────────────────┘
```

## Data Flow

### Request Flow
```
Frontend Request
    ↓
Axios Instance (with auth token)
    ↓
API Layer (FastAPI Router)
    ↓
Middleware (logging, security)
    ↓
Exception Handlers (error catching)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (data access)
    ↓
Database/Cache
    ↓
Response (JSON)
    ↓
Frontend State Management (Zustand/React Query)
    ↓
UI Re-render
```

## Security Features

1. **CORS Middleware**: Controlled cross-origin requests
2. **Security Headers**: Protection against common attacks
3. **Request Validation**: Pydantic schema validation
4. **Exception Handling**: Safe error responses
5. **Logging**: Security event tracking (future)

## Scalability Considerations

1. **Database Connection Pooling**: Efficient resource usage
2. **Caching Layer**: Redis for frequently accessed data
3. **Async/Await**: Non-blocking I/O operations
4. **Microservices Ready**: Modular structure
5. **API Versioning**: `/api/v1/` for backward compatibility
6. **Containerization**: Docker for consistent deployment

## Module Structure

### Module 1 (Current)
- Project foundation
- Basic structure
- Configuration
- Health check

### Module 2 (Future)
- Authentication & Authorization
- User management
- JWT tokens

### Module 3 (Future)
- Batch Management
- Course structure

### Module 4 (Future)
- Assignment Management
- Submission handling

### Module 5 (Future)
- AI Evaluation
- Assignment grading

### Module 6 (Future)
- Analytics
- Reporting

## Development Workflow

1. Create new feature branch
2. Implement changes following architecture
3. Write tests
4. Update documentation
5. Create pull request
6. Code review
7. Merge to main

## Deployment

The application is containerized for easy deployment:

```bash
docker-compose up --build
```

This starts:
- PostgreSQL database
- Redis cache
- FastAPI backend
- React frontend
