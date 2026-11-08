# Production Setup - Final Steps

## ✅ What's Done:
- ✅ Code pushed to GitHub (main branch)
- ✅ Render auto-deployed the backend
- ✅ Database migration completed (ward, last_login, login_count columns added)
- ✅ Admin account created
- ✅ Backend is responding at https://smartbursary-backend.onrender.com
- ✅ Frontend is deployed at https://smart-bursary.vercel.app

## 🔧 What You Need to Do:

### 1. Configure CORS on Render (CRITICAL)

**Why**: Without this, your frontend won't be able to communicate with the backend.

**Steps**:
1. Go to https://dashboard.render.com
2. Find your **smartbursary-backend** service
3. Click on **"Environment"** tab
4. Add or update this environment variable:
   ```
   CORS_ORIGINS=https://smart-bursary.vercel.app
   ```
5. Click **"Save Changes"**
6. Wait for Render to redeploy (2-3 minutes)

### 2. Test Production Login

After CORS is configured, test at: **https://smart-bursary.vercel.app/**

**Production Credentials**:
- **Email**: admin@smartbursary.com
- **Password**: ChangeMe123!

(Note: If ChangeMe123! doesn't work, try ChangeMe!)

### 3. Seed Production Data (Optional)

If you want demo data in production:

**Option A - Via API** (if logged in):
```bash
python backend/seed_production.py
```

**Option B - Manual** (via Render Shell):
1. Go to Render Dashboard → Your Service → Shell
2. Run: `python seed_test_data.py`

## 🎯 For Tomorrow's Presentation:

You can use EITHER:
- **Local**: http://localhost:5176/ (already has 68 demo applications)
- **Production**: https://smart-bursary.vercel.app/ (once CORS is fixed)

## 📝 Quick Reference:

### Local Development:
- Frontend: http://localhost:5176/
- Backend: http://localhost:8000
- Login: admin@smartbursary.com / admin123

### Production:
- Frontend: https://smart-bursary.vercel.app/
- Backend: https://smartbursary-backend.onrender.com
- Login: admin@smartbursary.com / ChangeMe123!

### Test Accounts (Local):
- Admin: admin@smartbursary.com / admin123
- Reviewer: reviewer.dagorettinorth@smartbursary.com / reviewer123
- Applicant: john.atieno.00@student.ke / student123

## 🚨 If Production Login Still Fails After CORS:

Run this command to check backend logs:
```bash
# In Render Dashboard → Your Service → Logs
# Look for CORS errors or authentication errors
```

Or recreate the admin account:
```
Visit: https://smartbursary-backend.onrender.com/api/setup/create-admin
```

## ✅ Success Checklist:

- [ ] CORS_ORIGINS set on Render
- [ ] Render redeployed successfully
- [ ] Can login at https://smart-bursary.vercel.app/
- [ ] Dashboard loads with data
- [ ] Applications can be viewed/managed

---

**Last Updated**: After fixing database migration and CORS
**Status**: Ready for CORS configuration on Render
