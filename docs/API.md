# SmartSkale LMS - API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Health Check

### Endpoint

```
GET /health
```

### Response

```json
{
  "status": "healthy",
  "application": "SmartSkale LMS",
  "version": "1.0.0"
}
```

### Status Codes

- `200 OK` - Server is healthy

## Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error message",
  "error_code": "ERROR_CODE",
  "details": {}
}
```

## Authentication (Future)

Authentication will be implemented in Module 2.

## Rate Limiting (Future)

Rate limiting will be implemented in a future module.
