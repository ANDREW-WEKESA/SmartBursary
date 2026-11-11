# SmartBursary API Documentation

## Base URL
- **Production:** `https://smartbursary-backend.onrender.com/api`
- **Local:** `http://localhost:8000/api`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

---

## Authentication Endpoints

### Register New User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "id_number": "12345678",
  "phone_number": "0712345678",
  "constituency": "Nairobi",
  "ward": "Central Ward"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "applicant"
}
```

---

### Login
**POST** `/auth/login`

Authenticate and receive access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## User Profile Endpoints

### Get Profile
**GET** `/profile`

Get current user's profile.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "constituency": "Nairobi",
  "profile_complete": true,
  ...
}
```

---

### Update Profile
**PATCH** `/profile`

Update user profile information.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "institution": "University of Nairobi",
  "student_number": "S20/12345/2023",
  "course": "Computer Science",
  "year_of_study": "Year 2",
  "national_id": "12345678",
  "monthly_household_income": 15000,
  "household_size": 5,
  "date_of_birth": "2002-05-15",
  "gender": "Male"
}
```

**Response:** `200 OK`

---

## Bursary Endpoints

### List All Bursaries
**GET** `/bursaries`

Get all active bursaries (filtered by user's constituency for applicants).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Nairobi CDF Bursary 2026",
    "description": "Constituency Development Fund bursary...",
    "constituency": "Nairobi",
    "amount_kes": 20000,
    "deadline": "2027-03-31",
    "active": true
  }
]
```

---

### Get Bursary Details
**GET** `/bursaries/{id}`

Get detailed information about a specific bursary.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

## Application Endpoints

### Submit Application
**POST** `/applications`

Submit a new bursary application.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "bursary_id": 1,
  "institution": "University of Nairobi",
  "student_number": "S20/12345/2023",
  "national_id": "12345678",
  "monthly_household_income": 15000,
  "household_size": 5,
  "course": "Computer Science",
  "year_of_study": "Year 2",
  "reason": "I need financial assistance to continue my studies..."
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "application_number": "SB-2026-00001",
  "status": "Submitted",
  "priority_score": 75,
  "submitted_at": "2026-10-02T10:30:00"
}
```

---

### Get My Applications
**GET** `/applications/my`

Get all applications submitted by current user.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "application_number": "SB-2026-00001",
    "bursary_name": "Nairobi CDF Bursary 2026",
    "status": "Under Review",
    "priority_score": 75,
    "submitted_at": "2026-10-02T10:30:00"
  }
]
```

---

### Get Application Details
**GET** `/applications/{application_number}`

Get detailed information about a specific application.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

## Admin Endpoints

### Get All Applications (Admin/Reviewer)
**GET** `/admin/applications`

Get all applications (filtered by constituency for reviewers).

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `status`: Filter by status (optional)
- `constituency`: Filter by constituency (optional)
- `skip`: Pagination offset (default: 0)
- `limit`: Results per page (default: 50)

**Response:** `200 OK`

---

### Update Application Status (Admin/Reviewer)
**PATCH** `/admin/applications/{application_number}`

Update application status and add review comments.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "status": "Approved",
  "reviewer_comment": "Application approved. All documents verified."
}
```

**Response:** `200 OK`

---

### Get Statistics (Admin)
**GET** `/admin/statistics`

Get system-wide statistics dashboard.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "total_applications": 1234,
  "pending_applications": 456,
  "approved_applications": 678,
  "total_bursaries": 294,
  "total_applicants": 890
}
```

---

## Setup Endpoints (Production Only)

### Seed Constituencies
**GET** `/setup/seed-constituencies`

Seed all 290 Kenya constituencies (one-time setup).

**Response:** `200 OK`

---

### Create Admin Account
**GET** `/setup/create-admin`

Create default admin account (one-time setup).

**Response:** `200 OK`

---

### Promote to Reviewer
**GET** `/setup/promote-reviewer?email=user@example.com`

Promote a user to reviewer role.

**Query Parameters:**
- `email`: User email to promote

**Response:** `200 OK`

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Please complete your profile before applying for bursaries"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limiting

- Production API is rate-limited to prevent abuse
- Limit: 100 requests per minute per IP
- Exceeded limit returns `429 Too Many Requests`

---

## CORS

- Frontend origins are whitelisted
- Allowed methods: GET, POST, PUT, PATCH, DELETE
- Credentials are supported

---

## Notes

1. All dates are in ISO 8601 format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`
2. All monetary amounts are in Kenyan Shillings (KES)
3. Application numbers follow format: `SB-YYYY-NNNNN`
4. Profile must be complete (95%+) before applying for bursaries
5. Document uploads use multipart/form-data

---

Last Updated: October 2, 2026
