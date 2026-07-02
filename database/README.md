# Database Migrations Directory

This directory will contain Alembic migrations for the SmartSkale LMS database.

## Setup

Alembic is configured but no migrations have been created yet. Migrations will be created in future modules when database models are implemented.

## Commands

### Initialize Alembic (if needed)
```bash
cd ../backend
alembic init migrations
```

### Create a migration
```bash
alembic revision --autogenerate -m "Description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migrations
```bash
alembic downgrade -1
```
