# SmartBursary Deployment Guide

This guide covers deploying SmartBursary to production using Render (backend) and Vercel (frontend).

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Production Migration Steps](#production-migration-steps)
3. [Render Backend Deployment](#render-backend-deployment)
4. [Vercel Frontend Deployment](#vercel-frontend-deployment)
5. [Environment Variables Reference](#environment-variables-reference)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting Common Issues](#troubleshooting-common-issues)
8. [Rollback Procedures](#rollback-procedures)

---

## Pre-Deployment Checklist

Before deploying to production, ensure you have:

- [ ] **Database Backup**: Created a backup of your production database (if upgrading an existing deployment)
- [ ] **Environment Variables Review**: Verified all required environment variables are set correctly
- [ ] **CORS Configuration**: Confirmed `CORS_ORIGINS` includes your Vercel frontend URL
- [ ] **Security Settings Check**:
  - [ ] `SECRET_KEY` is a strong, random value (not the development default)
  - [ ] `ADMIN_PASSWORD` is secure and documented
  - [ ] `POSTGRES_PASSWORD` is secure (if self-hosting database)
  - [ ] No sensitive credentials are committed to version control
- [ ] **Migration Script Ready**: `run_production_migration.py` is in your backend directory

---

## Production Migration Steps

### What the Migration Does

The `run_production_migration.py` script adds three new columns to the production database:
- `ward` (String) - Stores user's ward information
- `last_login` (DateTime) - Tracks when user last logged in
- `login_count` (Integer) - Counts total user logins

**Why this is needed**: The production database schema was out of sync with the application code, causing login failures with "no such column" errors.

### Running the Migration on Render

1. **Via Render Shell** (Recommended):
   ```bash
   # In Render Dashboard:
   # 1. Go to your backend service
   # 2. Click "Shell" tab
   # 3. Run the following command:
   python run_production_migration.py
   ```

2. **Via One-Off Job**:
   - In Render Dashboard, go to your service
   - Click "Manual Deploy" → "Clear build cache & deploy"
   - Or create a one-off job that runs the migration script

3. **Expected Output**:
   ```
   Starting production migration...
   Adding missing columns to users table...
   ✓ Added ward column
   ✓ Added last_login column
   ✓ Added login_count column
   Migration completed successfully!
   ```

### Verify Migration Success

After running the migration, verify it worked:

```bash
# In Render Shell:
python -c "from app.database import engine; from sqlalchemy import inspect; inspector = inspect(engine); print([c['name'] for c in inspector.get_columns('users')])"
```

You should see `ward`, `last_login`, and `login_count` in the column list.

### Rollback Instructions

If the migration fails or causes issues:

1. **Restore from Backup** (if you have one):
   - In Render PostgreSQL dashboard, restore from the backup created before migration

2. **Manual Rollback** (if no backup):
   ```sql
   -- Connect to your Render PostgreSQL database
   -- Run these SQL commands:
   ALTER TABLE users DROP COLUMN IF EXISTS ward;
   ALTER TABLE users DROP COLUMN IF EXISTS last_login;
   ALTER TABLE users DROP COLUMN IF EXISTS login_count;
   ```

3. **Revert Code**:
   - Roll back to the previous deployment in Render
   - Update your codebase to match the database schema

---

## Render Backend Deployment

### Current Production URL
- **Backend API**: https://smartbursary-backend.onrender.com

### Initial Setup

1. **Create Render Account**: Sign up at https://render.com

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the branch to deploy (e.g., `main`)

3. **Configure Service**:
   - **Name**: `smartbursary-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or specify if backend is in subdirectory)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Create PostgreSQL Database**:
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - **Name**: `smartbursary-db`
   - **Database**: `smartbursary`
   - **User**: `smartbursary_user`
   - **Region**: Same as your web service
   - **Plan**: Choose based on needs (Free tier available for testing)

### Required Environment Variables

Set these in Render Dashboard → Your Service → Environment:

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | *Auto-set by Render* | Connect your PostgreSQL database |
| `SECRET_KEY` | `<generate-random-string>` | **CRITICAL**: Use a secure random key |
| `CORS_ORIGINS` | `https://your-app.vercel.app` | Replace with your actual Vercel URL |
| `ADMIN_EMAIL` | `admin@smartbursary.com` | Default admin account email |
| `ADMIN_PASSWORD` | `<secure-password>` | **CRITICAL**: Change from default |
| `REVIEWER_EMAIL` | `reviewer@smartbursary.com` | Default reviewer account email |
| `REVIEWER_PASSWORD` | `<secure-password>` | **CRITICAL**: Change from default |

**Important**: 
- Generate `SECRET_KEY` using: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- After deployment, you'll get the Vercel URL and need to update `CORS_ORIGINS`

### Finding Your Vercel URL

After deploying the frontend:
1. Go to Vercel Dashboard
2. Click your project
3. Copy the production URL (e.g., `https://smart-bursary-abc123.vercel.app`)
4. Go back to Render → Your Service → Environment
5. Update `CORS_ORIGINS` to include this URL

### Example CORS Configuration

```
CORS_ORIGINS=https://smart-bursary-abc123.vercel.app,https://smartbursary.vercel.app
```

Multiple origins are comma-separated. Include both preview and production URLs if needed.

### Connecting PostgreSQL Database

1. In Render Dashboard, go to your Web Service
2. Click "Environment" tab
3. Click "Add Environment Variable"
4. For `DATABASE_URL`:
   - Click "Add from database"
   - Select your PostgreSQL database
   - Choose "Internal Database URL" for better performance

Render will automatically populate the connection string.

### How to Trigger Redeployment

**Automatic** (recommended):
- Push to your connected GitHub branch
- Render automatically builds and deploys

**Manual**:
- Go to Render Dashboard → Your Service
- Click "Manual Deploy" → "Deploy latest commit"
- Or "Clear build cache & deploy" if you need a fresh build

### How to Access Logs

1. Go to Render Dashboard
2. Click your backend service
3. Click "Logs" tab
4. View real-time logs or search historical logs

**Useful log commands**:
- Filter by keyword using the search box
- Download logs for offline analysis
- Set up log alerts for errors

### Running the Migration Script on Render

**Method 1: Shell Access**:
```bash
# In Render Dashboard → Your Service → Shell tab:
python run_production_migration.py
```

**Method 2: One-Time Job** (if shell isn't available on your plan):
- Create a file `migrate.sh` in your repo:
  ```bash
  #!/bin/bash
  python run_production_migration.py
  ```
- Deploy, then run it via Render's job feature

---

## Vercel Frontend Deployment

### Current Setup
- **GitHub Repository**: https://github.com/ANDREW-WEKESA/SmartBursary.git
- **Production URL**: Will be assigned by Vercel (e.g., `https://smart-bursary.vercel.app`)

### Initial Setup

1. **Create Vercel Account**: Sign up at https://vercel.com

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import from GitHub: `ANDREW-WEKESA/SmartBursary`
   - Vercel will detect it as a Vite project

3. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (or specify if frontend is in subdirectory)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Required Environment Variable

Set this in Vercel Dashboard → Your Project → Settings → Environment Variables:

| Variable | Value | Production | Preview | Development |
|----------|-------|------------|---------|-------------|
| `VITE_API_URL` | `https://smartbursary-backend.onrender.com/api` | ✓ | ✓ | ✓ |

**Important**: 
- This tells the frontend where to send API requests
- Must match your Render backend URL
- Must end with `/api` (the API prefix)

### Finding the Vercel Deployment URL

After your first deployment:

1. Go to Vercel Dashboard
2. Click your project name
3. Your production URL is displayed at the top
4. Copy this URL (e.g., `https://smart-bursary-abc123.vercel.app`)

**Next Step**: Update your Render backend's `CORS_ORIGINS` environment variable with this URL.

### How to Trigger Redeployment

**Automatic** (recommended):
- Push to your `main` branch on GitHub
- Vercel automatically builds and deploys

**Manual**:
- Go to Vercel Dashboard → Your Project
- Click "Deployments" tab
- Click "..." menu on any deployment → "Redeploy"

### Custom Domain (Optional)

To use a custom domain like `smartbursary.com`:

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain
3. Configure DNS records as instructed by Vercel
4. Update `CORS_ORIGINS` on Render to include the custom domain

---

## Environment Variables Reference

### Backend (Render) - Complete List

| Variable | Required | Production Value | Development Value | Notes |
|----------|----------|------------------|-------------------|-------|
| `DATABASE_URL` | ✓ | Render PostgreSQL URL | `sqlite:///./smartbursary.db` | Auto-set by Render when PostgreSQL connected |
| `SECRET_KEY` | ✓ | Random 32+ chars | `dev-secret-key-change-in-production` | **Security critical** - generate with `secrets.token_urlsafe(32)` |
| `CORS_ORIGINS` | ✓ | `https://your-app.vercel.app` | `http://localhost:5173` | Comma-separated list of allowed frontend URLs |
| `ADMIN_EMAIL` | ✓ | `admin@smartbursary.com` | Same | Email for default admin account |
| `ADMIN_PASSWORD` | ✓ | Secure password | `Admin@123` | **Security critical** - change from default |
| `REVIEWER_EMAIL` | ✓ | `reviewer@smartbursary.com` | Same | Email for default reviewer account |
| `REVIEWER_PASSWORD` | ✓ | Secure password | `Reviewer@123` | **Security critical** - change from default |
| `SMTP_HOST` | Optional | `smtp.gmail.com` | Same | Email server for notifications |
| `SMTP_PORT` | Optional | `587` | Same | Email server port |
| `SMTP_USERNAME` | Optional | Your email | Same | Email account for sending |
| `SMTP_PASSWORD` | Optional | App password | Same | Email app-specific password |
| `SMTP_FROM_EMAIL` | Optional | `noreply@smartbursary.com` | Same | From address for emails |
| `ENVIRONMENT` | Optional | `production` | `development` | Affects logging and debug mode |

### Frontend (Vercel) - Complete List

| Variable | Required | Production Value | Development Value | Notes |
|----------|----------|------------------|-------------------|-------|
| `VITE_API_URL` | ✓ | `https://smartbursary-backend.onrender.com/api` | `http://localhost:8000/api` | Backend API endpoint (must include `/api`) |

### Security Considerations

**Critical Variables** (must be changed from defaults):
- `SECRET_KEY`: Used for JWT tokens - if leaked, attackers can forge authentication
- `ADMIN_PASSWORD`: Admin has full system access
- `REVIEWER_PASSWORD`: Reviewer can access all applications

**Best Practices**:
- Never commit `.env` files to git
- Use different passwords for each environment
- Rotate passwords periodically
- Use Render's secret file feature for multi-line secrets
- Enable Render's environment variable encryption

**Generating Secure Values**:
```bash
# SECRET_KEY (32+ characters)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Random password
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## Post-Deployment Verification

### 1. Test Backend Health

```bash
# Check backend is running:
curl https://smartbursary-backend.onrender.com/health

# Expected response:
{"status":"healthy","database":"connected"}
```

### 2. Verify CORS Configuration

1. Open your Vercel frontend URL in a browser
2. Open browser DevTools (F12) → Console
3. Try to log in
4. If you see CORS errors, check:
   - `CORS_ORIGINS` includes your exact Vercel URL (no trailing slash)
   - Render service has been redeployed after updating `CORS_ORIGINS`

### 3. Test Login at Production URL

Test all three account types:

**Admin Account**:
- Email: `admin@smartbursary.com`
- Password: (your `ADMIN_PASSWORD` value)
- Should redirect to admin dashboard

**Reviewer Account**:
- Email: `reviewer@smartbursary.com`
- Password: (your `REVIEWER_PASSWORD` value)
- Should redirect to reviewer dashboard

**Applicant Account**:
- Create a new account via "Create an account" link
- Should receive email verification (if SMTP configured)
- Should redirect to applicant dashboard

### 4. Check Existing Production Data

If you're upgrading an existing deployment:

```bash
# In Render Shell:
python -c "from app.database import SessionLocal; from app.models import User; db = SessionLocal(); print(f'Users: {db.query(User).count()}'); db.close()"
```

Verify the user count matches expectations.

### 5. Confirm New Columns Exist

```bash
# In Render Shell:
python -c "from app.models import User; from sqlalchemy import inspect; inspector = inspect(User); print([c.name for c in inspector.columns])"
```

Verify `ward`, `last_login`, and `login_count` are in the list.

### 6. Test Creating a New User Account

1. Go to your Vercel URL
2. Click "Create an account"
3. Fill in applicant details
4. Submit registration
5. Verify account is created and login works

### 7. Test Submitting an Application

1. Log in as an applicant
2. Go to "Apply" page
3. Fill in application form
4. Upload required documents
5. Submit application
6. Verify:
   - Application appears in "My Applications"
   - Reference number is generated
   - Status is "Pending"
   - Reviewer can see it in their dashboard

---

## Troubleshooting Common Issues

### CORS Errors

**Symptoms**:
- Frontend shows "Network Error" or "CORS policy" errors
- Login fails with no backend error
- Browser console shows: `Access to XMLHttpRequest blocked by CORS policy`

**Solutions**:
1. Check `CORS_ORIGINS` in Render includes your Vercel URL:
   ```
   # Correct:
   CORS_ORIGINS=https://smart-bursary-abc123.vercel.app
   
   # Wrong (trailing slash):
   CORS_ORIGINS=https://smart-bursary-abc123.vercel.app/
   
   # Wrong (missing https):
   CORS_ORIGINS=smart-bursary-abc123.vercel.app
   ```

2. Verify `VITE_API_URL` in Vercel is correct:
   ```
   # Correct:
   VITE_API_URL=https://smartbursary-backend.onrender.com/api
   
   # Wrong (missing /api):
   VITE_API_URL=https://smartbursary-backend.onrender.com
   ```

3. After updating either variable, redeploy both services

### Login Failures - "no such column" Errors

**Symptoms**:
- Error: `no such column: users.ward`
- Error: `no such column: users.last_login`
- Error: `no such column: users.login_count`

**Solution**:
Run the production migration script:
```bash
# In Render Shell:
python run_production_migration.py
```

See [Production Migration Steps](#production-migration-steps) for details.

### 500 Internal Server Errors

**Symptoms**:
- Backend returns 500 errors
- Login or API calls fail unexpectedly

**How to diagnose**:
1. Check Render logs:
   - Go to Render Dashboard → Your Service → Logs
   - Look for Python tracebacks or error messages

2. Common causes:
   - Database connection failed (check `DATABASE_URL`)
   - Missing environment variable
   - Python package import error
   - Database schema mismatch

**Solutions**:
- Check all required environment variables are set
- Verify database is connected and running
- Run migration script if schema-related
- Check requirements.txt includes all dependencies

### Database Connection Issues

**Symptoms**:
- Error: `could not connect to server`
- Error: `password authentication failed`
- Health check returns `database: disconnected`

**Solutions**:
1. Verify PostgreSQL database is running in Render
2. Check `DATABASE_URL` is correctly set (should be auto-set if using Render PostgreSQL)
3. If using external database, verify:
   - Database server is accessible from Render
   - Firewall allows Render IP addresses
   - Credentials are correct

### Application Not Loading

**Symptoms**:
- Blank page or "Cannot GET /"
- Vercel shows build errors

**Solutions**:
1. Check Vercel build logs:
   - Go to Vercel Dashboard → Your Project → Deployments
   - Click the failed deployment → View logs

2. Common causes:
   - `VITE_API_URL` not set or incorrect
   - Build command failed
   - Missing dependencies in package.json

3. Fix and redeploy:
   - Update environment variables in Vercel
   - Push fix to GitHub (triggers auto-deploy)

### File Upload Failures

**Symptoms**:
- Documents fail to upload
- Error: "File too large"
- Uploads timeout

**Solutions**:
1. Check file size limits in backend:
   - Default: 5MB per file
   - Increase if needed in `app/main.py`: `app.add_middleware(RequestMiddleware, max_upload_size=...)`

2. Check Render plan limits:
   - Free tier has request timeout limits
   - Upgrade plan if handling large files

3. Consider using cloud storage (S3, Cloudflare R2) for production file uploads

---

## Rollback Procedures

### When to Rollback vs Fix Forward

**Rollback when**:
- Deployment causes complete service outage
- Data corruption or loss is occurring
- Security vulnerability was introduced
- Critical functionality is completely broken

**Fix forward when**:
- Issue affects only some users or features
- Fix is simple and can be deployed quickly
- Rollback would cause data loss
- Issue is already being investigated/fixed

### Revert to Previous Deployment on Render

**Method 1: Via Dashboard**:
1. Go to Render Dashboard → Your Service
2. Click "Events" tab
3. Find the last successful deployment
4. Click "..." menu → "Redeploy"

**Method 2: Via Git**:
1. Identify the last working commit:
   ```bash
   git log --oneline
   ```
2. Create a revert commit:
   ```bash
   git revert <bad-commit-hash>
   git push origin main
   ```
3. Render will auto-deploy the reverted code

### Database Rollback

**If you have a backup**:
1. Go to Render Dashboard → Your PostgreSQL Database
2. Click "Backups" tab
3. Select backup from before migration
4. Click "Restore"
5. Confirm restoration

**If migration failed mid-way**:
1. Access Render Shell
2. Run rollback commands:
   ```bash
   python -c "
   from app.database import engine
   engine.execute('ALTER TABLE users DROP COLUMN IF EXISTS ward')
   engine.execute('ALTER TABLE users DROP COLUMN IF EXISTS last_login')
   engine.execute('ALTER TABLE users DROP COLUMN IF EXISTS login_count')
   print('Rollback complete')
   "
   ```

3. Redeploy previous working code version

**If data was corrupted**:
- Restore from most recent backup before corruption
- You may lose data created after the backup
- Document and communicate data loss to users

### Vercel Rollback

**Instant Rollback**:
1. Go to Vercel Dashboard → Your Project → Deployments
2. Find a previous successful deployment
3. Click "..." menu → "Promote to Production"
4. Previous deployment becomes live immediately

**No data loss** - frontend rollbacks are safe as they don't affect the database.

### Emergency Contact

If rollback doesn't resolve the issue:

1. **Check Render Status**: https://status.render.com
2. **Check Vercel Status**: https://vercel-status.com
3. **Review Recent Changes**: Check git history and deployment logs
4. **Restore from Backup**: Use most recent database backup
5. **Contact Support**: Use Render/Vercel support if platform issue

---

## Quick Reference Card

### URLs
- **Backend API**: https://smartbursary-backend.onrender.com
- **Frontend**: `<your-vercel-url>.vercel.app`
- **Backend Logs**: Render Dashboard → Service → Logs
- **Frontend Logs**: Vercel Dashboard → Project → Deployments

### Key Commands

**Run Migration** (Render Shell):
```bash
python run_production_migration.py
```

**Check Database Columns** (Render Shell):
```bash
python -c "from app.database import engine; from sqlalchemy import inspect; inspector = inspect(engine); print([c['name'] for c in inspector.get_columns('users')])"
```

**Test Backend Health**:
```bash
curl https://smartbursary-backend.onrender.com/health
```

### Default Accounts

| Role | Email | Default Password | Dashboard |
|------|-------|------------------|-----------|
| Admin | admin@smartbursary.com | Set via `ADMIN_PASSWORD` env var | `/admin` |
| Reviewer | reviewer@smartbursary.com | Set via `REVIEWER_PASSWORD` env var | `/reviewer` |
| Applicant | *User-created* | *User-chosen* | `/` |

**Security**: Change all default passwords before production use!

---

## Next Steps After Deployment

1. **Security Hardening**:
   - Enable 2FA for Render and Vercel accounts
   - Set up monitoring and alerts
   - Review and rotate secrets quarterly
   - Configure rate limiting (if not already done)

2. **Monitoring Setup**:
   - Set up uptime monitoring (e.g., UptimeRobot, Pingdom)
   - Configure error tracking (e.g., Sentry)
   - Set up log aggregation and analysis

3. **Backup Strategy**:
   - Verify Render PostgreSQL backups are enabled
   - Test backup restoration process
   - Document backup retention policy

4. **Performance Optimization**:
   - Monitor response times in Render logs
   - Optimize slow database queries
   - Consider CDN for static assets

5. **User Communication**:
   - Announce maintenance windows before migrations
   - Provide status page for service health
   - Document user-facing changes

---

**Last Updated**: 2025-01-XX  
**Version**: 1.0  
**Maintained By**: SmartBursary Development Team
