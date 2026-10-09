# SmartBursary Deployment Guide

This guide will help you deploy SmartBursary to production using **Vercel** (frontend) and **Railway** (backend).

## Architecture

- **Frontend**: React/Vite → Vercel
- **Backend**: FastAPI/Python → Railway
- **Database**: PostgreSQL → Railway (included)
- **Email**: Configure SMTP provider

---

## Prerequisites

1. **GitHub Account** - Your code is already pushed to GitHub
2. **Railway Account** - Sign up at [railway.app](https://railway.app) (free tier available)
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free tier available)

---

## Part 1: Deploy Backend to Railway (15 minutes)

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `SmartBursary-Complete` repository
5. Railway will detect it's a Python project

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable is automatically set

### Step 3: Configure Environment Variables

In Railway project settings → **Variables**, add:

```
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:5173,http://localhost:5174
EMAIL_ENABLED=false
SMTP_HOST=localhost
SMTP_PORT=1025
```

**Note:** Replace `your-app.vercel.app` with your actual Vercel domain (you'll get this in Part 2)

### Step 4: Configure Root Directory

1. Go to **Settings** → **Build**
2. Set **Root Directory** to: `backend`
3. Railway will now build from the backend folder

### Step 5: Deploy

1. Click **"Deploy"**
2. Railway will:
   - Install Python dependencies from `requirements.txt`
   - Run database migrations automatically
   - Start the FastAPI server
3. Copy your Railway backend URL (e.g., `https://smartbursary-production.up.railway.app`)

### Step 6: Seed Initial Data

Railway provides a terminal for running commands:

1. Go to your Railway project
2. Click on your service → **"Shell"**
3. Run these commands:

```bash
cd backend
python seed_admin.py
python seed_test_data.py
```

This creates:
- Default admin account: `admin@smartbursary.com` / `admin123`
- 15 constituency admins
- 15 reviewers
- Test bursaries and applications

---

## Part 2: Deploy Frontend to Vercel (10 minutes)

### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your `SmartBursary-Complete` repository from GitHub
4. Vercel will detect it's a Vite project

### Step 2: Configure Build Settings

Vercel should auto-detect these, but verify:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### Step 3: Add Environment Variables

In Vercel project settings → **Environment Variables**, add:

```
VITE_API_URL=https://your-backend.railway.app/api
```

**Replace** `your-backend.railway.app` with your actual Railway backend URL from Part 1.

### Step 4: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. You'll get a URL like: `https://smart-bursary.vercel.app`

### Step 5: Update Backend CORS

Go back to Railway and update the `CORS_ORIGINS` variable:

```
CORS_ORIGINS=https://smart-bursary.vercel.app,http://localhost:5173
```

**Replace** with your actual Vercel URL. Railway will automatically redeploy.

---

## Part 3: Test Your Deployment

### Test Backend

1. Open: `https://your-backend.railway.app/api/health`
2. Should return: `{"status":"ok","service":"SmartBursary API"}`
3. Check API docs: `https://your-backend.railway.app/docs`

### Test Frontend

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Try logging in with: `admin@smartbursary.com` / `admin123`
3. Test creating a bursary, viewing applications, etc.

### Check Database

In Railway:
1. Go to your PostgreSQL database
2. Click **"Data"** to view tables
3. Verify `users`, `bursaries`, `applications` tables exist

---

## Part 4: Configure Email (Optional)

For production email notifications, configure a real SMTP provider:

### Option A: Gmail (Development Only)

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
EMAIL_ENABLED=true
```

### Option B: SendGrid (Recommended for Production)

1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Create an API key
3. Add to Railway:

```
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
EMAIL_ENABLED=true
```

### Option C: Mailgun

```
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=your-mailgun-smtp-username
SMTP_PASSWORD=your-mailgun-smtp-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
EMAIL_ENABLED=true
```

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection | Yes (auto) | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | JWT signing key | Yes | Min 32 characters |
| `CORS_ORIGINS` | Allowed frontend URLs | Yes | `https://app.vercel.app` |
| `EMAIL_ENABLED` | Enable email notifications | No | `true` or `false` |
| `SMTP_HOST` | Email server host | If email enabled | `smtp.gmail.com` |
| `SMTP_PORT` | Email server port | If email enabled | `587` |
| `SMTP_USERNAME` | Email username | If email enabled | `user@example.com` |
| `SMTP_PASSWORD` | Email password | If email enabled | Your password |
| `SMTP_FROM_EMAIL` | Sender email | If email enabled | `noreply@domain.com` |

### Frontend (Vercel)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | Yes | `https://backend.railway.app/api` |

---

## Troubleshooting

### Backend Issues

**Problem: "Internal Server Error" on Railway**
- Check Railway logs: Project → Service → **Logs**
- Common issues:
  - Missing environment variables
  - Database connection failed
  - Python version mismatch

**Problem: Database tables not created**
- Run migrations manually in Railway shell:
  ```bash
  cd backend
  python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
  ```

**Problem: CORS errors**
- Verify `CORS_ORIGINS` includes your Vercel domain
- Make sure there are no trailing slashes
- Redeploy backend after changing CORS

### Frontend Issues

**Problem: "Failed to fetch" or API errors**
- Verify `VITE_API_URL` environment variable in Vercel
- Check browser console for exact error
- Verify backend is accessible: `https://backend-url/api/health`

**Problem: Environment variables not working**
- Redeploy frontend after adding variables
- Environment variables in Vercel require redeploy to take effect

### Database Issues

**Problem: Connection timeout**
- Railway PostgreSQL may take a minute to start
- Check Railway database status

**Problem: Data not persisting**
- Verify you're using PostgreSQL, not SQLite
- Check `DATABASE_URL` is set in Railway

---

## Updating Your Deployment

### Update Backend

1. Push changes to GitHub
2. Railway auto-deploys from `main` branch
3. Or manually trigger deploy in Railway dashboard

### Update Frontend

1. Push changes to GitHub
2. Vercel auto-deploys from `main` branch
3. Or manually trigger deploy in Vercel dashboard

---

## Costs

### Free Tier Limits

**Railway:**
- $5 free credit per month
- ~500 hours of hosting
- 1GB RAM included
- Perfect for development/small projects

**Vercel:**
- 100GB bandwidth/month
- Unlimited deployments
- Perfect for most use cases

### Scaling

When you need more:
- **Railway**: Upgrade to Pro ($20/month for 8GB RAM)
- **Vercel**: Pro ($20/month) for team features
- Both scale automatically with traffic

---

## Security Checklist

Before going live:

- [ ] Change `SECRET_KEY` to a strong random value (min 32 chars)
- [ ] Change default admin password
- [ ] Set up real SMTP for emails (not localhost)
- [ ] Enable HTTPS (both Vercel and Railway provide this automatically)
- [ ] Review CORS origins (only allow your domains)
- [ ] Set up database backups in Railway
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring/alerting

---

## Custom Domain (Optional)

### Frontend (Vercel)

1. Go to Vercel project → **Settings** → **Domains**
2. Add your custom domain (e.g., `smartbursary.ke`)
3. Update DNS records as instructed
4. Vercel provides free SSL certificate

### Backend (Railway)

1. Go to Railway project → **Settings** → **Networking**
2. Add custom domain (e.g., `api.smartbursary.ke`)
3. Update DNS with provided CNAME
4. Railway provides free SSL certificate

### Update Environment Variables

After adding custom domains:

**Railway `CORS_ORIGINS`:**
```
CORS_ORIGINS=https://smartbursary.ke,https://www.smartbursary.ke
```

**Vercel `VITE_API_URL`:**
```
VITE_API_URL=https://api.smartbursary.ke/api
```

---

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## Summary

✅ **Backend deployed to Railway** with PostgreSQL  
✅ **Frontend deployed to Vercel** with environment variables  
✅ **Database tables created** and seeded with test data  
✅ **CORS configured** for production domains  
✅ **Ready for production use!**

**Your app is now live!** 🎉

- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.railway.app`
- API Docs: `https://your-backend.railway.app/docs`

Default login: `admin@smartbursary.com` / `admin123`

**Remember to change the default password immediately!**
