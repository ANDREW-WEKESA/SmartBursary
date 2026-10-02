# SmartBursary — Complete System Starter

A full-stack implementation starter based on the supplied SmartBursary HTML prototype and Software Requirements Specification. It keeps the original workflow and four bursary-program examples while adding a React/Vite interface, a FastAPI API, persistent SQL database models, authentication, uploads, review actions, audit logs, notifications and CSV reporting.

## Stack

- **Frontend:** React + Vite, responsive CSS, accessible form controls
- **Backend:** FastAPI + SQLAlchemy 2
- **Database:** SQLite by default for local development; PostgreSQL via `DATABASE_URL` for deployment
- **Authentication:** JWT bearer tokens, Argon2 password hashing, role-based API access
- **Documents:** PDF/JPG/JPEG/PNG, 5 MB default cap, generated storage names, owner/staff access checks

## Run locally (Windows PowerShell)

Open two terminals.

### 1. Backend

```powershell
cd .\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

The first startup creates database tables, inserts the four example bursary programs and creates the administrator specified in `.env`.

**Local demo administrator** (change these values in `backend/.env` before use):

- Email: `admin@smartbursary.com`
- Password: `ChangeMe123!`

API docs: http://127.0.0.1:8000/docs  
Health check: http://127.0.0.1:8000/api/health

### 2. Frontend

```powershell
cd .\frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open http://localhost:5173. The API defaults to `http://127.0.0.1:8000/api`.

## PostgreSQL

Install PostgreSQL and its Python driver (`pip install psycopg[binary]`), then set this in `backend/.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://smartbursary:YOUR_PASSWORD@localhost:5432/smartbursary
```

Create the database/user first. For production, use a managed PostgreSQL service, migrations (Alembic), HTTPS, managed secret storage, private document storage and automated backups.

## Roles and demo security

- `applicant`: register, browse programs, submit applications, view only their own applications, upload and download their own documents, read their notifications.
- `reviewer`: review applications, update statuses and verify documents.
- `admin`: reviewer permissions plus create/update bursary programs, view audit logs and reporting endpoints.
- Public self-registration always creates an `applicant`. Create additional staff accounts through a controlled admin provisioning process; do not promote users by editing client-side state.

The demo admin is created from environment variables on the first startup. Set a strong unique `SECRET_KEY` and change the demo admin password before deployment. Existing demo admin accounts are not automatically reset when environment values change.

## Implemented API surface

- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `POST /api/admin/users` (admin-only provisioning of `admin` or `reviewer` accounts; password minimum 12 characters)
- `GET /api/bursaries`, `POST /api/bursaries`, `PATCH /api/bursaries/{id}`
- `POST /api/applications`, `GET /api/applications`, `GET /api/applications/{application_number}`
- `PATCH /api/applications/{application_number}/status`
- `POST /api/applications/{application_number}/documents`
- `GET /api/documents/{id}/download`, `PATCH /api/documents/{id}/verification?status=Verified`
- `GET /api/dashboard/stats`, `GET /api/reports/applications.csv`, `GET /api/audit`
- `GET /api/notifications`, `PATCH /api/notifications/{id}/read`

## Important limitations before real deployment

1. The AI-style priority score is a **transparent demonstration heuristic**, not a trained AI model, eligibility determination or award decision. Duplicate matching flags a shared student number or national ID for human verification. Review criteria should be approved by the bursary provider and assessed for bias before operational use.
2. The SRS mentions draft saving, reviewer assignment, richer reporting, OCR/document analysis and email/SMS notifications. Those integrations are not fully implemented in this starter. In-app notifications are implemented; external delivery needs a provider and configuration.
3. The current schema uses `create_all` for a quick local start, not database migrations. Use Alembic before evolving production schema.
4. Uploads are stored locally in `backend/uploads`. Production should use private object storage, malware scanning, retention policies, file-content validation and backups.
5. This starter does not claim legal/compliance certification. Before live use, complete security review, privacy notice/consent, access review, audit retention, rate limiting, CSRF strategy where relevant, monitoring, recovery tests and accessibility testing.
6. Demo program names, amounts, criteria, and dates are examples inherited from the supplied prototype. Confirm all details with the actual bursary provider before publishing. Dates in the past are treated as closed by the UI/API.

## Project layout

```text
SmartBursary-Complete/
  frontend/                  React + Vite app
    src/App.jsx              Applicant and staff workflows
    src/api.js               Authenticated API client
    src/styles.css           Responsive light/dark design
  backend/
    app/main.py              API routes, seed data and startup
    app/models.py            SQLAlchemy entities
    app/schemas.py           Request/response validation
    app/security.py          JWT, password hashing, roles
    app/database.py          Database session configuration
    .env.example              Local configuration template
  reference-SmartBursary.html Original supplied prototype
  SmartBursary-Requirements.pdf  Original supplied SRS
```
