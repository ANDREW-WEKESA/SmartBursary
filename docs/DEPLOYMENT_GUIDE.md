# SmartBursary Deployment Guide

## Production Deployment

### Current Production Setup

**Frontend:** Vercel (https://smart-bursary.vercel.app/)  
**Backend:** Render (https://smartbursary-backend.onrender.com)  
**Database:** Neon.tech PostgreSQL

---

## Backend Deployment (Render)

### 1. Prerequisites
- GitHub repository
- Render account
- Neon PostgreSQL database

### 2. Environment Variables

Add these to Render:

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300
CORS_ORIGINS=https://smart-bursary.vercel.app,http://localhost:5174
```

### 3. Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Initial Setup

After deployment, run these one-time setup endpoints:

```bash
# Seed all 290 constituencies
curl https://your-backend.onrender.com/api/setup/seed-constituencies

# Create admin account  
curl https://your-backend.onrender.com/api/setup/create-admin

# Run database migration
curl https://your-backend.onrender.com/api/setup/run-migration
```

---

## Frontend Deployment (Vercel)

### 1. Environment Variables

Add to Vercel:

```env
VITE_API_URL=https://smartbursary-backend.onrender.com/api
```

### 2. Build Settings

**Framework Preset:** Vite  
**Build Command:** `npm run build`  
**Output Directory:** `dist`  
**Install Command:** `npm install`

### 3. Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## Database Setup (Neon.tech)

### 1. Create Project

1. Sign up at https://neon.tech
2. Create new project
3. Select region (US East recommended for Render)
4. Note connection string

### 2. Connection String Format

```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

### 3. Add to Render

Copy connection string to Render's `DATABASE_URL` environment variable.

---

## Local Development

### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python migrate_db.py

# Seed data
python seed_test_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start dev server
npm run dev
```

---

## Post-Deployment Checklist

### Backend
- [ ] Environment variables configured
- [ ] Database connection working
- [ ] Constituencies seeded (290)
- [ ] Admin account created
- [ ] CORS configured correctly
- [ ] Health endpoint responding

### Frontend
- [ ] API URL configured
- [ ] Build successful
- [ ] Login working
- [ ] Registration working
- [ ] Profile updates working
- [ ] Application submission working

### Testing
- [ ] Create test accounts (admin, reviewer, applicant)
- [ ] Submit test applications
- [ ] Review applications
- [ ] Approve/reject applications
- [ ] Check email notifications (if configured)

---

## Monitoring

### Backend Health Check
```bash
curl https://smartbursary-backend.onrender.com/
```

### Database Connection
```bash
curl https://smartbursary-backend.onrender.com/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@smartbursary.com","password":"ChangeMe!"}'
```

---

## Troubleshooting

### Backend Issues

**Problem:** 500 Internal Server Error  
**Solution:** Check Render logs, verify DATABASE_URL format

**Problem:** CORS errors  
**Solution:** Add frontend URL to CORS_ORIGINS env variable

**Problem:** Database connection failed  
**Solution:** Verify Neon database is active, check connection string

### Frontend Issues

**Problem:** "Failed to fetch"  
**Solution:** Check VITE_API_URL in .env, verify backend is running

**Problem:** Login not working  
**Solution:** Check backend CORS configuration, verify API endpoint

---

## Scaling

### Performance Optimization

1. **Backend:**
   - Upgrade Render plan for better performance
   - Add Redis for caching
   - Optimize database queries
   - Add CDN for static assets

2. **Database:**
   - Upgrade Neon plan for more connections
   - Add read replicas
   - Index frequently queried columns

3. **Frontend:**
   - Enable Vercel Edge Network
   - Optimize bundle size
   - Implement code splitting
   - Add service worker for offline support

---

## Backup Strategy

### Database Backups

Neon provides automatic backups. For additional safety:

```bash
# Export database
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql

# Restore database
psql $DATABASE_URL < backup-20261002.sql
```

### File Backups

Document uploads should be backed up separately:

```bash
# Backup uploads folder
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz backend/uploads/
```

---

## Security Checklist

- [ ] Environment variables secured
- [ ] SECRET_KEY is strong and unique
- [ ] Database uses SSL (sslmode=require)
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SQL injection protection (using SQLAlchemy)
- [ ] Password hashing (bcrypt)
- [ ] Input validation (Pydantic)
- [ ] File upload restrictions
- [ ] HTTPS enforced

---

## Support

For deployment issues:
- **Backend:** Check Render logs
- **Frontend:** Check Vercel logs
- **Database:** Check Neon dashboard

---

Last Updated: October 2, 2026
