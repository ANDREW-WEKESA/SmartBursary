# 🔐 SmartBursary Login Credentials

## Production & Development Accounts

### 👑 **ADMIN (Administrator)**
```
Email:    admin@smartbursary.com
Password: ChangeMe123!
Role:     Administrator (Full access to all features)
```

**Admin Can:**
- ✅ View ALL applications from all constituencies
- ✅ Manage bursary programs
- ✅ Approve/Reject applications
- ✅ Manage staff accounts
- ✅ View reports and analytics
- ✅ Download award letters/cheques for approved applications

---

### 👨‍💼 **REVIEWER (Constituency Reviewer)**
```
Email:    reviewer.westlands@smartbursary.com
Password: reviewer123
Role:     Reviewer (Limited to specific constituency)
```

**Alternative Reviewers (all password: reviewer123):**
- reviewer.dagorettinorth@smartbursary.com
- reviewer.langata@smartbursary.com
- reviewer.mvita@smartbursary.com
- reviewer.kisauni@smartbursary.com

**Reviewer Can:**
- ✅ View applications from their assigned constituency
- ✅ Review and update application status
- ✅ Add reviewer comments
- ✅ Download award letters for approved applications
- ❌ Cannot manage bursaries or staff

---

### 👨‍🎓 **APPLICANT (Student/Applicant)**

**Your Test Account:**
```
Email:    andrewwekesa@student.ke
Password: student123
Role:     Applicant
```

**Alternative Test Applicants (all password: student123):**
- john.kamau.00@student.ke
- mary.wanjiku.01@student.ke
- peter.ochieng.02@student.ke
- grace.atieno.10@student.ke

**Applicant Can:**
- ✅ Complete profile with personal/educational details
- ✅ Browse available bursaries
- ✅ Submit bursary applications
- ✅ Upload required documents
- ✅ Track application status
- ✅ Download award letter (only when approved)
- ❌ Cannot see review indicators or internal comments
- ❌ Cannot approve/reject applications

---

## 🌐 Access Links

### Local Development
- **Frontend:** http://localhost:5174
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Production (Vercel)
- **Main:** https://smart-bursary-xijg-git-main-andrew-wekesas-projects.vercel.app
- **Dev Preview:** https://smart-bursary-git-dev-preview-andrew-wekesas-projects.vercel.app

---

## 📋 Quick Test Workflow

1. **Login as Applicant** (`andrewwekesa@student.ke` / `student123`)
   - Complete your profile
   - Submit an application for a bursary

2. **Login as Admin** (`admin@smartbursary.com` / `ChangeMe123!`)
   - Go to Applications
   - Find the submitted application
   - Change status to "Approved"

3. **Login back as Applicant**
   - Go to My Applications
   - Click on your approved application
   - **Download Award Letter/Cheque** button will now be visible!

---

## 🔄 To Reset/Seed Test Data

Run this command in the backend folder:
```bash
cd backend
python seed_test_data.py
```

This will create:
- ✅ Multiple bursaries across constituencies
- ✅ Admin accounts for each constituency
- ✅ Reviewer accounts for each constituency
- ✅ Test applicants with sample applications

---

## ⚠️ Important Notes

- All passwords are for **DEVELOPMENT ONLY**
- Change passwords before deploying to production
- The admin account is created automatically on first API startup
- Award letter download only works for **Approved** or **Disbursed** applications

---

**Created:** October 14, 2026
**System:** SmartBursary - Kenya Bursary Management System
