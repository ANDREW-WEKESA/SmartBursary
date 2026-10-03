# OTP Email Verification - Testing Guide

## ✅ Feature Implemented!

New user registrations now require email verification via OTP (One-Time Password).

## What Was Added

### Backend Changes
1. **New Database Table: `email_otps`**
   - Stores verification codes with expiration
   - Tracks verification status
   - Supports multiple purposes (registration, password reset)

2. **User Model Updates**
   - Added `email_verified` field (boolean)
   - New users are inactive until email is verified
   - Existing users automatically marked as verified

3. **New API Endpoints**
   - `POST /api/auth/register` - Creates user and sends OTP email
   - `POST /api/auth/verify-otp` - Verifies code and activates account
   - `POST /api/auth/resend-otp` - Resends verification code

4. **Email Template**
   - Professional OTP email with 6-digit code
   - Clear expiration notice (10 minutes)
   - HTML and plain text versions

### Frontend Changes
- Two-step registration flow
- OTP input screen after registration
- Resend code functionality
- Go back option to restart registration

## 🚀 Test It Now

### Prerequisites
Start the test email server first:

```powershell
# Terminal 1: Email test server
cd c:\dev\SmartBursary-Complete\SmartBursary-Complete\backend
python test_email_server.py
```

```powershell
# Terminal 2: Backend
cd c:\dev\SmartBursary-Complete\SmartBursary-Complete\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

```powershell
# Terminal 3: Frontend
cd c:\dev\SmartBursary-Complete\SmartBursary-Complete\frontend
npm run dev
```

### Test Scenario 1: New User Registration with OTP

1. **Open** http://localhost:5173
2. **Click** "Create an account"
3. **Fill in registration form**:
   - Full name: Test User
   - Email: test@example.com
   - Password: password123
4. **Click** "Create account"
5. **Check the email test server terminal** - you should see:
   ```
   ===========================
   📧 EMAIL RECEIVED
   ===========================
   To: test@example.com
   Subject: Verify Your Email - SmartBursary
   
   [6-digit OTP code displayed]
   ```
6. **Copy the 6-digit code** from the email
7. **Enter the code** in the verification screen
8. **Click** "Verify email"
9. **Success!** You're logged in and account is activated

### Test Scenario 2: Resend OTP Code

1. **Register** a new account
2. **Wait** on the OTP verification screen
3. **Click** "Resend code"
4. **Check email server** - new OTP sent
5. **Enter new code** to verify

### Test Scenario 3: Expired OTP

1. **Register** a new account
2. **Wait** 11+ minutes (or manually edit the `expires_at` in database)
3. **Try to verify** with the old code
4. **See error**: "Invalid or expired verification code"
5. **Click** "Resend code" to get a new one

### Test Scenario 4: Invalid OTP

1. **Register** a new account
2. **Enter wrong code**: 000000
3. **See error**: "Invalid or expired verification code"
4. **Try again** with correct code

### Test Scenario 5: Existing Users (Already Verified)

1. **Login** as existing user: jane.doe@example.com / password123
2. **Success!** No OTP required (existing users auto-verified during migration)

## 📧 OTP Email Format

The verification email includes:
- **Large 6-digit code** in the center
- **10-minute expiration** warning
- **Professional styling** matching SmartBursary brand
- **Plain text fallback** for email clients without HTML support

## 🔧 Configuration

OTP settings in `backend/app/email_service.py`:

| Setting | Value |
|---------|-------|
| Code length | 6 digits |
| Expiration | 10 minutes |
| Characters | Numbers only (0-9) |

## 🛡️ Security Features

- ✅ OTP codes expire after 10 minutes
- ✅ One-time use (marked as verified after use)
- ✅ Account inactive until email verified
- ✅ Can't login without verification
- ✅ Old OTPs invalidated when new one requested
- ✅ Rate limiting recommended for production

## 📊 Database Schema

### `email_otps` Table
```sql
id INTEGER PRIMARY KEY
email VARCHAR(254)
otp_code VARCHAR(6)
purpose VARCHAR(50)  -- 'registration' or 'password_reset'
expires_at TIMESTAMP
verified BOOLEAN
created_at TIMESTAMP
```

### `users` Table (New Field)
```sql
email_verified BOOLEAN DEFAULT FALSE
```

## 🔄 Migration

Already run! The migration script:
- Added `email_verified` column to users table
- Created `email_otps` table
- Marked all existing users as verified
- Created index on `email_otps.email`

## 🚫 Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "An account with this email already exists" | Email already registered | Login instead or use different email |
| "Invalid or expired verification code" | Wrong code or > 10 minutes old | Resend code |
| "User not found" | Trying to verify non-existent email | Register first |
| "Email already verified" | Trying to verify twice | Just login |

## 🎯 Next Steps

You now have:
- ✅ Email notifications for applications
- ✅ OTP email verification for registration

**Still to implement (from original request):**
- ⏰ Application deadline enforcement
- 📊 Reports and analytics dashboard
- 🔍 Enhanced filters and sorting

Would you like me to continue with the remaining features?
