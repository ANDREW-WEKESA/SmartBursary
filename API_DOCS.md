# SmartBursary API Documentation

## Base URL
- Local: `http://localhost:8000/api`
- Production: `https://smartbursary-backend.onrender.com/api`

## Authentication

All authenticated endpoints require a JWT bearer token.

### Login
```http
POST /auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Register
```http
POST /auth/register
{
  "full_name": "John Doe",
  "email": "user@example.com",
  "password": "password123",
  "phone": "0712345678"
}
```

## Bursaries

### List Bursaries
```http
GET /bursaries
```

### Create Bursary (Admin)
```http
POST /bursaries
{
  "name": "Test Bursary",
  "constituency": "Westlands",
  "amount_kes": 20000
}
```

## Applications

### Submit Application
```http
POST /applications
{
  "bursary_id": 1,
  "student_name": "John Doe"
}
```

### Update Status (Reviewer/Admin)
```http
PATCH /applications/{id}/status
{
  "status": "approved"
}
```

## Status Codes
- 200 - Success
- 401 - Unauthorized
- 403 - Forbidden
- 404 - Not Found
