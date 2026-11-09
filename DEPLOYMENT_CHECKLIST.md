# Production Deployment Checklist

## Pre-Deployment

### Code Review
- [ ] All features tested locally
- [ ] No console errors or warnings
- [ ] Code follows project conventions
- [ ] Documentation updated

### Security
- [ ] Strong SECRET_KEY set
- [ ] Admin password changed from default
- [ ] CORS configured for production domain
- [ ] Environment variables secured
- [ ] No sensitive data in code

### Database
- [ ] Migration scripts ready
- [ ] Backup procedure tested
- [ ] Connection string configured
- [ ] All 290 constituencies seeded

### Performance
- [ ] Images optimized
- [ ] API response times acceptable
- [ ] Database queries optimized
- [ ] Caching configured

## Deployment Steps

### Backend (Render)
1. Push code to GitHub
2. Render auto-deploys from main branch
3. Set environment variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `CORS_ORIGINS`
   - `ADMIN_EMAIL`
   - `ADMIN_PASSWORD`
4. Run migration: `GET /api/setup/run-migration`
5. Create admin: `GET /api/setup/create-admin`
6. Seed constituencies: `GET /api/setup/seed-constituencies`

### Frontend (Vercel)
1. Push code to GitHub
2. Vercel auto-deploys from main branch
3. Set environment variable:
   - `VITE_API_URL=https://your-backend.onrender.com/api`
4. Verify build succeeds
5. Test production URL

## Post-Deployment

### Smoke Tests
- [ ] Health endpoint responding
- [ ] Login works
- [ ] Can create application
- [ ] Can upload documents
- [ ] Can approve/reject (as admin)
- [ ] Award letters generate

### Monitoring
- [ ] Check error logs
- [ ] Monitor response times
- [ ] Watch database connections
- [ ] Check disk usage

### User Communication
- [ ] Notify users of new features
- [ ] Update help documentation
- [ ] Announce maintenance windows

## Rollback Plan

If deployment fails:
1. Revert to previous Git commit
2. Redeploy from stable branch
3. Restore database from backup
4. Notify users of issue

## Success Criteria

- [ ] All test accounts can login
- [ ] Applications can be submitted
- [ ] Documents upload successfully
- [ ] Approvals work correctly
- [ ] No console errors
- [ ] Response time < 2 seconds
- [ ] Mobile responsive
- [ ] All 290 constituencies visible
