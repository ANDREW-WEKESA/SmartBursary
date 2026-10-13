# Implementation Plan: Fix Profile Endpoint Infinite Loading

## Root Cause Analysis

The production PostgreSQL database on Render is missing several columns that were added to the User model after initial deployment. Specifically:

**Confirmed missing columns from /api/setup/add-login-columns endpoint**:
- `last_login` (TIMESTAMP)
- `login_count` (INTEGER DEFAULT 0)
- `ward` (VARCHAR(100) DEFAULT '')

**Potentially missing columns** (added to models.py after initial deployment but never migrated):
- `county` (VARCHAR(100) DEFAULT '')
- `sub_county` (VARCHAR(100) DEFAULT '')
- `address` (TEXT DEFAULT '')
- `guardian_name` (VARCHAR(160) DEFAULT '')
- `guardian_phone` (VARCHAR(40) DEFAULT '')
- `guardian_relationship` (VARCHAR(50) DEFAULT '')
- `has_national_id_doc` (BOOLEAN DEFAULT FALSE)
- `has_student_id_doc` (BOOLEAN DEFAULT FALSE)
- `has_admission_letter` (BOOLEAN DEFAULT FALSE)

The `/api/profile` GET endpoint at line 435-437 in main.py executes a SQLAlchemy SELECT query with `joinedload(User.profile_documents)`. When SQLAlchemy tries to read these missing columns, PostgreSQL returns an error that causes the endpoint to return 500, which the frontend interprets as infinite loading.

The existing `/api/setup/add-login-columns` endpoint (lines 1376-1417) demonstrates the safe migration pattern: using raw SQL `ALTER TABLE` with try-except blocks that silently handle "column already exists" errors. However, this endpoint only adds 3 columns and doesn't add ALL the missing profile-related columns.

## Implementation Plan

- [ ] 1. **Create comprehensive migration endpoint** at `/api/setup/add-profile-columns` in backend/app/main.py after the existing `/api/setup/add-login-columns` endpoint (around line 1418).
      
      Add ALTER TABLE statements for ALL potentially-missing User table columns: `county`, `sub_county`, `ward`, `address`, `guardian_name`, `guardian_phone`, `guardian_relationship`, `has_national_id_doc`, `has_student_id_doc`, `has_admission_letter`, `last_login`, `login_count`. Each ALTER statement wrapped in try-except to silently skip if column exists. Return JSON response with success status and list of columns processed.
      
      **Files**: `backend/app/main.py`
      
      **Verify**: Start the backend locally with `uvicorn app.main:app --reload --port 8000` from backend directory, navigate to http://127.0.0.1:8000/docs and test the new `/api/setup/add-profile-columns` endpoint returns 200 with success message.

- [ ] 2. **Add defensive error handling to profile endpoints** in backend/app/main.py.
      
      Wrap the `/api/profile` GET endpoint (lines 435-437) in a try-except block that catches SQLAlchemy errors and returns a helpful error message directing the user to run the migration endpoint. Similarly add error handling to `/api/profile` PATCH endpoint (lines 439+) to catch column-missing errors during UPDATE operations.
      
      **Files**: `backend/app/main.py`
      
      **Verify**: Start the backend locally, make a GET request to `/api/profile` with a valid token. Endpoint should return user profile data successfully (200 status) or a clear error message (not 500).

- [ ] 3. **Update the existing `/api/setup/add-login-columns` endpoint** in backend/app/main.py (lines 1376-1417).
      
      Since this endpoint already adds `ward` (line 1405-1410) but may have been called before `ward` was added to the code, ensure it remains idempotent. Add a deprecation notice in the docstring pointing users to the new comprehensive `/api/setup/add-profile-columns` endpoint. Keep this endpoint for backward compatibility.
      
      **Files**: `backend/app/main.py`
      
      **Verify**: Start the backend, navigate to http://127.0.0.1:8000/docs, check that both setup endpoints exist and have clear documentation.

- [ ] 4. **Add migration instructions to README.md**.
      
      Add a new "Production Database Migrations" section after the "PostgreSQL" section (around line 50). Document the `/api/setup/add-profile-columns` endpoint, when to use it (after deployment when profile endpoint returns errors), and the safety guarantees (idempotent, won't drop data, safe to run multiple times). Include the full URL for Render production: `https://smartbursary-backend.onrender.com/api/setup/add-profile-columns`.
      
      **Files**: `README.md`
      
      **Verify**: Read README.md and confirm the new section is clear, positioned correctly, and includes the production URL.

- [ ] 5. **Create deployment verification script** at `backend/verify_deployment.py`.
      
      Python script that tests the production /api/health endpoint and /api/profile endpoint (with a test user token from environment variable `TEST_USER_TOKEN`). Script exits 0 if both succeed, exits 1 with error details if either fails. This script can be run after calling the migration endpoint to confirm the fix worked.
      
      **Files**: `backend/verify_deployment.py` (new file)
      
      **Verify**: Run `python backend/verify_deployment.py` locally (will fail without valid production token, but should show clear error message, not crash). Check the script has proper argument handling and help text.

- [ ] 6. **Update ProfileOut schema validation** in backend/app/schemas.py (lines 52-59).
      
      The ProfileOut schema includes fields like `county`, `sub_county`, `ward`, which must match the User model exactly. Review that all fields in ProfileOut have correct types matching models.py, especially the new guardian_* fields and document flags. Ensure `from_attributes=True` in model_config (already present at line 59) so Pydantic can serialize SQLAlchemy models even if some fields are missing (falls back to model defaults).
      
      **Files**: `backend/app/schemas.py`
      
      **Verify**: Start backend, create a test user with incomplete profile, call GET /api/profile - should return profile with empty strings for missing fields, not crash.

## Production Deployment Steps (User Action Required)

After implementing the above changes and deploying to Render:

1. Call the migration endpoint: `GET https://smartbursary-backend.onrender.com/api/setup/add-profile-columns`
2. Verify the response shows success and lists all columns processed
3. Test the profile endpoint: Login as a user and navigate to profile page - should load without infinite spinner
4. Optional: Run the verification script with a test user token

## Design Decisions

**Decision 1: Use raw SQL ALTER TABLE instead of SQLAlchemy migrations (Alembic)**

Rationale: The codebase already uses this pattern in `/api/setup/add-login-columns` (line 1376+). The README.md notes "The current schema uses `create_all` for a quick local start, not database migrations" (line 103). Introducing Alembic would require significant refactoring and doesn't match the project's "quick starter" philosophy. Raw SQL with IF NOT EXISTS-style error handling is simpler, more transparent, and matches existing patterns.

**Decision 2: Create a new comprehensive migration endpoint instead of modifying existing one**

Rationale: The existing `/api/setup/add-login-columns` endpoint name implies it only adds login-tracking columns. Creating a new `/api/setup/add-profile-columns` endpoint with a clear name makes it easier for users to understand what it does. We keep the old endpoint for backward compatibility (some production instances may have already called it).

**Decision 3: Add defensive error handling to profile endpoints instead of making migration mandatory**

Rationale: Profile endpoints should fail gracefully with helpful messages if columns are missing, not with cryptic 500 errors. This follows the "transparent demonstration" principle seen throughout the codebase. Users can continue using other features while the migration is pending.

**Decision 4: Use try-except blocks that silently skip existing columns**

Rationale: This makes the migration endpoint idempotent (safe to run multiple times), which is critical for a production system where we can't guarantee the endpoint hasn't been called before. The pattern is already established in `/api/setup/add-login-columns` lines 1389-1415.

**Decision 5: Add all guardian_* and has_*_doc fields even though they may not be missing**

Rationale: The User model in models.py includes these fields (lines 26-27, 37-39), but we cannot be certain when they were added relative to production deployment. Adding them to the migration is zero-risk (try-except will skip if they exist) and ensures completeness. The alternative—manually inspecting production DB—is not accessible to this workflow.

**Decision 6: Document migration in README instead of creating separate MIGRATION.md**

Rationale: The project follows a single-README pattern (no CONTRIBUTING.md, AGENTS.md, or similar). The README already has setup instructions and production notes, so adding migration instructions there keeps documentation centralized and discoverable.

## Verification Strategy

Each step includes inline verification using the project's actual commands:
- Backend: `uvicorn app.main:app --reload --port 8000` (from README line 31)
- API docs: http://127.0.0.1:8000/docs (from README line 35)
- Manual endpoint testing through FastAPI docs UI

No automated test suite exists in this codebase (no pytest, no test runner in package.json), so verification relies on manual testing and observation of HTTP responses.

## Files to Modify

1. `backend/app/main.py` - Add migration endpoint, defensive error handling (items 1, 2, 3)
2. `README.md` - Add migration documentation (item 4)
3. `backend/verify_deployment.py` - New verification script (item 5)
4. `backend/app/schemas.py` - Review and ensure ProfileOut matches model (item 6)

## Risk Assessment

**Low risk**: Changes are additive (new endpoint, new error handling). Existing functionality remains unchanged. Migration endpoint is idempotent and uses the established pattern from the codebase.

**One caveat**: If production database has OTHER columns missing beyond those in current models.py (e.g., a very old deployment missing `institution`, `student_number`, etc.), those will need to be identified separately. However, the task hypothesis specifically targets recently-added columns (ward, county, sub_county, guardian_*, document flags) based on the CORS errors showing the site is otherwise functional.
