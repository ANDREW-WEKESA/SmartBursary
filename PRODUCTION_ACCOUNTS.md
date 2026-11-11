# Production Demo Accounts

## ✅ Production is LIVE and Working!

**Production URL:** https://smart-bursary.vercel.app/

---

## 🔐 Demo Accounts

### Admin Account
- **Email:** admin@smartbursary.com  
- **Password:** ChangeMe!  
- **Role:** Administrator (full access)
- **Status:** ✅ Verified Working

### Reviewer Account
- **Email:** reviewer@smartbursary.com  
- **Password:** reviewer123  
- **Role:** Reviewer (can review and approve/reject applications)
- **Status:** ✅ Verified Working

### Applicant/Student Account
- **Email:** student@smartbursary.com  
- **Password:** student123  
- **Role:** Applicant (can submit bursary applications)
- **Status:** ✅ Verified Working

---

## 📊 Production Database Status

### ✅ What's Seeded:
1. **All 290 Kenya Constituencies** - Every constituency has:
   - CDF Bursary Program (KES 20,000)
   - Deadline: March 31, 2027
   - Active and ready for applications

2. **47 Counties** - Complete coverage of all Kenya counties

3. **294 Bursary Programs Total** - Including:
   - CDF programs for all constituencies
   - Some special programs

### Database Provider:
- **Neon.tech PostgreSQL** (Persistent, won't lose data)
- Backend: Render (https://smartbursary-backend.onrender.com)
- Frontend: Vercel (https://smart-bursary.vercel.app/)

---

## 📝 How to Demo Tomorrow

### Option 1: Register New Applicants Live (Recommended)
1. Go to https://smart-bursary.vercel.app/
2. Click "Register"
3. Fill in details (use any constituency)
4. Complete profile after login
5. Apply for bursary from your constituency
6. Login as reviewer to review
7. Login as admin for full system management

### Option 2: Use Test Accounts
1. Login as **student@smartbursary.com** / **student123**
2. Complete the profile (need to fill in all details)
3. Submit applications
4. Login as **reviewer@smartbursary.com** / **reviewer123** to review
5. Login as **admin@smartbursary.com** / **ChangeMe!** for admin functions

### Option 3: Use Local (Backup)
- If production has any issues, use http://localhost:5174/
- Local has 68 demo applications already created
- All three accounts work locally

---

## 🎯 Key Features to Demonstrate

1. **Constituency Coverage**
   - All 290 Kenya constituencies represented
   - Each has its own CDF bursary program
   - Applicants can only see programs from their constituency

2. **User Roles**
   - Admin: Full system access, can create bursaries, manage users
   - Reviewer: Can review and approve/reject applications from their constituency
   - Applicant: Can register, apply for bursaries, track status

3. **Application Process**
   - Profile completion required
   - Document uploads (National ID, Student ID, Admission Letter)
   - Priority scoring based on financial need
   - Status tracking (Pending, Approved, Rejected)

4. **Smart Features**
   - Auto-calculation of priority scores
   - Duplicate application detection
   - Financial need categorization
   - Award letter generation

---

## 🚨 Important Notes

### First Time Login Tips:
1. New applicants MUST complete their profile before applying
2. Profile requires: personal details, guardian info, institution details
3. Documents can be uploaded after application submission
4. Reviewer accounts can only see applications from their constituency

### If Production is Slow:
- Render free tier may take 30-60 seconds for first request after inactivity
- This is normal - subsequent requests are fast
- Consider using local (localhost:5174) as primary for presentation

### Database Persistence:
- ✅ Production uses Neon PostgreSQL (data persists)
- ✅ All constituencies and programs will be there tomorrow
- ✅ Any data created today will still be there tomorrow

---

## 📱 Quick Reference

| Account Type | Email | Password |
|-------------|-------|----------|
| Admin | admin@smartbursary.com | ChangeMe! |
| Reviewer | reviewer@smartbursary.com | reviewer123 |
| Student | student@smartbursary.com | student123 |

| URL Type | Address |
|----------|---------|
| Production | https://smart-bursary.vercel.app/ |
| Local Backup | http://localhost:5174/ |
| Backend API | https://smartbursary-backend.onrender.com |

---

## ✅ Pre-Presentation Checklist

- [x] Production is live and accessible
- [x] All 290 constituencies seeded
- [x] Admin account working
- [x] Reviewer account working  
- [x] Applicant account working
- [x] Database is persistent (Neon PostgreSQL)
- [ ] Test one full application flow before presentation
- [ ] Have local version running as backup (npm run dev in frontend, uvicorn in backend)
- [ ] Screenshot some key screens for backup slides

---

**Last Updated:** October 2, 2026  
**System Status:** ✅ Production Ready for Presentation
