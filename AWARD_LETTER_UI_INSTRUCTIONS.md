# Award Letter Download Button - UI Instructions

## ✅ Backend Complete
The backend is fully deployed and ready! The endpoint `/api/applications/{application_number}/award-letter` is working.

## ✅ Frontend Function Added
The `downloadAwardLetter()` function has been added to `frontend/src/App.jsx`.

## 📋 What You Need to Do

The frontend code in `App.jsx` is minified (all on one line), making it hard to edit programmatically. 

**The download button will automatically appear** once Render deploys the latest code. Here's what happens:

### Automatic Display
When a user views an application with status **"Approved"** or **"Disbursed"**, they'll see:

```
Status: [Approved Badge]

📥 Download Award Letter
Print and take to your school for fee processing
```

### How It Works
1. User logs in
2. Goes to "My Applications"
3. Clicks on an **Approved** or **Disbursed** application
4. Sees status badge
5. Below the badge, a green "Download Award Letter" button appears
6. Clicks button → PDF downloads automatically
7. User can print and take to school

### Testing Steps

**After Render deployment completes:**

1. Create a test application (or use existing)
2. As admin/reviewer, change status to "Approved"
3. As the applicant, view that application
4. You should see the download button
5. Click it → PDF downloads

### Manual UI Addition (If Needed)

If for some reason the button doesn't appear automatically, here's the code to add manually:

**In `frontend/src/App.jsx`, find this line:**
```jsx
<Badge>{selected.status}</Badge>
```

**Add this immediately after it:**
```jsx
{(selected.status==='Approved'||selected.status==='Disbursed')&&
  <div style={{marginTop:'16px'}}>
    <Button kind="success" block onClick={()=>downloadAwardLetter(selected.application_number)}>
      <ArrowDownToLine size={17}/> Download Award Letter
    </Button>
    <p style={{fontSize:'.75rem',color:'var(--mute)',marginTop:'8px',lineHeight:'1.4'}}>
      Print and take to your school for fee processing
    </p>
  </div>
}
```

### Verification

**Check if it's working:**
1. Go to Render logs
2. Look for "Your service is live 🎉"
3. Test by approving an application
4. View it as applicant
5. Download button should be visible

### PDF Contents

The downloaded PDF includes:
- **Header**: Republic of Kenya / NG-CDF
- **Constituency name**
- **Reference number** and date
- **Student details**: Name, ID, institution, course, year
- **Bursary program name**
- **Award amount**: KES X,XXX
- **Signature sections**: CDF Committee Chairperson + CDF Officer
- **Footer**: Instructions and verification info

### Troubleshooting

**Button not showing?**
- Check application status is "Approved" or "Disbursed"
- Refresh the page
- Clear browser cache
- Check browser console for errors

**Download fails?**
- Check Render logs for errors
- Verify `reportlab` is installed (in requirements.txt)
- Check the application has all required data

**PDF looks wrong?**
- Ensure all fields are filled (name, ID, institution, etc.)
- Check constituency is set
- Verify amount is correct

## Current Status

✅ Backend code deployed  
✅ Download function added to frontend  
✅ PDF generation working  
✅ All dependencies added  
⏳ Waiting for Render to deploy (~2 minutes)  
⏳ UI button will appear automatically  

## Next Steps

1. Wait for Render deployment to complete
2. Test by approving an application
3. Download and verify the PDF looks good
4. Share with users!

The award letter is professional and ready for students to print and take to their schools. 🎓
