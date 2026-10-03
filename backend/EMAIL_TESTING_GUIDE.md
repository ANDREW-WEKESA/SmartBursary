# Email Notifications Testing Guide

## Email Features Implemented

SmartBursary now sends automatic email notifications for:

1. **Application Submitted** - Sent to applicant when they submit an application
2. **New Application for Review** - Sent to reviewers when a new application is submitted in their constituency
3. **Status Changed** - Sent to applicant when application status changes (Approved, Rejected, Disbursed)

## Setup for Testing

### Option 1: Local Test Server (Recommended for Development)

1. **Start the test SMTP server** in one terminal:
   ```powershell
   cd c:\dev\SmartBursary-Complete\SmartBursary-Complete\backend
   python test_email_server.py
   ```

2. **The server runs on `localhost:1025`** and prints all emails to the console

3. **Start your backend** normally - it's already configured to use localhost:1025

4. **Test by**:
   - Logging in as an applicant and submitting an application
   - Logging in as a reviewer/admin and changing application status
   - Check the test_email_server.py terminal to see the emails

### Option 2: Using Mailpit (Better UI)

1. **Install Mailpit** (Windows):
   ```powershell
   # Using Chocolatey
   choco install mailpit
   
   # Or download from: https://github.com/axllent/mailpit/releases
   ```

2. **Run Mailpit**:
   ```powershell
   mailpit
   ```

3. **Access the UI**: Open http://localhost:8025 in your browser

4. **Configuration** (if needed): Mailpit runs on port 1025 by default, which matches the backend config

### Option 3: Real SMTP Server

Update your `.env` file with real SMTP credentials:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=SmartBursary System
EMAIL_ENABLED=true
```

**Note**: For Gmail, you need an [App Password](https://support.google.com/accounts/answer/185833)

## Email Configuration

All email settings are in `backend/app/config.py` and can be overridden via `.env`:

| Setting | Default | Description |
|---------|---------|-------------|
| `SMTP_HOST` | localhost | SMTP server hostname |
| `SMTP_PORT` | 1025 | SMTP server port (587 for TLS, 465 for SSL) |
| `SMTP_USERNAME` | "" | SMTP username (leave empty for test server) |
| `SMTP_PASSWORD` | "" | SMTP password |
| `SMTP_FROM_EMAIL` | noreply@smartbursary.com | Sender email address |
| `SMTP_FROM_NAME` | SmartBursary System | Sender display name |
| `EMAIL_ENABLED` | true | Enable/disable email sending |

## Testing Scenarios

### Scenario 1: Application Submission
1. Login as applicant (e.g., jane.doe@example.com)
2. Submit a new bursary application
3. Check for 2 emails:
   - Confirmation email to applicant
   - Notification email to constituency reviewers

### Scenario 2: Application Approval
1. Login as reviewer (e.g., nairobi.reviewer@example.com)
2. Open a pending application
3. Change status to "Approved"
4. Check for email sent to applicant with approval notice

### Scenario 3: Application Rejection
1. Login as reviewer
2. Change application status to "Rejected"
3. Check for email sent to applicant

### Scenario 4: Disbursement
1. Login as admin
2. Change approved application to "Disbursed"
3. Check for email with disbursement confirmation

## Disable Emails

To disable email notifications:

1. **Via environment variable**:
   ```env
   EMAIL_ENABLED=false
   ```

2. **Emails will be logged but not sent** when disabled

## Troubleshooting

### Emails not sending?

1. **Check the backend logs** for error messages
2. **Verify test server is running** (if using Option 1)
3. **Check EMAIL_ENABLED=true** in your .env
4. **Verify SMTP settings** match your server

### Connection refused error?

- The test SMTP server is not running
- Start it with: `python test_email_server.py`

### Emails sent but not received (real SMTP)?

- Check spam folder
- Verify SMTP credentials are correct
- For Gmail, ensure you're using an App Password, not your regular password

## Email Templates

All email templates are in `backend/app/email_service.py`. They include:

- **HTML version** - Styled with inline CSS for email clients
- **Plain text version** - Fallback for email clients that don't support HTML
- **Responsive design** - Works on mobile and desktop email clients

## Production Deployment

For production, update to a real SMTP service:

- **SendGrid** (recommended for high volume)
- **AWS SES** (cost-effective)
- **Mailgun**
- **Gmail SMTP** (low volume only)

Update your production `.env` with the service credentials.
