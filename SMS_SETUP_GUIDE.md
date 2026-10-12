# SMS Setup Guide - Africa's Talking

SmartBursary now sends SMS notifications for:
1. **Registration** - OTP code sent via SMS
2. **Application Submission** - Confirmation with application number
3. **Status Changes** - Especially Approved/Disbursed notifications

## Setup Instructions

### Step 1: Create Africa's Talking Account

1. Go to https://africastalking.com/
2. Click "Sign Up" (top right)
3. Fill in your details:
   - Full Name
   - Email Address
   - Phone Number (Kenyan number)
   - Company Name (can use "SmartBursary Test")
4. Verify your email

### Step 2: Get Sandbox Credentials (For Testing)

1. After login, go to **Sandbox** environment (top right corner)
2. Click on **Settings** → **API Key**
3. Click "Generate API Key"
4. **Copy your API Key** - looks like: `atsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. Your username in sandbox is: `sandbox`

### Step 3: Test in Sandbox First

**Sandbox Testing Rules:**
- Only sends to phone numbers you add as "test numbers"
- Free to use, no charges
- Add test numbers in: Sandbox → Settings → Add Phone Numbers

**Add your phone number:**
1. Go to Sandbox → Settings
2. Click "Add Phone Number"
3. Enter your Kenyan phone number: `+254XXXXXXXXX`
4. You'll receive a verification code via SMS
5. Enter the code to verify

### Step 4: Configure SmartBursary

Add these to your **Render Environment Variables**:

```
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=your-api-key-here
SMS_SENDER_ID=SmartBursary
SMS_ENABLED=true
```

**Important:**
- For testing: Use `username=sandbox`
- For production: Use your actual Africa's Talking username

### Step 5: Test SMS

1. Register a new user with YOUR phone number (the one you added in sandbox)
2. You should receive an SMS with the OTP code
3. Submit a bursary application
4. You should receive a confirmation SMS

### Step 6: Production Setup (After Testing)

**To go live (costs money):**

1. Switch to **Production** environment in Africa's Talking dashboard
2. Add credit to your account:
   - Minimum: KES 100
   - SMS cost: ~KES 0.80 per SMS to Kenyan numbers
3. Get your **Production API Key**:
   - Production → Settings → API Key
4. Get your **Production Username** (shown in dashboard)
5. Update Render environment variables:
   ```
   AFRICASTALKING_USERNAME=your-production-username
   AFRICASTALKING_API_KEY=your-production-api-key
   SMS_ENABLED=true
   ```

### Pricing (As of 2024)

**Kenya:**
- SMS: KES 0.80 per message
- Premium SMS: KES 2.00 per message

**Example Cost Calculation:**
- 100 applications/month × 2 SMS each (submission + status) = 200 SMS
- Cost: 200 × KES 0.80 = **KES 160/month**

### Troubleshooting

**SMS not received?**
1. Check Render logs for `[SMS]` messages
2. Verify phone number format: `+254XXXXXXXXX` (not `07XX...`)
3. In sandbox: Ensure phone number is added as test number
4. Check Africa's Talking dashboard → SMS → Logs

**"Invalid API Key" error?**
1. Regenerate API key in Africa's Talking dashboard
2. Update Render environment variable
3. Redeploy

**"Insufficient Balance" error?**
- You're in production mode without credit
- Add funds or switch back to sandbox for testing

### Disable SMS (Keep Email Only)

If you want to disable SMS temporarily:

```
SMS_ENABLED=false
```

### Custom Sender ID (Production Only)

The sender ID (what appears as the sender name) can be customized:

1. Go to Production → Settings → Sender IDs
2. Request a custom Sender ID (e.g., "SmartBursary")
3. Wait for approval (1-3 business days)
4. Update environment variable:
   ```
   SMS_SENDER_ID=YourApprovedID
   ```

**Note:** Sandbox always uses "AFRICASTKNG" as sender ID.

### Support

**Africa's Talking Support:**
- Email: support@africastalking.com
- Docs: https://developers.africastalking.com/docs/sms/overview
- Phone: +254 20 2606183

**Common Issues:**
1. Phone number format must be international: `+254XXXXXXXXX`
2. Sandbox requires phone numbers to be pre-registered
3. Production requires account credit
4. Sender ID customization only works in production

### Current SMS Messages

**Registration:**
```
Welcome to SmartBursary, [Name]! Your verification code is: [OTP]. 
Valid for 10 minutes. Do not share this code.
```

**Application Submitted:**
```
Dear [Name], your bursary application ([Number]) for [Bursary] has been received. 
Track your application at smart-bursary.vercel.app
```

**Status: Approved:**
```
Congratulations [Name]! Your bursary application [Number] has been APPROVED. 
Disbursement details will follow soon.
```

**Status: Disbursed:**
```
Great news [Name]! Your bursary funds for application [Number] have been DISBURSED. 
Check your payment details in the dashboard.
```

Messages are automatically sent - no manual intervention needed!
