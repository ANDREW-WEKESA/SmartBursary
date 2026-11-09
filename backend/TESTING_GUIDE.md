# SmartBursary Testing Guide

## Quick Start

### Local Development
```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## Test Accounts

### Admin
- **Email**: admin@smartbursary.com
- **Password**: admin123
- **Can**: Manage all bursaries, review applications, access reports

### Reviewer
- **Email**: reviewer@smartbursary.com
- **Password**: reviewer123
- **Can**: Review and approve/reject applications

### Applicant
- **Email**: student@smartbursary.com
- **Password**: student123
- **Can**: Browse bursaries, submit applications

## Testing Scenarios

### 1. Application Submission Flow
1. Login as applicant
2. Browse available bursaries
3. Select constituency-specific bursary
4. Fill application form
5. Upload required documents
6. Submit application
7. Track application status

### 2. Review Workflow
1. Login as reviewer/admin
2. View pending applications
3. Review application details
4. Verify documents
5. Approve or reject with comments
6. Generate award letter (if approved)

### 3. Admin Management
1. Login as admin
2. Create/edit bursary programs
3. Manage constituencies
4. Export reports (CSV)
5. View audit logs
6. Manage user accounts

## Data Seeding

### Seed All Constituencies
```bash
cd backend
python seed_constituencies.py
```
Creates 290 constituency bursaries

### Seed Test Data
```bash
cd backend
python seed_test_data.py
```
Creates 68 test applications across multiple constituencies

## API Testing

### Health Check
```
GET http://localhost:8000/api/health
```

### Login
```
POST http://localhost:8000/api/auth/login
{
  "email": "admin@smartbursary.com",
  "password": "admin123"
}
```

### Get Bursaries
```
GET http://localhost:8000/api/bursaries
Authorization: Bearer {token}
```

## Database Reset

To start fresh:
```bash
cd backend
rm smartbursary.db
python -m uvicorn app.main:app --reload
# Database will be recreated on startup
python seed_constituencies.py
python setup_local_accounts.py
```

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
npx kill-port 8000

# Kill process on port 5173
npx kill-port 5173
```

### Database Locked
- Close all connections to database
- Restart backend server

### CORS Errors
- Check frontend .env file has correct API_URL
- Verify backend CORS settings allow frontend origin

## Performance Testing

### Load Testing
- Use tools like Apache Bench or Locust
- Test with 100+ concurrent users
- Monitor response times

### Database Performance
- Check query execution time
- Monitor connection pool usage
- Optimize slow queries

## Security Testing

### Authentication
- Test password requirements
- Verify JWT token expiration
- Check role-based access control

### Input Validation
- Test SQL injection prevention
- Verify XSS protection
- Check file upload validation

## Accessibility Testing

### Screen Reader Testing
- Test with NVDA or JAWS
- Verify all interactive elements are reachable
- Check form labels and error messages

### Keyboard Navigation
- Tab through all forms
- Test modal dialogs
- Verify focus indicators

## Browser Compatibility

Test on:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## Continuous Integration

### Pre-commit Checks
```bash
# Run linter
npm run lint

# Run tests
npm run test

# Check types
npm run type-check
```

## Reporting Bugs

Include:
- Steps to reproduce
- Expected vs actual behavior
- Browser and OS
- Screenshots/screen recordings
- Console errors
