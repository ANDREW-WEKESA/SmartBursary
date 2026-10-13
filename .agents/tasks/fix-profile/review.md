# Profile column migration endpoints

Adds three admin-only endpoints to fix production database schema drift. The `/api/profile` endpoint failed with 500 errors because the production database was missing columns (`ward`, `county`, guardian fields, document flags) that exist in the User model. The fix provides idempotent ALTER TABLE migrations that admins can call to add missing columns without data loss. Each endpoint wraps ALTER statements in try-except blocks and returns detailed success/failure counts.

**Watch for:** (confirmed) Redundant local `text` import inside each function when `text` is already imported at the module level. (confirmed) `/api/setup/db-columns` returns column data but the query is not database-agnostic (PostgreSQL-specific `information_schema` query will fail on SQLite). (confirmed) Missing defensive error handling in `/api/profile` endpoints—users will see cryptic 500 errors if they access the endpoint before running migrations.

**Verdict**: NEEDS_CHANGES

## High-level view

Three endpoints were added: `/add-ward-column` adds 20 profile-related columns (location, guardian, education, personal, documents, financial), `/db-columns` lists current table columns from `information_schema`, and `/run-all-migrations` combines login-tracking columns with the 20 profile columns for a total of 22 migrations. All three are gated behind `require_roles("admin")` and use `text()` for raw SQL execution.

Each ALTER TABLE statement uses `IF NOT EXISTS`, making the endpoints safe to call repeatedly. The migration loop commits after each successful column addition and rolls back on error, continuing to the next column. This per-column error handling means a partially-failed migration can be re-run to complete the remaining columns.

The `/db-columns` diagnostic endpoint queries `information_schema.columns` directly, which works on PostgreSQL but not SQLite. This will break local development environments using SQLite, though the production target is PostgreSQL so the endpoint will work where it matters most.

The module-level import includes `text` from sqlalchemy (line 8), but each of the three new functions re-imports `text` locally with `from sqlalchemy import text` (lines 1577, 1632, 1656). The redundant imports don't break anything but clutter the functions.

## Issues (3)

1. **Redundant local text imports** — `text` is imported at module level (line 8) but re-imported inside each function (lines 1577, 1632, 1656). Remove the local imports and use the module-level import.

2. **SQLite incompatibility in /db-columns** — The diagnostic endpoint queries `information_schema.columns`, which is PostgreSQL-specific. Local development using SQLite will fail with "no such table: information_schema.columns". Either document that this endpoint only works on PostgreSQL, or add a database-agnostic fallback using SQLAlchemy's inspector API.

3. **Missing defensive error handling** — The plan called for wrapping `/api/profile` GET and PATCH endpoints in try-except blocks to catch column-missing errors and return helpful messages. This was not implemented. Users hitting `/api/profile` before running the migration will see cryptic 500 errors instead of guidance to run `/api/setup/run-all-migrations`.

<details>
<summary>Details</summary>

## Idempotent migration strategy

Each endpoint follows the same pattern: a list of `(column_name, ALTER TABLE ... IF NOT EXISTS)` tuples, a loop that executes each SQL statement with `text()`, individual try-except blocks that catch column-add failures, and a final response that separates successful from failed columns. The `IF NOT EXISTS` clause is critical for idempotency—the migration can be called multiple times without error.

The per-column commit/rollback approach (confirmed at lines 1605-1609 in `/add-ward-column`) means one column's failure doesn't abort the entire migration. An admin can call the endpoint, see which columns failed, fix the underlying issue (e.g., type conflict, constraint violation), and re-run the endpoint to retry just the failed columns. This is more robust than a single transaction that would roll back all columns on the first error.

The `/run-all-migrations` endpoint (lines 1649-1713) duplicates the column definitions from `/add-ward-column` (lines 1577-1622) but adds two login-tracking columns (`last_login`, `login_count`) at the beginning. This creates a single endpoint that applies all known schema updates, though it also means the column definitions exist in two places. If a future column is added to one endpoint but not the other, they'll drift.

## Diagnostic endpoint database specificity

The `/api/setup/db-columns` endpoint (lines 1625-1646) queries `information_schema.columns WHERE table_name = 'users'` to list all columns in the users table. This works on PostgreSQL (the production database per the README) but fails on SQLite (the local development default per README line 103: "SQLite for quick local start"). When run on SQLite, the query returns an error: `no such table: information_schema.columns`.

The endpoint is intended for production diagnostics (confirmed by the docstring: "Shows what columns actually exist in the production database"), so the PostgreSQL-only behavior may be acceptable. However, an admin testing locally before calling it in production will see the endpoint fail, which could erode confidence in the fix. A database-agnostic alternative would use SQLAlchemy's `Inspector` API: `from sqlalchemy import inspect; inspector = inspect(db.get_bind()); columns = inspector.get_columns('users')`.

## Missing defensive error handling in profile endpoints

The plan called for adding defensive error handling to the `/api/profile` GET and PATCH endpoints (plan item 2: "Wrap the `/api/profile` GET endpoint in try-except block"), but that was not implemented. The diff shows only additions at the end of `main.py` (lines 1566-1713); the profile endpoints earlier in the file remain unchanged. If the migration endpoints are not called before a user accesses `/api/profile`, the endpoint will still return cryptic 500 errors instead of helpful messages directing admins to run the migration.

</details>

<details>
<summary>File map</summary>

- **backend/app/main.py** — Added `text` import to existing imports (line 8); added three new admin-only setup endpoints: `/api/setup/add-ward-column` (20 profile columns), `/api/setup/db-columns` (diagnostic column list), `/api/setup/run-all-migrations` (22 columns total).

Full diff: `git diff HEAD~1 HEAD`

</details>
