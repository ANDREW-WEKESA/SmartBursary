"""Promote user to reviewer role"""
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
try:
    # Update reviewer@smartbursary.com to be a reviewer
    reviewer = db.query(User).filter_by(email='reviewer@smartbursary.com').first()
    if reviewer:
        reviewer.role = 'reviewer'
        db.commit()
        print(f'✅ Promoted {reviewer.email} to reviewer role')
    else:
        print('❌ Reviewer user not found')
        
    # Also update student to be applicant (just in case)
    student = db.query(User).filter_by(email='student@smartbursary.com').first()
    if student:
        student.role = 'applicant'
        db.commit()
        print(f'✅ Set {student.email} to applicant role')
        
finally:
    db.close()
